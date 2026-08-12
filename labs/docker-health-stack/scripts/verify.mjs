import { readFile } from "node:fs/promises";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const labRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");

export function inspectSources({ dockerfile, compose, server }) {
  const errors = [];
  const checks = [
    [dockerfile, /^USER\s+\d+:\d+$/m, "Dockerfile must select a numeric non-root USER."],
    [dockerfile, /^HEALTHCHECK\b/m, "Dockerfile must define HEALTHCHECK."],
    [dockerfile, /COPY\s+--chown=/, "Dockerfile COPY must assign non-root ownership."],
    [dockerfile, /^VOLUME\s+\[?["']?\/data/m, "Dockerfile must declare /data as persistent state."],
    [compose, /healthcheck:/, "Compose must define a healthcheck."],
    [compose, /condition:\s*service_healthy/, "Dependent probe must wait for service_healthy."],
    [compose, /state-data:\/data/, "Compose must mount state-data at /data."],
    [compose, /read_only:\s*true/, "Compose service must use a read-only root filesystem."],
    [compose, /cap_drop:[\s\S]*?-\s*ALL/, "Compose service must drop Linux capabilities."],
    [compose, /no-new-privileges:true/, "Compose service must disable privilege escalation."],
    [compose, /restart:\s*unless-stopped/, "App must define a restart policy."],
    [server, /\/health\/live/, "App must expose a liveness endpoint."],
    [server, /\/health\/ready/, "App must expose a readiness endpoint."],
    [server, /\/counter/, "App must expose persistent counter behavior."],
    [server, /\/admin\/failure/, "App must expose controlled failure injection."],
    [server, /x-failure-token/, "Failure injection must require a token."],
    [server, /rename\(/, "Persistent updates must use atomic rename."],
  ];
  for (const [source, pattern, message] of checks) {
    if (!pattern.test(source)) errors.push(message);
  }
  if (/^USER\s+(?:0|root)(?::(?:0|root))?$/m.test(dockerfile)) {
    errors.push("Dockerfile must not run as root.");
  }
  if (/TODO/i.test(`${dockerfile}\n${compose}\n${server}`)) errors.push("Target still contains TODO markers.");
  return errors;
}

export async function verifyTarget(target = "solution", root = labRoot) {
  try {
    const [dockerfile, compose, server] = await Promise.all([
      readFile(join(root, target, "Dockerfile"), "utf8"),
      readFile(join(root, target, "compose.yaml"), "utf8"),
      readFile(join(root, target, "app", "server.mjs"), "utf8"),
    ]);
    return inspectSources({ dockerfile, compose, server });
  } catch (error) {
    return [`Cannot read target files: ${error.message}`];
  }
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) {
  const target = process.argv[2] ?? "solution";
  const errors = await verifyTarget(target);
  if (errors.length > 0) {
    process.stderr.write(`Static verification failed for ${target}:\n- ${errors.join("\n- ")}\n`);
    process.exitCode = 1;
  } else {
    process.stdout.write(`Verified ${target}: container user, health, persistence, hardening, and failure controls found.\n`);
  }
}
