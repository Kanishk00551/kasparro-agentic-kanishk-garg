# Project Documentation: Multi-Agent Content Generation System

## Problem Statement

Design and implement a modular agentic automation system that:
- Takes a single product dataset as input
- Autonomously generates structured, machine-readable content pages
- Operates through multiple specialized agents with clear boundaries
- Produces JSON output for FAQ, Product Description, and Comparison pages
- Demonstrates production-quality system design and agent orchestration

**Constraints:**
- No external data sources or research allowed
- Must use ONLY the provided product data
- Output must be machine-readable JSON (not free text)
- System must be modular (not a monolithic script)
- Must demonstrate clear agent boundaries and responsibilities

---

## Solution Overview

The system implements a **DAG-based (Directed Acyclic Graph) multi-agent workflow** where specialized agents collaborate to transform raw product data into structured content pages. Each agent has a single responsibility, defined input/output contracts, and operates independently without hidden global state.

### Core Components

1. **Agents**: Four specialized agents with distinct responsibilities
2. **Content Blocks**: Reusable transformation functions that apply rules to data
3. **Templates**: Structured definitions of page formats with validation rules
4. **Orchestrator**: DAG-based workflow manager that coordinates agent execution
5. **Data Models**: Pydantic schemas for type safety and validation

### Key Design Principles

- **Separation of Concerns**: Each agent handles one aspect of content generation
- **Composability**: Content blocks can be reused across different agents
- **Type Safety**: Pydantic models ensure data integrity throughout the pipeline
- **Extensibility**: New agents or content types can be added without modifying existing code
- **Observability**: Comprehensive logging at each pipeline stage

---

## Scopes & Assumptions

### In Scope
- Parsing and validating product data
- Generating 15+ categorized user questions
- Creating fictional Product B for comparison
- Assembling three distinct page types (FAQ, Product, Comparison)
- Outputting machine-readable JSON
- DAG-based orchestration with state management

### Out of Scope
- External data retrieval or web scraping
- Machine learning model training
- User interface or web frontend
- Real-time API endpoints
- Database persistence
- Multi-product batch processing

### Assumptions
- Input data follows the specified product schema
- Generated content must be derived solely from input data
- Fictional Product B must maintain the same schema as Product A
- Minimum 5 questions required for FAQ page
- System runs as a batch process (not real-time)

---

## System Design

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                   Workflow Orchestrator                      │
│                     (DAG Coordinator)                        │
└─────────────────────────────────────────────────────────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
         ▼                   ▼                   ▼
    ┌─────────┐        ┌──────────┐       ┌─────────────┐
    │ Parser  │        │ Question │       │ Comparison  │
    │  Agent  │        │   Agent  │       │    Agent    │
    └─────────┘        └──────────┘       └─────────────┘
         │                   │                   │
         │                   │                   │
         └───────────────────┼───────────────────┘
                             │
                             ▼
                      ┌─────────────┐
                      │   Writer    │
                      │    Agent    │
                      └─────────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
         ▼                   ▼                   ▼
    ┌─────────┐      ┌──────────────┐    ┌──────────────┐
    │ faq.json│      │product_page  │    │ comparison   │
    │         │      │    .json     │    │    .json     │
    └─────────┘      └──────────────┘    └──────────────┘
```

### Agent Architecture

#### 1. ParserAgent
**Responsibility**: Convert raw product data into validated internal model

**Input**: 
```python
{
  "name": str,
  "concentration": str,
  "skin_type": str,  # comma-separated
  "key_ingredients": str,  # comma-separated
  "benefits": str,  # comma-separated
  "how_to_use": str,
  "side_effects": str,
  "price": str
}
```

**Output**: `ProductModel` (Pydantic)

**Operations**:
- Split comma-separated strings into lists
- Validate required fields
- Normalize data format
- Create type-safe model instance

**No Dependencies**: First node in DAG

---

#### 2. QuestionGeneratorAgent
**Responsibility**: Generate categorized user questions from product data

**Input**: `ProductModel`

**Output**: `List[QuestionModel]` (minimum 15 questions)

**Operations**:
- Generate questions across 6 categories:
  - Informational
  - Safety
  - Usage
  - Purchase
  - Comparison
  - Ingredients
- Create contextual answers using product data
- Ensure category diversity

**Dependencies**: ParserAgent

**Question Categories Distribution**:
- Informational: 4 questions
- Ingredients: 2 questions
- Usage: 3 questions
- Safety: 3 questions
- Purchase: 2 questions
- Comparison: 1 question

---

#### 3. ComparisonAgent
**Responsibility**: Create fictional Product B and generate comparison table

**Input**: `ProductModel` (Product A)

**Output**: `Tuple[ProductModel, List[ComparisonRow], str]`
- Product B (fictional but structured)
- Comparison table with attribute rows
- Summary text

**Operations**:
- Generate fictional Product B with same schema
- Compare key attributes (name, ingredients, price, benefits, etc.)
- Use `compare_ingredients_block` to find common/unique ingredients
- Use `parse_price_block` to compare pricing
- Generate natural language summary

**Dependencies**: ParserAgent, ContentBlocks

**Comparison Attributes**:
- Product Name
- Active Ingredient
- Suitable Skin Types
- Key Ingredients
- Common Ingredients
- Primary Benefits
- Usage Instructions
- Side Effects
- Price (with winner determination)

---

#### 4. WriterAgent
**Responsibility**: Assemble content into structured JSON pages

**Input**: Various (depends on page type)

**Output**: `Dict[str, Any]` (JSON-serializable)

**Operations**:
- `assemble_faq_page()`: Selects 5+ diverse questions, structures FAQ
- `assemble_product_page()`: Uses content blocks to build product description
- `assemble_comparison_page()`: Structures comparison data

**Dependencies**: All other agents, ContentBlocks, Templates

**Page Assembly Logic**:
- FAQ: Prioritizes category diversity in question selection
- Product: Applies all content blocks (benefits, usage, safety)
- Comparison: Combines product data with comparison analysis

---

### Content Blocks Architecture

Content blocks are **pure functions** that transform data according to specific rules. They are stateless and reusable across agents.

#### Available Blocks

1. **generate_benefits_block**
   - Input: `ProductModel`
   - Output: `List[BenefitDetail]`
   - Logic: Structures each benefit with description

2. **extract_usage_block**
   - Input: `ProductModel`
   - Output: `UsageInstructions`
   - Logic: Parses timing, frequency, application method from text

3. **generate_safety_block**
   - Input: `ProductModel`
   - Output: `SafetyInfo`
   - Logic: Generates precautions based on side effects keywords

4. **compare_ingredients_block**
   - Input: `ProductModel`, `ProductModel`
   - Output: `Dict[str, List[str]]`
   - Logic: Set operations to find common/unique ingredients

5. **parse_price_block**
   - Input: `str` (price)
   - Output: `Dict[str, Any]`
   - Logic: Extracts numeric value, currency, determines price range

---

### Template Engine Architecture

Templates define the **structure, validation rules, and dependencies** for each page type. They act as contracts that agents must fulfill.

#### FAQ Template
```python
{
  "page_type": "faq",
  "required_fields": ["product_name", "questions", "total_questions"],
  "questions_schema": {
    "minimum_count": 5,
    "fields": ["question", "answer", "category"],
    "category_options": [enum values]
  },
  "dependencies": ["QuestionGeneratorAgent"]
}
```

#### Product Page Template
```python
{
  "page_type": "product_page",
  "required_fields": [
    "product_name", "concentration", "price",
    "benefits", "usage_instructions", "safety_info", "key_ingredients"
  ],
  "benefits_schema": {...},
  "usage_schema": {...},
  "safety_schema": {...},
  "dependencies": ["ParserAgent", "ContentBlocks"]
}
```

#### Comparison Template
```python
{
  "page_type": "comparison",
  "required_fields": ["product_a", "product_b", "comparison_table", "summary"],
  "comparison_row_schema": {
    "fields": ["attribute", "product_a_value", "product_b_value", "winner"],
    "minimum_rows": 5
  },
  "product_b_rules": {
    "must_be_fictional": True,
    "must_match_schema": "ProductModel"
  },
  "dependencies": ["ComparisonAgent", "ContentBlocks"]
}
```

---

### Orchestration Workflow (DAG)

The **WorkflowOrchestrator** implements a state machine with the following transitions:

```
INITIALIZED
    ↓
PARSED (ParserAgent)
    ↓
    ├─→ QUESTIONS_GENERATED (QuestionGeneratorAgent)
    │        ↓
    │   FAQ_ASSEMBLED (WriterAgent)
    │
    └─→ COMPARISON_GENERATED (ComparisonAgent)
             ↓
        COMPARISON_PAGE_ASSEMBLED (WriterAgent)
    
PRODUCT_PAGE_ASSEMBLED (WriterAgent)
    ↓
COMPLETED
```

**State Management**:
- Each state transition is logged
- Intermediate results stored in orchestrator instance
- Failure transitions to FAILED state with error logging

**Execution Order**:
1. Parse raw data → ProductModel
2. Generate questions (can run parallel with comparison)
3. Generate comparison (can run parallel with questions)
4. Assemble FAQ page
5. Assemble Product page
6. Assemble Comparison page
7. Complete

**Parallelization Opportunities**:
- QuestionGeneratorAgent and ComparisonAgent can run concurrently (both only depend on ParserAgent)
- In current implementation: sequential for simplicity
- Architecture supports async execution

---

### Data Flow

```
Raw Product Data (Dict)
    ↓
[ParserAgent]
    ↓
ProductModel (Pydantic)
    ↓
    ├─→ [QuestionGeneratorAgent] → List[QuestionModel]
    │                                      ↓
    │                              [WriterAgent.assemble_faq_page]
    │                                      ↓
    │                                  faq.json
    │
    ├─→ [ComparisonAgent] → (ProductB, ComparisonTable, Summary)
    │                                      ↓
    │                      [WriterAgent.assemble_comparison_page]
    │                                      ↓
    │                                comparison.json
    │
    └─→ [ContentBlocks] → (Benefits, Usage, Safety)
                              ↓
                [WriterAgent.assemble_product_page]
                              ↓
                        product_page.json
```

---

### Extension Points

The system is designed for easy extension:

1. **New Agents**: 
   - Inherit from `BaseAgent`
   - Implement `execute()` method
   - Add to orchestrator workflow

2. **New Content Blocks**:
   - Add static method to `ContentBlocks` class
   - No changes to existing blocks needed

3. **New Page Types**:
   - Define new Pydantic model
   - Add template definition
   - Create assembly method in WriterAgent

4. **New Question Categories**:
   - Extend `QuestionCategory` enum
   - Update QuestionGeneratorAgent logic

---

## Technical Decisions

### Why Pydantic?
- Type safety and validation
- Automatic JSON serialization
- Clear schema documentation
- Runtime type checking

### Why DAG Architecture?
- Clear dependency management
- Enables parallel execution
- Easy to visualize and debug
- Standard pattern in workflow engines

### Why Separate Content Blocks?
- Reusability across agents
- Easier to test in isolation
- Single responsibility principle
- Can be versioned independently

### Why State Machine in Orchestrator?
- Explicit state transitions
- Better error handling
- Audit trail for debugging
- Supports rollback/retry logic

---

## Output Examples

### faq.json
```json
{
  "page_type": "faq",
  "product_name": "GlowBoost Vitamin C Serum",
  "questions": [
    {
      "question": "What is GlowBoost Vitamin C Serum?",
      "answer": "GlowBoost Vitamin C Serum is a skincare serum...",
      "category": "Informational"
    }
  ],
  "total_questions": 5
}
```

### product_page.json
```json
{
  "page_type": "product_page",
  "product_name": "GlowBoost Vitamin C Serum",
  "concentration": "10% Vitamin C",
  "price": "₹699",
  "benefits": [...],
  "usage_instructions": {...},
  "safety_info": {...},
  "key_ingredients": [...]
}
```

### comparison_page.json
```json
{
  "page_type": "comparison",
  "product_a": {...},
  "product_b": {...},
  "comparison_table": [...],
  "summary": "..."
}
```

---

## Success Metrics

The system successfully:
✅ Parses raw data into clean internal model  
✅ Generates 15+ categorized questions  
✅ Creates fictional Product B with valid schema  
✅ Produces three distinct JSON output files  
✅ Maintains clear agent boundaries  
✅ Implements reusable content blocks  
✅ Uses template-based validation  
✅ Provides comprehensive logging  
✅ Demonstrates extensible architecture