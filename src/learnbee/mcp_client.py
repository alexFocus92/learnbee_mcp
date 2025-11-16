import asyncio
import json
import os

from mcp import ClientSession
from mcp.client.sse import sse_client

MCP_SERVER_URL = os.environ.get(
    "MCP_SERVER_URL", "http://localhost:7860/gradio_api/mcp/sse"
)


class MCPClient:

    async def with_session(self, func):
        """
        Create a session with the MCP server and execute the provided function.
        - See: https://modelcontextprotocol.io/docs/concepts/transports#server-sent-events-sse
        """
        async with sse_client(MCP_SERVER_URL) as streams:
            async with ClientSession(streams[0], streams[1]) as session:
                await session.initialize()
                return await func(session)

    async def list(self):
        """List available tools from the MCP server."""
        async def _list(session):
            response = await session.list_tools()
            return response

        return await self.with_session(_list)

    async def get_book_list(self) -> str:
        """Get the list of books available on the MCP server."""
        async def _get_book_list(session):
            tool_name = "get_book_list"
            response = await session.call_tool(tool_name)
            if response.isError:
                raise ValueError(f"Error calling tool: {tool_name}")
            return response.content[0].text

        return await self.with_session(_get_book_list)

    async def get_book_content(self, book_name: str, max_length: int = 0) -> str:
        """Get the content of a book from the MCP server."""
        async def _get_book_content(session):
            tool_name = "get_book_content"
            input_data = {"book_name": book_name, "max_length": max_length}
            response = await session.call_tool(tool_name, input_data)
            if response.isError:
                raise ValueError(f"Error calling tool: {tool_name}")
            return response.content[0].text

        return await self.with_session(_get_book_content)


async def main():
    mcp_client = MCPClient()

    tools = await mcp_client.list()
    print("Available tools:")
    print("=" * 20)
    for tool in tools.tools:
        print(f"Name: {tool.name}")
        print(f"Description: {tool.description}")
        print(f"Input Schema: {tool.inputSchema}")
        print(f"Annotations: {tool.annotations}")
        print("-" * 20)

    book_list_str = await mcp_client.get_book_list()
    book_list = json.loads(book_list_str)
    print(f"Number of books available: {len(book_list)}")

    book_name = book_list[0]
    book_content = await mcp_client.get_book_content(book_name, max_length=100)
    print(f"Content of the book '{book_name}':")
    print(book_content + "...")


if __name__ == "__main__":
    asyncio.run(main())
