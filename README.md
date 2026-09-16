# Bio-Doc AI: Clinical Document Intelligence

**Scalable RAG architecture for biomedical document analysis**

**Author:** Oguma Eluanatein Odo  
**Focus:** Healthcare AI · Retrieval-Augmented Generation · Clinical documents

---

## The Problem

Clinicians and researchers face a growing volume of papers, guidelines, and internal documents. Finding precise, source-backed answers quickly is difficult without specialized tooling.

## The Solution

**Bio-Doc AI** is a Retrieval-Augmented Generation (RAG) system for medical and biomedical documents. Upload PDFs, ask questions, and receive answers grounded in the uploaded content with source tracking.

### Key Capabilities

- End-to-end workflow: PDF ingestion → chunking → vector index → grounded answers
- Semantic retrieval with FAISS
- Source-aware responses (context from your documents)
- Privacy-minded design: documents processed for the session; API keys via environment variables
- Designed as a portfolio / educational demonstration of clinical RAG patterns

> **Note:** This is a portfolio project for demonstrating RAG engineering skills. It is **not** a medical device and must not be used for clinical decision-making.

---

## Technical Stack

| Component       | Technology              |
|----------------|-------------------------|
| Language       | Python 3.10+            |
| LLM            | OpenAI (configurable)   |
| RAG framework  | LangChain               |
| Vector store   | FAISS                   |
| UI             | Streamlit               |
| PDF parsing    | PyPDF / related loaders |

### Project layout

```text
bio-doc-ai/
├── .github/workflows/   # CI
├── .streamlit/          # Theme config
├── data/samples/        # Sample PDFs for demo
├── src/
│   ├── engine.py        # RAG pipeline & vector logic
│   ├── styles.py        # UI components
│   └── utils.py         # Document handling
├── tests/
├── app.py               # Streamlit entry point
├── requirements.txt
└── README.md
```

---

## Getting Started

### Local

```bash
git clone https://github.com/eluan216/bio-doc-ai.git
cd bio-doc-ai
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

export OPENAI_API_KEY="your-key-here"
streamlit run app.py
```

### Streamlit Cloud

1. Fork the repository
2. Connect to [Streamlit Cloud](https://share.streamlit.io)
3. Add `OPENAI_API_KEY` as a secret
4. Deploy with main file `app.py`

---

## Testing

```bash
pytest tests/ -v
pytest tests/ --cov=src
```

CI runs via GitHub Actions on push.

---

## Security & Privacy Notes

- API keys kept in environment variables / Streamlit secrets
- Designed for session-based document use (no long-term document storage assumed)
- Suitable for demonstrating architecture; production clinical use would require formal validation, access control, and compliance review

---

## Author

**Oguma Eluanatein Odo**  
B.Sc. Biomedical Technology  
Focus: Healthcare interoperability & clinical AI  
[LinkedIn](https://linkedin.com/in/eluanatein-oguma-5552571b6) · [GitHub](https://github.com/eluan216) · ogumaeluan@gmail.com

---

## License

MIT
