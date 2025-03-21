# ✨ litemcp

A minimal, lightweight client designed to simplify SDK adoption into MCP.

litemcp enables rapid and intuitive integration of various AI SDKs (e.g., LangChain, Agent SDK) into your MCP projects, emphasizing simplicity, flexibility, and minimal dependencies.

## 🌟 Key Features

- **Simplicity:** Streamlined interfaces ensure easy integration.
- **Flexibility:** Quickly adopt diverse SDKs with minimal effort.
- **Lightweight:** Designed with minimal dependencies to maximize clarity and performance.

## 🛠 Installation

Install via pip:

```bash
pip install litemcp
```

## 🚀 Quick Start

Here's a concise example demonstrating integration with OpenAI Agent SDK:

```python
import asyncio
import sys
from mcp_server import MCPServerManager
from openai_agent_sdk import Agent, Runner

async def main():
    async with MCPServerManager(sys.argv[1]) as server_manager:
        mcp_server_tools = await server_manager.agent_sdk_tools()
        agent = Agent(
            name="assistant",
            instructions="You are an AI assistant.",
            tools=mcp_server_tools,
        )
        result = await Runner.run(agent, "List all the kubernetes clusters")
        print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
```

### 🔐 Tool Call Validator(Optional)

You can add a **custom validation function** to control MCP tool calls. This helps prevent server tools from directly accessing your system without permission—such as integrating a **human-in-the-loop** step.

---

#### 1. Define the Validator

```python
def applier_validator(func_args) -> Optional[str]:
    """
    Return:
    - None: allow the tool call
    - str : block the tool call and return message instead
    """
    user_input = console.input(
        f"  🛠  Cluster - [yellow]{cluster}[/yellow] ⎈ Proceed with this YAML? (yes/no): "
    ).strip().lower()

    if user_input in {"yes", "y"}:
        return None
    if user_input in {"no", "n"}:
        console.print("[red]Exiting process.[/red]")
        sys.exit(0)
    return user_input
```

---

#### 2. Register the Validator with MCP Server

```python
async with MCPServerManager(sys.argv[1]) as server_manager:
    server_manager.register_validator("yaml_applier", applier_validator)

    mcp_server_tools = await server_manager.function_tools()

    engineer = Agent(...)
```

## 📖 MCP Configuration Schema

Configure your MCP environment with optional server enabling and tool exclusion:

```json
{
  "mcpServers": {
    "fetch": {
      "command": "uvx",
      "args": ["mcp-server-fetch"]
    },
    "youtube": {
      "command": "npx",
      "args": ["-y", "github:anaisbetts/mcp-youtube"],
      "exclude_tools": ["..."]
    },
    "mcp-server-commands": {
      "command": "npx",
      "args": ["mcp-server-commands"],
      "requires_confirmation": [
        "run_command",
        "run_script"
      ],
      "enabled": false
    },
     "multicluster-mcp-server": {
      "command": "node",
      "args": [".../multicluster-mcp-server/build/index.js"],
      "enabled": false
    }
  }
}
```

- Use `"enabled": true/false` to activate or deactivate servers.
- Use `"exclude_tools"` to omit unnecessary tools from the current MCP server.

## 📖 Documentation

Detailed documentation coming soon!

## 📢 Contributing

Contributions and suggestions are welcome! Please open an issue or submit a pull request.

## 📜 License

liteMCP is available under the MIT License.
