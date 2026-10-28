import sqlite3
import json
from datetime import datetime

class Database:
    def __init__(self, db_path: str = "llmops.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        
        cur.execute('''CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dataset_version TEXT,
            config_snapshot TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        cur.execute('''CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id INTEGER,
            question_id INTEGER,
            question TEXT,
            answer TEXT,
            expected_answer TEXT,
            latency_ms REAL,
            tokens_prompt REAL,
            tokens_completion REAL,
            correctness REAL,
            context_relevance REAL,
            faithfulness REAL,
            error TEXT,
            FOREIGN KEY (run_id) REFERENCES runs (id)
        )''')
        
        conn.commit()
        conn.close()
    
    def create_run(self, dataset_version: str, config_snapshot: dict):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("INSERT INTO runs (dataset_version, config_snapshot) VALUES (?, ?)",
                    (dataset_version, json.dumps(config_snapshot)))
        run_id = cur.lastrowid
        conn.commit()
        conn.close()
        return run_id
    
    def add_result(self, run_id: int, result: dict):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute('''INSERT INTO results 
            (run_id, question_id, question, answer, expected_answer, latency_ms, 
             tokens_prompt, tokens_completion, correctness, context_relevance, faithfulness, error)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (run_id, result['question_id'], result['question'], result['answer'], 
             result['expected_answer'], result['latency_ms'], result.get('tokens_prompt'),
             result.get('tokens_completion'), result.get('correctness'),
             result.get('context_relevance'), result.get('faithfulness'), result.get('error')))
        conn.commit()
        conn.close()
    
    def get_run(self, run_id: int):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM runs WHERE id = ?", (run_id,))
        row = cur.fetchone()
        conn.close()
        if row:
            run = dict(row)
            run['config_snapshot'] = json.loads(run['config_snapshot'])
            return run
        return None
    
    def get_run_results(self, run_id: int):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM results WHERE run_id = ?", (run_id,))
        rows = cur.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    def list_runs(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM runs ORDER BY created_at DESC")
        rows = cur.fetchall()
        conn.close()
        runs = []
        for row in rows:
            run = dict(row)
            run['config_snapshot'] = json.loads(run['config_snapshot'])
            runs.append(run)
        return runs

db = Database()
