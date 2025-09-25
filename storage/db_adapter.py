import sqlite3
import json
from typing import Dict

class SQLiteAdapter:
    def __init__(self, db_path: str = "results.db"):
        self.conn = sqlite3.connect(db_path)
        self._init_schema()

    def _init_schema(self):
        c = self.conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            run_id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipe TEXT,
            start_time TEXT,
            end_time TEXT,
            status TEXT
        )
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS context_data (
            run_id INTEGER,
            key TEXT,
            value_json TEXT,
            FOREIGN KEY(run_id) REFERENCES runs(run_id)
        )
        """)
        self.conn.commit()

    def insert_run(self, recipe: str, start: str, end: str, status: str, ctx: Dict):
        c = self.conn.cursor()
        c.execute("INSERT INTO runs (recipe, start_time, end_time, status) VALUES (?, ?, ?, ?)",
                  (recipe, start, end, status))
        run_id = c.lastrowid
        for k, v in ctx.items():
            c.execute("INSERT INTO context_data (run_id, key, value_json) VALUES (?, ?, ?)",
                      (run_id, k, json.dumps(v)))
        self.conn.commit()
