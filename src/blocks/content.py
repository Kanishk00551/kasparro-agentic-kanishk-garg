from typing import Dict, Any, List
from src.models.schemas import ProductModel, BenefitDetail, UsageInstructions, SafetyInfo

class ContentBlocks:
    """Reusable content transformation logic blocks"""
    
    @staticmethod
    def generate_benefits_block(product: ProductModel) -> List[BenefitDetail]:
        """Transform raw benefits into structured benefit details"""
        benefits = []
        for benefit in product.benefits:
            benefits.append(BenefitDetail(
                benefit=benefit,
                description=f"Helps with {benefit.lower()} for healthier-looking skin"
            ))
        return benefits
    
    @staticmethod
    def extract_usage_block(product: ProductModel) -> UsageInstructions:
        """Extract and structure usage information"""
        instruction = product.how_to_use
        
        # Parse frequency
        frequency = "Daily (AM)" if "morning" in instruction.lower() else "As directed"
        
        # Parse timing
        timing = "Before sunscreen" if "before sunscreen" in instruction.lower() else "As needed"
        
        # Extract application method
        application_method = "Topical application"
        if "drops" in instruction.lower():
            drops = [word for word in instruction.split() if word.replace('–', '-').replace('—', '-').split('-')[0].isdigit()]
            if drops:
                application_method = f"Apply {drops[0]} drops"
        
        return UsageInstructions(
            instruction=instruction,
            frequency=frequency,
            timing=timing,
            application_method=application_method
        )
    
    @staticmethod
    def generate_safety_block(product: ProductModel) -> SafetyInfo:
        """Generate safety information block"""
        precautions = []
        
        if "sensitive" in product.side_effects.lower():
            precautions.extend([
                "Patch test recommended for sensitive skin",
                "Start with lower frequency if irritation occurs"
            ])
        
        if "tingling" in product.side_effects.lower():
            precautions.append("Mild tingling is normal and should subside")
        
        if not precautions:
            precautions.append("Follow usage instructions as directed")
        
        return SafetyInfo(
            side_effects=product.side_effects,
            suitable_skin_types=product.skin_type,
            precautions=precautions
        )
    
    @staticmethod
    def compare_ingredients_block(product_a: ProductModel, product_b: ProductModel) -> Dict[str, List[str]]:
        """Compare ingredients between two products"""
        set_a = set(product_a.key_ingredients)
        set_b = set(product_b.key_ingredients)
        
        return {
            "common": list(set_a & set_b),
            "unique_to_a": list(set_a - set_b),
            "unique_to_b": list(set_b - set_a)
        }
    
    @staticmethod
    def parse_price_block(price_str: str) -> Dict[str, Any]:
        """Parse and structure price information"""
        numeric_value = int(''.join(filter(str.isdigit, price_str)))
        currency = ''.join(filter(lambda x: not x.isdigit(), price_str)).strip()
        
        return {
            "display_price": price_str,
            "numeric_value": numeric_value,
            "currency": currency,
            "price_range": "Budget" if numeric_value < 500 else "Mid-range" if numeric_value < 1000 else "Premium"
        }
