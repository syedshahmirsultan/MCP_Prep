from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession
from contextlib import AsyncExitStack
import asyncio
from pydantic import AnyUrl


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

    async def list_resources(self):
        print("Listing Resources")
        result = await self.session.list_resources()
        return result.resources
    

    async def get_template_resource(self):
        print("Getting Template Resource")
        result = await self.session.list_resource_templates()
        return result.resourceTemplates

    async def read_resource(self,uri:str):
        result = await self.session.read_resource(AnyUrl(uri))
        print("Result:",result)
        return result.contents[0].text




async def main():
    async with MCPClient("http://127.0.0.1:8000/mcp") as client:
        tools = await client.list_tools()
        print("Tools:",tools)
        result = await client.call_tool("Add Two Nums",{"a":1,"b":2})
        print("Result:",result.content)
        resources = await client.list_resources()
        print("Resources:",resources)
        template_resources = await client.get_template_resource()
        resource  = template_resources[0].uriTemplate.replace("{doc_name}","intro")
        print("Template Resources:",resource)
        result = await client.read_resource(resource)
        print("Template Resource Result:",result)
        listOfDocs = await client.read_resource("docs://documents")
        print("List of Docs:",listOfDocs)

# Run the main function
def run_main():
   return asyncio.run(main())
