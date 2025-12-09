
# Multi-Agent Content Generation System

A modular agentic automation system that generates structured content pages from product data.

## Architecture

This system implements a DAG-based multi-agent workflow with the following components:
See `docs/projectdocumentation.md` for detailed system design.

### Agents
1. **ParserAgent**: Converts raw data into validated Pydantic models
2. **QuestionGeneratorAgent**: Generates 15+ categorized user questions
3. **ComparisonAgent**: Creates fictional Product B and generates comparison
4. **WriterAgent**: Assembles content into structured JSON pages

### Content Blocks
Reusable transformation functions:
- `generate_benefits_block`: Structures benefit information
- `extract_usage_block`: Parses usage instructions
- `generate_safety_block`: Creates safety information
- `compare_ingredients_block`: Compares product ingredients
- `parse_price_block`: Structures price data

### Templates
Structured page definitions with rules and dependencies:
- FAQ Page Template
- Product Page Template
- Comparison Page Template

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the pipeline
python src/main.py
```

## Output

The system generates three JSON files in the `output/` directory:
- `faq.json`: FAQ page with 5+ categorized Q&As
- `product_page.json`: Complete product description
- `comparison_page.json`: Side-by-side product comparison

## Project Structure

```
src/
├── models/schemas.py          # Pydantic models
├── agents/                    # Agent implementations
├── blocks/content_blocks.py   # Reusable logic blocks
├── templates/page_templates.py # Template definitions
├── orchestrator/workflow.py   # DAG orchestration
└── main.py                    # Entry point
```

