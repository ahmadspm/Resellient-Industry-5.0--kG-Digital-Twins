import json
import numpy as np
import pandas as pd
from tqdm import tqdm
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

# =========================================================
# 1. Load DeepWalk embeddings and metadata
# =========================================================

embeddings = np.load("code_and_file_part1llm/node_text_embeddings_minilm.npy")
print(f"✅ Loaded embeddings with shape: {embeddings.shape}")

# Load node metadata
with open("code_and_file_part1llm/graph_nodes_updated.json", "r") as f:
    node_data = json.load(f)

nodes = list(node_data["nodes"].keys())
print(f"✅ Loaded {len(nodes):,} nodes from graph_nodes.json")

node_info = node_data["nodes"]

# =========================================================
# 2. Load MiniLM for text encoding
# =========================================================
print("\n🧠 Loading MiniLM model (all-MiniLM-L6-v2)...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# =========================================================
# 3. Function to find most similar node
# =========================================================
def find_most_similar_node(query: str, embeddings, nodes, node_info, model):
    """
    Given a natural-language query, find the top-1 most similar node
    from the embedding space.
    """
    if not isinstance(query, str) or query.strip() == "":
        return None

    query_vec = model.encode([query])[0].reshape(1, -1)
    sims = cosine_similarity(query_vec, embeddings)[0]

    top_idx = int(np.argmax(sims))
    node_id = nodes[top_idx]
    info = node_info.get(node_id, {})
    label = info.get("label", "Unknown")
    score = float(sims[top_idx])
    desc = info.get("attributes", {}).get("description") or info.get("attributes", {}).get("title", "")

    return {
        "node_id": node_id,
        "label": label,
        "score": score,
        "description": desc[:300] + ("..." if len(desc) > 300 else "")
    }

# =========================================================
# 4. Read incorrect predictions
# =========================================================
print("\n📄 Reading incorrect_predictions.csv ...")
df = pd.read_csv("incorrect_predictions-fine.csv")
print(f"✅ Loaded {len(df)} incorrect or multi-result rows")

# =========================================================
# 5. Generate embedding-based node suggestion
# =========================================================
embed_results = []

for _, row in tqdm(df.iterrows(), total=len(df), desc="🔍 Finding most similar nodes"):
    question = row.get("Question", "")
    result = find_most_similar_node(question, embeddings, nodes, node_info, model)
    if result:
        embed_results.append(result["node_id"])
    else:
        embed_results.append("None")

df["embed_result"] = embed_results

# =========================================================
# 6. Save the results
# =========================================================
output_path = "fallback_incorrect-fine-2021.csv"
df.to_csv(output_path, index=False)
print(f"\n💾 Saved results with embed suggestions to '{output_path}'")

print("\n✅ Sample Output:")
print(df.head())
