# Build a Local MCP Server

## Learning objectives

By the end of this lesson, you will be able to:

- create a Python MCP project with the current stable SDK;
- expose a typed tool, resource template, and prompt;
- run the server through the MCP development tooling; and
- explain what the SDK derives from type hints and docstrings.

## Pin the generation of the protocol and SDK

MCP evolves quickly. This lesson targets the 2026-07-28 specification and version 2 of the official Python SDK, the current stable line at the time of writing. Record the exact installed version in your lab. When documentation and installed code disagree, consult the SDK's matching-version documentation and migration guide.

The SDK converts Python type hints and registered handlers into protocol schemas and routing. That removes serialization boilerplate, not the need for domain validation, permission checks, tests, or threat modeling.

## Free local practice

Install the free `uv` package manager using its official instructions, then:

```bash
uv init study-mcp
cd study-mcp
uv add "mcp[cli]"
uv run mcp version
```

Create `server.py`:

```python
from mcp.server import MCPServer

mcp = MCPServer("Study Review")

MODULES = {
    "1": "Learning How to Learn",
    "6": "Web, APIs, and Webhooks",
    "8": "Model Context Protocol",
}


@mcp.tool()
def next_review_interval(score: int) -> dict[str, int]:
    """Return a suggested review interval for a score from 0 through 3."""
    if score not in range(4):
        raise ValueError("score must be an integer from 0 through 3")
    return {"days": [1, 2, 4, 8][score]}


@mcp.resource("course://modules/{number}")
def read_module(number: str) -> str:
    """Read the title of a course module."""
    if number not in MODULES:
        raise ValueError(f"unknown module: {number}")
    return MODULES[number]


@mcp.prompt(title="Review a Course Module")
def review_module(number: str) -> str:
    """Create a retrieval-practice prompt for one module."""
    return (
        f"Review module {number}. First retrieve its key ideas without sources, "
        "then check the course resource and record corrections."
    )
```

Launch the development environment:

```bash
uv run mcp dev server.py
```

The command starts the MCP Inspector and prints a local URL. It requires Node.js and `npx`; use the in-memory client in the next lesson if you do not have them. In the Inspector:

1. list all three primitive types;
2. call the tool with scores `0`, `3`, `4`, and `"3"`;
3. read known and unknown module resources; and
4. render the prompt for module `8`.

## Inspect generated contracts

Confirm that the tool schema has an integer argument and structured result, that the resource is a URI template, and that the prompt exposes a required argument. Then tighten `score` with a constrained type following current SDK documentation and rerun the invalid cases.

For stdio servers, stdout is protocol transport. Application logs must not corrupt it; use the logging facilities and stderr behavior documented by the SDK.

## Completion criteria

- [ ] You recorded Python, `uv`, MCP SDK, and protocol versions.
- [ ] Inspector discovers the tool, resource template, and prompt.
- [ ] Valid tool calls return structured data and invalid calls fail clearly.
- [ ] Unknown resources do not return invented content.
- [ ] You can explain which schema elements came from names, type hints, decorators, and docstrings.

## References

- [MCP Python SDK v2](https://py.sdk.modelcontextprotocol.io/) - current stable SDK requirements, installation, minimal server, and Inspector workflow.
- [MCP Python SDK: Get Started](https://py.sdk.modelcontextprotocol.io/get-started/) - copyable examples tested by the SDK's own continuous integration.
- [MCP Python SDK on GitHub](https://github.com/modelcontextprotocol/python-sdk) - official source, release history, examples, issues, and migration information.
- [uv Documentation](https://docs.astral.sh/uv/) - official installation and project-management guide for the free open-source Python tool used in the lab.

## Continue

Next: [Test, Inspect, and Connect MCP Servers](04-test-inspect-and-connect-mcp-servers.md)
