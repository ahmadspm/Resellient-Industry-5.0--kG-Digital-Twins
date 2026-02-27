import pandas as pd
import ast
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score

# === Load CSV ===
df = pd.read_csv("cti-rcm-fine-results-2021.csv")

# Convert stringified list (e.g., "['A', 'B']") to real Python list
df["Cypher_Results"] = df["Cypher_Results"].apply(
    lambda x: ast.literal_eval(x) if isinstance(x, str) else []
)

# Prepare binary labels for both evaluation types
contain_true, contain_pred = [], []
exact_true, exact_pred = [], []
wrong_rows = []  # collect rows with wrong or multiple predictions

for idx, row in df.iterrows():
    gt = str(row["Answer"]).strip()
    preds = [str(p).strip() for p in row["Cypher_Results"]]

    contain_true.append(1)
    exact_true.append(1)

    # Containment version
    contain_pred.append(1 if gt in preds else 0)

    # Exact-match version
    exact_pred.append(1 if preds == [gt] else 0)

    # Identify incorrect, multi-result, or empty predictions
    if (gt not in preds) or (len(preds) != 1):
        wrong_rows.append({
            "Row_Index": idx,
            "Question": row.get("Question", ""),  # Include the question text
            "Answer": gt,
            "Predicted_List": preds,
            "Correct_in_Contain": gt in preds,
            "Num_Predicted": len(preds)
        })

def print_metrics(title, y_true, y_pred):
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)

    print(f"\n=== {title} ===")
    print(f"Accuracy : {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall   : {recall:.4f}")
    print(f"F1-score : {f1:.4f}")

# Compute both sets of metrics
print_metrics("Contain Version (lenient)", contain_true, contain_pred)
print_metrics("Exact Match Version (strict)", exact_true, exact_pred)

# Export wrong predictions to CSV (now with Question column)
wrong_df = pd.DataFrame(wrong_rows)
wrong_df.to_csv("incorrect_predictions-fine.csv", index=False)

print(f"\nSaved {len(wrong_df)} incorrect/multi-result rows to 'incorrect_predictions-fine.csv'")


