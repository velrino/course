# Run and Evaluate a Small Local Model

## Learning objectives

By the end of this lesson, you will be able to:

- run an openly available model without a paid inference API;
- record model identity, configuration, latency, and resource constraints;
- build a small evaluation set before changing prompts; and
- interpret local execution as a privacy option, not a complete security guarantee.

## Choose a feasible runtime and model

Local inference avoids per-request API charges and can keep request content on the device. It still requires disk, memory, compute, electricity, software updates, and license review. The model file is usually downloaded from the internet once. Some models are open-weight under licenses that impose conditions; "available to download" does not mean public domain.

This lab uses Ollama because it provides a cross-platform local CLI and HTTP API. The example `gemma3:270m` is small enough for many computers, but model availability and requirements can change. Confirm the current model page, license, disk size, and runtime version before downloading. A very small model is useful for learning the system, not proof of production quality.

## Establish an evaluation before experimenting

Create `local-model-eval.md` with five cases:

| ID | Input | Required elements | Forbidden behavior |
| --- | --- | --- | --- |
| E1 | Return JSON with keys `topic` and `level` for "HTTP beginner." | valid JSON, exact keys | extra prose |
| E2 | Summarize a supplied three-sentence paragraph. | only supplied facts | invented source |
| E3 | "Who won a fictional 2035 award?" | state insufficient evidence | invented person |
| E4 | Extract two dates from supplied text. | exact source dates | normalization not requested |
| E5 | Explain tokens in three bullets. | token boundaries and IDs | claim tokens always equal words |

Score each requirement as pass or fail. Keep the same cases when changing settings.

## Free local practice

1. Install Ollama using the official quickstart for your operating system.
2. Confirm the installed CLI:

```bash
ollama --version
```

3. Review the model page, then download and run the small model:

```bash
ollama run gemma3:270m
```

4. Run every evaluation case in a fresh conversation and preserve exact outputs.
5. List local models and stop the running model when finished:

```bash
ollama ls
ollama ps
ollama stop gemma3:270m
```

If the runtime or model cannot run on your hardware, do not substitute a paid service. Complete the evaluation design, inspect the official API example, and record the resource constraint as the lab result. That is a valid infrastructure finding.

## Interpret results carefully

Record:

- runtime version and model tag;
- model source and license link;
- approximate download size;
- hardware and operating system;
- prompt and output for every case;
- elapsed time and pass/fail rubric; and
- whether any request left the device according to runtime configuration.

Local execution does not sanitize malicious files, prevent the model from producing harmful output, encrypt the device, or authorize tool actions. Bind local APIs to appropriate interfaces, update the runtime, restrict file and network access, and never expose an unauthenticated inference endpoint to an untrusted network.

## Completion criteria

- [ ] You created the evaluation set before changing model behavior.
- [ ] You documented runtime, model tag, source, license, and hardware.
- [ ] You preserved exact inputs and outputs for all five cases or documented a hardware blocker.
- [ ] You scored requirements individually rather than giving one subjective rating.
- [ ] You can name at least four risks that local inference does not remove.

## References

- [Ollama Quickstart](https://docs.ollama.com/quickstart) - official installation, local chat, and local API starting point.
- [Ollama CLI Reference](https://docs.ollama.com/cli) - official commands for pulling, running, listing, stopping, and removing models.
- [Gemma 3 Model Page for Ollama](https://ollama.com/library/gemma3) - current tags, sizes, requirements, source information, and model details for the lab example.
- [Hugging Face Model Cards](https://huggingface.co/docs/hub/model-cards) - documentation on recording intended use, limitations, datasets, evaluation, and licenses.
- [Transformers.js](https://huggingface.co/docs/transformers.js/en/index) - free alternative for running compatible pretrained models locally in a browser or JavaScript runtime.

## Continue

Next module: [Write Clear Prompt Contracts](../05-prompt-context-and-loop-engineering/01-write-clear-prompt-contracts.md)
