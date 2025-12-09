
from fastapi import FastAPI
from src.orchestrator.workflow import WorkflowOrchestrator

app = FastAPI()

@app.post("/generate")
async def generate_content(product_data: dict):
    orchestrator = WorkflowOrchestrator()
    outputs = orchestrator.execute_pipeline(product_data)
    return outputs