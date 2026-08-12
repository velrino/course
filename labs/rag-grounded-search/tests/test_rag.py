from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest


LAB = Path(__file__).resolve().parents[1]
IMPLEMENTATION = os.environ.get("RAG_SEARCH_IMPL", "solution")
MODULE_PATH = LAB / IMPLEMENTATION / "rag.py"
SPEC = importlib.util.spec_from_file_location("rag_under_test", MODULE_PATH)
assert SPEC and SPEC.loader
rag = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(rag)


class SearchTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.documents = rag.load_corpus(LAB / "fixtures" / "corpus.jsonl")
        cls.index = rag.SearchIndex(cls.documents)


class RetrievalTests(SearchTestCase):
    def test_relevant_policy_is_ranked_first(self):
        results = self.index.retrieve("Pro API request limit per minute", k=3)
        self.assertEqual(results[0]["id"], "api-rate-limits")
        self.assertGreater(results[0]["score"], results[1]["score"])

    def test_ties_are_stable_and_queries_are_repeatable(self):
        first = self.index.retrieve("plan", k=10)
        second = self.index.retrieve("plan", k=10)
        self.assertEqual(first, second)

        tied_documents = [
            {"id": "chunk-b", "title": "Shared", "source": "local://b", "text": "equal term"},
            {"id": "chunk-a", "title": "Shared", "source": "local://a", "text": "equal term"},
        ]
        tied = rag.SearchIndex(tied_documents).retrieve("equal", k=2)
        self.assertEqual([result["id"] for result in tied], ["chunk-a", "chunk-b"])

    def test_invalid_k_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "at least 1"):
            self.index.retrieve("refund", k=0)


class GroundingTests(SearchTestCase):
    def test_answer_is_extractive_and_cited(self):
        response = rag.grounded_answer(
            self.index, "How many minutes before a password reset link expires?"
        )
        self.assertEqual(response["status"], "answered")
        self.assertIn("20 minutes", response["answer"])
        self.assertIn("[security-passwords]", response["answer"])
        self.assertTrue(rag.citations_are_valid(response, self.documents))

    def test_unrelated_and_empty_queries_abstain(self):
        for query in ("Where can employees park?", ""):
            with self.subTest(query=query):
                response = rag.grounded_answer(self.index, query)
                self.assertEqual(response["status"], "abstained")
                self.assertEqual(response["citations"], [])

    def test_tampered_citation_is_invalid(self):
        response = rag.grounded_answer(self.index, "When are ticket attachments deleted?")
        response["citations"][0]["id"] = "missing-document"
        self.assertFalse(rag.citations_are_valid(response, self.documents))


class CorpusTests(unittest.TestCase):
    def test_duplicate_document_ids_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "duplicate.jsonl"
            record = {"id": "same", "title": "One", "source": "local://one", "text": "Text"}
            path.write_text(json.dumps(record) + "\n" + json.dumps(record) + "\n")
            with self.assertRaisesRegex(rag.CorpusError, "duplicate"):
                rag.load_corpus(path)

    def test_malformed_json_reports_its_line(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.jsonl"
            path.write_text('{"id":"unfinished"\n', encoding="utf-8")
            with self.assertRaisesRegex(rag.CorpusError, "line 1"):
                rag.load_corpus(path)


class EvaluationTests(SearchTestCase):
    def test_evaluation_matches_golden_file(self):
        cases = rag.load_cases(LAB / "fixtures" / "evaluation.jsonl")
        actual = rag.evaluate(self.index, cases, k=3)
        expected = json.loads((LAB / "fixtures" / "expected-evaluation.json").read_text())
        self.assertEqual(actual, expected)
        self.assertEqual(actual["metrics"]["recall_at_k"], 1.0)
        self.assertEqual(actual["metrics"]["abstention_accuracy"], 1.0)


if __name__ == "__main__":
    unittest.main()
