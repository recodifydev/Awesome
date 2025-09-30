from pathlib import Path
from typing import Dict, Any, List, Optional
from google.adk.evaluation.agent_evaluator import AgentEvaluator
from pydantic import BaseModel

class EvalConfig(BaseModel):
    """Configuration for agent evaluation."""
    tool_trajectory_avg_score: float = 1.0
    response_match_score: float = 0.8

class AgentEvaluation:
    """Handles agent evaluation using ADK."""
    
    def __init__(self, agent_module: str, eval_config: Optional[EvalConfig] = None):
        self.agent_module = agent_module
        self.config = eval_config or EvalConfig()
        
    async def evaluate_test_file(self, test_file_path: str) -> Dict[str, Any]:
        """Evaluate agent using a test file."""
        results = await AgentEvaluator.evaluate(
            agent_module=self.agent_module,
            eval_dataset_file_path_or_dir=test_file_path,
            criteria={
                "tool_trajectory_avg_score": self.config.tool_trajectory_avg_score,
                "response_match_score": self.config.response_match_score
            }
        )
        return self._process_results(results)
    
    async def evaluate_eval_set(self, eval_set_path: str) -> Dict[str, Any]:
        """Evaluate agent using an eval set."""
        results = await AgentEvaluator.evaluate(
            agent_module=self.agent_module,
            eval_dataset_file_path_or_dir=eval_set_path,
            criteria={
                "tool_trajectory_avg_score": self.config.tool_trajectory_avg_score,
                "response_match_score": self.config.response_match_score
            }
        )
        return self._process_results(results)
    
    def _process_results(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Process evaluation results."""
        return {
            "success": results.get("success", False),
            "total_cases": results.get("total_cases", 0),
            "passed_cases": results.get("passed_cases", 0),
            "failed_cases": results.get("failed_cases", 0),
            "detailed_results": results.get("detailed_results", [])
        }