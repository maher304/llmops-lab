import json
import time
from typing import Dict, Any, List
from app.core.config import settings

class BaselineEvaluator:
    def __init__(self):
        self.deterministic = settings.deterministic_mode
    
    def evaluate(self, question: str, expected_answer: str, config: Dict[str, Any]) -> Dict[str, Any]:
        start = time.time()
        
        if self.deterministic:
            # Deterministic baseline - simple similarity-based scoring
            q_lower = question.lower()
            if 'machine learning' in q_lower:
                answer = "Machine learning is a branch of AI that learns patterns from data to make predictions without explicit programming."
            elif 'rag' in q_lower:
                answer = "RAG combines retrieval from knowledge bases with generation to produce grounded answers."
            elif 'agent' in q_lower:
                answer = "An AI agent is an autonomous system that perceives, reasons, and acts to achieve goals using tools and planning."
            else:
                answer = f"Deterministic response for: {question}"
            
            latency_ms = (time.time() - start) * 1000 + 50  # Add small simulated latency
            
            # Simple correctness score based on keyword overlap
            expected_words = set(expected_answer.lower().split())
            answer_words = set(answer.lower().split())
            overlap = len(expected_words.intersection(answer_words))
            correctness = min(1.0, overlap / max(len(expected_words), 1))
            
            return {
                "answer": answer,
                "latency_ms": round(latency_ms, 2),
                "tokens_prompt": len(question.split()) * 1.3,
                "tokens_completion": len(answer.split()) * 1.3,
                "correctness": round(correctness, 3),
                "context_relevance": 0.75 if config.get('use_rag') else None,
                "faithfulness": 0.80 if config.get('use_rag') else None,
                "error": None
            }
        
        return {"error": "LLM not configured"}
    
    def compare_runs(self, run1_results: List[Dict], run2_results: List[Dict]) -> Dict[str, Any]:
        def avg_metric(results, metric):
            values = [r.get(metric) for r in results if r.get(metric) is not None]
            return sum(values) / len(values) if values else None
        
        return {
            "run1_avg_correctness": avg_metric(run1_results, "correctness"),
            "run2_avg_correctness": avg_metric(run2_results, "correctness"),
            "run1_avg_latency": avg_metric(run1_results, "latency_ms"),
            "run2_avg_latency": avg_metric(run2_results, "latency_ms"),
            "comparison": "Deterministic comparison of runs"
        }

evaluator = BaselineEvaluator()
