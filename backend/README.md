# WWLD Backend - What Would Lenny Do?

A production-ready backend that extracts real quotes and advice from Lenny's 300+ podcast transcripts using Claude AI.

## Features

- **Real Quote Extraction**: Uses Claude to find and extract actual advice from transcripts
- **Semantic Problem Categorization**: Automatically categorizes user problems to find relevant speakers
- **Solution Generation**: Returns 3+ expert perspectives with frameworks and real quotes
- **Intelligent Caching**: Caches solutions to reduce API costs
- **Fast Initialization**: Loads all 300+ transcripts on startup
- **RESTful API**: Simple endpoints for querying solutions

## Architecture

```
Frontend (HTML/JS)
        ↓
    FastAPI Backend
        ↓
    ┌─────────────────────┐
    │ Solution Generator  │ (Uses Claude 3.5 Sonnet)
    │ - Categorizes problems
    │ - Finds relevant speakers
    │ - Extracts quotes
    └─────────────────────┘
        ↓
    ┌─────────────────────┐
    │ Transcript Processor│
    │ - Loads all .txt files
    │ - Indexes speakers
    │ - Enables search
    └─────────────────────┘
        ↓
    ┌─────────────────────┐
    │ Cache Manager       │
    │ - File-based cache
    │ - Reduces API calls
    └─────────────────────┘
```

## Setup

### 1. Install Dependencies

```bash
cd /Users/jeevan.patil/Downloads/Lenny/backend
pip install -r requirements.txt
```

### 2. Set Environment Variables

```bash
# Get your API key from https://console.anthropic.com
export ANTHROPIC_API_KEY="your-api-key-here"
```

### 3. Run Backend

```bash
python main.py
```

Server starts at: `http://localhost:8000`

### 4. Test the Backend

In another terminal:

```bash
python test_backend.py
```

## API Endpoints

### Main Endpoint: Ask Lenny

**POST** `/ask`

Request:
```json
{
  "problem": "How do I know if we have product-market fit?",
  "num_solutions": 3,
  "problem_category": null
}
```

Response:
```json
{
  "problem": "How do I know if we have product-market fit?",
  "category": "product-market-fit",
  "solutions": [
    {
      "speaker": "Sean Ellis",
      "speaker_role": "Growth Expert & PMF Pioneer",
      "icon": "📈",
      "insight": "Product-market fit is when your customer growth accelerates and becomes self-sustaining. You'll know it when users are begging for your product.",
      "framework": "growth loop",
      "framework2": "retention metrics",
      "episode_name": "Sean Ellis",
      "episode_timestamp": "00:12:34",
      "confidence": 0.85
    }
  ]
}
```

### Get Popular Problems

**GET** `/problems`

Returns list of 10 popular problems users can ask about.

### Get All Speakers

**GET** `/speakers`

Returns list of all 300+ speakers in transcripts.

### Get Transcripts Info

**GET** `/transcripts`

Returns metadata about all loaded transcripts.

### Search Transcripts

**POST** `/search`

Request:
```json
{
  "keyword": "product-market fit",
  "limit": 5
}
```

### Cache Statistics

**GET** `/cache/stats`

Returns info about cached solutions and cache size.

**DELETE** `/cache/clear`

Clears all cached solutions.

## How It Works

### Problem Categorization

When a user submits a problem:

1. Backend analyzes keywords in the problem
2. Maps to one of 10 problem categories
3. Identifies 3 most relevant speakers for that category
4. Fetches their transcripts

### Quote Extraction

For each relevant speaker:

1. Backend retrieves their transcript
2. Sends transcript + problem to Claude 3.5 Sonnet
3. Claude finds the most relevant insight/quote that addresses the problem
4. Claude extracts frameworks and concepts mentioned
5. Returns structured solution

### Caching

- Solutions are cached using MD5 hash of problem + category
- First call to API hits Claude, subsequent calls use cache
- Cache persists across server restarts
- Can be cleared with `/cache/clear` endpoint

## Problem Categories

- `product-market-fit`: Determining if you have PMF
- `product-eng-conflict`: Product-engineering team dynamics
- `prioritization`: Deciding what to build next
- `team-burnout`: Managing team health and burnout
- `go-to-market`: Launch and marketing strategy
- `building-teams`: Hiring and structuring product teams
- `data-driven`: Data, metrics, and analytics
- `communication`: Communication and messaging
- `scaling`: Growing without losing culture
- `pricing`: Pricing and monetization

## Key Speakers by Category

### Product-Market Fit
- Sean Ellis
- Brian Balfour
- Marty Cagan

### Product-Engineering Conflict
- Brian Chesky (Airbnb CEO)
- Marty Cagan
- Will Larson

### Prioritization
- Jake Knapp + John Zeratsky
- Richard Rumelt
- Itamar Gilad

### Team Burnout
- Andy Johns
- Jason Fried
- Jerry Colonna

### Go-to-Market
- Jason M Lemkin (SaaS expert)
- April Dunford (positioning)
- Andy Raskin (messaging)

## Performance

- **Transcript Loading**: ~2 seconds
- **Problem Categorization**: <100ms
- **Cache Hit**: ~50ms
- **Claude API Call**: 2-5 seconds
- **Full Solution Generation**: 2-5 seconds (first call), <100ms (cached)

## Costs

- Each `/ask` call with new problem: ~$0.02-0.05 (Claude API)
- Cached calls: Free
- Estimated cost for 100 unique problems: $2-5

## Customization

### Add More Problem Categories

Edit `solution_generator.py`:

```python
PROBLEM_CATEGORIES = {
    "your-category": [
        "Speaker Name 1",
        "Speaker Name 2",
        "Speaker Name 3"
    ]
}
```

### Modify Insight Extraction

Edit the prompt in `_extract_insight_with_claude()` method in `solution_generator.py`.

### Change Cache Location

```python
cache_manager = CacheManager(cache_dir=Path("/custom/path"))
```

## Development

### Run with Auto-Reload

```bash
python main.py
# or
uvicorn main:app --reload
```

### Interactive API Docs

While server is running, visit:
```
http://localhost:8000/docs
```

This provides interactive Swagger UI to test all endpoints.

### Debugging

Enable verbose logging:

```python
# In main.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Production Deployment

### Using Gunicorn

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 main:app
```

### Using Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables

```bash
ANTHROPIC_API_KEY=your-key
TRANSCRIPTS_DIR=/path/to/transcripts
CACHE_DIR=/path/to/cache
```

## Limitations

- Transcript search uses regex/keyword matching (not semantic search yet)
- Quote extraction depends on transcript structure
- Some episodes may have formatting inconsistencies
- Claude may occasionally not find relevant content

## Future Enhancements

- [ ] Semantic search using embeddings
- [ ] Episode timestamp extraction and linking
- [ ] Multi-speaker collaborative solutions
- [ ] User feedback loop to improve categorization
- [ ] Advanced filtering (company stage, industry, etc.)
- [ ] Export solutions as PDF playbooks
- [ ] Persistent database for solutions
- [ ] Rate limiting and authentication

## Support

- Check logs for API errors
- Use `/health` endpoint to verify backend is running
- Test with `/problems` endpoint to see popular queries
- Clear cache if getting stale results: `DELETE /cache/clear`

## License

MIT
