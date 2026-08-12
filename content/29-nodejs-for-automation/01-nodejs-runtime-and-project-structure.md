# Node.js Runtime and Project Structure

Node.js runs JavaScript outside a browser and is especially useful for automation that waits on files, databases, subprocesses, or network services. Its JavaScript runs on an event loop. Many built-in I/O APIs delegate work and settle a promise later, allowing one process to keep multiple operations in flight. A long synchronous loop or a large synchronous file read still blocks that loop, so "asynchronous" is an architectural choice, not an automatic property.

Use a currently supported Node release. The examples in this module target Node 22 or newer and use ECMAScript modules (ESM). Check the installed runtime with `node --version`; do not assume that the interactive shell, a scheduler, and a production host use the same binary.

## Learning objectives

- Explain the event loop distinction between I/O concurrency and CPU parallelism.
- Create a private ESM project with repeatable scripts and an explicit runtime requirement.
- Separate configuration, pure domain logic, and side-effecting adapters.
- Fail early when required configuration or input is invalid.
- Keep secrets and machine-specific values out of source code.

## Runtime model for automation

An automation normally has four boundaries:

1. **Input adapter:** CLI arguments, files, HTTP requests, or queue messages.
2. **Validation and domain logic:** deterministic functions that reject malformed data and decide what should happen.
3. **Output adapter:** filesystem writes, API calls, database statements, or subprocesses.
4. **Operational shell:** configuration, logging, retries, cancellation, and exit status.

Keep the middle deterministic. A function that accepts a value and returns a value is inexpensive to test. A function that reads environment variables, fetches a URL, mutates a record, and writes a file in one block is difficult to replay safely.

Node supports CommonJS and ESM, but mixing their conventions casually causes import and packaging surprises. Setting `"type": "module"` makes `.js` files in this package ESM. Commit `package-lock.json` whenever dependencies are introduced, and use `npm ci` in automated environments to install exactly the locked tree. This first project has no third-party runtime dependencies.

Environment variables arrive as strings or are absent. Parse and validate them once at startup. Do not log tokens, passwords, webhook secrets, full request headers, or unredacted personal data.

## Free local practice

Create the project:

```sh
mkdir node-automation-lab
cd node-automation-lab
mkdir src test
```

Create `package.json`:

```json
{
  "name": "node-automation-lab",
  "private": true,
  "type": "module",
  "engines": {
    "node": ">=22"
  },
  "scripts": {
    "start": "node src/cli.js",
    "test": "node --test"
  }
}
```

Create `src/config.js`:

```javascript
export function loadConfig(env = process.env) {
  const outputDir = env.OUTPUT_DIR?.trim();
  if (!outputDir) {
    throw new Error("OUTPUT_DIR is required");
  }

  const timeoutMs = Number(env.TIMEOUT_MS ?? "5000");
  if (!Number.isInteger(timeoutMs) || timeoutMs < 100 || timeoutMs > 60_000) {
    throw new Error("TIMEOUT_MS must be an integer from 100 to 60000");
  }

  return Object.freeze({ outputDir, timeoutMs });
}
```

Create `src/domain.js`:

```javascript
export function normalizeRecord(value) {
  if (value === null || typeof value !== "object" || Array.isArray(value)) {
    throw new TypeError("record must be an object");
  }

  const validId = typeof value.id === "string" || Number.isSafeInteger(value.id);
  if (!validId || typeof value.name !== "string") {
    throw new TypeError("record.id must be a string or integer and record.name must be a string");
  }
  const id = String(value.id).trim();
  const name = value.name.trim();
  if (!id || !name) {
    throw new TypeError("record.id and record.name are required");
  }

  return { id, name: name.replaceAll(/\s+/g, " ") };
}
```

Create `src/cli.js`:

```javascript
import { loadConfig } from "./config.js";
import { normalizeRecord } from "./domain.js";

try {
  const config = loadConfig();
  const raw = process.argv[2];
  if (!raw) throw new Error("pass one JSON record as the first argument");

  const record = normalizeRecord(JSON.parse(raw));
  console.log(JSON.stringify({ config, record }));
} catch (error) {
  console.error(JSON.stringify({
    level: "error",
    event: "startup_failed",
    message: error instanceof Error ? error.message : String(error)
  }));
  process.exitCode = 1;
}
```

Run it:

```sh
OUTPUT_DIR=var/output npm start -- '{"id":7,"name":"  Ada   Lovelace "}'
TIMEOUT_MS=invalid OUTPUT_DIR=var/output npm start -- '{"id":7,"name":"Ada"}'
```

The first command should emit normalized JSON. The second should fail with exit status 1. Notice that domain code never reads `process.env`, writes output, or terminates the process.

## Completion criteria

- `node --version` reports 22 or newer and `npm start` runs the ESM entry point.
- Valid input is normalized, while missing configuration, malformed JSON, and missing fields return a nonzero exit status.
- You can identify which files own configuration, domain logic, and process-level behavior.
- No secret or host-specific value is committed to `package.json` or JavaScript source.
- You can explain why `readFileSync` or CPU-heavy loops in a request handler can delay unrelated work.

## References

- [Node.js: Introduction to Node.js](https://nodejs.org/en/learn/getting-started/introduction-to-nodejs)
- [Node.js: The Node.js event loop](https://nodejs.org/en/learn/asynchronous-work/event-loop-timers-and-nexttick)
- [Node.js: ECMAScript modules](https://nodejs.org/api/esm.html)
- [Node.js: Modules and package type](https://nodejs.org/api/packages.html)
- [Node.js: Environment variables](https://nodejs.org/api/environment_variables.html)
- [npm: package.json](https://docs.npmjs.com/cli/v11/configuring-npm/package-json)
- [npm: package-lock.json](https://docs.npmjs.com/cli/v11/configuring-npm/package-lock-json)

[Next lesson: Files, CLI, and Data Validation](./02-files-cli-and-data-validation.md)
