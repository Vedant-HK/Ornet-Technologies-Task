# Task 3: ML & LLM Conceptual Debugging

# 1. Hallucination

**Problem:** The chatbot gives a confident answer, but the information is not supported by the company documents.

**Possible reasons:**
- The model uses its existing knowledge instead of relying on the provided context.
- The prompt does not clearly tell the model to stick to the available documents.
- The retrieved information is insufficient to answer the question correctly.

**How I would fix it:**
- Clearly instruct the model to answer based on the retrieved documents.
- Tell it to admit when the required information is unavailable instead of making assumptions.
- Ask it to include document references to support important factual claims.
- Check whether the retrieval process is returning the right information.
- Test the chatbot with different questions to identify where unsupported answers occur.

Prompt instructions can help reduce hallucinations, but they cannot guarantee that the model will never produce an incorrect answer.

# 2. Poor Retrieval

**Problem:** The required information exists in the documents, but the chatbot retrieves unrelated or less relevant passages.

**Possible reasons:**
- The documents were not extracted or processed correctly.
- The chunks are too large, too small, or split at the wrong places.
- The embedding model does not capture the meaning of the queries effectively.
- The search or ranking process is not selecting the most relevant passages.

**How I would fix it:**
- First, check which passages are being retrieved for questions that produce incorrect answers.
- Review the document extraction, chunk size, overlap and metadata.
- Try a suitable embedding model and consider combining keyword search with semantic search.
- Adjust the number of retrieved chunks (`top-k`) and use a reranker if needed.
- Test retrieval against questions with known relevant documents. Metrics such as Recall@k and Mean Reciprocal Rank (MRR) can help measure how well the search is performing.

I would check the retrieval results separately from the LLM's response. This helps identify whether the problem is with finding the right information or generating the answer.

# 3. Overfitting

**Problem:** A model performs well on its training data but gives poor results when tested on new, unseen data.

**Possible reasons:**
- The model has memorized training examples instead of learning general patterns.
- The model is too complex for the amount of available data.
- Training continues for too long, causing the model to fit the training data too closely.
- The training data is limited or does not represent real-world situations.

**How I would fix it:**
- Divide the dataset into training, validation and test sets.
- Use regularization or early stopping, or try a simpler model if necessary.
- Add more diverse training examples where possible.
- Use cross-validation to check whether the model performs consistently.
- Keep the test set separate and use it for the final evaluation.

The main goal is to help the model learn patterns that work on new data, rather than simply performing well on examples it has already seen.

# 4. Data Leakage

**Problem:** A model achieves unusually high test accuracy, but its performance drops when it is used on real-world data.

**Possible reasons:**
- Information from the test set has accidentally influenced training.
- Duplicate or very similar records appear in both training and test sets.
- Some input features contain information that would not actually be available when making a prediction.
- Preprocessing or feature selection was performed using the entire dataset before splitting it.

**How I would fix it:**
- Split the data before fitting preprocessing steps such as scaling and imputation. Fit these steps on the training set and apply them to the other sets.
- Check for duplicate records and overlap between the data splits.
- Review the features to ensure they do not reveal the target or contain information from the future.
- Use chronological splits for time-dependent data and group-based splits when related records must stay together.
- Evaluate the model again using a clean test set and compare its results with a simple baseline.

Data leakage can make a model appear much better than it actually is, so the evaluation process must reflect how the model will be used in practice.

# 5. Prompt Engineering vs. Retrieval-Augmented Generation (RAG)

**Prompt engineering** is about giving the LLM clear instructions on how to respond. For example, a prompt can define the model's role, specify the response format, set constraints and explain how to handle questions when the answer is uncertain.

However, prompt instructions alone do not provide a search mechanism for finding relevant information across a large collection of documents.

**Retrieval-Augmented Generation (RAG)** allows the system to retrieve relevant information from an external knowledge source and provide it to the LLM before generating an answer. A typical RAG pipeline involves processing documents, splitting them into chunks, creating an index, retrieving relevant passages and generating a response using that context.

**The main difference is that** prompt engineering guides how the model responds, while RAG helps the model access relevant external information. They are not competing approaches; they can be combined to produce more useful and better-grounded answers.

# Summary

| Concept | Main approach |
|---|---|
| Hallucination | Ground answers in evidence and allow the model to admit when information is missing. |
| Poor retrieval | Inspect retrieved passages and improve document processing, search and ranking. |
| Overfitting | Improve generalization using validation, regularization and representative data. |
| Data leakage | Check data splits, preprocessing steps, duplicate records and feature availability. |
| Prompt engineering vs. RAG | Use instructions to guide responses and retrieval to provide relevant external information. |

# Assumptions and Scope

These solutions are based on a typical document-question-answering chatbot and a supervised machine-learning workflow. The actual cause of a problem should be confirmed by checking the system, its data and its evaluation results before deciding which fix to apply.

**AI assistance disclosure:** AI assistance was used to help organize this response. The final content has been reviewed for understanding before submission.
