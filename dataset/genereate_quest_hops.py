import pandas as pd

# Load CSV
df = pd.read_csv("67CVE_malware.csv")



# Ensure column names match your CSV
df.columns = df.columns.str.strip()  # clean whitespace
unique_cves = df["CVE"].unique()

# Question templates
# templates = [
#     "What mitigation should be applied for {cve}?",
#     "What are the recommended mitigations for {cve}?",
#     "Which mitigation actions address {cve}?",
#     "How can {cve} be mitigated?",
#     "What defensive measures correspond to {cve}?",
#     "List the ATT&CK mitigations associated with {cve}.",
#     "How should an analyst mitigate {cve}?"
# ]

# templates = [
#     "What ATT&CK technique is associated with {cve}?",
#     "Which attack techniques are linked to {cve}?",
#     "What ATT&CK techniques does {cve} map to?",
#     "List the attack techniques related to {cve}.",
#     "Which techniques could be used to exploit {cve}?",
#     "What adversary techniques correspond to {cve}?",
#     "How does {cve} relate to ATT&CK techniques?"
# ]

# templates = [
#     "What CAPEC attack pattern is associated with {cve}?",
#     "Which CAPEC patterns are linked to {cve}?",
#     "What CAPEC does {cve} map to?",
#     "List the CAPEC attack patterns related to {cve}.",
#     "Which CAPEC entries describe attacks exploiting {cve}?",
#     "What adversary attack patterns (CAPEC) correspond to {cve}?",
#     "What CAPEC attack patterns characterize the exploitation of {cve}?"
# ]


templates = [
    "Which malware is associated with {cve}?",
    "What malware families exploit {cve}?",
    "List the malware linked to {cve}.",
    "Which adversary malware uses techniques derived from {cve}?",
    "What malware campaigns are connected to {cve}?",
    "Which malware variants leverage vulnerabilities like {cve}?",
    "Which malware tools are used by groups exploiting {cve}?"
]

# templates = [
#     "What CWE weakness is associated with {cve}?",
#     "Which CWE does {cve} map to?",
#     "What underlying CWE classification applies to {cve}?",
#     "List the CWE weaknesses related to {cve}.",
#     "Which software weakness (CWE) contributes to {cve}?",
#     "What is the primary CWE category for {cve}?",
#     "Which CWE entry best describes the vulnerability in {cve}?",
# ]
# Generate questions
questions = []
for cve in unique_cves:
    for t in templates:
        questions.append(t.format(cve=cve))

# Print results
for q in questions:
    print(q)

# OPTIONAL: Save to file
pd.DataFrame({"question": questions}).to_csv("generated_questions_malw.csv", index=False)
