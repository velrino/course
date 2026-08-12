import { spawnSync } from "node:child_process";

const target = process.argv[2] ?? "solution";
const result = spawnSync(process.execPath, ["--test", "test/contract.test.js"], {
  stdio: "inherit",
  env: { ...process.env, LAB_TARGET: target },
});
process.exit(result.status ?? 1);
