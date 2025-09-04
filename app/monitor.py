# app/monitor.py (safe version)

import csv, os, time

LOG_PATH = "logs/usage.csv"

# جرّبي تستوردي الأسعار؛ لو مش موجودة خليها 0
try:
    from .config import (
        PRICE_OPENAI_FAST_IN, PRICE_OPENAI_FAST_OUT,
        PRICE_OPENAI_SMART_IN, PRICE_OPENAI_SMART_OUT,
        PRICE_OPENAI_EMBED,
        PRICE_ANTHROPIC_FAST_IN, PRICE_ANTHROPIC_FAST_OUT,
        PRICE_ANTHROPIC_SMART_IN, PRICE_ANTHROPIC_SMART_OUT,
    )
except Exception:
    PRICE_OPENAI_FAST_IN  = 0.0
    PRICE_OPENAI_FAST_OUT = 0.0
    PRICE_OPENAI_SMART_IN  = 0.0
    PRICE_OPENAI_SMART_OUT = 0.0
    PRICE_OPENAI_EMBED     = 0.0
    PRICE_ANTHROPIC_FAST_IN  = 0.0
    PRICE_ANTHROPIC_FAST_OUT = 0.0
    PRICE_ANTHROPIC_SMART_IN  = 0.0
    PRICE_ANTHROPIC_SMART_OUT = 0.0

def _ensure_headers():
    if not os.path.exists(LOG_PATH):
        os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
        with open(LOG_PATH, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(
                ["ts","provider","model","input_tokens","output_tokens","cost_usd","note"]
            )

def _price(provider: str, model: str, input_tokens: int, output_tokens: int) -> float:
    # HF مفيش تسعير دقيق من الواجهة → 0
    if provider in ("hf", "huggingface"):
        return 0.0
    # تقديرات OpenAI/Anthropic إن وُجدت
    cost = 0.0
    if provider == "openai":
        # اختيار بدائي: اعتبر أي موديل غير "mini/fast" = smart
        if "mini" in (model or "").lower() or "fast" in (model or "").lower():
            cost += (input_tokens/1000.0)*PRICE_OPENAI_FAST_IN + (output_tokens/1000.0)*PRICE_OPENAI_FAST_OUT
        else:
            cost += (input_tokens/1000.0)*PRICE_OPENAI_SMART_IN + (output_tokens/1000.0)*PRICE_OPENAI_SMART_OUT
    elif provider == "openai-embed":
        cost += (input_tokens/1000.0)*PRICE_OPENAI_EMBED
    elif provider == "anthropic":
        if "haiku" in (model or "").lower():
            cost += (input_tokens/1000.0)*PRICE_ANTHROPIC_FAST_IN + (output_tokens/1000.0)*PRICE_ANTHROPIC_FAST_OUT
        else:
            cost += (input_tokens/1000.0)*PRICE_ANTHROPIC_SMART_IN + (output_tokens/1000.0)*PRICE_ANTHROPIC_SMART_OUT
    return round(cost, 6)

def log_usage(provider: str, model: str, input_tokens: int = 0, output_tokens: int = 0, note: str = ""):
    _ensure_headers()
    cost = _price(provider, model, input_tokens, output_tokens)
    with open(LOG_PATH, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([int(time.time()), provider, model, input_tokens, output_tokens, cost, note])
    return cost