import json
import random
import itertools
from pathlib import Path

# -----------------------------
# CONFIG
# -----------------------------
GRAPH_FILE = "..\Downloads\code_and_file_part1llm\graph_nodes_updated.json"        # your node JSON file
OUTPUT_FILE = "benchmark_dataset.json"
NUM_SAMPLES = 300                 # total number of benchmark questions

# Relationships (from your schema)
RELATIONSHIPS = [
    ("CVE", "HAS_CWE", "CWE"),
    ("CVE", "TARGETS", "Target"),
    ("CWE", "HAS_DETECTION", "CWEDetection"),
    ("CWE", "HAS_CONSEQUENCE", "CWEConsequence"),
    ("CWE", "HAS_CWE_MITIGATION", "CWEMitigation"),
    ("CWE", "HAS_MODE_OF_INTRODUCTION", "CWEModeOfIntroduction"),
    ("CWE", "HAS_CAPEC", "CAPEC"),
    ("CAPEC", "HAS_CAPEC_CONSEQUENCE", "CAPECConsequence"),
    ("CAPEC", "HAS_TECHNIQUE", "Technique"),
    ("CAPEC", "HAS_ATTACK", "Attack"),
    ("Group", "BELONG_TO", "Tactic"),
    ("Group", "USE_MALWARE", "Malware"),
    ("Group", "HAS_CAMPAIGN", "Campaign"),
    ("Group", "USE_TECHNIQUE", "Technique"),
    ("Malware", "USE_TECHNIQUE", "Technique"),
    ("Mitigation", "MITIGATES", "Technique"),
    ("Technique", "ATTACK", "Asset"),
    ("Product", "HAS_VULNERABILITY", "CVE")
]

# Templates for natural question phrasing
TEMPLATES = {
    1: [
        "Which {end_label} is associated with {start_label} {entity_id}?",
        "Find all {end_label}s connected to {start_label} {entity_id}.",
        "Show me {end_label}s linked to {start_label} {entity_id}.",
        "List all {end_label}s related to {start_label} {entity_id}."
    ],
    2: [
        "Which {end_label} is connected to {start_label} {entity_id} through its {mid_label}?",
        "Find all {end_label}s related to {start_label} {entity_id} via {mid_label}.",
        "What {end_label}s can be reached from {start_label} {entity_id} through {mid_label}?"
    ],
    3: [
        "Which {end_label} is linked to {start_label} {entity_id} through {mid1_label} and {mid2_label}?",
        "Find all {end_label}s connected to {start_label} {entity_id} via {mid1_label} and {mid2_label} relationships."
    ]
}


# -----------------------------
# HELPERS
# -----------------------------
def random_cve_id():
    """Generate a realistic CVE ID."""
    return f"CVE-{random.randint(2017, 2025)}-{random.randint(1000, 99999)}"


def find_two_hop_paths(schema):
    """Find valid 2-hop connection chains."""
    chains = []
    for (a, r1, b) in schema:
        for (x, r2, y) in schema:
            if b == x:
                chains.append([(a, r1, b), (x, r2, y)])
    return chains


def find_three_hop_paths(schema):
    """Find valid 3-hop connection chains."""
    chains = []
    for (a, r1, b) in schema:
        for (x, r2, y) in schema:
            if b == x:
                for (p, r3, q) in schema:
                    if y == p:
                        chains.append([(a, r1, b), (x, r2, y), (p, r3, q)])
    return chains


def build_query(path_triplets, entity_id):
    """
    Build valid Cypher query given a chain of triplets like:
    [("CVE", "HAS_CWE", "CWE"), ("CWE", "HAS_CONSEQUENCE", "CWEConsequence")]
    """
    parts = []
    var_names = [chr(97 + i) for i in range(len(path_triplets) + 1)]  # a, b, c, d...
    for i, (src, rel, dst) in enumerate(path_triplets):
        left_var = var_names[i]
        right_var = var_names[i + 1]
        # label both nodes properly
        parts.append(f"({left_var}:{src})-[:{rel}]->({right_var}:{dst})")
    match_clause = "-".join(parts)
    return f"MATCH {match_clause} WHERE toLower(a.cve_id) CONTAINS toLower('{entity_id}') RETURN {var_names[-1]}"


# -----------------------------
# MAIN
# -----------------------------
def main():
    print("🔍 Generating valid Cypher benchmark dataset...")
    Path(OUTPUT_FILE).unlink(missing_ok=True)

    try:
        with open(GRAPH_FILE) as f:
            graph = json.load(f)
        print(f"Loaded graph with {len(graph.get('nodes', {}))} nodes.")
    except Exception as e:
        print(f"⚠️ Could not load graph ({e}). Proceeding without node data.")
        graph = {}

    onehop = [r for r in RELATIONSHIPS if r[0] == "CVE"]
    twohop = find_two_hop_paths(RELATIONSHIPS)
    threehop = find_three_hop_paths(RELATIONSHIPS)

    data = []

    for _ in range(NUM_SAMPLES):
        hop_type = random.choices([1, 2, 3], weights=[0.4, 0.4, 0.2])[0]
        cve_id = random_cve_id()

        if hop_type == 1:
            s1, r1, e1 = random.choice(onehop)
            q = random.choice(TEMPLATES[1]).format(start_label=s1, end_label=e1, entity_id=cve_id)
            # cypher = build_query([(s1, r1, e1)], cve_id)
            data.append({
                "id": f"{cve_id}_{r1}",
                "question": q,
                # "answer_query": cypher,
                "hops": 1,
                "path": [s1, e1]
            })

        elif hop_type == 2:
            chain = random.choice(twohop)
            (s1, r1, m1), (s2, r2, e1) = chain
            q = random.choice(TEMPLATES[2]).format(
                start_label=s1, mid_label=m1, end_label=e1, entity_id=cve_id
            )
            cypher = build_query([(s1, r1, m1), (s2, r2, e1)], cve_id)
            data.append({
                "id": f"{cve_id}_{r1}_{r2}",
                "question": q,
                "answer_query": cypher,
                "hops": 2,
                "path": [s1, m1, e1]
            })

        else:  # 3-hop
            chain = random.choice(threehop)
            (s1, r1, m1), (s2, r2, m2), (s3, r3, e1) = chain
            q = random.choice(TEMPLATES[3]).format(
                start_label=s1, mid1_label=m1, mid2_label=m2, end_label=e1, entity_id=cve_id
            )
            # cypher = build_query([(s1, r1, m1), (s2, r2, m2), (s3, r3, e1)], cve_id)
            data.append({
                "id": f"{cve_id}_{r1}_{r2}_{r3}",
                "question": q,
                "hops": 3,
                "path": [s1, m1, m2, e1]
            })

    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=2)

    print(f"✅ Generated {len(data)} valid benchmark questions → {OUTPUT_FILE}")


if __name__ == "__main__":
    main()