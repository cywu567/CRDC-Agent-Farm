from pydantic import BaseModel

class RunRequest(BaseModel):
    tool: str
    goal: str | None = None

class RunResponse(BaseModel):
    result: str
