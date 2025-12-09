
from src.agents.base_agent import BaseAgent
from src.models.schemas import ProductModel
from typing import Dict, Any

class ParserAgent(BaseAgent):
    """Agent responsible for parsing raw product data into clean internal model"""
    
    def __init__(self):
        super().__init__("ParserAgent")
    
    def execute(self, raw_data: Dict[str, Any]) -> ProductModel:
        """
        Parse raw product data into validated Pydantic model
        
        Input: Dict with raw product fields
        Output: ProductModel (validated)
        """
        self.log_execution("Starting data parsing...")
        
        # Clean and validate data
        product = ProductModel(
            name=raw_data["name"],
            concentration=raw_data["concentration"],
            skin_type=raw_data["skin_type"] if isinstance(raw_data["skin_type"], list) else [s.strip() for s in raw_data["skin_type"].split(",")],
            key_ingredients=raw_data["key_ingredients"] if isinstance(raw_data["key_ingredients"], list) else [i.strip() for i in raw_data["key_ingredients"].split(",")],
            benefits=raw_data["benefits"] if isinstance(raw_data["benefits"], list) else [b.strip() for b in raw_data["benefits"].split(",")],
            how_to_use=raw_data["how_to_use"],
            side_effects=raw_data["side_effects"],
            price=raw_data["price"]
        )
        
        self.log_execution(f"Successfully parsed product: {product.name}")
        return product
