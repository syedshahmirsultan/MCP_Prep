import requests

url = "http://127.0.0.1:8000/mcp"

headers = {
    "Content-Type":"application/json",
    "Accept":"application/json,text/event-stream"}

# # payload for list tools
# payload = {
#     "jsonrpc":"2.0",
#      "method":"tools/list",
#      "id":"2",
#      "params":{}
# }


# payload for calling Add Two Nums tool

# payload ={
#     "jsonrpc":"2.0",
#     "method":"tools/call",
#     "id":"2",
#     "params":{
#     "name":"Add Two Nums",
#     "arguments":{
#         "a":1,
#         "b":2
#     }
#     }
# }


# payload for calling Subtract Two Nums tool

payload ={
    "jsonrpc":"2.0",
    "method":"tools/call",
    "id":"2",
    "params":{
    "name":"Subtract Two Nums",
    "arguments":{
        "a":9,
        "b":2
    }
    }
}


def call_mcp():
    try:
        response = requests.post(url=url,headers=headers,json=payload)
        print("Response :",response.status_code)
        print("Response :",response.text)
    except Exception as e:
        print(f"   -> An error occurred: {e}")
        return {"error": str(e)}


call_mcp()