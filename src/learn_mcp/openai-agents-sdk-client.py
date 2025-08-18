from agents import Agent,Runner, OpenAIChatCompletionsModel
from openai import AsyncOpenAI
from agents.mcp import MCPServerStreamableHttpParams,MCPServerStreamableHttp,create_static_tool_filter
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

mcp_url = "http://127.0.0.1:8000/mcp"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


#Reference: https://ai.google.dev/gemini-api/docs/openai
client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)


model = OpenAIChatCompletionsModel(
    openai_client=client,
    model="gemini-2.0-flash"
)


async def main():
   tools_filter = create_static_tool_filter(blocked_tool_names=["add_two_nums","subtract_two_nums"])
   mcp_param = MCPServerStreamableHttpParams(url=mcp_url)
   async with MCPServerStreamableHttp(params=mcp_param,tool_filter=tools_filter) as mcp_server_client:
    # print("Tools List:",await mcp_server_client.list_tools())

    agent = Agent(
    name="MCP Agent",
    model=model,
    mcp_servers=[mcp_server_client]
   )

    result = await Runner.run(agent,"What is the mood of John?")
    print("Result:",result)
    return result

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"An unhandled error occurred in the agent script: {e}")


##GEMINI_API_KEY = AIzaSyApU3pAQuPj1KHEwoSpFpiFLsm8fLMS4TI
##OPENAI_API_KEY = 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