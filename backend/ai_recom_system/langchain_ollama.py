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

        base = os.environ.get("LOCAL_LLM_URL") or "http://localhost:8080"
        model = self.model or os.environ.get("OLLAMA_MODEL")
        if not model:
            raise RuntimeError("No Ollama model configured (OLLAMA_MODEL)")

        url = f"{base}/models/{model}:generate"
        payload = {"inputs": prompt, "parameters": {
            "temperature": float(self.temperature), "max_new_tokens": 256}}
        r = requests.post(url, json=payload, timeout=30)
        r.raise_for_status()
        out = r.json()
        # pick best text field from TGI-like responses
        if isinstance(out, dict):
            if "outputs" in out and isinstance(out["outputs"], list) and out["outputs"]:
                text = out["outputs"][0].get(
                    "generated_text") or out["outputs"][0].get("text", "")
            else:
                text = out.get("generated_text") or out.get(
                    "text") or json.dumps(out)
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
