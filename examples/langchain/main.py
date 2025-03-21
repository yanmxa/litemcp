import asyncio
import sys
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from typing import List
from langchain_core.tools import BaseTool

from litemcp.manager import MCPServerManager

load_dotenv()


async def main(config):
    chat = ChatOpenAI(model="gpt-3.5-turbo-0125")
    async with MCPServerManager(config) as server_manager:

        # bind tools
        tools: List[BaseTool] = await server_manager.langchain_tools()
        chat_with_tools = chat.bind_tools(tools, tool_choice="any")

        messages = [
            SystemMessage(content="You're a helpful assistant"),
            HumanMessage(content="List the dirs in the /Users"),
        ]
        tool_calls = chat_with_tools.invoke(messages).tool_calls

        # invoke the tool_call
        tool_map = {tool.name: tool for tool in tools}
        for tool_call in tool_calls:
            selected_tool = tool_map[tool_call["name"].lower()]
            tool_output = await selected_tool.ainvoke(tool_call["args"])
            print(tool_output)


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1]))

# """
# $ python examples/langchain/main.py examples/langchain/mcp-config.json

# Secure MCP Filesystem Server running on stdio
# Allowed directories: [ '/Users' ]
# [FILE] .localized
# [DIR] Shared
# [DIR] yanmeng
# """
