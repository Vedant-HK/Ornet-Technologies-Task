# Task 3 — ML & LLM Conceptual Debugging

## Objective
Explain likely causes and practical remedies for five common ML/LLM system problems.

## Topics covered
1. **Hallucination:** Ground answers in retrieved context, instruct the model to acknowledge missing evidence, request document references, and test unsupported-answer behavior.
2. **Poor retrieval:** Inspect retrieved passages, document extraction, chunk size and overlap, embeddings, ranking, top-k, hybrid search, and reranking. Evaluate retrieval separately with known relevant documents and metrics such as Recall@k and MRR.
3. **Overfitting:** Use train/validation/test splits, regularization, early stopping, representative data, and cross-validation while reserving the test set for final evaluation.
4. **Data leakage:** Check split overlap and duplicates, fit preprocessing only on training data, inspect target/future information in features, and use chronological or group-based splits where appropriate.
5. **Prompt engineering vs. RAG:** Prompt engineering guides model behavior; RAG retrieves external information and supplies it as context. They can be combined.

## Deliverable
`Task3/README.md` contains the written responses, a comparison summary, assumptions, scope, and AI-assistance disclosure. This task is primarily a written conceptual deliverable; no executable application or automated test suite is required by the assessment prompt.

## Assumptions and limitations
The responses describe a typical document-question-answering chatbot and supervised ML workflow. The actual root cause should be confirmed through system inspection and evaluation rather than assumed from symptoms alone.

## Suggested demonstration
For each scenario, state the symptom, one or more plausible causes, a practical diagnostic check, and a targeted corrective action. Explain why prompt instructions reduce but cannot eliminate hallucinations, and why retrieval and generation need separate evaluation.
