from typing import List, Dict, Tuple
import numpy as np

# موجودين عندك بالفعل:
# from openai import OpenAI
# import anthropic

from huggingface_hub import InferenceClient
from .config import (
    # … مفاتيح OpenAI/Anthropic لو بتستخدميهم …
    HUGGINGFACE_TOKEN, HF_CHAT_MODEL, HF_EMBED_MODEL
)

class HuggingFaceProvider:
    """
    شات + Embeddings باستخدام Inference API.
    - الشات: بننسّق رسائل chat إلى prompt واحد لـ instruct models.
    - embeddings: باستخدام task=feature-extraction (جملة لكل سطر).
    """
    def _init_(self, token: str = None, chat_model: str = None, embed_model: str = None):
        self.token = token or HUGGINGFACE_TOKEN
        if not self.token:
            raise RuntimeError("HUGGINGFACE_TOKEN غير موجود في البيئة (.env)")
        self.chat_model = chat_model or HF_CHAT_MODEL
        self.embed_model = embed_model or HF_EMBED_MODEL
        self.chat_client = InferenceClient(model=self.chat_model, token=self.token)
        self.embed_client = InferenceClient(model=self.embed_model, token=self.token)

    def _format_chat(self, messages: List[Dict[str, str]]) -> str:
        """حوّل رسائل OpenAI-style إلى نص واحد لنموذج instruct."""
        system = ""
        user_blocks = []
        for m in messages:
            role, content = m.get("role"), m.get("content", "")
            if role == "system":
                system += content + "\n"
            elif role == "user":
                user_blocks.append(f"User: {content}")
            elif role == "assistant":
                user_blocks.append(f"Assistant: {content}")
        prompt = ""
        if system.strip():
            prompt += f"[System]\n{system.strip()}\n\n"
        prompt += "\n".join(user_blocks) + "\nAssistant:"
        return prompt

    def chat(self, messages: List[Dict[str, str]], temperature: float = 0.2, max_new_tokens: int = 512):
        prompt = self._format_chat(messages)
        # text-generation (stream=False)
        text = self.chat_client.text_generation(
            prompt,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            do_sample=temperature > 0,
            # stop sequences اختيارية حسب النموذج
        )
        # Inference API ما بيرجعش usage tokens بدقة؛ هنرجع 0
        usage = {"input_tokens": 0, "output_tokens": 0}
        return text.strip(), usage, self.chat_model

    def embed(self, texts: List[str]) -> np.ndarray:
        # feature-extraction بيرجع قائمة أبعاد لكل نص
        # هنضمن إن الناتج np.array [N, D]
        vecs = []
        for t in texts:
            feat = self.embed_client.feature_extraction(t)
            # بعض النماذج ترجع [seq_len, D]؛ ناخد متوسط المحاور
            arr = np.array(feat, dtype="float32")
            if arr.ndim == 2:
                arr = arr.mean(axis=0)
            vecs.append(arr)
        # محاذاة الأبعاد: (لو اختلفت الأبعاد — غير متوقع — هنرمي خطأ واضح)
        dims = {v.shape for v in vecs}
        if len(dims) != 1:
            raise RuntimeError(f"عدم تطابق أبعاد embeddings: {dims}")
        return np.vstack(vecs)