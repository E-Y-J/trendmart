import os
import logging
import json
from typing import Optional, Any, Dict

logger = logging.getLogger(__name__)


class OllamaWrapper:
    """Simple Ollama caller with Python client and HTTP fallback."""

    def __init__(self, model: Optional[str] = None, temperature: float = 0.0):
        self.model = model or os.environ.get("OLLAMA_MODEL")
        self.temperature = float(temperature)

    def _call_ollama_client(self, prompt: str) -> Dict[str, Any]:
        try:
            import ollama
        except Exception as exc:
            raise RuntimeError("ollama python client not installed") from exc

        # synchronous client call
        resp = ollama.chat(model=self.model, messages=[
                           {"role": "user", "content": prompt}], stream=False)
        text = resp if not isinstance(resp, dict) else resp.get(
            "content") or resp.get("generated_text") or str(resp)
        return {"text": text, "raw": resp}

    def _call_ollama_http(self, prompt: str) -> Dict[str, Any]:
        import requests

        # Prefer OLLAMA_HOST used by the python client; fall back to LOCAL_LLM_URL
        base = os.environ.get("OLLAMA_HOST") or os.environ.get(
            "LOCAL_LLM_URL") or "http://localhost:11434"
        model = self.model or os.environ.get("OLLAMA_MODEL")
        if not model:
            raise RuntimeError("No Ollama model configured (OLLAMA_MODEL)")

        # Use Ollama's HTTP generate API
        url = f"{base}/api/generate"
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": float(self.temperature), "num_predict": 256}
        }
        r = requests.post(url, json=payload, timeout=30)
        r.raise_for_status()
        out = r.json()
        # Response typically contains a 'response' field with the text
        if isinstance(out, dict):
            text = out.get("response") or out.get("text") or json.dumps(out)
        else:
            text = str(out)
        return {"text": text, "raw": out}

    def generate(self, prompt: str) -> Dict[str, Any]:
        """Return generated text (tries client, then HTTP)."""
        try:
            return self._call_ollama_client(prompt)
        except Exception:
            logger.debug(
                "ollama python client unavailable, falling back to HTTP client", exc_info=True
            )

        # try HTTP
        return self._call_ollama_http(prompt)
