
from typing import Dict, Any, List

class PageTemplates:
    """
    Template engine that defines structure, rules, and dependencies
    for different page types
    """
    
    @staticmethod
    def get_faq_template() -> Dict[str, Any]:
        """
        FAQ Page Template Definition
        
        Structure:
        - page_type: fixed string
        - product_name: required string
        - questions: list of question objects
        - total_questions: computed field
        
        Rules:
        - Minimum 5 questions
        - Questions must have: question, answer, category
        - Categories must be from predefined enum
        
        Dependencies:
        - QuestionGeneratorAgent output
        """
        return {
            "page_type": "faq",
            "required_fields": ["product_name", "questions", "total_questions"],
            "questions_schema": {
                "minimum_count": 5,
                "fields": ["question", "answer", "category"],
                "category_options": ["Informational", "Safety", "Usage", "Purchase", "Comparison", "Ingredients"]
            },
            "dependencies": ["QuestionGeneratorAgent"]
        }
    
    @staticmethod
    def get_product_page_template() -> Dict[str, Any]:
        """
        Product Page Template Definition
        
        Structure:
        - page_type: fixed string
        - product_name: required string
        - concentration: required string
        - price: required string
        - benefits: list of benefit objects
        - usage_instructions: structured usage object
        - safety_info: structured safety object
        - key_ingredients: list of strings
        
        Rules:
        - Benefits must have: benefit, description
        - Usage must have: instruction, frequency, timing, application_method
        - Safety must have: side_effects, suitable_skin_types, precautions
        
        Dependencies:
        - ContentBlocks: generate_benefits_block
        - ContentBlocks: extract_usage_block
        - ContentBlocks: generate_safety_block
        """
        return {
            "page_type": "product_page",
            "required_fields": [
                "product_name", "concentration", "price",
                "benefits", "usage_instructions", "safety_info", "key_ingredients"
            ],
            "benefits_schema": {
                "fields": ["benefit", "description"],
                "block_dependency": "generate_benefits_block"
            },
            "usage_schema": {
                "fields": ["instruction", "frequency", "timing", "application_method"],
                "block_dependency": "extract_usage_block"
            },
            "safety_schema": {
                "fields": ["side_effects", "suitable_skin_types", "precautions"],
                "block_dependency": "generate_safety_block"
            },
            "dependencies": ["ParserAgent", "ContentBlocks"]
        }
    
    @staticmethod
    def get_comparison_template() -> Dict[str, Any]:
        """
        Comparison Page Template Definition
        
        Structure:
        - page_type: fixed string
        - product_a: full product object
        - product_b: full product object
        - comparison_table: list of comparison rows
        - summary: string
        
        Rules:
        - Both products must have same schema
        - Comparison table must include: attribute, product_a_value, product_b_value, winner
        - Summary must synthesize key differences
        
        Dependencies:
        - ComparisonAgent for product_b generation
        - ContentBlocks: compare_ingredients_block
        - ContentBlocks: parse_price_block
        """
        return {
            "page_type": "comparison",
            "required_fields": ["product_a", "product_b", "comparison_table", "summary"],
            "comparison_row_schema": {
                "fields": ["attribute", "product_a_value", "product_b_value", "winner"],
                "minimum_rows": 5
            },
            "product_b_rules": {
                "must_be_fictional": True,
                "must_match_schema": "ProductModel",
                "must_differ_from_a": True
            },
            "dependencies": ["ComparisonAgent", "ContentBlocks"]
        }