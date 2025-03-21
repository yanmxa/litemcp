import asyncio
import sys
from agents import Agent, Runner
from dotenv import load_dotenv

from litemcp.manager import MCPServerManager

load_dotenv()


async def main(config):
    async with MCPServerManager(config) as server_manager:
        mcp_server_tools = await server_manager.agent_sdk_tools()
        agent = Agent(
            name="assistant",
            instructions="You are an AI assistant.",
            tools=mcp_server_tools,
        )
        result = await Runner.run(agent, "List all the kubernetes clusters")
        print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1]))

"""
$ python examples/agent_sdk/main.py examples/agent_sdk/mcp-config.json

Here are the Kubernetes clusters available:

1. **cluster1**
   - Hub Accepted: True
   - Managed Cluster URL: https://api.....com:6443
   - Joined: True
   - Available: True
   - Age: 30 days

2. **cluster2**
   - Hub Accepted: True
   - Managed Cluster URL: https://api.....com:6443
   - Joined: True
   - Available: True
   - Age: 30 days
"""
