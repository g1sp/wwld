# WWLD - What Would Lenny Do? | Quick Start Guide

A click-baity AI-powered tool that extracts real advice from 300+ Lenny podcast episodes.

## 🚀 Getting Started in 5 Minutes

### 1. Set Your API Key

```bash
export ANTHROPIC_API_KEY="your-anthropic-api-key"
```

Get your key at: https://console.anthropic.com/api_keys

### 2. Install Dependencies

```bash
cd /Users/jeevan.patil/Downloads/Lenny/backend
pip install -r requirements.txt
```

### 3. Start the Backend

```bash
python main.py
```

You should see:
```
🚀 Initializing WWLD Backend...
📁 Loading transcripts from: /Users/jeevan.patil/Downloads/Lenny
📖 Loading transcripts...
   Found 298 transcript files
   ✅ Loaded 298 transcripts successfully
🎤 Extracting speakers...
   ✅ Found 300+ unique speakers
✅ Loaded 298 transcripts
✅ Cache manager initialized
✅ Ready to generate solutions
```

Server runs at: http://localhost:8000

### 4. Test the Backend

In another terminal:

```bash
cd /Users/jeevan.patil/Downloads/Lenny/backend
python test_backend.py
```

### 5. Open the Frontend

Open in your browser:
```
file:///Users/jeevan.patil/Downloads/Lenny/frontend_backend_integration.html
```

Click a popular problem or type your own, and hit ASK!

## 📖 File Structure

```
/Lenny/
├── wwld.html                          # Original static version
├── frontend_backend_integration.html   # Frontend that calls API
├── QUICKSTART.md                       # This file
├── backend/
│   ├── main.py                        # FastAPI server
│   ├── transcript_processor.py         # Load & index transcripts
│   ├── solution_generator.py           # Use Claude to extract wisdom
│   ├── cache_manager.py                # Cache solutions
│   ├── test_backend.py                 # Test suite
│   ├── requirements.txt                # Dependencies
│   └── README.md                       # Full documentation
└── /Lenny/ (transcripts)
    ├── Andy Johns.txt
    ├── Brian Chesky.txt
    └── ... 296 more transcript files
```

## 🎯 How It Works

1. **User inputs problem** → Frontend sends to backend
2. **Backend categorizes** → Maps to relevant speakers (e.g., "PMF" → Sean Ellis)
3. **Claude extracts** → Finds real quotes from transcripts
4. **Results returned** → Frontend displays with frameworks

## 🧪 Quick Tests

### Health Check
```bash
curl http://localhost:8000/health
```

### Get Popular Problems
```bash
curl http://localhost:8000/problems
```

### Get All Speakers
```bash
curl http://localhost:8000/speakers
```

### Ask a Question
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{
    "problem": "How do I know if we have product-market fit?",
    "num_solutions": 3
  }'
```

### Interactive API Docs
While backend is running, visit:
```
http://localhost:8000/docs
```

## 💡 Example Questions

Try asking WWLD:

- "How do I know if we have product-market fit?"
- "My engineering and product team don't get along"
- "How do I prioritize what to build next?"
- "We're burning out our team"
- "How do we launch a new product?"
- "How do I build a high-performing product team?"
- "How do I make data-driven decisions?"
- "What's the right pricing strategy?"

## 🔧 Customization

### Add More Problem Categories

Edit `backend/solution_generator.py`:

```python
PROBLEM_CATEGORIES = {
    "your-new-category": [
        "Speaker Name 1",
        "Speaker Name 2",
        "Speaker Name 3"
    ]
}
```

### Change Number of Solutions

In the frontend, change this line:
```javascript
num_solutions: 5  // Was 3, now returns 5 solutions
```

### Use Different Claude Model

In `backend/solution_generator.py`:
```python
model="claude-3-opus-20250219"  # Use latest Opus instead
```

## ⚡ Performance Tips

- First query: 2-5 seconds (hits Claude API)
- Repeated queries: <100ms (uses cache)
- Cache stored in: `backend/.cache/`

Clear cache with:
```bash
curl -X DELETE http://localhost:8000/cache/clear
```

## 🐛 Troubleshooting

### "Connection refused" error
- Make sure backend is running: `python main.py`
- Check it's on localhost:8000

### "ANTHROPIC_API_KEY not found"
```bash
export ANTHROPIC_API_KEY="your-key"
echo $ANTHROPIC_API_KEY  # Verify it's set
```

### Slow API calls
- Check your internet connection
- First call always slower (API latency)
- Subsequent calls use cache (instant)

### Transcripts not loading
```bash
ls /Users/jeevan.patil/Downloads/Lenny/*.txt | wc -l
# Should show 298 files
```

## 📊 What Gets Extracted

For each solution, Claude extracts:

```
{
  "speaker": "Sean Ellis",
  "speaker_role": "Growth Expert & PMF Pioneer",
  "insight": "[actual quote from transcript]",
  "framework": "growth loop",
  "framework2": "retention metrics",
  "episode_name": "Sean Ellis",
  "episode_timestamp": "00:12:34"
}
```

## 🎓 Learning Resources

- **Backend README**: `backend/README.md`
- **API Docs**: http://localhost:8000/docs (interactive)
- **Test Suite**: `python backend/test_backend.py`

## 💰 Costs

- **Per question**: ~$0.02-0.05 (Claude API cost)
- **Cached questions**: Free
- **Typical usage**: $1-2/month

## 🚀 Deploy to Production

### Simple Deployment (Heroku)

```bash
# Create Procfile
echo "web: gunicorn -w 4 -b 0.0.0.0:\$PORT main:app" > backend/Procfile

# Deploy
heroku create wwld-backend
heroku config:set ANTHROPIC_API_KEY="your-key"
git push heroku main
```

### Using Docker

```bash
# Build
docker build -t wwld-backend backend/

# Run
docker run -e ANTHROPIC_API_KEY="your-key" -p 8000:8000 wwld-backend
```

## 🤝 Contributing

Ideas for improvement:
- [ ] Add semantic search with embeddings
- [ ] Extract episode timestamps automatically
- [ ] Multi-speaker collaborative solutions
- [ ] Export as PDF playbook
- [ ] Rate limiting and auth
- [ ] Database for persistence

## 📝 License

MIT - Use freely!

---

**Questions?** Check the backend README or run `python test_backend.py`

**Ready to dive deeper?** Start with the API docs at `http://localhost:8000/docs`
