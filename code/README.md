# How to Start

GRICS is ready to use once the knowledge graph has been installed.

Please note that the components of this project are not directly connected in real time, as the language model and the knowledge base are hosted on different devices.

The outputs from `base_llm` and `llm_fine_tune` are generated Cypher queries, which are saved as CSV files. These CSV files are then imported into Neo4j for execution.

If any generated queries fail to execute, they are stored separately. The corresponding questions are then processed using embeddings to identify similar nodes within the knowledge graph.

---

## File Descriptions

### `base_llm`

This file can be used directly with a defined prompt.

If you are working with a different knowledge graph structure, it is strongly recommended to modify the prompt to match your schema.

The output of this file is a generated Cypher query based on a given question (e.g., *"What is the Technique ID of CVE ID XXXXX?"*).

The script can:
- Process a CSV file containing multiple questions (e.g., CTI_BENCHMARK)
- Handle a single question with minor code adjustments

---

### `llm_fine_tune`

This file is used to fine-tune the base model in order to:

- Improve understanding of paraphrased questions  
- Enhance the model’s ability to generate IT/OT-related queries requiring deeper contextual understanding  

Running this file produces a fine-tuned model, which can also be downloaded from [model_link](https://drive.google.com/file/d/1b_6akH2ZQDOi6QzALJX4YFFYvqS5-FTB/view?usp=sharing)

---

### `get_result_neo4j`

This file demonstrates how to connect to Neo4j and execute generated Cypher queries.

It takes a CSV file containing questions and their generated queries as input. The script:

- Executes each query in Neo4j  
- Generates a new CSV file containing failed (broken) queries  

---

### `get_result_neo4j_embedding`

This file also connects to Neo4j and executes generated queries.

Unlike `get_result_neo4j`, it focuses on returning the overall execution results rather than isolating failed queries.

---

### `get_similar_embedding`

This file demonstrates how to retrieve semantically similar embeddings from a CSV file.

It is used when a generated query fails, enabling the system to identify related nodes in the knowledge graph through semantic similarity.

Before running this file, you need to embed the BRIDG-ICS node CSV file. In this project, the `MiniLM-L6-v2` model is used to generate the embeddings. The model can be downloaded from:

*(insert download link here)*


---

### `Evaluation` Folder

The `Evaluation` folder contains example scripts for benchmarking and testing both:

- `base_llm`
- `llm_fine_tune`

These scripts are used to evaluate and compare model performance.