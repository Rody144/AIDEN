import os
from dotenv import load_dotenv
load_dotenv()

# ... الموجود مسبقًا ...

# Hugging Face
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

# أسماء نماذج افتراضية — تقدري تغيّريها لاحقًا
HF_CHAT_MODEL = os.getenv("HF_CHAT_MODEL", "meta-llama/Meta-Llama-3-8B-Instruct")
HF_EMBED_MODEL = os.getenv("HF_EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")