from typing import List, Any, Dict, Callable, Set

from langchain_core.tools import BaseTool, StructuredTool, ToolException
from mcp import ClientSession
from mcp.types import (
    CallToolResult,
    EmbeddedResource,
    ImageContent,
    TextContent,
)
from mcp.types import (
    Tool,
)

# The original implementation from https://github.com/langchain-ai/langchain-mcp-adapters
NonTextContent = ImageContent | EmbeddedResource


def _convert_call_tool_result(
    call_tool_result: CallToolResult,
) -> tuple[str | list[str], list[NonTextContent] | None]:
    text_contents: list[TextContent] = []
    non_text_contents = []
    for content in call_tool_result.content:
        if isinstance(content, TextContent):
            text_contents.append(content)
        else:
            non_text_contents.append(content)

    tool_content: str | list[str] = [content.text for content in text_contents]
    if len(text_contents) == 1:
        tool_content = tool_content[0]

    if call_tool_result.isError:
        raise ToolException(tool_content)

    return tool_content, non_text_contents or None


async def covert_to_langchain_tools(
    tools: List[Tool],
    client_session: ClientSession,
    validators: Dict[str, Callable[[dict], str]],
) -> List[BaseTool]:

    def build_langchain_tool(tool: Tool) -> BaseTool:
        """Wraps a single MCP tool with validator and LangChain-compatible interface."""
        validator = validators.get(tool.name)

        async def invoke_tool(**kwargs: dict[str, Any]):
            # Step 1: Run validator if available
            if validator:
                validation_result = validator(kwargs)
                if validation_result:
                    return validation_result, None

            # Step 2: Call the MCP server
            result = await client_session.call_tool(tool.name, kwargs)

            # Step 3: Convert to LangChain-compatible format
            return _convert_call_tool_result(result)

        return StructuredTool(
            name=tool.name,
            description=tool.description or "",
            args_schema=tool.inputSchema,
            coroutine=invoke_tool,
            response_format="content_and_artifact",
        )

    return [build_langchain_tool(tool) for tool in tools]
