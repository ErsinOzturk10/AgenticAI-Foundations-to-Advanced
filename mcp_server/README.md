# Custom MCP Server & Client

Build and run your own MCP server, then connect to it from a separate terminal.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Terminal 1 — Start the server

```bash
python my_server.py
```

You should see:

```
🚀 Starting My Custom MCP Server...
   Host: localhost
   Port: 8000
   Transport: SSE
```

### Terminal 2 — Run the client

```bash
python my_client.py
```

The client will:

1. Connect to the server via SSE
2. List all available tools
3. Call each tool and print the results

## Server Tools

| Tool | Parameters | Description |
|------|-----------|-------------|
| `greet` | `name` (string) | Returns a greeting message |
| `add` | `a`, `b` (number) | Adds two numbers |
| `multiply` | `a`, `b` (number) | Multiplies two numbers |
| `current_time` | — | Returns current date and time |

## How It Works

- **Server** (`my_server.py`): Uses `FastMCP` to define tools as simple Python functions with the `@server.tool()` decorator. Runs on `localhost:8000` using SSE transport.
- **Client** (`my_client.py`): Uses `sse_client` to connect to the server, then uses `ClientSession` to list and call tools.
