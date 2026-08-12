# Free and Local Learning Environment

## Objectives

Set up a reproducible environment without making a paid AI service a prerequisite.

## Minimum setup

Install only what the current module needs. A practical base consists of:

- Git for version history.
- Python 3 and an isolated virtual environment.
- A code editor with a plain terminal.
- Docker Desktop or Docker Engine when your computer supports containers.
- A modern browser for n8n and local web interfaces.

Use `python -m venv .venv` when a lesson does not specify another environment manager. Keep secrets in environment variables or an ignored `.env` file. Never commit access tokens.

## Three compute paths

### Path A: No local model

Use deterministic mock model functions. A mock can return fixed JSON based on a small set of inputs. This path is sufficient for learning workflow state, retries, schemas, tool permissions, logging, evaluation, and human approval.

### Path B: Small local model

Tools such as Ollama can run compatible open-weight models locally. Hardware requirements vary significantly by model and quantization. Start small, confirm the model's license, and do not claim that local execution automatically makes a system secure; prompts and outputs may still be logged by your own applications.

### Path C: Hosted notebook or API

Some services provide limited free access, but quotas and terms can change. Treat hosted execution as optional. Remove personal or confidential data, set a strict spending limit before adding billing, and preserve a local mock mode so development does not stop when a quota ends.

## Reproducibility checklist

For every coded artifact, record:

- operating system and architecture;
- language and package versions;
- installation and run commands;
- required environment-variable names, never their values;
- sample non-sensitive input;
- expected output shape;
- cleanup command and persistent data location.

Pin direct dependencies for finished projects. During early lessons, prefer a short requirements file over a large generated environment dump you do not understand.

## Practice

Create a private practice repository. Add `.gitignore`, `learning-journal.md`, and a minimal Python program that prints the Python version. Run it inside a virtual environment, commit it, clone the repository into a temporary directory, and verify that the documented setup works from scratch.

## Completion criteria

- You can rebuild the practice environment from written instructions.
- No secret is present in version control.
- You selected a compute path that fits your hardware and budget.
- Your environment has a model-independent mock path.

## References

- [Python: Creating Virtual Environments](https://docs.python.org/3/tutorial/venv.html)
- [Git Reference](https://git-scm.com/docs)
- [Docker Get Started](https://docs.docker.com/get-started/)
- [Ollama Documentation](https://docs.ollama.com/)
- [GitHub: Ignoring Files](https://docs.github.com/en/get-started/getting-started-with-git/ignoring-files)
