import os
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


class OllamaAdapter:
    """
    Unified adapter for Ollama.
    Contract:
      - chat(messages: List[{'role','content'}], model?, temperature?, max_tokens?) -> {'text': str, 'raw': Any}
      - call(prompt: str, ...) -> same as chat but wraps into a single user message
    Env used:
      - OLLAMA_MODEL (fallback model)
      - OLLAMA_HOST or LOCAL_LLM_URL (base URL for HTTP)
    """

    def __init__(self, model: Optional[str] = None, temperature: float = 0.0):
        self.model = model or os.environ.get("OLLAMA_MODEL")
        self.temperature = float(temperature)

    def _have_client(self) -> bool:
        '''Check if Ollama python client is available.'''
        try:
            import ollama  # type: ignore
            return True
        except Exception:
            return False

    def _client_chat(self, messages: List[Dict[str, str]], model: str, max_tokens: int) -> Dict[str, Any]:
        '''Chat via Ollama python client.
         messages: List of {"role": "user|assistant|system", "content": str}
         model: Model name
         max_tokens: Max tokens to generate
        '''
        import ollama
        # Ollama client does not support temperature or max_tokens directly yet
        resp = ollama.chat(model=model, messages=messages, stream=False)
        # Normalize likely shapes
        if isinstance(resp, dict):
            msg = resp.get("message") or {}
            text = msg.get("content") or resp.get(
                "content") or resp.get("response") or str(resp)
        else:
            text = str(resp)
        return {"text": text, "raw": resp}

    def _http_chat(self, messages: List[Dict[str, str]], model: str, max_tokens: int, timeout: int = 30) -> Dict[str, Any]:
        '''Chat via Ollama HTTP API.
         messages: List of {"role": "user|assistant|system", "content": str}
         model: Model name
         max_tokens: Max tokens to generate
         timeout: HTTP timeout in seconds
        '''
        import requests
        base = os.environ.get("OLLAMA_HOST") or os.environ.get(
            "LOCAL_LLM_URL") or "http://localhost:11434"
        url = f"{base}/api/chat"
        payload = {
            "model": model,
            "messages": messages,
            "stream": False,
            "options": {"temperature": float(self.temperature), "num_predict": int(max_tokens)},
        }
        r = requests.post(url, json=payload, timeout=timeout)
        r.raise_for_status()
        out = r.json()
        if isinstance(out, dict):
            msg = out.get("message") or {}
            text = msg.get("content") or out.get("response") or str(out)
        else:
            text = str(out)
        return {"text": text, "raw": out}

    def chat(self, messages: List[Dict[str, str]], *, model: Optional[str] = None, temperature: Optional[float] = None, max_tokens: int = 256, timeout: int = 30) -> Dict[str, Any]:
        '''Chat with the model.
        messages: List of {"role": "user|assistant|system", "content": str}
        model: Optional model override
        temperature: Optional temperature override
        max_tokens: Max tokens to generate
        timeout: HTTP timeout in seconds
        '''
        model = model or self.model or os.environ.get("OLLAMA_MODEL")
        if not model:
            raise RuntimeError("OLLAMA_MODEL not configured")
        if temperature is not None:
            self.temperature = float(temperature)
        try:
            if self._have_client():
                return self._client_chat(messages, model=model, max_tokens=max_tokens)
        except Exception:
            logger.debug(
                "Ollama python client failed, falling back to HTTP", exc_info=True)
        return self._http_chat(messages, model=model, max_tokens=max_tokens, timeout=timeout)

    def call(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Single-prompt convenience."""
        return self.chat([{"role": "user", "content": prompt}], **kwargs)
