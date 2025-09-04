from huggingface_hub import InferenceClient
import os

token = os.getenv("HUGGINGFACE_TOKEN")
print("HAS_TOKEN:", token is not None)

client = InferenceClient(
    model="meta-llama/Meta-Llama-3-8B-Instruct",
    token=token
)

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break

    response = client.chat.completions.create(
        messages=[{"role": "user", "content": user_input}],
        max_tokens=200
    )

    print("AI:", response.choices[0].message["content"])

