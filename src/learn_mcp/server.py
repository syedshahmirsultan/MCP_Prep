from mcp.server.fastmcp import FastMCP


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