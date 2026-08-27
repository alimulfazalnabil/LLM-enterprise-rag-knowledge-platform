# Evaluation Methodology

Use a versioned golden dataset with expected answers and relevant chunks. Compare vector-only, BM25-only, hybrid, hybrid plus reranking, and hybrid plus compression. Report Precision@K, Recall@K, MRR, faithfulness, answer correctness, answer relevance, citation accuracy, latency, and token usage. LLM judges are secondary to ground truth and manual review. Empty or unexecuted reports must not contain invented numbers.
