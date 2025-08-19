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
    mcp_params = MCPServerStreamableHttpParams(url=mcp_url)
    async with MCPServerStreamableHttp(params=mcp_params,cache_tools_list=True) as mcp_server_client:
        print("Tools List:",await mcp_server_client.list_tools())
        agent = Agent(
            name="MCP Agent",
            model=model,
            mcp_servers=[mcp_server_client]
        )
        result = await Runner.run(agent,"What is the mood of John?")
        print("Result:",result.final_output)
        return result


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"An unhandled error occurred in the agent script: {e}")
