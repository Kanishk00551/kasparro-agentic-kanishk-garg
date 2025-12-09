from abc import ABC, abstractmethod
from typing import Any, Dict
import logging

logging.basicConfig(level=logging.INFO)

class BaseAgent(ABC):
    """Abstract base class for all agents"""
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.logger = logging.getLogger(agent_name)
    
    @abstractmethod
    def execute(self, input_data: Any) -> Any:
        """Execute agent's primary function"""
        pass
    
    def log_execution(self, message: str):
        """Log agent execution"""
        self.logger.info(f"[{self.agent_name}] {message}")
