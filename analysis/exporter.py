import json
import csv

def export_to_csv(ctx: dict, path: str):
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["key", "value_json"])
        for k, v in ctx.items():
            writer.writerow([k, json.dumps(v)])
