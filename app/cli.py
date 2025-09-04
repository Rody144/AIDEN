# app/cli.py
# CLI بسيط يعمل مع HuggingFaceProvider فقط

import argparse
import json
from typing import List, Dict

# مزوّد هاجينج فيس
from .providers import HuggingFaceProvider

# مخزن الـ RAG
from .simple_doc_store import SimpleDocStore

# ============== مساعدات ==============

def _build_messages(system: str, user: str, history: List[Dict] = None):
    msgs = []
    if system:
        msgs.append({"role": "system", "content": system})
    if history:
        msgs.extend(history)
    msgs.append({"role": "user", "content": user})
    return msgs

# ============== أوامر CLI ==============

def chat_cmd(args):
    """محادثة برسالة واحدة مع مزوّد HF"""
    system = "أنت مساعد أعمال مهذب ودقيق."
    user_msg = args.message

    p = HuggingFaceProvider()
    messages = _build_messages(system, user_msg)
    text, usage, used_model = p.chat(messages, temperature=args.temperature)

    print("\n=== Reply ===\n")
    print(text)
    meta = {"provider": "hf", "model": used_model, "usage": usage}
    print("\n--- meta ---")
    print(json.dumps(meta, ensure_ascii=False, indent=2))


def ingest_cmd(args):
    """بناء الفهرس للـ RAG"""
    store = SimpleDocStore()
    # جرّب الاسمَين لضمان التوافق
    if hasattr(store, "ingest_folder"):
        n = store.ingest_folder(args.path)
    else:
        n = store.ingest(args.path)  # type: ignore
    print(f"✅ Ingest done for path: {args.path} (chunks={n})")


def ask_cmd(args):
    """سؤال باستخدام RAG + توليد إجابة بالمزوّد HF"""
    store = SimpleDocStore()

    # جلب السياق من الفهرس
    k = getattr(args, "k", 5)
    if hasattr(store, "search"):
        results = store.search(args.question, k=k)
        context = "\n\n".join([f"[{i+1}] {r['text']}" for i, r in enumerate(results)])
        sources = [f"{r['meta'].get('source','?')}#chunk{r['meta'].get('chunk','?')} (score={r.get('score',0):.3f})"
                   for r in results]
    else:
        # لو فيه method ask داخلي بيرجع نص جاهز
        answer = store.ask(args.question)  # type: ignore
        print("\n=== Answer ===\n")
        print(answer)
        return

    # توليد الإجابة باستخدام القالب العام
    system = "أنت مساعد يستخدم سياق الشركة للإجابة بدقة."
    prompt = (
        "السياق من مستندات الشركة:\n"
        f"{context}\n\n"
        f"السؤال:\n{args.question}\n\n"
        "استخدم السياق بالأعلى. إن لم تجد الإجابة، قل أنك لا تملك معلومات كافية."
    )

    p = HuggingFaceProvider()
    messages = _build_messages(system, prompt)
    text, usage, used_model = p.chat(messages, temperature=args.temperature)

    # طباعة النتيجة + المصادر المستخدمة
    print("\n=== Context used ===")
    for s in sources:
        print(s)
    print("\n=== Answer ===\n")
    print(text)
    meta = {"provider": "hf", "model": used_model, "usage": usage}
    print("\n--- meta ---")
    print(json.dumps(meta, ensure_ascii=False, indent=2))


# ============== نقطة الدخول ==============

def main():
    ap = argparse.ArgumentParser(prog="aiden", description="AIDEN CLI (Hugging Face only)")
    sub = ap.add_subparsers()

    # chat
    p = sub.add_parser("chat", help="Basic one-shot chat")
    p.add_argument("--message", required=True)
    p.add_argument("--temperature", type=float, default=0.2)
    p.set_defaults(func=chat_cmd)

    # ingest
    pi = sub.add_parser("ingest", help="Ingest txt/md files into the local RAG index")
    pi.add_argument("--path", required=True, help="Folder path containing .txt/.md documents")
    pi.set_defaults(func=ingest_cmd)

    # ask
    pa = sub.add_parser("ask", help="Ask a question using RAG over ingested docs")
    pa.add_argument("--question", required=True)
    pa.add_argument("--k", type=int, default=5)
    pa.add_argument("--temperature", type=float, default=0.2)
    pa.set_defaults(func=ask_cmd)

    args = ap.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        ap.print_help()


if __name__ == "__main__":
    main()