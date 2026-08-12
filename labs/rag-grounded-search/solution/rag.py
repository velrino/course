#!/usr/bin/env python3
"""Deterministic retrieval, grounded extraction, and evaluation."""

from __future__ import annotations

import argparse
from collections import Counter
import json
import math
from pathlib import Path
import re
from typing import Any, Iterable


TOKEN = re.compile(r"[a-z0-9]+")
SENTENCE = re.compile(r"(?<=[.!?])\s+")
STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "before", "can", "do",
    "does", "for", "from", "how", "i", "in", "is", "it", "many", "of",
    "on", "or", "the", "to", "what", "when", "where", "which", "with",
}
ABSTENTION = "I do not have enough evidence in the provided knowledge base."


class CorpusError(ValueError):
    """Raised when a corpus or evaluation fixture breaks its contract."""


def tokenize(text: str) -> list[str]:
    return TOKEN.findall(text.lower())


def query_terms(text: str) -> list[str]:
    return [token for token in tokenize(text) if token not in STOP_WORDS]


def _read_jsonl(path: Path) -> Iterable[tuple[int, Any]]:
    if path.is_symlink() or not path.is_file():
        raise CorpusError(f"expected a regular JSONL file: {path}")
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            yield line_number, json.loads(line)
        except json.JSONDecodeError as exc:
            raise CorpusError(f"invalid JSON on line {line_number}") from exc


def load_corpus(path: Path) -> list[dict[str, str]]:
    documents: list[dict[str, str]] = []
    seen: set[str] = set()
    for line_number, raw in _read_jsonl(path):
        if not isinstance(raw, dict):
            raise CorpusError(f"corpus line {line_number} must be an object")
        document: dict[str, str] = {}
        for field in ("id", "title", "source", "text"):
            value = raw.get(field)
            if not isinstance(value, str) or not value.strip():
                raise CorpusError(f"corpus line {line_number} has an invalid {field}")
            document[field] = value.strip()
        if document["id"] in seen:
            raise CorpusError(f"duplicate document ID: {document['id']}")
        seen.add(document["id"])
        documents.append(document)
    if not documents:
        raise CorpusError("corpus must contain at least one document")
    return documents


def load_cases(path: Path) -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    seen: set[str] = set()
    for line_number, raw in _read_jsonl(path):
        if not isinstance(raw, dict):
            raise CorpusError(f"evaluation line {line_number} must be an object")
        case_id = raw.get("id")
        query = raw.get("query")
        answerable = raw.get("answerable")
        relevant = raw.get("relevant_ids")
        if not isinstance(case_id, str) or not case_id or case_id in seen:
            raise CorpusError(f"evaluation line {line_number} has an invalid ID")
        if not isinstance(query, str) or not query.strip():
            raise CorpusError(f"evaluation line {line_number} has an invalid query")
        if not isinstance(answerable, bool) or not isinstance(relevant, list):
            raise CorpusError(f"evaluation line {line_number} has invalid labels")
        if any(not isinstance(item, str) for item in relevant):
            raise CorpusError(f"evaluation line {line_number} has invalid relevant IDs")
        if answerable != bool(relevant):
            raise CorpusError(f"evaluation line {line_number} has inconsistent labels")
        seen.add(case_id)
        cases.append(
            {"id": case_id, "query": query.strip(), "answerable": answerable,
             "relevant_ids": relevant}
        )
    if not cases:
        raise CorpusError("evaluation set must contain at least one case")
    return cases


class SearchIndex:
    """A compact BM25-style index with deterministic ordering."""

    def __init__(self, documents: list[dict[str, str]]) -> None:
        if not documents:
            raise ValueError("documents must not be empty")
        self.documents = [dict(document) for document in documents]
        self.term_counts: list[Counter[str]] = []
        self.lengths: list[int] = []
        document_frequency: Counter[str] = Counter()
        for document in self.documents:
            terms = query_terms(document["title"] + " " + document["text"])
            counts = Counter(terms)
            self.term_counts.append(counts)
            self.lengths.append(sum(counts.values()))
            document_frequency.update(counts.keys())
        self.document_frequency = document_frequency
        self.average_length = sum(self.lengths) / len(self.lengths)

    def retrieve(self, query: str, k: int = 3) -> list[dict[str, Any]]:
        if k < 1:
            raise ValueError("k must be at least 1")
        terms = query_terms(query)
        if not terms:
            return []
        query_counts = Counter(terms)
        total_documents = len(self.documents)
        ranked: list[dict[str, Any]] = []
        k1 = 1.5
        b = 0.75
        for document, counts, length in zip(self.documents, self.term_counts, self.lengths):
            score = 0.0
            for term, query_frequency in query_counts.items():
                frequency = counts.get(term, 0)
                if not frequency:
                    continue
                df = self.document_frequency[term]
                inverse_frequency = math.log(1 + (total_documents - df + 0.5) / (df + 0.5))
                denominator = frequency + k1 * (1 - b + b * length / self.average_length)
                score += inverse_frequency * (frequency * (k1 + 1) / denominator) * query_frequency
            if score > 0:
                ranked.append({**document, "score": round(score, 6)})
        ranked.sort(key=lambda result: (-result["score"], result["id"]))
        return ranked[:k]


def _best_sentence(document: dict[str, Any], terms: set[str]) -> str:
    candidates = [part.strip() for part in SENTENCE.split(document["text"]) if part.strip()]
    scored = []
    for position, sentence in enumerate(candidates):
        overlap = len(terms.intersection(query_terms(sentence)))
        scored.append((overlap, -position, sentence))
    return max(scored)[2]


def grounded_answer(
    index: SearchIndex,
    query: str,
    *,
    min_score: float = 0.75,
    min_coverage: float = 0.34,
) -> dict[str, Any]:
    terms = set(query_terms(query))
    results = index.retrieve(query, k=3)
    if not terms or not results:
        return {"query": query, "status": "abstained", "answer": ABSTENTION,
                "citations": [], "evidence": []}

    best = results[0]
    document_terms = set(query_terms(best["title"] + " " + best["text"]))
    matched_terms = sorted(terms.intersection(document_terms))
    coverage = len(matched_terms) / len(terms)
    if best["score"] < min_score or coverage < min_coverage:
        return {"query": query, "status": "abstained", "answer": ABSTENTION,
                "citations": [], "evidence": []}

    sentence = _best_sentence(best, terms)
    citation_id = best["id"]
    return {
        "query": query,
        "status": "answered",
        "answer": f"{sentence} [{citation_id}]",
        "citations": [
            {"id": citation_id, "title": best["title"], "source": best["source"]}
        ],
        "evidence": [
            {"id": citation_id, "score": best["score"],
             "coverage": round(coverage, 6), "matched_terms": matched_terms}
        ],
    }


def citations_are_valid(response: dict[str, Any], documents: list[dict[str, str]]) -> bool:
    if response.get("status") == "abstained":
        return response.get("citations") == [] and response.get("answer") == ABSTENTION
    if response.get("status") != "answered":
        return False
    known_documents = {document["id"]: document for document in documents}
    citations = response.get("citations")
    answer = response.get("answer")
    if not isinstance(citations, list) or not citations or not isinstance(answer, str):
        return False
    for citation in citations:
        if not isinstance(citation, dict) or citation.get("id") not in known_documents:
            return False
        document = known_documents[citation["id"]]
        if citation.get("title") != document["title"] or citation.get("source") != document["source"]:
            return False
        if f"[{citation['id']}]" not in answer:
            return False
    return True


def evaluate(
    index: SearchIndex,
    cases: list[dict[str, Any]],
    *,
    k: int = 3,
) -> dict[str, Any]:
    answerable_count = sum(case["answerable"] for case in cases)
    retrieval_hits = 0
    reciprocal_rank_total = 0.0
    abstention_correct = 0
    answered_responses = 0
    valid_citations = 0
    details: list[dict[str, Any]] = []

    for case in cases:
        results = index.retrieve(case["query"], k=k)
        top_ids = [result["id"] for result in results]
        response = grounded_answer(index, case["query"])
        predicted_answerable = response["status"] == "answered"
        abstention_correct += predicted_answerable == case["answerable"]
        if predicted_answerable:
            answered_responses += 1
            valid_citations += citations_are_valid(response, index.documents)

        retrieval_hit: bool | None = None
        reciprocal_rank = 0.0
        if case["answerable"]:
            relevant = set(case["relevant_ids"])
            retrieval_hit = any(identifier in relevant for identifier in top_ids)
            retrieval_hits += retrieval_hit
            for rank, identifier in enumerate(top_ids, 1):
                if identifier in relevant:
                    reciprocal_rank = 1.0 / rank
                    break
            reciprocal_rank_total += reciprocal_rank

        details.append(
            {
                "id": case["id"],
                "expected_answerable": case["answerable"],
                "status": response["status"],
                "top_ids": top_ids,
                "retrieval_hit": retrieval_hit,
                "reciprocal_rank": round(reciprocal_rank, 6),
            }
        )

    return {
        "schema_version": 1,
        "k": k,
        "metrics": {
            "case_count": len(cases),
            "answerable_case_count": answerable_count,
            "recall_at_k": round(retrieval_hits / answerable_count, 6),
            "mean_reciprocal_rank": round(reciprocal_rank_total / answerable_count, 6),
            "abstention_accuracy": round(abstention_correct / len(cases), 6),
            "citation_validity": round(valid_citations / answered_responses, 6)
            if answered_responses else 1.0,
        },
        "cases": details,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    search = subparsers.add_parser("search")
    search.add_argument("--corpus", type=Path, required=True)
    search.add_argument("--query", required=True)
    evaluation = subparsers.add_parser("evaluate")
    evaluation.add_argument("--corpus", type=Path, required=True)
    evaluation.add_argument("--cases", type=Path, required=True)
    evaluation.add_argument("--k", type=int, default=3)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    documents = load_corpus(args.corpus)
    index = SearchIndex(documents)
    if args.command == "search":
        output = grounded_answer(index, args.query)
    else:
        output = evaluate(index, load_cases(args.cases), k=args.k)
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
