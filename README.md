# Resellient-Industry-5.0--kG-Digital-Twins
This repository contains the implementation of GRICS (Graph-Integrated Retrieval for Industry-Centric Security) — a Knowledge-Graph-Augmented Retrieval-Augmented Generation (KG-RAG) framework designed for explainable, human–AI collaborative threat reasoning in Industry 5.0 cyber-physical systems.

GRICS
Graph-Aware Retrieval-Augmented Framework for Explainable Threat Reasoning in Industry 5.0


## Overview

GRICS (Graph-Integrated Retrieval for Industry-Centric Security) is a Knowledge-Graph-Augmented Retrieval-Augmented Generation (KG-RAG) framework designed for:

Explainable cyber threat reasoning

Multi-hop attack path analysis

Human–AI collaborative cybersecurity decision support

Industry 5.0 cyber-physical systems

GRICS integrates structured cybersecurity knowledge (CVE, CWE, CAPEC, MITRE ATT&CK) with a dual-LLM architecture to enable interpretable, ontology-grounded reasoning across IT and OT environments.

## Core Contributions

✅ Graph-aware RAG for cyber-physical environments

✅ BRIDG-ICS ontology operationalization

✅ Dual-LLM architecture (Symbolic Retrieval + Answer Synthesis)

✅ Hybrid symbolic + embedding fallback retrieval

✅ Multi-hop reasoning (up to 5 hops)

✅ Quantitative explainability metrics

✅ Adversarial robustness evaluation

## System Architecture

GRICS follows a structured two-stage pipeline:

# Symbolic Retrieval Stage

Natural language query → Cypher generation

Executed over Neo4j BRIDG-ICS knowledge graph

Retrieves interpretable subgraphs

# Answer Generation Stage

Retrieved graph evidence → LLM synthesis

Produces grounded explanations

Preserves reasoning chains (e.g., CVE → CWE → CAPEC → ATT&CK)

# Embedding Fallback

If symbolic execution returns empty results:

Semantic similarity search identifies anchor nodes

Refined Cypher query reattempted

## Security Aware Knowledge Graph

The BRIDG-ICS knowledge graph integrates:

CVE

CWE

CAPEC

MITRE ATT&CK

Industrial assets (IT & OT)

Communication flows

Risk attributes:

pExploit

riskWeight

controlStrength

costAttack

This enables:

Vulnerability Propagation Risk (VPR) computation

ATT&CK technique reachability

Cross-layer attack path reasoning

## Evaluation Summary

GRICS is evaluated on:

CTI-RCM (2021, 2024)

CTI-ATE benchmark

Multi-hop reasoning (1–5 hops)

Explainability metrics:

Hallucination Rate (HR)

Query Violation Rate (QVR)

Schema Consistency Rate (SCR)

Adversarial robustness:

Attack Success Rate (ASR)

Tokens per Query (TPQ)

Results demonstrate:

Improved multi-hop stability

Reduced hallucination under increasing relational depth

Strong grounding in symbolic retrieval

Higher interpretability compared to baseline LLMs

## Repository Structure
GRICS/
│
├── kg/
│   ├── bridg_ics_schema.cypher
│   ├── graph_population.py
│   └── embeddings/
│
├── retrieval/
│   ├── cypher_llm/
│   ├── hybrid_retrieval.py
│   └── fallback_logic.py
│
├── finetuning/
│   ├── dataset/
│   ├── training_config.yaml
│   └── lora_training.py
│
├── evaluation/
│   ├── cti_benchmark/
│   ├── adversarial_testing/
│   └── explainability_metrics.py
│
├── use_cases/
│   ├── attack_path_reasoning.py
│   ├── vulnerability_analysis.py
│   ├── mitigation_derivation.py
│   └── technique_attribution.py
│
└── README.md
⚙️ Installation
1️⃣ Clone Repository
git clone https://github.com/your-org/GRICS.git
cd GRICS
2️⃣ Install Dependencies
pip install -r requirements.txt
3️⃣ Neo4j Setup

Install Neo4j (v5+ recommended)

Import BRIDG-ICS schema

Populate graph database

🚀 Running the System
Run Hybrid Retrieval
python retrieval/hybrid_retrieval.py --query "Find mitigations for CVE-2025-9492"
Run Attack Path Analysis
python use_cases/attack_path_reasoning.py --source MQTT_BROKER_1 --target SAFETY_PLC_2
📈 Threat-Modelling Metrics
Vulnerability Propagation Risk (VPR)
𝑉
𝑃
𝑅
=
∑
𝑝
𝐸
𝑥
𝑝
𝑙
𝑜
𝑖
𝑡
𝑖
⋅
𝑟
𝑖
𝑠
𝑘
𝑊
𝑒
𝑖
𝑔
ℎ
𝑡
𝑖
⋅
(
1
−
𝑐
𝑜
𝑛
𝑡
𝑟
𝑜
𝑙
𝑆
𝑡
𝑟
𝑒
𝑛
𝑔
𝑡
ℎ
𝑖
)
VPR=∑pExploit
i
	​

⋅riskWeight
i
	​

⋅(1−controlStrength
i
	​

)

Used for:

Zone-level risk aggregation

OT/DMZ/IT risk comparison

Propagation prioritization

Human-Centric Design

GRICS supports:

Inspectable reasoning chains

Transparent symbolic retrieval

Analyst validation of intermediate steps

Evidence-grounded mitigation derivation

Designed to align with Industry 5.0 human-in-the-loop principles.

Research Extensions

Planned improvements:

Confidence-aware traversal

Hierarchical reasoning strategies

Structural adversarial robustness testing

Real-time embedding updates

Digital Twin integration

📜 Citation

If you use this work, please cite:

@article{GRICS2025,
  title={GRICS: A Knowledge-Graph-Augmented Framework for Explainable and Human–AI Collaborative Threat Reasoning in Industry 5.0 Systems},
  author={Nandiya, P. and Mohsin, A. and Sarker, I.H and Ibrahim, A. and Janicke, H.},
  journal={IEEE Access},
  year={2026}
}
