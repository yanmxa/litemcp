import json
from mcp import types, ClientSession, Tool
from typing import List, Any, Dict, Callable, Set
from agents.tool import FunctionTool
from agents.run_context import RunContextWrapper


async def covert_to_agent_sdk_tools(
    tools: List[Tool],
    client_session: ClientSession,
    validators: Dict[str, Callable[[dict], str]],
) -> List[FunctionTool]:
    async def on_invoke_tool(
        ctx: RunContextWrapper[Any], parameters: str, tool_name: str
    ) -> str:
        """Handles tool invocation with JSON parsing."""
        params = json.loads(parameters) if isinstance(parameters, str) else parameters
        # human in loop
        validator = validators.get(tool_name)
        if validator:
            if result := validator(params):
                return result
        # add access control in here
        result: types.CallToolResult = await client_session.call_tool(tool_name, params)

        if result.isError:
            return "".join(c.text for c in result.content)
        return str(result)

    return [
        FunctionTool(
            name=tool.name,
            description=tool.description,
            params_json_schema=tool.inputSchema,
            on_invoke_tool=lambda ctx, params, tool_name=tool.name: on_invoke_tool(
                ctx, params, tool_name
            ),
            strict_json_schema=False,
        )
        for tool in tools
    ]


async def covert_to_openai_tool_schemas(
    tools: List[Tool],
    client_session: ClientSession,
    validators: Dict[str, Callable[[dict], str]],
) -> List[Dict]:
    return [
        {
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.inputSchema,
            },
        }
        for tool in tools
    ]
