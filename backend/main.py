"""
WWLD Backend - What Would Lenny Do?
Extracts real quotes and advice from Lenny's podcast transcripts using Claude AI
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
import json
from pathlib import Path
from transcript_processor import TranscriptProcessor
from solution_generator import SolutionGenerator
from cache_manager import CacheManager

# Initialize FastAPI app
app = FastAPI(
    title="WWLD Backend",
    description="Extract wisdom from Lenny's podcast transcripts",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize processors
transcript_processor = None
solution_generator = None
cache_manager = None

class ProblemQuery(BaseModel):
    problem: str
    num_solutions: int = 3
    problem_category: Optional[str] = None  # Optional: can be pre-categorized

class Solution(BaseModel):
    speaker: str
    speaker_role: str
    icon: str
    insight: str
    framework: str
    framework2: str
    episode_name: str
    episode_timestamp: str = None
    confidence: float

class ResultResponse(BaseModel):
    problem: str
    category: str
    solutions: list

# ===== ROUTES =====

@app.on_event("startup")
async def startup_event():
    """Initialize processors on startup"""
    global transcript_processor, solution_generator, cache_manager

    # Use TRANSCRIPTS_DIR env var or default to current directory
    transcripts_dir = Path(os.getenv('TRANSCRIPTS_DIR', '.'))

    print("🚀 Initializing WWLD Backend...")
    print(f"📁 Loading transcripts from: {transcripts_dir}")

    # Enable demo mode if no API credentials available
    demo_mode = not os.getenv('ANTHROPIC_API_KEY')

    transcript_processor = TranscriptProcessor(transcripts_dir)
    solution_generator = SolutionGenerator(transcript_processor, demo_mode=demo_mode)
    cache_manager = CacheManager()

    print(f"✅ Loaded {transcript_processor.transcript_count} transcripts")
    print(f"✅ Cache manager initialized")
    if demo_mode:
        print(f"📋 Running in DEMO MODE (no API credentials found)")
    print(f"✅ Ready to generate solutions")

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "transcripts_loaded": transcript_processor.transcript_count if transcript_processor else 0
    }

@app.post("/ask", response_model=ResultResponse)
async def ask_lenny(query: ProblemQuery):
    """
    Main endpoint: Ask Lenny for advice on a problem

    Takes a problem description and returns 3+ expert solutions with real quotes
    """
    if not transcript_processor or not solution_generator:
        raise HTTPException(status_code=503, detail="Processors not initialized")

    try:
        # Determine category
        category = query.problem_category or solution_generator.categorize_problem(query.problem)

        # Check cache first
        cached = cache_manager.get(query.problem, category)
        if cached:
            print(f"📦 Cache hit for: {query.problem[:50]}...")
            return cached

        # Generate solutions based on problem
        result = solution_generator.generate_solutions(
            problem=query.problem,
            num_solutions=query.num_solutions,
            category=category
        )

        # Cache the result
        cache_manager.set(query.problem, category, result)

        return result

    except Exception as e:
        print(f"❌ Error generating solutions: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/problems")
async def get_popular_problems():
    """Get list of popular problems from transcripts"""
    if not solution_generator:
        raise HTTPException(status_code=503, detail="Processors not initialized")

    return {
        "problems": solution_generator.get_popular_problems()
    }

@app.get("/speakers")
async def get_speakers():
    """Get list of all speakers in transcripts"""
    if not transcript_processor:
        raise HTTPException(status_code=503, detail="Processors not initialized")

    return {
        "speakers": transcript_processor.get_all_speakers(),
        "count": len(transcript_processor.get_all_speakers())
    }

@app.get("/transcripts")
async def get_transcripts_info():
    """Get info about loaded transcripts"""
    if not transcript_processor:
        raise HTTPException(status_code=503, detail="Processors not initialized")

    return {
        "total_transcripts": transcript_processor.transcript_count,
        "transcripts": transcript_processor.get_transcript_names()
    }

@app.post("/search")
async def search_transcripts(query: dict):
    """
    Search transcripts by keyword or topic

    query = {
        "keyword": "string to search for",
        "limit": 5
    }
    """
    if not transcript_processor:
        raise HTTPException(status_code=503, detail="Processors not initialized")

    keyword = query.get("keyword")
    limit = query.get("limit", 5)

    if not keyword:
        raise HTTPException(status_code=400, detail="keyword required")

    results = transcript_processor.search_transcripts(keyword, limit)
    return {
        "keyword": keyword,
        "results": results,
        "count": len(results)
    }

@app.get("/cache/stats")
async def get_cache_stats():
    """Get cache statistics"""
    if not cache_manager:
        raise HTTPException(status_code=503, detail="Cache not initialized")

    return cache_manager.get_stats()

@app.delete("/cache/clear")
async def clear_cache():
    """Clear all cached solutions"""
    if not cache_manager:
        raise HTTPException(status_code=503, detail="Cache not initialized")

    cache_manager.clear()
    return {"message": "Cache cleared successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
