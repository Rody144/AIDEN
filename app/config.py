import os
from dotenv import load_dotenv
load_dotenv()

# ... الموجود مسبقًا ...

# Hugging Face
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

# أسماء نماذج افتراضية — تقدري تغيّريها لاحقًا
HF_CHAT_MODEL = os.getenv("HF_CHAT_MODEL", "meta-llama/Meta-Llama-3-8B-Instruct")
HF_EMBED_MODEL = os.getenv("HF_EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
# Dummy prices since we are not using OpenAI/Anthropic now
PRICE_OPENAI_FAST_IN = 0.0
PRICE_OPENAI_FAST_OUT = 0.0
PRICE_OPENAI_SMART_IN = 0.0
PRICE_OPENAI_SMART_OUT = 0.0
PRICE_ANTHROPIC_SMART_IN = 0.0
PRICE_ANTHROPIC_SMART_OUT = 0.0
# Dummy fallback for OpenAI (not used with HuggingFace)
OPENAI_EMBED_MODEL = None