import csv, os, time
from .config import (
    PRICE_OPENAI_FAST_IN, PRICE_OPENAI_FAST_OUT,
    PRICE_OPENAI_SMART_IN, PRICE_OPENAI_SMART_OUT,
    PRICE_OPENAI_EMBED,
    PRICE_ANTHROPIC_FAST_IN, PRICE_ANTHROPIC_FAST_OUT,
    PRICE_ANTHROPIC_SMART_IN, PRICE_ANTHROPIC_SMART_OUT,
    OPENAI_FAST_MODEL, OPENAI_SMART_MODEL
)
LOG_PATH = "logs/usage.csv"

def _ensure_headers():
    if not os.path.exists(LOG_PATH):
        os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
        with open(LOG_PATH, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(["ts","provider","model","input_tokens","output_tokens","cost_usd","note"])

def _price(provider: str, model: str, input_tokens: int, output_tokens: int) -> float:
    cost = 0.0
    if provider == "openai":
        if model == OPENAI_FAST_MODEL:
            cost += (input_tokens/1000)*PRICE_OPENAI_FAST_IN + (output_tokens/1000)*PRICE_OPENAI_FAST_OUT
        else:
            cost += (input_tokens/1000)*PRICE_OPENAI_SMART_IN + (output_tokens/1000)*PRICE_OPENAI_SMART_OUT
    elif provider == "openai-embed":
        cost += (input_tokens/1000)*PRICE_OPENAI_EMBED
    elif provider == "anthropic":
        if "haiku" in model.lower():
            cost += (input_tokens/1000)*PRICE_ANTHROPIC_FAST_IN + (output_tokens/1000)*PRICE_ANTHROPIC_FAST_OUT
        else:
            cost += (input_tokens/1000)*PRICE_ANTHROPIC_SMART_IN + (output_tokens/1000)*PRICE_ANTHROPIC_SMART_OUT
    return round(cost, 6)

def log_usage(provider: str, model: str, input_tokens: int, output_tokens: int, note: str=""):
    _ensure_headers()
    cost = _price(provider, model, input_tokens, output_tokens)
    with open(LOG_PATH, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([int(time.time()), provider, model, input_tokens, output_tokens, cost, note])
    return cost