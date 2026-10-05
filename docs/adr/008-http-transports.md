# ADR 008: Optional HTTP Transports

- **Status:** Accepted
- **Date:** 2026-10-03
- **Supersedes:** [ADR 002](002-transport-protocol.md)

## Context

ADR 002 selected stdio as the sole transport. The server now needs to support
clients that connect over HTTP while retaining the existing local subprocess
behavior for clients such as Claude Desktop and Claude Code.

The MCP SDK supports three transports on the same `FastMCP` server:

1. **stdio** -- local stdin/stdout communication
2. **Streamable HTTP** -- the current HTTP transport
3. **SSE** -- the legacy HTTP transport for client compatibility

## Decision

Keep **stdio** as the default and expose the HTTP transports as explicit CLI
options:

```text
--transport=stdio
--transport=streamable-http
--transport=sse
```

HTTP transports bind to `127.0.0.1` on port `8096` by default. The bind
address and port can be changed with `--host` and `--port`.

## Rationale

Keeping stdio as the default preserves existing client configurations and
avoids introducing a network listener for local use. Explicit transport
selection makes HTTP deployment deliberate rather than accidental.

Streamable HTTP is preferred for new integrations. SSE remains available for
clients that have not migrated to the newer transport.

The HTTP transports do not provide application-level authentication in this
server. Localhost defaults limit exposure; deployments that bind to other
interfaces must provide authentication and TLS through the deployment layer.

## Consequences

- Existing invocations continue to use stdio without changes.
- Streamable HTTP is served at `/mcp`.
- SSE is served at `/sse`, with messages posted to `/messages/`.
- HTTP deployments require network lifecycle and access-control management.
- `server.json` and Smithery continue to advertise stdio as the default
  package transport.
