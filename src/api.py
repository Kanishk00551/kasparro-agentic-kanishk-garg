from fastapi import FastAPI
from src.orchestrator.workflow import WorkflowOrchestrator
from src.models.schemas import ProductModel

app = FastAPI()

@app.post("/generate")
async def generate_content(product_data: ProductModel):
    """
    Generate structured content pages from product data.
    """
    orchestrator = WorkflowOrchestrator()
    
    # Convert Pydantic model to dict for the pipeline
    # The pipeline expects a dictionary to pass to ParserAgent
    outputs = orchestrator.execute_pipeline(product_data.model_dump())
    
    return outputs
