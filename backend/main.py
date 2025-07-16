from fastapi import FastAPI
from backend.models import RunRequest, RunResponse
from backend.agent_runner import run_tool

app = FastAPI()

@app.post("/run", response_model=RunResponse)
def handle_run(request: RunRequest):
    result = run_tool(tool=request.tool, goal=request.goal)
    return RunResponse(result=str(result))
