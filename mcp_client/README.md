# MCP Client - Connecting to an External MCP Server

## Requirements

- **Python 3.10+**
- **Node.js and npm** (for the npx command)

## Installation

```bash
pip install -r requirements.txt
```

## Examples

| File | What it does |
|------|-------------|
| `connect_to_remote_mcp_server.py` | Full demo: lists tools/resources/prompts + calls tools |
| `example_echo_tool.py` | Sends a message and gets it back (echo) |
| `example_add_tool.py` | Adds two numbers using get-sum (42 + 58) |
| `example_list_tools.py` | Lists all available tools on a server |
| `example_get_env.py` | Reads an environment variable using get-env |
| `example_read_file.py` | Reads a file from disk |

```bash
python connect_to_remote_MCP_server.py
python example_echo_tool.py
python example_add_tool.py
python example_list_tools.py
python example_get_env.py
python example_read_file.py
```

## Connecting to a Different MCP Server

Modify the `SERVER_PARAMS` variable in any script:

```python
# Filesystem MCP Server example
SERVER_PARAMS = StdioServerParameters(
    command="npx",
    args=["-y", "@modelcontextprotocol/server-filesystem", "/path/to/directory"],
)
```

## What is MCP?

**Model Context Protocol (MCP)** is an open standard that enables LLMs to access external tools and data sources through a standardized protocol. It was developed by Anthropic.

- 📖 [MCP Documentation](https://modelcontextprotocol.io)
- 📦 [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
