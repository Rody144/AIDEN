def choose_route(user_text: str):
    t = user_text.lower()
    long_query = len(user_text) > 300
    complex_signals = any(w in t for w in ["حلّل","تحليل","استنتاج","رياضيات","code","optimize","prove","إستراتيجية","strategy"])
    if long_query or complex_signals:
        return {"provider":"anthropic", "tier":"smart"}
    return {"provider":"openai", "tier":"fast"}
