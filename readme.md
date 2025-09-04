# AIDEN

AIDEN is a command-line assistant for business document management and Q&A, powered by Hugging Face models. It allows you to ingest business documents, build a local RAG (Retrieval-Augmented Generation) index, and ask questions in Arabic or English using state-of-the-art AI.

## Features

- **Document Ingestion:** Easily add `.txt` and `.md` files to your local index.
- **RAG-based Q&A:** Ask questions and get answers based on your ingested documents.
- **Hugging Face Integration:** Uses Hugging Face models for natural language understanding and generation.
- **Arabic Language Support:** Designed for Arabic business use cases.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/ehab123/AIDEN.git
   cd AIDEN
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. (Optional) Set your Hugging Face token:
   ```
   export HUGGINGFACE_TOKEN=your_token_here
   ```

## Usage

### Ingest Documents

Add business documents to the local index:
```
python -m app.cli ingest --path data/business_docs
```

### Ask a Question

Query your indexed documents:
```
python -m app.cli ask --question "ما هي سياسة الاسترجاع لدينا؟"
```

### Chat

One-shot chat with the assistant:
```
python -m app.cli chat --message "كيف يمكنني تحسين خدمة العملاء؟"
```

## Project Structure

```
AIDEN/
├── app/
│   ├── cli.py
│   ├── providers.py
│   ├── simple_doc_store.py
│   └── rag.py
├── data/
│   └── business_docs/
├── requirements.txt
└── README.md
```

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License.

## Contact

For questions or support, contact [Rodr144](https://github.com/Rody144).