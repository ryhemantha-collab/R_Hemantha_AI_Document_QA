"""Lightweight benchmark evaluation for document QA."""
import csv
from pathlib import Path
from reasoning_engine import answer_question

def evaluate_questions(csv_path, kb):
    rows = []
    tp = fp = fn = passed = 0
    with open(csv_path, newline="", encoding="utf-8") as f:
        for item in csv.DictReader(f):
            result = answer_question(item["question"], kb)
            expected = {x for x in item["expected_terms"].casefold().split(";") if x}
            actual = set(" ".join(result["evidence"]).casefold().replace(".", " ").split())
            hit = len(expected & actual)
            precision = hit / max(1, len(actual))
            recall = hit / max(1, len(expected))
            ok = recall >= 0.5
            passed += int(ok)
            tp += hit
            fp += max(0, len(actual)-hit)
            fn += max(0, len(expected)-hit)
            rows.append({"Question":item["question"],"Pass": "PASS" if ok else "CHECK","Evidence statements":len(result["evidence"]),"Expected-term recall":round(recall,2),"Answer":result["answer"][:180]})
    precision = tp/max(1,tp+fp)
    recall = tp/max(1,tp+fn)
    f1 = 2*precision*recall/max(1e-9,precision+recall)
    return {"pass_rate":passed/max(1,len(rows)),"precision":precision,"recall":recall,"f1":f1}, rows
