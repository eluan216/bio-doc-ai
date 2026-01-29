# Bio-Doc AI - Architecture & Development Guide

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Streamlit UI Layer (app.py)                 │
│                  - Chat interface                               │
│                  - File upload handling                         │
│                  - Session state management                     │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│                      Core Engine (src/engine.py)                │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ RAG Pipeline:                                            │  │
│  │  1. PDF Loading & Text Extraction                        │  │
│  │  2. Text Chunking (Recursive Character Splitter)         │  │
│  │  3. Embedding Generation (OpenAI)                        │  │
│  │  4. Vector Store Creation (FAISS)                        │  │
│  │  5. Semantic Search Retrieval                            │  │
│  │  6. LLM Query (GPT-4o-mini)                              │  │
│  └──────────────────────────────────────────────────────────┘  │
└──────────────────────────┬──────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        ↓                  ↓                  ↓
   ┌─────────┐        ┌─────────┐        ┌────────┐
   │ OpenAI  │        │ FAISS   │        │ Logs   │
   │ API     │        │ Vector  │        │ System │
   │         │        │ Database│        │        │
   └─────────┘        └─────────┘        └────────┘
```

## Module Responsibilities

### `src/engine.py` - RAG Pipeline Engine
**Responsibility**: Document processing and AI query pipeline

| Function | Purpose | Inputs | Outputs | Error Handling |
|----------|---------|--------|---------|-----------------|
| `load_pdf()` | Extract text from PDF | file_path, max_pages | text context | FileNotFoundError, ValueError |
| `create_vector_store()` | Build FAISS index | file_path, api_key | FAISS store | ValueError on embedding failure |
| `retrieve_context()` | Semantic search | vector_store, query | relevant chunks | ValueError on retrieval failure |
| `initialize_llm()` | LLM setup | api_key | ChatOpenAI instance | ValueError on init failure |
| `query_document()` | LLM inference | llm, context, question | response text | ValueError on query failure |
| `get_ai_response()` | Entry point | file_path, query, api_key | final response | All child exceptions |

### `src/utils.py` - Utilities & Validation
**Responsibility**: File handling, validation, utilities

| Function | Purpose |
|----------|---------|
| `save_temp_pdf()` | Save uploaded files with error handling |
| `cleanup_temp_file()` | Clean up temporary files safely |
| `validate_api_key()` | Validate OpenAI API key format |
| `get_sample_pdfs()` | Discover available sample documents |
| `estimate_tokens()` | Calculate token usage (for cost estimation) |
| `check_file_size()` | Enforce file size limits (security) |

### `src/styles.py` - UI Components
**Responsibility**: Streamlit styling and visual components

### `app.py` - UI Orchestration
**Responsibility**: Streamlit interface and event handling

## Error Handling Strategy

### Exception Hierarchy
```
Exception
├── FileNotFoundError       → Missing PDF file
├── ValueError              → Invalid inputs/API responses
├── KeyError                → Missing configuration
└── RuntimeError            → External service failures
```

### Logging Levels
- **ERROR**: Critical failures requiring intervention
- **WARNING**: Degraded functionality but operation continues
- **INFO**: Important operational events
- **DEBUG**: Detailed diagnostic information

## Testing Strategy

### Test Categories
1. **Unit Tests**: Individual function behavior
2. **Integration Tests**: End-to-end pipeline
3. **Edge Cases**: Empty files, malformed PDFs, rate limits
4. **Performance**: Token usage, response times

### Running Tests
```bash
# All tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=src --cov-report=html

# Specific test
pytest tests/test_engine.py::TestEngineInitialization -v
```

## Performance Characteristics

### Latency
- PDF Loading: ~200-500ms (depends on size)
- Vector Store Creation: ~1-5s (depends on page count)
- Semantic Search: ~50-200ms
- LLM Inference: ~1-3s (network dependent)
- **Total End-to-End**: ~3-10s typical

### Token Usage (Rough Estimates)
- 1 page of text: ~500-1000 tokens
- Embedding creation: ~0.0001 per token
- LLM completion: ~0.15 per token (gpt-4o-mini)

## Deployment Options

### Local Development
```bash
streamlit run app.py
```

### Docker Container
```bash
docker build -t bio-doc-ai .
docker run -p 8501:8501 -e OPENAI_API_KEY=sk-... bio-doc-ai
```

### Docker Compose
```bash
docker-compose up -d
```

### Streamlit Cloud
1. Push to GitHub
2. Connect repository to Streamlit Cloud
3. Add `OPENAI_API_KEY` as secret
4. Deploy (automatic on push)

## Security Considerations

### Data Privacy
- ✅ PDFs processed locally (not stored on servers)
- ✅ API key isolated in environment variables
- ✅ No user data persisted
- ✅ Temporary files cleaned up after processing

### Input Validation
- File size limits (25MB)
- API key format validation
- Query string sanitization
- PDF file validation

### Production Hardening
- ✅ Type hints throughout codebase
- ✅ Comprehensive error handling
- ✅ Request logging for audit trails
- ✅ Rate limiting via OpenAI API
- ✅ Non-root Docker user

## Configuration

### Environment Variables
```bash
OPENAI_API_KEY          # Required: OpenAI API key
STREAMLIT_SERVER_PORT   # Optional: Streamlit port (default: 8501)
LOG_LEVEL               # Optional: Logging level (default: INFO)
MAX_FILE_SIZE_MB        # Optional: Max PDF size (default: 25)
```

### Streamlit Configuration (`.streamlit/config.toml`)
```toml
[theme]
primaryColor = "#007BFF"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#1F2937"
```

## Future Enhancements

### Short Term
- [ ] Batch processing for multiple PDFs
- [ ] Response caching (Redis)
- [ ] Advanced metrics dashboard
- [ ] User authentication

### Medium Term
- [ ] Multi-language support
- [ ] Custom embedding models
- [ ] Document versioning
- [ ] Citation tracking with page numbers

### Long Term
- [ ] Fine-tuned models for medical domain
- [ ] Real-time collaborative editing
- [ ] Knowledge graph integration
- [ ] Enterprise compliance (HIPAA, GDPR)

## Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'langchain_openai'`
**Solution**: `pip install -r requirements.txt` and restart

**Issue**: `OpenAI API rate limit exceeded`
**Solution**: Implement exponential backoff; check API quotas

**Issue**: `PDF parsing fails on image-heavy documents`
**Solution**: Consider OCR solution (e.g., Tesseract) for future

## Contributing

See the main [README.md](../README.md) for contribution guidelines.

## License

MIT License - See LICENSE file
