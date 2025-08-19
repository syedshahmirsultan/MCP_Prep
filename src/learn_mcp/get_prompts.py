from agents import Agent,Runner, OpenAIChatCompletionsModel
from openai import AsyncOpenAI
from agents.mcp import MCPServerStreamableHttpParams,MCPServerStreamableHttp
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

mcp_url = "http://127.0.0.1:8000/mcp"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    openai_client=client,
    model="gemini-2.0-flash"
)

async def main():
    mcp_server_client = MCPServerStreamableHttpParams(url=mcp_url)
    async with MCPServerStreamableHttp(params=mcp_server_client) as mcp_server_client:
        prompt_list = await mcp_server_client.list_prompts()
        print("Prompts List:",prompt_list)
        prompt = await mcp_server_client.get_prompt("Summarize",{"doc_content":"Hello World"})
        print("Prompt:",prompt)
        return prompt


asyncio.run(main())

    
