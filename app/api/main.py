from fastapi import FastAPI, HTTPException
from app.models.schemas import EvalRunCreate
from app.services.evaluator import evaluator
from app.core.database import db
import json

app = FastAPI(
    title="LLMOps Lab",
    description="LLM evaluation and observability platform",
    version="1.0.0"
)

@app.post("/runs")
def create_run(run_request: EvalRunCreate):
    # Load dataset
    try:
        with open('data/evaluation_dataset.json', 'r') as f:
            dataset = json.load(f)
    except:
        raise HTTPException(status_code=500, detail="Dataset not found")
    
    config_snapshot = {"configs": [c.dict() for c in run_request.configs], "dataset_version": run_request.dataset_version}
    run_id = db.create_run(run_request.dataset_version, config_snapshot)
    
    results_all = []
    for config in run_request.configs:
        config_dict = config.dict()
        for item in dataset:
            eval_result = evaluator.evaluate(item['question'], item['expected_answer'], config_dict)
            result_record = {
                "question_id": item['id'],
                "question": item['question'],
                "answer": eval_result.get('answer', ''),
                "expected_answer": item['expected_answer'],
                "latency_ms": eval_result.get('latency_ms', 0),
                "tokens_prompt": eval_result.get('tokens_prompt'),
                "tokens_completion": eval_result.get('tokens_completion'),
                "correctness": eval_result.get('correctness'),
                "context_relevance": eval_result.get('context_relevance'),
                "faithfulness": eval_result.get('faithfulness'),
                "error": eval_result.get('error')
            }
            db.add_result(run_id, result_record)
            results_all.append(result_record)
    
    return {"run_id": run_id, "status": "completed", "results_count": len(results_all)}

@app.get("/runs")
def list_runs():
    runs = db.list_runs()
    return {"runs": runs}

@app.get("/runs/{run_id}")
def get_run(run_id: int):
    run = db.get_run(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    results = db.get_run_results(run_id)
    return {"run": run, "results": results}

@app.get("/runs/{run_id}/compare")
def compare_runs(run_id: int):
    results = db.get_run_results(run_id)
    # For demo, compare with aggregated metrics
    comparison = evaluator.compare_runs(results, results)
    return comparison

@app.get("/dashboard")
def dashboard():
    runs = db.list_runs()
    return {
        "total_runs": len(runs),
        "latest_run": runs[0] if runs else None,
        "metrics_computed": ["latency_ms", "correctness"],
        "metrics_skipped": ["tokens when unavailable", "cost when not configured", "ragas metrics if dependencies missing"],
        "note": "Simulated/deterministic data - not real LLM benchmark results"
    }

@app.get("/health")
def health():
    return {"status": "healthy", "deterministic_mode": True, "mlflow_available": True}
