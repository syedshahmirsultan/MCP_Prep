from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base
from mcp.types import PromptMessage,TextContent

mcp = FastMCP(name="Server 1", stateless_http=True)

mcp_app = mcp.streamable_http_app()


@mcp.tool(name="Add Two Nums",description="This tool Adds Two Numbers")
def add_two_nums(a:int,b:int):
    print("Adding two nums !")
    return a+b

@mcp.tool(name="Subtract Two Nums",description="This Subtracts Two Numbers")
def subtract_two_nums(a:int,b:int):
    print("Subtracting two nums !")
    return a-b


docs ={
    "intro":"Introduction To MCP",
    "useCase":"This is a Use Case",
    "Advantages":"This is an Advantage",
    "Disadvantages":"This is a Disadvantage"
}

@mcp.resource("docs://documents",mime_type="application/json")
def documents():
    "Returns the Docs List"
    print("Returning Docs List",list(docs.keys()))
    return list(docs.keys())


@mcp.resource("docs://documents/{doc_name}",mime_type="application/json")
def document(doc_name:str):
    "Returns the Doc Content"
    print("Returning Doc Content for ",docs[doc_name])
    return docs[doc_name]



@mcp.prompt(name="MCP Prompt",description="This is a MCP Prompt")
def mcp_prompt(doc_content:str)->list[base.Message]:
    prompt = f"""You are a helpful assistant that can answer questions about the following document:
    {doc_content}
    """
    return [base.UserMessage(prompt)]


@mcp.prompt(name="Summarize",description="Sumarize the given document")
def summarize(doc_content:str)->list[PromptMessage]:
    prompt = f"""You are a helpful assistant that can summarize the following document:
    {doc_content}
    """
    return [PromptMessage(role="user",content=TextContent(type="text",text=prompt))]
