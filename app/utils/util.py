from langchain_core.documents import Document
import numpy as np
import tiktoken
import re
from contextvars import ContextVar

def format_docs(docs: list[Document]) -> str:
    """Format documents into a single context string.

    Args:
        docs: List of Document objects

    Returns:
        Formatted context string
    """
    return "\n".join(doc.page_content for doc in docs)


enc = tiktoken.get_encoding("cl100k_base")

def token_len(text: str) -> int:
    tokens = enc.encode(text)
    return len(tokens)

def chunk_quality_report(docs):
    sizes = np.array([token_len(d.page_content) for d in docs])

    report = {
        "count": len(sizes),
        "mean": round(float(np.mean(sizes)), 1),
        "median": int(np.median(sizes)),
        "std": round(float(np.std(sizes)), 1),
        "cv_percent": round(float(np.std(sizes) / np.mean(sizes) * 100), 1),
        "min": int(np.min(sizes)),
        "max": int(np.max(sizes)),
        "p90": int(np.percentile(sizes, 90)),
        "p95": int(np.percentile(sizes, 95)),
    }

    issues = []

    if report["min"] < 120:
        issues.append("MICRO_CHUNKS_PRESENT")

    if report["max"] > 600:
        issues.append("JUMBO_CHUNKS_PRESENT")

    if report["cv_percent"] > 30:
        issues.append("CV_TOO_HIGH (HARD FAIL)")
    elif report["cv_percent"] > 20:
        issues.append("CV_TOO_HIGH (SOFT FAIL)")

    if report["p95"] > report["mean"] * 1.4:
        issues.append("LONG_TAIL_RISK")

    return report, issues

def reciprocal_rank_fusion(results_dict, weights, k=60, top_n=5):
    scores = {}
    doc_lookup = {}

    for name, docs in results_dict.items():
        weight = weights.get(name, 1.0)
        for rank, doc in enumerate(docs or []):
            doc_id = doc.metadata.get("id")
            if not doc_id:
                source = doc.metadata.get("source")
                doc_id = source or f"{name}:{rank}:{abs(hash(doc.page_content))}"
                doc.metadata["id"] = doc_id

            doc_lookup[doc_id] = doc
            rrf_score = weight * (1.0 / (k + rank))
            scores[doc_id] = scores.get(doc_id, 0.0) + rrf_score

    ranked_ids = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [doc_lookup[doc_id] for doc_id, _ in ranked_ids[:top_n]]


def normalize(q: str) -> str:
    q = q.lower().strip()
    q = re.sub(r"[^\w\s]", "", q)
    q = " ".join(q.split())
    return q


CURRENT_REQUEST_USER: ContextVar[dict] = ContextVar("current_user")

def set_current_user(user_info: dict):
    CURRENT_REQUEST_USER.set(user_info)

def get_current_user() -> dict:
    return CURRENT_REQUEST_USER.get({})