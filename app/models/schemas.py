from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class EvalConfig(BaseModel):
    name: str
    model_name: str
    use_rag: bool = False
    temperature: float = 0.7

class EvalRunCreate(BaseModel):
    dataset_version: str = "v1"
    configs: List[EvalConfig]

class EvalResult(BaseModel):
    question_id: int
    question: str
    answer: str
    expected_answer: str
    latency_ms: float
    tokens_prompt: Optional[int] = None
    tokens_completion: Optional[int] = None
    correctness: Optional[float] = None
    context_relevance: Optional[float] = None
    faithfulness: Optional[float] = None
    error: Optional[str] = None
