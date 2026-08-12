# Test, Inspect, and Connect MCP Servers

## Learning objectives

By the end of this lesson, you will be able to:

- test an MCP server in memory without an LLM or network;
- use the Inspector to examine discovery, schemas, calls, and failures;
- choose stdio or Streamable HTTP by deployment boundary; and
- connect a local server to a host using an auditable launch command.

## Test protocol behavior without model variability

An MCP server can be tested directly. Do not make every test depend on a language model deciding to call the right tool. Verify discovery, schema, handler behavior, errors, and authorization deterministically first.

## Free local practice

Create `client.py` beside the prior lesson's server:

```python
import asyncio

from mcp import Client

from server import mcp


async def main() -> None:
    async with Client(mcp) as client:
        tools = await client.list_tools()
        names = [tool.name for tool in tools.tools]
        assert "next_review_interval" in names

        result = await client.call_tool("next_review_interval", {"score": 2})
        assert result.structured_content == {"days": 4}
        print(names)
        print(result.structured_content)


asyncio.run(main())
```

Run it locally:

```bash
uv run python client.py
```

Add assertions for boundary scores, invalid types, unknown resource IDs, and prompt arguments. Move repeated cases into `pytest` when the test set grows. Keep the in-memory tests even after adding transport-level integration tests.

## Use Inspector as a protocol workbench

The Inspector can:

- connect through supported transports;
- show tools, resources, prompts, descriptions, and schemas;
- call and read primitives with chosen arguments;
- display results and errors; and
- exercise missing, invalid, and concurrent cases.

It is a development tool, not production authorization. Do not expose it to untrusted networks or enter production secrets casually.

## Choose the transport boundary

Use **stdio** when one host launches one local child process. It has no listening network port, inherits a controlled environment, and reserves stdout for protocol messages. Use absolute executable and file paths because desktop hosts may start from an unexpected working directory.

Use **Streamable HTTP** for remote servers, shared services, or independent deployment. The 2026-07-28 protocol is stateless, but the service still needs HTTPS, authentication, authorization, timeouts, body limits, rate limits, safe routing headers, and observability. The legacy HTTP+SSE transport is deprecated for new work.

## Connect to a host safely

First verify that this launch command waits silently rather than exiting:

```bash
uv run --with "mcp[cli]" mcp run /absolute/path/to/study-mcp/server.py
```

Then register the same command in a compatible host's MCP configuration, following that host's current documentation. Inspect the generated or edited configuration before approval. A local MCP entry authorizes the host to execute a local command; treat it like installing software.

## Completion criteria

- [ ] In-memory tests cover discovery, success, boundary, type, and missing-resource cases.
- [ ] The Inspector shows the expected schemas and structured result.
- [ ] You can justify stdio or Streamable HTTP for two deployment scenarios.
- [ ] Local configuration uses an absolute path and a reviewed command.
- [ ] No application logging corrupts stdio protocol output.

## References

- [MCP Python SDK: Testing](https://py.sdk.modelcontextprotocol.io/get-started/testing/) - official in-memory testing patterns and assertions for server behavior.
- [MCP Inspector](https://modelcontextprotocol.io/docs/tools/inspector) - official interactive testing and debugging guide.
- [Connect to a Real Host](https://py.sdk.modelcontextprotocol.io/get-started/real-host/) - current official v2 guidance for stdio launch commands and common configuration failures.
- [MCP Python SDK: Writing Clients](https://py.sdk.modelcontextprotocol.io/client/) - current examples for in-memory, stdio, and Streamable HTTP clients.
- [The 2026-07-28 MCP Specification](https://blog.modelcontextprotocol.io/posts/2026-07-28/) - source for current stateless behavior and deprecations.

## Continue

Next: [Secure and Govern MCP Integrations](05-secure-and-govern-mcp-integrations.md)
