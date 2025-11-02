"""
main.py - Email Type Classifier with CSV output
-----------------------------------------------
Classifies emails into one of six categories:
Forum, Promotions, Social Media, Spam, Updates, or Verify Code
using few-shot prompting and GPT-4o.
"""

from dotenv import load_dotenv
load_dotenv()  # loads OPENAI_API_KEY from .env

from openai import OpenAI
import csv, json, os, time
from collections import Counter

client = OpenAI()

# ---------------- 1. Load prompt templates ----------------
with open("prompts.json", "r", encoding="utf-8") as f:
    TEMPLATE = json.load(f)

# ---------------- 2. Build chat messages ------------------
def make_messages(email_text: str):
    msgs = [{"role": "system", "content": TEMPLATE["system"]}]
    for ex in TEMPLATE["few_shot"]:
        msgs.append({"role": "user", "content": ex["input"]})
        msgs.append({"role": "assistant", "content": ex["label"]})
    msgs.append({"role": "user", "content": email_text})
    return msgs

# ---------------- 3. Call model ---------------------------
def classify(email_text: str, model="gpt-4o"):
    """Classify a single email string using OpenAI Chat Completions API."""
    resp = client.chat.completions.create(
        model=model,
        messages=make_messages(email_text),
        temperature=0.0,
    )
    time.sleep(0.25)  # avoid rate-limit
    return resp.choices[0].message.content.strip().lower()

# ---------------- 4. Evaluate and write to CSV ------------
def evaluate(csv_in="emails.csv", csv_out="results.csv"):
    results = []
    with open(csv_in, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            email_text = row["text"]
            true_label = row["category"]
            if not email_text or not true_label:
                continue  # skip empty rows
            true_label = true_label.lower()

            pred_label = classify(email_text)
            correct = int(true_label == pred_label)
            results.append({
                "id": row.get("id", ""),
                "email_text": email_text,
                "true_label": true_label,
                "pred_label": pred_label,
                "correct": correct
            })

    # write predictions
    with open(csv_out, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["id", "email_text", "true_label", "pred_label", "correct"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    # summary metrics
    acc = sum(r["correct"] for r in results) / len(results)
    counts = Counter(r["pred_label"] for r in results)
    print(f"Wrote {len(results)} rows to {csv_out}")
    print(f"Accuracy: {acc:.2f}")
    print("Predicted label counts:", dict(counts))

# ---------------- 5. Run ----------------
if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        raise EnvironmentError("OPENAI_API_KEY not loaded from .env")
    evaluate()
