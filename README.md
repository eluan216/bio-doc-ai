# Bio-Doc AI: Clinical Document Intelligence

Scalable RAG architecture for biomedical document analysis.

**Author:** Oguma Eluanatein Odo  
**Focus:** Healthcare AI · Retrieval-Augmented Generation · Clinical documents

> **Not a medical device.** Portfolio / educational project only. Do not use for clinical decisions.

---

## Quick start

```bash
git clone https://github.com/eluan216/bio-doc-ai.git
cd bio-doc-ai
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

export OPENAI_API_KEY="your-key-here"
streamlit run app.py
```

**Required to run end-to-end:**

1. Packages in `requirements.txt` (includes `langchain-openai`, `langchain-community`, `faiss-cpu`, …)
2. A valid **OpenAI API key** (`OPENAI_API_KEY` or sidebar input)

Without the key, the UI still loads; queries will prompt you to add one.

---

## What it does

- PDF upload → text extraction / optional FAISS retrieval → grounded answers via OpenAI
- Toggle vector search off to avoid embedding API calls on free-tier budgets
- Session-based document handling (no long-term document storage assumed)

---

## Stack

| Layer | Technology |
|-------|------------|
| UI | Streamlit |
| RAG | LangChain |
| LLM / embeddings | OpenAI (`gpt-4o-mini`, OpenAI embeddings) |
| Vector store | FAISS |
| PDF | PyPDF / LangChain loaders |

---

## Layout

```text
bio-doc-ai/
├── src/
│   ├── engine.py    # RAG pipeline
│   ├── styles.py
│   └── utils.py
├── tests/
├── app.py
├── requirements.txt
└── README.md
```

---

## Tests

```bash
pip install -r requirements.txt
pytest tests/ -v
```

Some tests skip if no sample PDF or live OpenAI key is available.

---

## Author

**Oguma Eluanatein Odo**  
[LinkedIn](https://linkedin.com/in/eluanatein-oguma-5552571b6) · [GitHub](https://github.com/eluan216) · ogumaeluan@gmail.com

## License

MIT
