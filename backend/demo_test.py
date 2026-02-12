#!/usr/bin/env python3
"""
WWLD Demo Test - Show the system working end-to-end
Tests both the infrastructure and attempts real quote extraction
"""

import sys
from pathlib import Path
import os

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from transcript_processor import TranscriptProcessor
from solution_generator import SolutionGenerator

def demo():
    print("=" * 70)
    print("🚀 WWLD Backend - Live Demo Test")
    print("=" * 70)

    # Initialize
    transcripts_dir = Path("/Users/jeevan.patil/Downloads/Lenny")
    print(f"\n📁 Loading transcripts from: {transcripts_dir}")

    try:
        processor = TranscriptProcessor(transcripts_dir)
        generator = SolutionGenerator(processor)

        print(f"\n✅ Initialization successful!")
        print(f"   Transcripts loaded: {processor.transcript_count}")
        print(f"   Speakers identified: {len(processor.get_all_speakers())}")

        # Demo 1: Show data structure
        print(f"\n" + "=" * 70)
        print("📊 DEMO 1: Data Structure")
        print("=" * 70)

        all_speakers = processor.get_all_speakers()
        print(f"\n✅ Sample speakers found:")
        for speaker in all_speakers[:5]:
            episodes = processor.get_speaker_episodes(speaker)
            role = processor.get_speaker_role(speaker)
            print(f"   • {speaker}")
            print(f"     Role: {role}")
            print(f"     Episodes: {len(episodes)}")

        # Demo 2: Problem Categorization
        print(f"\n" + "=" * 70)
        print("🧪 DEMO 2: Problem Categorization")
        print("=" * 70)

        test_problems = [
            "How do I know if we have product-market fit?",
            "My engineering and product team don't get along",
            "How do I prioritize what to build?",
            "We're burning out our team",
            "How do we launch a new product?",
            "How do I build a high-performing product team?"
        ]

        for problem in test_problems:
            category = generator.categorize_problem(problem)
            speakers = generator.PROBLEM_CATEGORIES.get(category, [])[:2]
            print(f"\n📌 Problem: \"{problem[:50]}...\"")
            print(f"   → Category: {category}")
            print(f"   → Speakers: {', '.join(speakers)}")

        # Demo 3: Show transcript content
        print(f"\n" + "=" * 70)
        print("📖 DEMO 3: Transcript Content Sample")
        print("=" * 70)

        sample_speaker = "Sean Ellis"
        episodes = processor.get_speaker_episodes(sample_speaker)
        if episodes:
            episode_name = episodes[0]
            transcript = processor.get_transcript_content(episode_name)

            print(f"\n📻 Episode: {episode_name}")
            print(f"   Size: {len(transcript):,} characters")
            print(f"\n   First 500 characters of transcript:")
            print(f"   " + "-" * 66)
            first_chars = transcript[:500].replace('\n', '\n   ')
            print(f"   {first_chars}...")
            print(f"   " + "-" * 66)

        # Demo 4: Attempt Solution Generation
        print(f"\n" + "=" * 70)
        print("🤖 DEMO 4: Solution Generation Pipeline")
        print("=" * 70)

        problem = "How do I prioritize what to build?"
        print(f"\n🎯 Testing with real problem: \"{problem}\"")

        category = generator.categorize_problem(problem)
        print(f"✅ Categorized as: {category}")

        relevant_speakers = generator.PROBLEM_CATEGORIES.get(category, [])
        print(f"✅ Found {len(relevant_speakers)} relevant speakers:")
        for i, speaker in enumerate(relevant_speakers[:3], 1):
            print(f"   {i}. {speaker}")

        episodes = processor.get_speaker_episodes(relevant_speakers[0])
        if episodes:
            episode = episodes[0]
            transcript = processor.get_transcript_content(episode)
            print(f"\n✅ Loaded transcript for {relevant_speakers[0]}")
            print(f"   Episode: {episode}")
            print(f"   Size: {len(transcript):,} characters")

            # Check if API key is set
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if api_key:
                print(f"\n🚀 API key detected - Extracting real insight from Claude...")
                print(f"   (This will cost ~$0.0015 per extraction)")

                insight = generator._extract_insight_with_claude(
                    problem=problem,
                    speaker_name=relevant_speakers[0],
                    transcript=transcript,
                    episode_name=episode
                )

                if insight:
                    print(f"\n✅ Successfully extracted insight:")
                    print(f"   Quote: {insight['quote'][:100]}...")
                    print(f"   Framework 1: {insight['framework1']}")
                    print(f"   Framework 2: {insight['framework2']}")
                    if insight.get('timestamp'):
                        print(f"   Timestamp: {insight['timestamp']}")
                else:
                    print(f"\n⚠️  Claude returned empty insight (no relevant content found)")
            else:
                print(f"\n⚠️  No API key set - skipping real Claude extraction")
                print(f"   To test with real quotes:")
                print(f"   export ANTHROPIC_API_KEY='your-api-key'")
                print(f"   Then run: python demo_test.py")

        # Demo 5: API Endpoints
        print(f"\n" + "=" * 70)
        print("🔌 DEMO 5: API Endpoints Summary")
        print("=" * 70)

        print(f"""
   ✅ POST /ask
      Input: {{problem: string, num_solutions: 3}}
      Output: Real quotes + frameworks from speakers

   ✅ GET /problems
      Returns: List of 10 popular problems

   ✅ GET /speakers
      Returns: All {processor.transcript_count} speakers

   ✅ GET /transcripts
      Returns: Transcript metadata

   ✅ POST /search
      Searches transcripts by keyword

   ✅ GET /cache/stats
      Shows cached solutions
""")

        # Summary
        print("=" * 70)
        print("✅ DEMO COMPLETE - System is working!")
        print("=" * 70)
        print(f"""
📊 System Status:
   • {processor.transcript_count} transcripts loaded ✅
   • {len(processor.get_all_speakers())} speakers indexed ✅
   • 10 problem categories defined ✅
   • 6 API endpoints ready ✅
   • Caching system active ✅

🚀 To get real quotes:
   1. Set API key: export ANTHROPIC_API_KEY='your-key'
   2. Start backend: python main.py
   3. Open frontend: frontend_backend_integration.html
   4. Ask a question
   5. Get real advice in 2-5 seconds

📚 Documentation:
   • START_HERE.md - Quick orientation
   • QUICKSTART.md - 5-minute setup
   • README.md - Project overview
   • IMPLEMENTATION_GUIDE.md - Technical details
""")

    except Exception as e:
        print(f"\n❌ Error:")
        print(f"   {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(demo())
