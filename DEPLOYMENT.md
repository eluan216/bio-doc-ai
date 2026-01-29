# Bio-Doc AI - Deployment Guide

## Quick Start

### Prerequisites
- Python 3.10+ or Docker
- OpenAI API key (get at https://platform.openai.com/api-keys)
- Git

### Local Installation (5 minutes)

```bash
# 1. Clone repository
git clone https://github.com/eluan216/bio-doc-ai.git
cd bio-doc-ai

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set API key
export OPENAI_API_KEY="sk-your-key-here"

# 5. Run locally
streamlit run app.py
```

App will open at: http://localhost:8501

---

## Production Deployment

### Option 1: Streamlit Cloud (Recommended - Free & Easy)

1. **Fork this repository** to your GitHub account
2. **Go to** https://share.streamlit.io
3. **Click** "Create app"
4. **Select** your forked repository:
   - Repo: `your-username/bio-doc-ai`
   - Branch: `main`
   - Main file path: `app.py`
5. **Add Secrets** (Important!):
   - Click "Advanced settings"
   - Under "Secrets", paste:
   ```
   OPENAI_API_KEY = "sk-your-key-here"
   ```
6. **Deploy!** → Your app is live ✨

**Cost**: Free tier (unlimited deploys)  
**Uptime**: 99.9%  
**Auto-scaling**: Automatic

---

### Option 2: Docker (Self-Hosted)

#### Docker (Local)
```bash
# Build image
docker build -t bio-doc-ai .

# Run container
docker run -p 8501:8501 -e OPENAI_API_KEY=sk-... bio-doc-ai

# Access at http://localhost:8501
```

#### Docker Compose (Recommended)
```bash
# Create .env file
echo "OPENAI_API_KEY=sk-your-key-here" > .env

# Start services
docker-compose up -d

# View logs
docker-compose logs -f bio-doc-ai

# Stop services
docker-compose down
```

---

### Option 3: Cloud Providers

#### AWS (EC2 + ECS)
```bash
# Build and push image
aws ecr create-repository --repository-name bio-doc-ai
docker build -t bio-doc-ai .
docker tag bio-doc-ai:latest YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/bio-doc-ai:latest
docker push YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/bio-doc-ai:latest

# Deploy to ECS using CloudFormation or Console
```

**Cost**: ~$10-50/month for EC2 micro instance  
**Scaling**: Manual or via ECS Auto Scaling

#### Google Cloud Run
```bash
# Push to Google Container Registry
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/bio-doc-ai

# Deploy
gcloud run deploy bio-doc-ai \
  --image gcr.io/YOUR_PROJECT_ID/bio-doc-ai:latest \
  --platform managed \
  --region us-central1 \
  --set-env-vars OPENAI_API_KEY=sk-...
```

**Cost**: Free tier (2M requests/month), then ~$0.40 per 1M requests  
**Scaling**: Automatic

#### Heroku (Deprecated but still works)
```bash
heroku create your-app-name
heroku config:set OPENAI_API_KEY=sk-...
git push heroku main
```

---

## Performance Optimization

### Caching Strategy
```python
# Add to app.py for faster load times
@st.cache_resource
def load_vector_store():
    return create_vector_store(...)
```

### Response Time Targets
- Initial page load: < 2s
- PDF upload: < 5s
- Query response: < 3s
- Total: < 10s

### Scaling Considerations
| Users | Recommendation |
|-------|-----------------|
| 1-10 | Streamlit Cloud Free |
| 10-100 | Streamlit Cloud Pro ($9/mo) |
| 100+ | Docker on AWS/GCP/Azure |
| 1000+ | Kubernetes cluster |

---

## Security Checklist

- [ ] API key in environment variables (not hardcoded)
- [ ] HTTPS enabled (automatic on Streamlit Cloud)
- [ ] Input validation on all user data
- [ ] File size limits enforced
- [ ] Temporary files cleaned up
- [ ] Logging enabled for audit trail
- [ ] Rate limiting in place

---

## Monitoring & Logging

### Streamlit Cloud Logs
```bash
# View deployment logs
streamlit logs [your-app-url]
```

### Docker Logs
```bash
# View container logs
docker logs -f bio-doc-ai

# With timestamps
docker logs -f --timestamps bio-doc-ai
```

### Application Logs
Logs are written to stderr and captured by:
- Streamlit Cloud: Dashboard
- Docker: `docker logs`
- Local: Console output

---

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 8501
lsof -i :8501

# Kill process
kill -9 <PID>

# Or use different port
streamlit run app.py --server.port 8502
```

### API Rate Limited
```
Error: RateLimitError: 429 Too Many Requests
```
**Solution**: 
- Upgrade OpenAI plan
- Add retry logic with exponential backoff
- Implement response caching

### Memory Issues with Large PDFs
```
Error: MemoryError
```
**Solution**:
- Reduce `max_pages` parameter
- Split large PDFs before upload
- Use streaming architecture

### Docker Permission Denied
```
Error: permission denied while trying to connect to Docker daemon
```
**Solution**:
```bash
# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker
```

---

## Cost Estimation

### Monthly Costs (Typical Usage)

| Service | Free Tier | Paid Tier | Usage |
|---------|-----------|-----------|-------|
| Streamlit Cloud | Yes | $9/mo | Hosting |
| OpenAI API | $5 credit | $0.10-1.00 | ~100 queries/month |
| Storage | Included | - | Logs, samples |
| **Total** | **$0** | **~$10-15/mo** | - |

### OpenAI Token Pricing
- Embedding: $0.00002 per token
- Prompt (gpt-4o-mini): $0.00015 per token
- Completion (gpt-4o-mini): $0.0006 per token

**Example**: 500-page document → ~5,000 queries = $5-10/month

---

## Rollback & Downgrade

### Streamlit Cloud
1. Go to app settings
2. Click "Git" → Select previous commit
3. Redeploy

### Docker
```bash
# Revert to previous image
docker pull bio-doc-ai:previous-tag
docker run -p 8501:8501 bio-doc-ai:previous-tag
```

---

## Support

**Issues?** Open a GitHub issue: https://github.com/eluan216/bio-doc-ai/issues

**Questions?** Check the [ARCHITECTURE.md](ARCHITECTURE.md) guide
