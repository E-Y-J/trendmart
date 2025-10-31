import json
import logging
import os
from typing import List, Dict, Any, Optional

# Note: I lazily import huggingface_hub inside call_llm so the module can be
# imported without the dependency when using Ollama-only flows.

logger = logging.getLogger(__name__)

# System prompt: strict instructions for the LLM to obey content/citation rules.
SYSTEM_PROMPT = (
    "You are a product recommendation assistant. Answer concisely and only using the provided "
    "context. If the answer is not directly supported by the context, say: "
    "\"I don't know based on the provided information.\" Do NOT hallucinate. "
    "When returning sources, return only product ids from the context in a top-level JSON field "
    "`source_ids`."
)

# Configurable limits
MAX_PROMPT_LENGTH = 2000  # characters
MAX_CONTEXT_ITEMS = 10
MAX_CONTEXT_TEXT = 4000  # characters (total context serialized)


class LLMError(Exception):
    pass


def _sanitize_prompt(prompt: str) -> str:
    if not prompt or not prompt.strip():
        raise ValueError("prompt must be a non-empty string")
    p = prompt.strip()
    if len(p) > MAX_PROMPT_LENGTH:
        p = p[:MAX_PROMPT_LENGTH]
    return p


def _prepare_context(context: Optional[List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
    """
    Normalize and truncate context to a safe size. Each item is expected to be a product dict
    that includes at least an 'id' and 'name' and optional 'description'.
    """
    if not context:
        return []
    # Keep only the first MAX_CONTEXT_ITEMS items
    items = context[:MAX_CONTEXT_ITEMS]
    # Ensure each item is simple JSON-serializable and trim large text fields
    trimmed = []
    total_len = 0
    for it in items:
        obj = {
            "id": it.get("id"),
            "name": (it.get("name") or "")[:200],
            "description": (it.get("description") or "")[:1000],
            "price": it.get("price"),
            "tags": it.get("tags") or []
        }
        total_len += len(json.dumps(obj))
        trimmed.append(obj)
        if total_len > MAX_CONTEXT_TEXT:
            break
    return trimmed


def _build_system_message() -> Dict[str, str]:
    return {"role": "system", "content": SYSTEM_PROMPT}


def _build_user_message(prompt: str, context: List[Dict[str, Any]]) -> Dict[str, str]:
    # Pass the context as a JSON string to the LLM so it can reference product ids and text.
    context_payload = json.dumps({"products": context}, ensure_ascii=False)
    content = f"Context: {context_payload}\n\nQuestion: {prompt}"
    return {"role": "user", "content": content}


def call_llm(messages: List[Dict[str, str]], *, model: Optional[str] = None, timeout: int = 30, temperature: float = 0.0) -> Dict[str, Any]:
    """
    Calls the Hugging Face Inference API using huggingface_hub.InferenceClient.

    Environment variables used:
      - HUGGINGFACE_API_TOKEN (or HF_API_TOKEN) : required API token
      - HUGGINGFACE_MODEL : optional default model id if `model` is None

    Returns a dict with at least a 'text' key and a 'raw' key containing the full HF response.
    """
    token = os.environ.get(
        "HUGGINGFACE_API_TOKEN") or os.environ.get("HF_API_TOKEN")
    if not token:
        raise LLMError(
            "Hugging Face API token not set. Set HUGGINGFACE_API_TOKEN or HF_API_TOKEN.")

    model = model or os.environ.get(
        "HUGGINGFACE_MODEL") or "gpt2"

    # Join messages into a single prompt string that is predictable for the HF model
    prompt = "\n\n".join(
        [f"{m.get('role', '').upper()}: {m.get('content', '')}" for m in messages])

    try:
        from huggingface_hub import InferenceClient  # type: ignore
    except Exception as imp_err:
        raise LLMError(
            "huggingface_hub is not installed in this environment. Install it or use the Ollama-based llm_caller.") from imp_err

    client = InferenceClient(token=token)
    try:
        # text_generation returns either list/dict depending on model; pass basic generation params
        result = client.text_generation(
            model=model, inputs=prompt, max_new_tokens=512, temperature=temperature)
    except Exception as exc:
        logger.exception("Hugging Face LLM call failed")
        raise LLMError(str(exc))

    # Normalize result to a text string
    text = ""
    try:
        if isinstance(result, list) and result:
            # some models return a list of outputs
            first = result[0]
            text = first.get("generated_text") or first.get(
                "text") or str(first)
        elif isinstance(result, dict):
            text = result.get("generated_text") or result.get(
                "text") or json.dumps(result)
        else:
            text = str(result)
    except Exception:
        text = str(result)

    return {"text": text, "raw": result}


def generate_answer(prompt: str,
                    context: Optional[List[Dict[str, Any]]] = None,
                    k: int = 5,
                    temperature: float = 0.0,
                    model: Optional[str] = None,
                    llm_caller=call_llm) -> Dict[str, Any]:
    """
    Generate an answer using the LLM.

    Args:
        prompt: user question string
        context: list of product dicts (product_to_dict outputs)
        k: number of retrieved items (not used directly here but kept for API compatibility)
        temperature: sampling temperature
        model: optional model id to pass to the LLM adapter (Hugging Face model id)
        llm_caller: injectable function that accepts messages list and returns a dict with 'text' key.

    Returns:
        dict: { "answer": str, "source_ids": [ids], "raw": <llm raw response> }
    """
    prompt = _sanitize_prompt(prompt)
    ctx = _prepare_context(context)

    messages = [
        _build_system_message(),
        _build_user_message(prompt, ctx)
    ]

    try:
        resp = llm_caller(messages=messages, model=model,
                          timeout=30, temperature=temperature)
    except Exception as exc:
        logger.exception("LLM call failed")
        # Fail-closed: return a safe fallback
        return {"answer": "I'm unable to answer that right now.", "source_ids": [], "raw": {"error": str(exc)}}

    # Expect resp to have 'text' with either plain text or JSON.
    raw_text = resp.get("text") if isinstance(resp, dict) else str(resp)
    answer = None
    source_ids: List[int] = []

    # Try to parse JSON first (preferred contract: assistant returns JSON with answer and source_ids).
    try:
        parsed = json.loads(raw_text)
        if isinstance(parsed, dict):
            answer = parsed.get("answer") or parsed.get("text") or ""
            sids = parsed.get("source_ids", [])
            # Normalize source ids to ints
            source_ids = [int(x) for x in sids if x is not None]
    except Exception:
        # Fallback: treat raw_text as plain text and attempt to extract ids heuristically
        answer = raw_text.strip()
        # simple heuristic: look for patterns like [1,2,3] in the text
        try:
            import re
            m = re.search(r"\[([0-9,\s]+)\]", raw_text)
            if m:
                ids = [int(x.strip())
                       for x in m.group(1).split(",") if x.strip().isdigit()]
                source_ids = ids
        except Exception:
            source_ids = []

    return {"answer": answer or "", "source_ids": source_ids, "raw": resp}
