import asyncio
import sys
from openai import OpenAI

from dotenv import load_dotenv

from litemcp.manager import MCPServerManager

load_dotenv()


async def main(config):
    client = OpenAI()
    async with MCPServerManager(config) as server_manager:
        schemas = await server_manager.schemas()
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": "List the dirs in the /Users"}],
            tools=schemas,
        )
        print(completion.choices[0].message.tool_calls)

        # tool call
        tool_call = completion.choices[0].message.tool_calls[0]
        result = await server_manager.tool_call(
            tool_call.function.name, tool_call.function.arguments
        )
        print(result.content[0].text)


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1]))

"""
$ python examples/llm/openai_call.py examples/llm/mcp-config.json

[ChatCompletionMessageToolCall(id='call_qiITkP63oRM5BXGuS3ubpes8', function=Function(arguments='{"path":"/Users"}', name='list_directory'), type='function')]
[FILE] .localized
[DIR] Shared
[DIR] yanmeng
"""
