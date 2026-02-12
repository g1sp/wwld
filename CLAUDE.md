# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

WWLD ("What Would Lenny Do?") is a full-stack AI-powered Q&A system that extracts real quotes from Lenny's podcast transcripts using Claude AI. Users submit problems related to product/leadership, the system categorizes them into one of 10 domains, identifies relevant expert speakers, and returns 3 expert perspectives with actionable frameworks—all based on actual verbatim quotes.

**Key Innovation:** Real quote extraction from 298 podcast transcripts (300+ speakers) rather than synthesized advice, combined with intelligent problem categorization and file-based caching.

## Architecture

The system uses a **multi-layer stateless service model**:

```
Frontend (HTML/CSS/JS)
    ↓ HTTP/JSON
FastAPI Backend
    ├── Solution Generator (Claude Integration)
    ├── Cache Manager (File-based, MD5 keys)
    └── Transcript Processor (298 indexed transcripts)
```

### Key Architectural Patterns

1. **Stateless API Design** - No database; all state lives in files/transcripts
2. **Problem Categorization** - 10 predefined categories with mapped speakers (e.g., "prioritization" → Jake Knapp, Richard Rumelt, Itamar Gilad)
3. **Intelligent Caching** - MD5-based cache keys; typically 50%+ hit rate
4. **Claude-Powered Extraction** - Prompt-based extraction with verbatim requirement prevents hallucination
5. **Lazy Loading** - Transcripts loaded at startup, reused across all queries

### Data Pipeline

1. User submits problem → 2. Backend categorizes (keyword matching) → 3. Identifies relevant speakers → 4. Fetches transcript (first 8000 chars) → 5. Claude extracts quote + frameworks → 6. Caches result → 7. Returns to frontend

**Performance:** First query 2-5s (Claude latency), cached queries <100ms (file I/O).

## Technology Stack

- **Backend:** Python 3.9+, FastAPI, Uvicorn, Pydantic
- **Frontend:** Vanilla HTML/CSS/JavaScript
- **AI:** Anthropic Claude 3.5 Sonnet API (~$0.01-0.02/query)
- **Data:** 298 local .txt transcript files (10MB+), file-based caching in `.cache/`
- **Dependencies:** See `backend/requirements.txt`

## Essential Commands

**Setup & Installation**
```bash
cd backend
bash setup.sh                    # Auto-setup: venv, dependencies, API key verification, transcript loading
# OR manual: pip install -r requirements.txt
```

**Development**
```bash
python backend/main.py           # Start FastAPI server (localhost:8000)
curl http://localhost:8000/docs  # Interactive Swagger API docs
```

**Testing**
```bash
python backend/test_backend.py   # Full test suite
curl http://localhost:8000/health  # Health check
```

**Useful Endpoints**
```bash
# Main endpoint
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"problem": "How do I prioritize what to build?", "num_solutions": 3}'

# Diagnostics
curl http://localhost:8000/problems      # Popular problems
curl http://localhost:8000/speakers      # All speakers
curl http://localhost:8000/cache/stats   # Cache stats
curl -X DELETE http://localhost:8000/cache/clear  # Clear cache
```

**Frontend**
```bash
# Option 1: Static file
open frontend_backend_integration.html

# Option 2: Python simple server (from project root)
python3 -m http.server 8001
# Then visit http://localhost:8001/frontend_backend_integration.html
```

## File Structure

```
backend/
  ├── main.py                    # FastAPI server + 6 REST endpoints
  ├── solution_generator.py      # Claude integration, problem categorization
  ├── transcript_processor.py    # Loads & indexes 298 .txt files
  ├── cache_manager.py           # File-based caching with MD5 keys
  ├── test_backend.py            # Full test suite
  ├── requirements.txt           # Python dependencies
  ├── setup.sh                   # One-click setup
  ├── .cache/                    # Auto-created cache directory (JSON files)
  └── README.md                  # Complete API reference

frontend_backend_integration.html # Live frontend (connects to FastAPI backend)
wwld.html                        # Static HTML template

[300+ .txt files]                # Podcast transcripts named by speaker
```

## API Endpoints (6 core)

| Endpoint | Method | Purpose | Example Input |
|----------|--------|---------|----------------|
| `/ask` | POST | Main endpoint: get expert solutions | `{"problem": "...", "num_solutions": 3}` |
| `/problems` | GET | Get 10 popular problem examples | - |
| `/speakers` | GET | List all 300+ speakers | - |
| `/transcripts` | GET | Transcript metadata | - |
| `/search` | POST | Search transcripts by keyword | `{"keyword": "...", "limit": 10}` |
| `/cache/stats` | GET | Cache diagnostics | - |
| `/cache/clear` | DELETE | Clear all cached results | - |
| `/health` | GET | Health check | - |

## Problem Categories & Speakers

System automatically routes problems to one of 10 categories, each with 3-4 expert speakers:

- **Product-Market Fit** → Sean Ellis, Brian Balfour, Marty Cagan
- **Product-Eng Conflict** → Brian Chesky, Marty Cagan, Will Larson
- **Prioritization** → Jake Knapp, Richard Rumelt, Itamar Gilad
- **Team Burnout** → Andy Johns, Jason Fried, Jerry Colonna
- **Go-to-Market** → Jason M Lemkin, April Dunford, Andy Raskin
- **Building Teams** → Marty Cagan, Ken Norton, Melissa Perri
- **Data-Driven** → Ronny Kohavi, Nicole Forsgren, Patrick Campbell
- **Communication** → Nancy Duarte, Kim Scott, Matt Abrahams
- **Scaling** → Eric Ries, Bill Carr, Boz
- **Pricing** → Jason M Lemkin, Madhavan Ramanujam, Eli Schwartz

Keyword-based matching with fallback to default category.

## Caching Strategy

- **Cache Key:** `MD5(problem.lower() + ":" + category)`
- **Storage:** JSON files in `backend/.cache/`
- **Index:** `index.json` tracks all entries
- **TTL:** Unlimited (manual clear only)
- **Impact:** Reduces API costs by 50%+ with typical 50%+ hit rate

## Solution Structure (Claude Response Format)

Each solution includes:
```json
{
  "speaker": "Speaker Name",
  "role": "Their role/context",
  "emoji": "🎯",
  "quote": "Verbatim quote from transcript",
  "framework": "Actionable framework 1",
  "framework2": "Actionable framework 2",
  "timestamp": "HH:MM:SS reference in transcript"
}
```

## Important Implementation Details

1. **Transcript Loading:** All 298 transcripts are loaded at startup (approximately 2 seconds). Each is a plain .txt file named by speaker.

2. **Quote Extraction:** Claude is prompted to find verbatim quotes addressing the user's problem. The system validates that extracted content exists in the transcript to prevent hallucination.

3. **Problem Categorization:** Uses keyword matching (e.g., "prioritize" or "build roadmap" → prioritization category). Falls back to default if no keywords match.

4. **CORS Enabled:** Allows frontend (loaded from filesystem) to make requests to backend API.

5. **Stateless Design:** No session state or database. Each request is independent; horizontal scaling is possible.

## Environment Setup

**Required:**
- Python 3.9+
- Anthropic API key (set as `ANTHROPIC_API_KEY` environment variable)
- Internet connection (for Claude API calls)

**Optional:**
- Docker (for containerized deployment)
- Pytest (for advanced testing)

## Documentation Files

| File | Purpose |
|------|---------|
| `START_HERE.md` | Quick entry point (recommended first read) |
| `README.md` | Main project overview |
| `QUICKSTART.md` | 5-minute setup guide |
| `IMPLEMENTATION_GUIDE.md` | Deep technical dive (data flow, patterns) |
| `backend/README.md` | Complete API reference |
| `PROJECT_SUMMARY.txt` | Stats and use cases |

## Common Development Tasks

**Add a New Problem Category:**
1. Edit `solution_generator.py` → `PROBLEM_CATEGORIES` dict
2. Add keywords and corresponding speakers
3. Restart backend

**Add/Update Transcripts:**
1. Add/replace `.txt` file in root directory
2. Restart backend (auto-reloads all transcripts)

**Modify Claude Prompts:**
1. Edit `solution_generator.py` → `extract_solution()` function
2. Adjust system prompt or extraction logic
3. Test with `curl` or `test_backend.py`

**Deploy:**
- Backend is stateless (horizontally scalable)
- Set `ANTHROPIC_API_KEY` environment variable
- Frontend can be served from any static host
- Backend can run on Heroku, Docker, AWS Lambda, etc.

## Testing & Validation

```bash
# Run full test suite
python backend/test_backend.py

# Test individual endpoints
curl http://localhost:8000/health
curl http://localhost:8000/problems

# Test the main ask endpoint
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"problem": "How should I hire my first engineer?", "num_solutions": 3}'
```

## Performance Notes

- **First Query:** 2-5 seconds (Claude API response time)
- **Cached Query:** <100ms (file I/O only)
- **Startup:** ~2 seconds (load 298 transcripts)
- **Claude Token Usage:** ~3000 tokens per query (~$0.01-0.02 cost)
- **Cache Hit Rate:** Typically 50%+ with repeat users

## Deployment & Security Considerations

- ✅ Stateless API (ready for horizontal scaling)
- ✅ CORS enabled for local development
- ⚠️ **Production Notes:** Add API rate-limiting, authentication, and consider removing CORS for production use
- ⚠️ Ensure `ANTHROPIC_API_KEY` is never committed or logged
