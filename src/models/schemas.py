
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class ProductModel(BaseModel):
    """Internal clean model for product data"""
    name: str
    concentration: str
    skin_type: List[str]
    key_ingredients: List[str]
    benefits: List[str]
    how_to_use: str
    side_effects: str
    price: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "GlowBoost Vitamin C Serum",
                "concentration": "10% Vitamin C",
                "skin_type": ["Oily", "Combination"],
                "key_ingredients": ["Vitamin C", "Hyaluronic Acid"],
                "benefits": ["Brightening", "Fades dark spots"],
                "how_to_use": "Apply 2-3 drops in the morning before sunscreen",
                "side_effects": "Mild tingling for sensitive skin",
                "price": "₹699"
            }
        }

class QuestionCategory(str, Enum):
    INFORMATIONAL = "Informational"
    SAFETY = "Safety"
    USAGE = "Usage"
    PURCHASE = "Purchase"
    COMPARISON = "Comparison"
    INGREDIENTS = "Ingredients"

class QuestionModel(BaseModel):
    """Model for a single FAQ question"""
    question: str
    answer: str
    category: QuestionCategory

class FAQPageModel(BaseModel):
    """Output model for FAQ page"""
    page_type: str = "faq"
    product_name: str
    questions: List[QuestionModel]
    total_questions: int

class BenefitDetail(BaseModel):
    """Structured benefit information"""
    benefit: str
    description: str

class UsageInstructions(BaseModel):
    """Structured usage information"""
    instruction: str
    frequency: str
    timing: str
    application_method: str

class SafetyInfo(BaseModel):
    """Structured safety information"""
    side_effects: str
    suitable_skin_types: List[str]
    precautions: List[str]

class ProductPageModel(BaseModel):
    """Output model for product description page"""
    page_type: str = "product_page"
    product_name: str
    concentration: str
    price: str
    benefits: List[BenefitDetail]
    usage_instructions: UsageInstructions
    safety_info: SafetyInfo
    key_ingredients: List[str]

class ComparisonRow(BaseModel):
    """Single comparison attribute"""
    attribute: str
    product_a_value: str
    product_b_value: str
    winner: Optional[str] = None

class ComparisonPageModel(BaseModel):
    """Output model for comparison page"""
    page_type: str = "comparison"
    product_a: ProductModel
    product_b: ProductModel
    comparison_table: List[ComparisonRow]
    summary: str