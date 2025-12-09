import logging 
from src.agents.base_agent import BaseAgent
from src.models.schemas import (
    ProductModel, QuestionModel, FAQPageModel, ProductPageModel, 
    ComparisonPageModel, ComparisonRow
)
from src.blocks.content import ContentBlocks
from src.templates.page_templates import PageTemplates
from typing import List, Dict, Any

class WriterAgent:  # ← Remove BaseAgent inheritance
    """Agent responsible for assembling content into structured pages"""
    
    def __init__(self):
        self.agent_name = "WriterAgent"
        self.logger = logging.getLogger("WriterAgent")
        self.content_blocks = ContentBlocks()
        self.templates = PageTemplates()
    
    def log_execution(self, message: str):
        """Log agent execution"""
        self.logger.info(f"[{self.agent_name}] {message}")
    
    # ... rest of your methods stay the same ...
    
    def assemble_faq_page(self, product: ProductModel, questions: List[QuestionModel]) -> Dict[str, Any]:
        """
        Assemble FAQ page from product and questions
        
        Input: ProductModel, List[QuestionModel]
        Output: Dict (JSON-serializable FAQ page)
        """
        self.log_execution("Assembling FAQ page...")
        
        # Use template to validate structure
        template = self.templates.get_faq_template()
        
        # Select top 5 questions (minimum requirement)
        # Prioritize diverse categories
        categories_seen = set()
        selected_questions = []
        
        for question in questions:
            if len(selected_questions) >= 5:
                break
            if question.category not in categories_seen or len(selected_questions) < 3:
                selected_questions.append(question)
                categories_seen.add(question.category)
        
        # Ensure we have at least 5
        while len(selected_questions) < 5 and len(selected_questions) < len(questions):
            for q in questions:
                if q not in selected_questions:
                    selected_questions.append(q)
                    if len(selected_questions) >= 5:
                        break
        
        faq_page = FAQPageModel(
            product_name=product.name,
            questions=selected_questions,
            total_questions=len(selected_questions)
        )
        
        self.log_execution(f"FAQ page assembled with {faq_page.total_questions} questions")
        return faq_page.model_dump()
    
    def assemble_product_page(self, product: ProductModel) -> Dict[str, Any]:
        """
        Assemble product description page
        
        Input: ProductModel
        Output: Dict (JSON-serializable product page)
        """
        self.log_execution("Assembling product page...")
        
        # Use content blocks to generate structured sections
        benefits = self.content_blocks.generate_benefits_block(product)
        usage = self.content_blocks.extract_usage_block(product)
        safety = self.content_blocks.generate_safety_block(product)
        
        product_page = ProductPageModel(
            product_name=product.name,
            concentration=product.concentration,
            price=product.price,
            benefits=benefits,
            usage_instructions=usage,
            safety_info=safety,
            key_ingredients=product.key_ingredients
        )
        
        self.log_execution("Product page assembled successfully")
        return product_page.model_dump()
    
    def assemble_comparison_page(
        self, 
        product_a: ProductModel, 
        product_b: ProductModel,
        comparison_table: List[ComparisonRow],
        summary: str
    ) -> Dict[str, Any]:
        """
        Assemble comparison page
        
        Input: ProductModel (A), ProductModel (B), comparison_table, summary
        Output: Dict (JSON-serializable comparison page)
        """
        self.log_execution("Assembling comparison page...")
        
        comparison_page = ComparisonPageModel(
            product_a=product_a,
            product_b=product_b,
            comparison_table=comparison_table,
            summary=summary
        )
        
        self.log_execution("Comparison page assembled successfully")
        return comparison_page.model_dump()