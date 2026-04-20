# `scripts/som-client`

`SomClient` is a tiny stdlib-only client for the Remote MCP bridge.

## Environment

- `SOM_MCP_URL` (default: `http://localhost:8080`)
- `SOM_MCP_TOKEN` (required for `Authorization: Bearer ...` in this stage)
- `CF_ACCESS_CLIENT_ID` (optional)
- `CF_ACCESS_CLIENT_SECRET` (optional)
- `SOM_MCP_USER_AGENT` (optional)
- `SOM_REMOTE_MCP_AUDIT_HMAC_KEY` (used by `verify_audit.py` when required)

## Usage

```python
from som_client import SomClient

client = SomClient.from_env()
health = client.ping()
pkt = client.handoff(
    prior={"role": "worker"},
    next_tier=2,
    artifacts=[],
)
```

## Headers

`SomClient` sends:

- `Authorization: Bearer <SOM_MCP_TOKEN>`
- `Cf-Access-Client-Id` and `Cf-Access-Client-Secret` when both are set
- `User-Agent` when `SOM_MCP_USER_AGENT` is set

## Error behavior

Errors are intentionally payload-safe: transport/protocol failures return
`SomClientError` with no request-body echo.

## CLI

`python3 scripts/som-client/som_client.py`  
Sends a `ping` request and exits non-zero on transport failure.
