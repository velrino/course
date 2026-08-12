import { constants } from "node:fs";
import { mkdir, open, readdir, rename, rm } from "node:fs/promises";
import { randomUUID } from "node:crypto";
import { resolve, sep } from "node:path";
import * as z from "zod/v4";

export const TaskIdSchema = z.string().regex(
  /^[a-z0-9][a-z0-9-]{0,63}$/,
  "Use 1-64 lowercase letters, digits, or hyphens, starting with a letter or digit.",
);

export const TaskSchema = z.object({
  id: TaskIdSchema,
  title: z.string().min(1).max(120),
  details: z.string().max(2000),
  status: z.enum(["open", "completed"]),
  createdAt: z.iso.datetime(),
  completedAt: z.iso.datetime().nullable(),
  completionNote: z.string().max(500).nullable(),
});

export type Task = z.infer<typeof TaskSchema>;

export class StoreError extends Error {
  constructor(public readonly code: string, message: string, options: ErrorOptions = {}) {
    super(message, options);
    this.name = "StoreError";
  }
}

export class TaskStore {
  readonly root: string;

  constructor(root: string) {
    this.root = resolve(root);
  }

  async initialize(): Promise<void> {
    await mkdir(this.root, { recursive: true, mode: 0o700 });
  }

  private pathFor(taskId: string): string {
    const parsedId = TaskIdSchema.safeParse(taskId);
    if (!parsedId.success) throw new StoreError("invalid_task_id", "Task ID has an invalid format.");
    const candidate = resolve(this.root, `${parsedId.data}.json`);
    if (!candidate.startsWith(`${this.root}${sep}`)) {
      throw new StoreError("path_outside_root", "Task path is outside the configured workspace.");
    }
    return candidate;
  }

  private async readPath(path: string): Promise<Task> {
    let handle;
    try {
      handle = await open(path, constants.O_RDONLY | constants.O_NOFOLLOW);
      const parsed = TaskSchema.safeParse(JSON.parse(await handle.readFile("utf8")));
      if (!parsed.success) throw new StoreError("invalid_task_file", "Task file does not match the task schema.");
      return parsed.data;
    } catch (error) {
      if (error instanceof StoreError) throw error;
      if ((error as NodeJS.ErrnoException).code === "ENOENT") {
        throw new StoreError("task_not_found", "Task does not exist.");
      }
      if ((error as NodeJS.ErrnoException).code === "ELOOP") {
        throw new StoreError("unsafe_task_file", "Symbolic-link task files are not allowed.");
      }
      if (error instanceof SyntaxError) throw new StoreError("invalid_task_file", "Task file is not valid JSON.");
      throw new StoreError("store_unavailable", "Task storage is unavailable.", { cause: error });
    } finally {
      await handle?.close();
    }
  }

  async list(status?: Task["status"]): Promise<Task[]> {
    await this.initialize();
    const entries = await readdir(this.root, { withFileTypes: true });
    const tasks: Task[] = [];
    for (const entry of entries) {
      if (!entry.isFile() || !entry.name.endsWith(".json")) continue;
      const id = entry.name.slice(0, -5);
      if (!TaskIdSchema.safeParse(id).success) continue;
      try {
        const task = await this.readPath(this.pathFor(id));
        if (status === undefined || task.status === status) tasks.push(task);
      } catch (error) {
        if (!(error instanceof StoreError) || error.code === "store_unavailable") throw error;
      }
    }
    return tasks.sort((a, b) => a.id.localeCompare(b.id));
  }

  async get(taskId: string): Promise<Task> {
    await this.initialize();
    return this.readPath(this.pathFor(taskId));
  }

  async create(input: { id: string; title: string; details?: string }, now = new Date()): Promise<Task> {
    await this.initialize();
    const path = this.pathFor(input.id);
    const task = TaskSchema.parse({
      id: input.id,
      title: input.title,
      details: input.details ?? "",
      status: "open",
      createdAt: now.toISOString(),
      completedAt: null,
      completionNote: null,
    });

    let handle;
    try {
      handle = await open(
        path,
        constants.O_WRONLY | constants.O_CREAT | constants.O_EXCL | constants.O_NOFOLLOW,
        0o600,
      );
      await handle.writeFile(`${JSON.stringify(task, null, 2)}\n`);
      return task;
    } catch (error) {
      if ((error as NodeJS.ErrnoException).code === "EEXIST") {
        throw new StoreError("task_exists", "A task with this ID already exists.");
      }
      throw new StoreError("store_unavailable", "Task storage is unavailable.", { cause: error });
    } finally {
      await handle?.close();
    }
  }

  async complete(taskId: string, completionNote: string | undefined, now = new Date()): Promise<Task> {
    await this.initialize();
    const path = this.pathFor(taskId);
    const existing = await this.readPath(path);
    if (existing.status === "completed") return existing;
    const completed = TaskSchema.parse({
      ...existing,
      status: "completed",
      completedAt: now.toISOString(),
      completionNote: completionNote ?? null,
    });
    const temporary = resolve(this.root, `.${taskId}.${process.pid}.${randomUUID()}.tmp`);
    if (!temporary.startsWith(`${this.root}${sep}`)) {
      throw new StoreError("path_outside_root", "Temporary task path is outside the configured workspace.");
    }
    try {
      const handle = await open(
        temporary,
        constants.O_WRONLY | constants.O_CREAT | constants.O_EXCL | constants.O_NOFOLLOW,
        0o600,
      );
      try {
        await handle.writeFile(`${JSON.stringify(completed, null, 2)}\n`);
      } finally {
        await handle.close();
      }
      await rename(temporary, path);
      return completed;
    } catch (error) {
      throw new StoreError("store_unavailable", "Task storage is unavailable.", { cause: error });
    } finally {
      await rm(temporary, { force: true });
    }
  }
}
