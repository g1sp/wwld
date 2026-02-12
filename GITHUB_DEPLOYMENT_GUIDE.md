# 🚀 Running WWLD on GitHub

This guide shows you how to run the WWLD (What Would Lenny Do?) application from your GitHub repository.

## 📋 Prerequisites

Before running the application, make sure you have:

- **Python 3.9+** installed ([Download](https://www.python.org/downloads/))
- **Git** installed ([Download](https://git-scm.com/))
- **Anthropic API Key** (get one at [console.anthropic.com](https://console.anthropic.com))
- A modern web browser (Chrome, Firefox, Safari, Edge)

---

## Option 1: Clone from GitHub and Run Locally (Recommended)

### Step 1: Clone the Repository

```bash
git clone https://github.com/g1sp/wwld.git
cd wwld
```

### Step 2: Set Up Python Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Step 4: Set Your API Key

```bash
# macOS/Linux:
export ANTHROPIC_API_KEY="your-api-key-here"

# Windows (PowerShell):
$env:ANTHROPIC_API_KEY="your-api-key-here"

# Windows (Command Prompt):
set ANTHROPIC_API_KEY=your-api-key-here
```

Get your API key from: https://console.anthropic.com/account/keys

### Step 5: Start the Backend Server

```bash
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Step 6: Start the Frontend (New Terminal)

Keep the backend running, then in a new terminal:

```bash
# From the root wwld directory
python3 -m http.server 8001
```

You should see:
```
Serving HTTP on 0.0.0.0 port 8001 (http://0.0.0.0:8001/) ...
```

### Step 7: Open in Browser

Go to: **http://localhost:8001/frontend_backend_integration.html**

---

## Option 2: Quick Setup with Bash Script

If you're on macOS/Linux, you can use the provided setup script:

```bash
# Clone the repo
git clone https://github.com/g1sp/wwld.git
cd wwld/backend

# Run the setup script (one-click setup)
bash setup.sh

# Follow the prompts to enter your API key
```

Then open two terminals:

**Terminal 1 (Backend):**
```bash
cd wwld/backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python main.py
```

**Terminal 2 (Frontend):**
```bash
cd wwld
python3 -m http.server 8001
```

---

## Option 3: Using Docker (If Installed)

If you have Docker installed, you can containerize the application:

```bash
# Build Docker image
docker build -t wwld-backend -f backend/Dockerfile .

# Run container with API key
docker run -e ANTHROPIC_API_KEY="your-api-key" -p 8000:8000 wwld-backend
```

Then open frontend as usual in a separate terminal.

---

## File Structure

```
wwld/
├── frontend_backend_integration.html    # Open this in browser
├── wwld.html                            # Alternative frontend
├── backend/
│   ├── main.py                          # Start this (FastAPI server)
│   ├── solution_generator.py            # Claude integration
│   ├── transcript_processor.py          # Loads 300+ transcripts
│   ├── cache_manager.py                 # File-based caching
│   ├── requirements.txt                 # Python dependencies
│   ├── setup.sh                         # One-click setup
│   ├── .cache/                          # Cache directory (auto-created)
│   └── [test files]
├── [300+ .txt files]                    # Podcast transcripts
└── [Documentation files]                # README, guides, etc.
```

---

## ✅ Verification Checklist

After starting both servers, verify everything is working:

### 1. Check Backend Health
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status":"healthy","transcripts_loaded":304}
```

### 2. Get Popular Problems
```bash
curl http://localhost:8000/problems
```

Expected response:
```json
{"problems":["How do I prioritize?", "How do I hire?", ...]}
```

### 3. Test Main Endpoint
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"problem": "How do I prioritize?", "num_solutions": 3}'
```

### 4. Open Frontend
- Go to: http://localhost:8001/frontend_backend_integration.html
- Try asking a question
- See results appear

---

## 🎯 Testing the New Features

Once running, test all the new features:

### Feature 1: Problem History
1. Type: "How do I prioritize?"
2. Click ASK
3. See history panel appear above input
4. Ask another question
5. History shows 2 items
6. Refresh page (F5) → History persists ✅

### Feature 2: Favorites
1. Click ★ star on any solution
2. Star turns gold ⭐
3. Scroll down → "Saved Insights" panel appears
4. Refresh page (F5) → Favorites persist ✅

### Feature 3: Export
1. Click "📥 Export" button
2. Choose JSON or Text
3. File downloads to Downloads folder ✅

### Feature 4: Share
1. Click "🔗 Share" button
2. Click "📋 Copy Link"
3. Open new tab and paste URL
4. Same results appear ✅

See **START_TESTING_NOW.md** for detailed testing steps.

---

## 🐛 Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'anthropic'"

**Solution:**
```bash
cd backend
pip install -r requirements.txt
```

### Problem: "ANTHROPIC_API_KEY not set"

**Solution:**
```bash
# Set your API key
export ANTHROPIC_API_KEY="your-key-here"

# Then start the server
python main.py
```

### Problem: "Address already in use" (Port 8000 or 8001)

**Solution:**
```bash
# Find what's using the port (macOS/Linux)
lsof -i :8000
lsof -i :8001

# Kill the process
kill -9 <PID>

# Or use different ports
python main.py --port 8002  # Backend on different port
python3 -m http.server 8003  # Frontend on different port
```

### Problem: "Connection refused" in browser

**Make sure both servers are running:**

Terminal 1: `python main.py` (should show "Uvicorn running")
Terminal 2: `python3 -m http.server 8001` (should show "Serving HTTP")

### Problem: No results from backend

**Check:**
1. API key is set correctly
2. Internet connection is working
3. Anthropic API is accessible
4. Backend logs show successful responses

### Problem: Frontend won't load

**Check:**
1. You're visiting the correct URL: http://localhost:8001/frontend_backend_integration.html
2. HTTP server is running (`python3 -m http.server 8001`)
3. JavaScript console has no errors (F12 → Console)

---

## 📊 API Endpoints Reference

These endpoints are available when the backend is running:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Health check |
| `/problems` | GET | Get popular problem examples |
| `/speakers` | GET | List all speakers |
| `/ask` | POST | Main endpoint: get expert solutions |
| `/search` | POST | Search transcripts |
| `/cache/stats` | GET | Cache statistics |
| `/cache/clear` | DELETE | Clear cache |

### Example: Get Solutions
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{
    "problem": "How do I build a product?",
    "num_solutions": 3,
    "problem_category": null
  }'
```

---

## 🌐 Accessing from Other Machines

To access the application from another computer on your network:

1. **Find your local IP:**
   ```bash
   # macOS/Linux:
   ifconfig | grep "inet "

   # Windows:
   ipconfig | find "IPv4"
   ```

2. **Start servers with network binding:**
   ```bash
   # Backend
   uvicorn main:app --host 0.0.0.0 --port 8000

   # Frontend
   python3 -m http.server 8001 --bind 0.0.0.0
   ```

3. **Access from another machine:**
   ```
   http://<your-ip>:8001/frontend_backend_integration.html
   ```

---

## 🚀 Performance Tips

### Optimize Backend Performance
```bash
# Use multiple workers
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Cache Management
The application automatically caches results. To clear cache:
```bash
curl -X DELETE http://localhost:8000/cache/clear
```

Check cache stats:
```bash
curl http://localhost:8000/cache/stats
```

---

## 📝 Environment Variables

```bash
# Required
export ANTHROPIC_API_KEY="sk-ant-..."

# Optional
export PYTHONUNBUFFERED=1          # See logs in real-time
export LOGLEVEL=INFO                # Logging level
export API_HOST="127.0.0.1"         # API host
export API_PORT=8000                # API port
```

---

## 📚 Documentation

For more information, see:

- **START_TESTING_NOW.md** - Quick 5-minute test
- **QUICK_START_NEW_FEATURES.md** - 2-minute user guide
- **TESTING_GUIDE.md** - 46+ test scenarios
- **FEATURES_OVERVIEW.md** - Feature documentation
- **README_NEW_FEATURES.md** - Master documentation index
- **IMPLEMENTATION_COMPLETE.md** - Technical specifications

---

## 🎓 Understanding the Architecture

```
Your Browser
    ↓ HTTP requests
    ├── Frontend: http://localhost:8001/frontend_backend_integration.html
    │   (HTML/CSS/JavaScript with localStorage)
    │
    ↓ API calls (JSON)
    │
Backend: http://localhost:8000
    ├── FastAPI Server (main.py)
    ├── Solution Generator (Claude AI integration)
    ├── Transcript Processor (loads 300+ transcripts)
    └── Cache Manager (file-based caching)

    ↓ API calls to Anthropic

Anthropic Claude API
    (Processes your questions and returns expert insights)
```

---

## 🔄 Development Workflow

To make changes and test them:

1. **Edit files** in your editor (e.g., VS Code)

2. **Frontend changes:**
   - Edit `frontend_backend_integration.html`
   - Refresh browser (F5)
   - Changes appear immediately

3. **Backend changes:**
   - Edit files in `backend/`
   - Restart `python main.py`
   - Test with new API calls

4. **Test thoroughly:**
   - Follow TESTING_GUIDE.md
   - Run 46+ test scenarios

5. **Commit and push:**
   ```bash
   git add .
   git commit -m "Description of changes"
   git push origin main
   ```

---

## 🎯 Quick Start Commands (Copy & Paste)

### macOS/Linux

```bash
# Clone repo
git clone https://github.com/g1sp/wwld.git
cd wwld

# Terminal 1: Backend
cd backend
export ANTHROPIC_API_KEY="your-api-key"
pip install -r requirements.txt
python main.py

# Terminal 2: Frontend
cd wwld  # back to root
python3 -m http.server 8001

# Then open in browser:
# http://localhost:8001/frontend_backend_integration.html
```

### Windows (PowerShell)

```powershell
# Clone repo
git clone https://github.com/g1sp/wwld.git
cd wwld

# Terminal 1: Backend
cd backend
$env:ANTHROPIC_API_KEY="your-api-key"
pip install -r requirements.txt
python main.py

# Terminal 2: Frontend
cd ..\
python -m http.server 8001

# Then open in browser:
# http://localhost:8001/frontend_backend_integration.html
```

---

## ✅ You're Ready!

You now have everything you need to run WWLD locally. Start with the quick start commands above, then explore the features and documentation.

**Questions?** Check the troubleshooting section or refer to the comprehensive documentation files included in the repository.

**Happy coding!** 🚀
