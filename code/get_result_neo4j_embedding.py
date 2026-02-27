import pandas as pd
from neo4j import GraphDatabase
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# ================================================================
# 1️⃣ Neo4j connection
# ================================================================
URI = "bolt://localhost:7687"
AUTH = ("neo4j", "12345678")
driver = GraphDatabase.driver(URI, auth=AUTH)

# ================================================================
# 2️⃣ Load CSV
# ================================================================
csv_path = "incorrect_predictions_with_fallback-fine-2021.csv"
df = pd.read_csv(csv_path)

required_cols = ["Question", "Fallback_Cypher", "Answer"]
for col in required_cols:
    if col not in df.columns:
        raise ValueError(f"❌ Missing required column: {col}")

if "Fallback_Result" not in df.columns:
    df["Fallback_Result"] = None

print(f"✅ Loaded {len(df)} rows from {csv_path}")

# ================================================================
# 3️⃣ Helper: run Cypher safely
# ================================================================
def run_cypher_safely(tx, query):
    """Run a Cypher query and return results or [] if invalid."""
    try:
        result = list(tx.run(query))
        return [dict(r) for r in result] if result else []
    except Exception as e:
        # Uncomment for debugging
        # print(f"⚠️ Query failed: {e}")
        return []

# ================================================================
# 4️⃣ Helper: extract unique CWE IDs
# ================================================================
def extract_cwe_ids(records):
    """Extract unique CWE IDs from Neo4j query results."""
    cwe_ids = set()
    for record in records:
        for key, val in record.items():
            try:
                if hasattr(val, "get") and "cwe_id" in val:
                    cwe_ids.add(val["cwe_id"].upper())
                elif isinstance(val, dict) and "cwe_id" in val:
                    cwe_ids.add(val["cwe_id"].upper())
            except Exception:
                continue
    return sorted(cwe_ids)

# ================================================================
# 5️⃣ Execute Fallback Cyphers
# ================================================================
predictions = []
contain_pred = []  # lenient (contains ground truth)
exact_pred = []    # strict (exact match)

with driver.session() as session:
    for idx, row in df.iterrows():
        cypher_query = row["Fallback_Cypher"]

        if not isinstance(cypher_query, str) or not cypher_query.strip():
            df.at[idx, "Fallback_Result"] = []
            predictions.append([])
            continue

        results = session.execute_read(run_cypher_safely, cypher_query)
        unique_cwe = extract_cwe_ids(results)
        df.at[idx, "Fallback_Result"] = unique_cwe
        predictions.append(unique_cwe)
        # break
        print(f"✅ Processed {idx+1}/{len(df)} | CWE: {unique_cwe}")

driver.close()

# ================================================================
# 6️⃣ Evaluation (Contain vs Exact)
# ================================================================
y_true = [str(a).strip().upper() for a in df["Answer"]]
y_pred = [p for p in predictions]

contain_y_true, contain_y_pred = [], []
exact_y_true, exact_y_pred = [], []

for gt, preds in zip(y_true, y_pred):
    contain_y_true.append(1)
    exact_y_true.append(1)

    contain_y_pred.append(1 if gt in preds else 0)
    exact_y_pred.append(1 if preds == [gt] else 0)

# Compute metrics
def print_metrics(title, y_true, y_pred):
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, zero_division=0)
    rec = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)

    print(f"\n=== {title} ===")
    print(f"Accuracy : {acc:.4f}")
    print(f"Precision: {prec:.4f}")
    print(f"Recall   : {rec:.4f}")
    print(f"F1-score : {f1:.4f}")

print_metrics("Contain Version (lenient)", contain_y_true, contain_y_pred)
print_metrics("Exact Match Version (strict)", exact_y_true, exact_y_pred)

# ================================================================
# 7️⃣ Save Results
# ================================================================
output_file = "fallback_rcm_fine.csv"
df.to_csv(output_file, index=False)
print(f"\n🎉 Saved results with fallback predictions to {output_file}")
