"""LangChain-compatible Ollama LLM wrapper.

This wrapper prefers the official `ollama` Python client when available and
falls back to a simple HTTP call against `LOCAL_LLM_URL` when the client is
not installed or unavailable. It exposes a minimal contract that our RAG
pipeline will use:

- generate(messages: List[Dict[str,str]], max_tokens: int, temperature: float) -> {"text": str, "raw": Any}
- call(prompt: str, **kwargs) -> same as generate (convenience)

The wrapper intentionally keeps dependencies lazy so importing the module
doesn't force heavy packages to be present.
"""
from typing import List, Dict, Any, Optional
import os
import logging

logger = logging.getLogger(__name__)


class OllamaLLM:
    def __init__(self, model: Optional[str] = None, temperature: float = 0.0):
        self.model = model or os.environ.get("OLLAMA_MODEL")
        self.temperature = float(temperature)
        self._have_client = None

    def _have_ollama_client(self) -> bool:
        if self._have_client is None:
            try:
                import ollama  # type: ignore

                self._have_client = True
            except Exception:
                self._have_client = False
        return self._have_client

    def _call_client(self, messages: List[Dict[str, str]], max_tokens: int = 256, temperature: float = 0.0) -> Dict[str, Any]:
        import ollama  # type: ignore

        # ollama.chat expects messages like [{"role":"user","content":"..."}]
        resp = ollama.chat(model=self.model, messages=messages, stream=False)
        # resp may be a dict or a string depending on client; normalize
        if isinstance(resp, dict):
            text = resp.get("content") or resp.get(
                "generated_text") or str(resp)
        else:
            text = str(resp)
        return {"text": text, "raw": resp}

    def _call_http(self, messages: List[Dict[str, str]], max_tokens: int = 256, temperature: float = 0.0, timeout: int = 30) -> Dict[str, Any]:
        import requests

        base = os.environ.get("LOCAL_LLM_URL", "http://localhost:8080")
        model = self.model or os.environ.get("OLLAMA_MODEL")
        if not model:
            raise RuntimeError("OLLAMA_MODEL not configured")

        url = f"{base}/models/{model}:generate"
        # Flatten messages into a single input for simple instruction-following models
        prompt = "\n\n".join(
            [f"{m.get('role').upper()}: {m.get('content')}" for m in messages])
        payload = {"inputs": prompt, "parameters": {
            "temperature": float(temperature), "max_new_tokens": int(max_tokens)}}
        r = requests.post(url, json=payload, timeout=timeout)
        r.raise_for_status()
        out = r.json()
        # normalize typical TGI/ollama-like response shapes
        if isinstance(out, dict):
            if "outputs" in out and isinstance(out["outputs"], list) and out["outputs"]:
                text = out["outputs"][0].get(
                    "generated_text") or out["outputs"][0].get("text", "")
            else:
                text = out.get("generated_text") or out.get("text") or str(out)
        else:
            text = str(out)
        return {"text": text, "raw": out}

    def generate(self, messages: List[Dict[str, str]], max_tokens: int = 256, temperature: Optional[float] = None, timeout: int = 30) -> Dict[str, Any]:
        """Generate text given a list of messages.

        messages: list of dicts with 'role' and 'content' keys.
        Returns: {'text': str, 'raw': Any}
        """
        temperature = self.temperature if temperature is None else float(
            temperature)
        try:
            if self._have_ollama_client():
                return self._call_client(messages, max_tokens=max_tokens, temperature=temperature)
        except Exception:
            logger.debug(
                "Ollama client call failed; falling back to HTTP", exc_info=True)

        return self._call_http(messages, max_tokens=max_tokens, temperature=temperature, timeout=timeout)

    def call(self, prompt: str, max_tokens: int = 256, temperature: Optional[float] = None, timeout: int = 30) -> Dict[str, Any]:
        """Convenience call that wraps a single-user prompt into messages and calls generate."""
        messages = [{"role": "user", "content": prompt}]
        return self.generate(messages, max_tokens=max_tokens, temperature=temperature, timeout=timeout)
