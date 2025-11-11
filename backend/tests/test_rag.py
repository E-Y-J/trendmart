import pytest

from ai_recom_system import rag_service


def fake_load_index():
    class FakeStore:
        def search_similar_products(self, query, top_k=3):
            # return a few fake product dicts
            return [({"id": 1, "name": "Test Product A", "description": "A test product"}, 0.9), ({"id": 2, "name": "Test Product B", "description": "Another test"}, 0.8)]

    return FakeStore()


def fake_ollama_caller(messages, **kwargs):
    # Return JSON string in text to exercise parser
    return {"text": '{"answer": "This is a fake answer.", "source_ids": [1,2]}', "raw": {"fake": True}}


def test_answer_question_monkeypatched(monkeypatch):
    # Monkeypatch the simple index loader and the ollama caller factory
    monkeypatch.setattr(rag_service, "load_simple_index", fake_load_index)
    # Replace the factory to return our fake caller
    monkeypatch.setattr(rag_service, "_ollama_llm_caller_factory",
                        lambda model=None, temperature=0.0: fake_ollama_caller)

    res = rag_service.answer_question("What is the test?", k=2)
    assert res["answer"] == "This is a fake answer."
    assert res["source_ids"] == [1, 2]

    print(f'{rag_service.__name__} test_answer_question_monkeypatched passed: {res}')
