import { spawnSync } from "node:child_process";

const target = process.argv[2] ?? "solution";
const result = spawnSync(process.execPath, ["--import", "tsx", "--test", "test/sdk-contract.test.ts"], {
  stdio: "inherit",
  env: { ...process.env, LAB_TARGET: target },
});
process.exit(result.status ?? 1);
