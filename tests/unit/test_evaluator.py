import pytest
from app.services.evaluator import evaluator

def test_evaluate_deterministic():
    result = evaluator.evaluate("What is machine learning?", 
                                "Machine learning is a subset of artificial intelligence",
                                {"name": "test", "model_name": "llama2", "use_rag": False})
    assert "answer" in result
    assert "latency_ms" in result
    assert result["latency_ms"] > 0
    assert "correctness" in result
    assert result["correctness"] >= 0
    assert result["correctness"] <= 1
    assert result["error"] is None

def test_evaluate_with_rag():
    result = evaluator.evaluate("What is RAG?",
                                "Retrieval-Augmented Generation combines retrieval with generation",
                                {"name": "test", "model_name": "llama2", "use_rag": True})
    assert result["context_relevance"] is not None
    assert result["faithfulness"] is not None
