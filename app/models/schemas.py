from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class EvalConfig(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    model_name: str = Field(min_length=1, max_length=120)
    use_rag: bool = False
    temperature: float = Field(default=0.7, ge=0, le=2)

class EvalRunCreate(BaseModel):
    dataset_version: str = Field(default="v1", min_length=1, max_length=40)
    configs: List[EvalConfig] = Field(min_length=1, max_length=20)

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
