from src.agents.base_agent import BaseAgent
from src.models.schemas import ProductModel, QuestionModel, QuestionCategory
from typing import List

class QuestionGeneratorAgent(BaseAgent):
    """Agent responsible for generating categorized user questions"""
    
    def __init__(self):
        super().__init__("QuestionGeneratorAgent")
    
    def execute(self, product: ProductModel) -> List[QuestionModel]:
        """
        Generate at least 15 categorized questions based on product data
        
        Input: ProductModel
        Output: List[QuestionModel] (minimum 15 questions)
        """
        self.log_execution("Generating categorized questions...")
        
        questions = []
        
        # INFORMATIONAL questions
        questions.append(QuestionModel(
            question=f"What is {product.name}?",
            answer=f"{product.name} is a skincare serum with {product.concentration}, designed for {' and '.join(product.skin_type).lower()} skin types.",
            category=QuestionCategory.INFORMATIONAL
        ))
        
        questions.append(QuestionModel(
            question=f"What is the concentration of active ingredient in {product.name}?",
            answer=f"The concentration is {product.concentration}.",
            category=QuestionCategory.INFORMATIONAL
        ))
        
        questions.append(QuestionModel(
            question="What skin types is this product suitable for?",
            answer=f"This product is suitable for {' and '.join(product.skin_type).lower()} skin types.",
            category=QuestionCategory.INFORMATIONAL
        ))
        
        # INGREDIENTS questions
        questions.append(QuestionModel(
            question="What are the key ingredients?",
            answer=f"The key ingredients are {', '.join(product.key_ingredients)}.",
            category=QuestionCategory.INGREDIENTS
        ))
        
        questions.append(QuestionModel(
            question=f"Does {product.name} contain Hyaluronic Acid?",
            answer=f"Yes, {product.name} contains Hyaluronic Acid as one of its key ingredients.",
            category=QuestionCategory.INGREDIENTS
        ))
        
        # USAGE questions
        questions.append(QuestionModel(
            question="How do I use this product?",
            answer=product.how_to_use,
            category=QuestionCategory.USAGE
        ))
        
        questions.append(QuestionModel(
            question="When should I apply this serum?",
            answer="Apply in the morning before sunscreen for best results.",
            category=QuestionCategory.USAGE
        ))
        
        questions.append(QuestionModel(
            question="How many drops should I use?",
            answer="Use 2-3 drops for each application.",
            category=QuestionCategory.USAGE
        ))
        
        # SAFETY questions
        questions.append(QuestionModel(
            question="Are there any side effects?",
            answer=product.side_effects,
            category=QuestionCategory.SAFETY
        ))
        
        questions.append(QuestionModel(
            question="Is this safe for sensitive skin?",
            answer=f"{product.side_effects}. A patch test is recommended.",
            category=QuestionCategory.SAFETY
        ))
        
        questions.append(QuestionModel(
            question="Can I use this product daily?",
            answer="Yes, this product can be used daily in your morning routine.",
            category=QuestionCategory.SAFETY
        ))
        
        # PURCHASE questions
        questions.append(QuestionModel(
            question="What is the price?",
            answer=f"The price is {product.price}.",
            category=QuestionCategory.PURCHASE
        ))
        
        questions.append(QuestionModel(
            question="Is this product affordable?",
            answer=f"At {product.price}, this product is in the mid-range category for vitamin C serums.",
            category=QuestionCategory.PURCHASE
        ))
        
        # COMPARISON questions
        questions.append(QuestionModel(
            question="What makes this different from other vitamin C serums?",
            answer=f"This serum combines {product.concentration} with {' and '.join(product.key_ingredients)}, specifically formulated for {' and '.join(product.skin_type).lower()} skin types.",
            category=QuestionCategory.COMPARISON
        ))
        
        questions.append(QuestionModel(
            question=f"What benefits does {product.name} provide?",
            answer=f"The main benefits are {' and '.join(product.benefits).lower()}.",
            category=QuestionCategory.INFORMATIONAL
        ))
        
        questions.append(QuestionModel(
            question="Can this help with dark spots?",
            answer="Yes, this serum is designed to help fade dark spots as one of its primary benefits.",
            category=QuestionCategory.INFORMATIONAL
        ))
        
        self.log_execution(f"Generated {len(questions)} questions across {len(set(q.category for q in questions))} categories")
        return questions