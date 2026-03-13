from fastapi import FastAPI
from agents.travel_agent import Agent
from pydantic import BaseModel

app = FastAPI()

class Query(BaseModel):
    query: str

agent = Agent()
executor = agent.agent_execute()

@app.post("/agent")
def run_agent(request: Query):
    result = executor.invoke({"input": request.query})
    return {"reply": result}

@app.get("/")
async def main():
    return {"message": "AI travel agent is running"}