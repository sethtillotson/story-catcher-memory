import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from mem0 import MemoryClient

app = FastAPI()
mem0 = MemoryClient(api_key=os.environ["MEM0_API_KEY"])

@app.post("/retrieveMemories")
async def retrieve_memories(request: Request):
    data = await request.json()
    query = data.get("message", "caller context")
    user_id = data.get("user_id", "seth")
    try:
        results = mem0.search(query, user_id=user_id, limit=5)
        memories = [r["memory"] for r in results.get("results", [])]
        return JSONResponse({"memories": memories, "text": "\n".join(memories) or "No previous memories found."})
    except Exception as e:
        return JSONResponse({"text": f"Memory retrieval failed: {str(e)}"}, status_code=500)

@app.post("/addMemories")
async def add_memories(request: Request):
    data = await request.json()
    message = data.get("message", "")
    user_id = data.get("user_id", "seth")
    try:
        mem0.add([{"role": "user", "content": message}], user_id=user_id)
        return JSONResponse({"text": "Memory saved."})
    except Exception as e:
        return JSONResponse({"text": f"Memory save failed: {str(e)}"}, status_code=500)

@app.get("/")
def health():
    return {"status": "ok"}
