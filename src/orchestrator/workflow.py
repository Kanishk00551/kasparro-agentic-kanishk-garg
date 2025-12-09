from typing import Dict, Any, List
import logging
from enum import Enum

from src.agents.parser_agent import ParserAgent
from src.agents.question_agent import QuestionGeneratorAgent
from src.agents.comparison_agent import ComparisonAgent
from src.agents.writer_agent import WriterAgent
from src.models.schemas import ProductModel

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class WorkflowState(Enum):
    """Workflow states for the DAG"""
    INITIALIZED = "initialized"
    PARSED = "parsed"
    QUESTIONS_GENERATED = "questions_generated"
    COMPARISON_GENERATED = "comparison_generated"
    FAQ_ASSEMBLED = "faq_assembled"
    PRODUCT_PAGE_ASSEMBLED = "product_page_assembled"
    COMPARISON_PAGE_ASSEMBLED = "comparison_page_assembled"
    COMPLETED = "completed"
    FAILED = "failed"

class WorkflowOrchestrator:
    """
    DAG-based orchestrator for the multi-agent content generation pipeline
    
    Workflow Graph (DAG):
    
        [Raw Data]
            |
            v
        [ParserAgent] ────────────────────────────────┐
            |                                          |
            v                                          v
        [QuestionGeneratorAgent]              [ComparisonAgent]
            |                                          |
            v                                          v
        [WriterAgent: FAQ]                 [WriterAgent: Comparison]
                                                       ^
                                                       |
        [WriterAgent: Product] ────────────────────────┘
            
    State Transitions:
    INITIALIZED → PARSED → QUESTIONS_GENERATED → FAQ_ASSEMBLED
                 ↓                              ↘ COMPARISON_GENERATED → COMPARISON_PAGE_ASSEMBLED
                 → PRODUCT_PAGE_ASSEMBLED → COMPLETED
    """
    
    def __init__(self):
        self.logger = logging.getLogger("WorkflowOrchestrator")
        self.state = WorkflowState.INITIALIZED
        
        # Initialize agents
        self.parser_agent = ParserAgent()
        self.question_agent = QuestionGeneratorAgent()
        self.comparison_agent = ComparisonAgent()
        self.writer_agent = WriterAgent()
        
        # State storage
        self.product = None
        self.questions = None
        self.product_b = None
        self.comparison_table = None
        self.comparison_summary = None
        
        # Output storage
        self.outputs = {
            "faq": None,
            "product_page": None,
            "comparison": None
        }
    
    def _transition_state(self, new_state: WorkflowState):
        """Transition to a new workflow state"""
        self.logger.info(f"State transition: {self.state.value} → {new_state.value}")
        self.state = new_state
    
    def execute_pipeline(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the complete content generation pipeline
        
        Input: Raw product data dictionary
        Output: Dictionary containing all three generated pages
        """
        try:
            self.logger.info("="*70)
            self.logger.info("Starting Multi-Agent Content Generation Pipeline")
            self.logger.info("="*70)
            
            # Step 1: Parse raw data
            self.logger.info("\n[STEP 1] Parsing raw product data...")
            self.product = self.parser_agent.execute(raw_data)
            self._transition_state(WorkflowState.PARSED)
            
            # Step 2: Generate questions (parallel-capable with comparison)
            self.logger.info("\n[STEP 2] Generating categorized questions...")
            self.questions = self.question_agent.execute(self.product)
            self._transition_state(WorkflowState.QUESTIONS_GENERATED)
            
            # Step 3: Generate comparison data (parallel-capable with questions)
            self.logger.info("\n[STEP 3] Generating product comparison...")
            self.product_b, self.comparison_table, self.comparison_summary = \
                self.comparison_agent.execute(self.product)
            self._transition_state(WorkflowState.COMPARISON_GENERATED)
            
            # Step 4: Assemble FAQ page
            self.logger.info("\n[STEP 4] Assembling FAQ page...")
            self.outputs["faq"] = self.writer_agent.assemble_faq_page(
                self.product, 
                self.questions
            )
            self._transition_state(WorkflowState.FAQ_ASSEMBLED)
            
            # Step 5: Assemble Product page
            self.logger.info("\n[STEP 5] Assembling Product page...")
            self.outputs["product_page"] = self.writer_agent.assemble_product_page(
                self.product
            )
            self._transition_state(WorkflowState.PRODUCT_PAGE_ASSEMBLED)
            
            # Step 6: Assemble Comparison page
            self.logger.info("\n[STEP 6] Assembling Comparison page...")
            self.outputs["comparison"] = self.writer_agent.assemble_comparison_page(
                self.product,
                self.product_b,
                self.comparison_table,
                self.comparison_summary
            )
            self._transition_state(WorkflowState.COMPARISON_PAGE_ASSEMBLED)
            
            # Complete
            self._transition_state(WorkflowState.COMPLETED)
            self.logger.info("\n" + "="*70)
            self.logger.info("Pipeline completed successfully!")
            self.logger.info("="*70)
            
            return self.outputs
            
        except Exception as e:
            self._transition_state(WorkflowState.FAILED)
            self.logger.error(f"Pipeline failed: {str(e)}", exc_info=True)
            raise
    
    def get_pipeline_status(self) -> Dict[str, Any]:
        """Get current pipeline status"""
        return {
            "current_state": self.state.value,
            "product_parsed": self.product is not None,
            "questions_generated": self.questions is not None,
            "comparison_generated": self.product_b is not None,
            "outputs_ready": {
                "faq": self.outputs["faq"] is not None,
                "product_page": self.outputs["product_page"] is not None,
                "comparison": self.outputs["comparison"] is not None
            }
        }
