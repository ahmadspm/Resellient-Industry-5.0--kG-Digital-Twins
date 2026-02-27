import pandas as pd
import ast
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# === Load both CSVs ===
main_df = pd.read_csv("cti-rcm-fine-results-2021.csv")
fallback_df = pd.read_csv("fallback_rcm_fine.csv")

# --- Safely parse stringified lists ---
def safe_parse(x):
    if isinstance(x, str):
        try:
            return ast.literal_eval(x)
        except:
            return []
    return x if isinstance(x, list) else []

main_df["Cypher_Results"] = main_df["Cypher_Results"].apply(safe_parse)
fallback_df["Fallback_Result"] = fallback_df["Fallback_Result"].apply(safe_parse)

# --- Extract only relevant columns ---
final_df = main_df[["Answer", "Cypher_Results"]].copy()

# --- Replace predictions based on Row_Index ---
if "Row_Index" not in fallback_df.columns:
    raise ValueError("❌ 'Row_Index' column not found in fallback_results_with_metrics.csv")

replaced_rows = 0
for _, row in fallback_df.iterrows():
    i = int(row["Row_Index"])
    if i in final_df.index:
        final_df.at[i, "Cypher_Results"] = row["Fallback_Result"]
        replaced_rows += 1

print(f"✅ Replaced {replaced_rows} rows with fallback results.\n")

# === Compute metrics ===
contain_true, contain_pred = [], []
exact_true, exact_pred = [], []

for _, row in final_df.iterrows():
    gt = str(row["Answer"]).strip().upper()
    preds = [str(p).strip().upper() for p in row["Cypher_Results"]]

    contain_true.append(1)
    exact_true.append(1)

    contain_pred.append(1 if gt in preds else 0)
    exact_pred.append(1 if preds == [gt] else 0)

# === Helper to print metrics ===
def print_metrics(title, y_true, y_pred):
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, zero_division=0)
    rec = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    print(f"=== {title} ===")
    print(f"Accuracy : {acc:.4f}")
    print(f"Precision: {prec:.4f}")
    print(f"Recall   : {rec:.4f}")
    print(f"F1-score : {f1:.4f}\n")

# === Run evaluation ===
print_metrics("Contain Version (lenient, merged fallback)", contain_true, contain_pred)
print_metrics("Exact Match Version (strict, merged fallback)", exact_true, exact_pred)
