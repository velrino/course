# Python Projects, Types, and Boundaries

## Learning objectives

- Create an isolated, reproducible Python automation project.
- Separate pure decision logic from input/output side effects.
- Use types, dataclasses, exceptions, and explicit configuration boundaries.

## Structure for change and failure

An automation script becomes operational software when someone schedules it, trusts its output, or gives it credentials. Keep the entry point thin and separate four concerns:

```text
configuration -> adapters/input -> domain decisions -> adapters/output
```

Pure functions accept values and return values without reading files, clocks, environment variables, or networks. They are easy to test. Adapters perform side effects and translate failures into domain-specific exceptions. Dependency direction should point inward: decision code does not import a particular HTTP client or database.

Use a virtual environment per project and record direct dependencies in `pyproject.toml` or the repository's established lock format. Do not commit `.venv` or secrets. Pin a supported Python range and provide one documented setup command. Type hints make contracts visible; a type checker catches mismatches but does not validate hostile runtime data.

Model internal records with `@dataclass(frozen=True)` where immutability is useful. Validate external data at the boundary. Raise narrow exceptions such as `InvalidRecord` or `TemporaryServiceError`; do not catch `Exception` merely to continue with corrupt state. Use context managers for files, locks, transactions, and connections so cleanup occurs on both success and failure.

## Free local practice

Create a project named `invoice_audit`:

```text
invoice-audit/
  pyproject.toml
  src/invoice_audit/{__init__.py,domain.py,io.py,cli.py}
  tests/
```

Create a virtual environment with `python -m venv .venv`. Define immutable `Invoice` and `Finding` dataclasses. Write a pure `audit(invoice, rules) -> list[Finding]` function for negative amounts, duplicate IDs, and totals that disagree with line items. Put CSV loading and result writing in `io.py`; put argument parsing and exit codes in `cli.py`.

Add a `Config` dataclass built once from command-line arguments and selected environment variables. Reject missing or invalid configuration before reading inputs. Make the main function return an integer and call `raise SystemExit(main())`. Run a type checker such as `mypy` or `pyright` if available.

## Completion criteria

- A fresh virtual environment can install and run the project from documented metadata.
- Domain decisions have no file, network, environment, or wall-clock access.
- Invalid external records fail with a field-specific message and nonzero exit code.
- No credential, machine-specific path, or `.venv` content is committed.

## References

- [Python tutorial](https://docs.python.org/3/tutorial/) - official language, data structure, exception, class, and module introduction.
- [Python virtual environments](https://docs.python.org/3/library/venv.html) - standard-library environment isolation.
- [Python dataclasses](https://docs.python.org/3/library/dataclasses.html) - generated data-object methods and frozen instances.
- [Python packaging project metadata](https://packaging.python.org/en/latest/specifications/pyproject-toml/) - standardized `pyproject.toml` tables.
- [Typing documentation](https://typing.python.org/en/latest/) - official typing guides and specification.
