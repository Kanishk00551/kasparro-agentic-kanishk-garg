
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
<img width="872" height="706" alt="Screenshot 2025-12-09 233155" src="https://github.com/user-attachments/assets/cb40e399-64be-423a-a399-db85f409970f" />
<img width="877" height="787" alt="Screenshot 2025-12-09 233211" src="https://github.com/user-attachments/assets/b7cd2901-acc3-4fe1-a20b-461828984631" />
<img width="645" height="436" alt="Screenshot 2025-12-09 233224" src="https://github.com/user-attachments/assets/c4e221c5-fce4-417c-bf49-b351423f1ed6" />



