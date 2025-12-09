
from src.agents.base_agent import BaseAgent
from src.models.schemas import ProductModel, ComparisonRow
from src.blocks.content import ContentBlocks
from typing import List, Tuple

class ComparisonAgent(BaseAgent):
    """Agent responsible for creating product comparisons"""
    
    def __init__(self):
        super().__init__("ComparisonAgent")
        self.content_blocks = ContentBlocks()
    
    def _create_fictional_product_b(self, product_a: ProductModel) -> ProductModel:
        """
        Create a structured fictional Product B for comparison
        Must maintain same schema as Product A
        """
        return ProductModel(
            name="RadiantGlow Niacinamide Serum",
            concentration="5% Niacinamide",
            skin_type=["Dry", "Sensitive"],
            key_ingredients=["Niacinamide", "Hyaluronic Acid", "Zinc"],
            benefits=["Pore minimizing", "Reduces redness"],
            how_to_use="Apply 3-4 drops in the evening after cleansing",
            side_effects="Generally well-tolerated",
            price="₹899"
        )
    
    def execute(self, product_a: ProductModel) -> Tuple[ProductModel, List[ComparisonRow], str]:
        """
        Generate comparison between Product A and fictional Product B
        
        Input: ProductModel (Product A)
        Output: Tuple of (Product B, comparison_table, summary)
        """
        self.log_execution("Creating product comparison...")
        
        product_b = self._create_fictional_product_b(product_a)
        comparison_table = []
        
        # Compare Name
        comparison_table.append(ComparisonRow(
            attribute="Product Name",
            product_a_value=product_a.name,
            product_b_value=product_b.name,
            winner=None
        ))
        
        # Compare Active Ingredient
        comparison_table.append(ComparisonRow(
            attribute="Active Ingredient",
            product_a_value=product_a.concentration,
            product_b_value=product_b.concentration,
            winner=None
        ))
        
        # Compare Skin Type
        comparison_table.append(ComparisonRow(
            attribute="Suitable Skin Types",
            product_a_value=", ".join(product_a.skin_type),
            product_b_value=", ".join(product_b.skin_type),
            winner=None
        ))
        
        # Compare Key Ingredients
        ingredient_comparison = self.content_blocks.compare_ingredients_block(product_a, product_b)
        comparison_table.append(ComparisonRow(
            attribute="Key Ingredients",
            product_a_value=", ".join(product_a.key_ingredients),
            product_b_value=", ".join(product_b.key_ingredients),
            winner=None
        ))
        
        comparison_table.append(ComparisonRow(
            attribute="Common Ingredients",
            product_a_value=", ".join(ingredient_comparison["common"]) if ingredient_comparison["common"] else "None",
            product_b_value=", ".join(ingredient_comparison["common"]) if ingredient_comparison["common"] else "None",
            winner=None
        ))
        
        # Compare Benefits
        comparison_table.append(ComparisonRow(
            attribute="Primary Benefits",
            product_a_value=", ".join(product_a.benefits),
            product_b_value=", ".join(product_b.benefits),
            winner=None
        ))
        
        # Compare Usage
        comparison_table.append(ComparisonRow(
            attribute="How to Use",
            product_a_value=product_a.how_to_use,
            product_b_value=product_b.how_to_use,
            winner=None
        ))
        
        # Compare Side Effects
        comparison_table.append(ComparisonRow(
            attribute="Side Effects",
            product_a_value=product_a.side_effects,
            product_b_value=product_b.side_effects,
            winner="Product B"
        ))
        
        # Compare Price
        price_a = self.content_blocks.parse_price_block(product_a.price)
        price_b = self.content_blocks.parse_price_block(product_b.price)
        
        comparison_table.append(ComparisonRow(
            attribute="Price",
            product_a_value=product_a.price,
            product_b_value=product_b.price,
            winner="Product A" if price_a["numeric_value"] < price_b["numeric_value"] else "Product B"
        ))
        
        # Generate summary
        summary = (
            f"{product_a.name} focuses on {' and '.join(product_a.benefits).lower()} "
            f"with {product_a.concentration}, while {product_b.name} targets "
            f"{' and '.join(product_b.benefits).lower()} using {product_b.concentration}. "
            f"Both products contain {', '.join(ingredient_comparison['common']) if ingredient_comparison['common'] else 'different ingredients'}. "
            f"{product_a.name} is more affordable at {product_a.price} compared to {product_b.price}."
        )
        
        self.log_execution(f"Generated comparison with {len(comparison_table)} attributes")
        return product_b, comparison_table, summary

