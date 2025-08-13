from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession
from contextlib import AsyncExitStack
import asyncio


class MCPClient:
    def __init__(self,url:str):
        self.url = url
        self.stack = AsyncExitStack()
        self.session = None
    
    async def __aenter__(self):
        read, write,_ = await self.stack.enter_async_context(streamablehttp_client(self.url))
        
        self.session = await self.stack.enter_async_context(ClientSession(read,write))
        
        self.session.initialize()
        
        return self

    async def __aexit__(self,exc_type,exc_val,exc_tb):
        await self.stack.aclose()

    async def call_tool(self,tool_name:str,arguments:dict):
        print("Calling Tool")
        return await self.session.call_tool(tool_name,arguments)

    async def list_tools(self):
        print("Listing Tools")
        return (await self.session.list_tools()).tools


async def main():
    async with MCPClient("http://127.0.0.1:8000/mcp") as client:
        tools = await client.list_tools()
        print("Tools:",tools)
        result = await client.call_tool("Add Two Nums",{"a":1,"b":2})
        print("Result:",result.content)


# Run the main function
def run_main():
   return asyncio.run(main())
