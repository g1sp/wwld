#!/usr/bin/env python3
"""
Test script for WWLD Backend
Test the solution generation pipeline
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from transcript_processor import TranscriptProcessor
from solution_generator import SolutionGenerator
from cache_manager import CacheManager

def main():
    print("=" * 60)
    print("🚀 WWLD Backend Test Suite")
    print("=" * 60)

    # Initialize
    import os
    transcripts_dir = Path(os.getenv('TRANSCRIPTS_DIR', Path(__file__).parent.parent))
    print(f"\n📁 Loading transcripts from: {transcripts_dir}")

    try:
        processor = TranscriptProcessor(transcripts_dir)
        generator = SolutionGenerator(processor)
        cache = CacheManager()

        print(f"\n✅ Initialization successful!")
        print(f"   Transcripts loaded: {processor.transcript_count}")
        print(f"   Speakers identified: {len(processor.get_all_speakers())}")

        # Print stats
        stats = processor.get_transcript_stats()
        print(f"\n📊 Transcript Statistics:")
        print(f"   Total characters: {stats['total_characters']:,}")
        print(f"   Average length: {stats['average_transcript_length']:,.0f} chars")
        print(f"   Largest episode: {stats['largest_episode']}")

        # Test problem categorization
        print(f"\n🧪 Testing Problem Categorization:")
        test_problems = [
            "How do I know if we have product-market fit?",
            "My engineering and product team don't get along",
            "How do I prioritize what to build?",
            "We're burning out our team"
        ]

        for problem in test_problems:
            category = generator.categorize_problem(problem)
            print(f"   '{problem[:50]}...' → {category}")

        # Test solution generation
        print(f"\n🔍 Testing Solution Generation (this will call Claude API):")
        print(f"   Note: First call will hit API, subsequent calls use cache")

        test_query = "How do I know if we have product-market fit?"
        print(f"\n   Problem: {test_query}")

        # First call (should hit Claude)
        print(f"\n   🔄 Generating solutions (1st call - Claude API)...")
        result1 = generator.generate_solutions(problem=test_query)

        print(f"\n   Results received:")
        print(f"   Category: {result1['category']}")
        print(f"   Solutions found: {len(result1['solutions'])}")

        for i, sol in enumerate(result1['solutions'], 1):
            print(f"\n   Solution {i}:")
            print(f"      Speaker: {sol['speaker']}")
            print(f"      Role: {sol['speaker_role']}")
            print(f"      Quote: {sol['insight'][:100]}...")
            print(f"      Frameworks: {sol['framework']}, {sol['framework2']}")
            print(f"      Episode: {sol['episode_name']}")

        # Test caching
        print(f"\n   💾 Testing cache...")
        cache_stats = cache.get_stats()
        print(f"   Cached solutions: {cache_stats['cached_solutions']}")

        print(f"\n✅ Test completed successfully!")

    except Exception as e:
        print(f"\n❌ Test failed with error:")
        print(f"   {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
