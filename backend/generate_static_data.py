#!/usr/bin/env python3
"""
Generate Static Data for GitHub Pages Deployment
Generates pre-cached responses for all popular problems and exports as data.json
This enables fully static GitHub Pages deployment without backend API calls
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from transcript_processor import TranscriptProcessor
from solution_generator import SolutionGenerator

class StaticDataGenerator:
    """Generate pre-cached responses for static site deployment"""

    def __init__(self, transcripts_dir: Path = None, demo_mode: bool = False):
        """Initialize generator with transcript processor"""
        if transcripts_dir is None:
            transcripts_dir = Path(__file__).parent.parent

        self.transcripts_dir = Path(transcripts_dir)
        self.demo_mode = demo_mode
        self.output_path = Path(__file__).parent.parent / "data.json"

        print(f"📁 Loading transcripts from: {self.transcripts_dir}")
        self.processor = TranscriptProcessor(self.transcripts_dir)
        self.generator = SolutionGenerator(self.processor, demo_mode=demo_mode)

    def generate_all_data(self) -> Dict:
        """Generate complete static data package"""
        print("\n🔄 Generating static data...")

        data = {
            "metadata": {
                "generated": datetime.now().isoformat(),
                "version": "1.0",
                "source": "WWLD Backend",
                "total_problems": len(self.generator.POPULAR_PROBLEMS),
                "total_solutions": len(self.generator.POPULAR_PROBLEMS) * 3,
                "note": "Pre-generated responses for GitHub Pages static deployment"
            },
            "responses": {},
            "speakers": self._generate_speakers_list(),
            "categories": list(self.generator.PROBLEM_CATEGORIES.keys()),
            "popular_problems": self.generator.POPULAR_PROBLEMS
        }

        # Generate solutions for each popular problem
        for i, problem in enumerate(self.generator.POPULAR_PROBLEMS, 1):
            print(f"\n[{i}/{len(self.generator.POPULAR_PROBLEMS)}] Generating solutions for:")
            print(f"   📌 {problem}")

            try:
                result = self.generator.generate_solutions(problem, num_solutions=3)

                # Normalize problem key (lowercase, for lookups)
                problem_key = problem.lower()
                data["responses"][problem_key] = result

                # Show what we got
                num_solutions = len(result.get("solutions", []))
                print(f"   ✅ Generated {num_solutions} solutions")

                if num_solutions > 0:
                    for sol in result["solutions"]:
                        print(f"      • {sol['speaker']}")

            except Exception as e:
                print(f"   ⚠️  Error generating solutions: {str(e)}")
                continue

        return data

    def _generate_speakers_list(self) -> List[Dict]:
        """Generate list of all speakers with metadata"""
        speakers = []

        # Get all unique speakers from categories
        all_speakers = set()
        for speakers_list in self.generator.PROBLEM_CATEGORIES.values():
            all_speakers.update(speakers_list)

        for speaker_name in sorted(all_speakers):
            role = self.processor.get_speaker_role(speaker_name)
            episodes = self.processor.get_speaker_episodes(speaker_name) or []

            speakers.append({
                "name": speaker_name,
                "role": role,
                "episodes_count": len(episodes),
                "icon": self.generator._get_speaker_icon(speaker_name)
            })

        return speakers

    def save_data(self, data: Dict) -> Path:
        """Save data to JSON file"""
        print(f"\n💾 Saving to: {self.output_path}")

        try:
            with open(self.output_path, 'w') as f:
                json.dump(data, f, indent=2)

            file_size = self.output_path.stat().st_size
            print(f"✅ Successfully saved ({file_size:,} bytes)")

            return self.output_path

        except Exception as e:
            print(f"❌ Error saving data: {str(e)}")
            raise

    def run(self) -> bool:
        """Generate and save all static data"""
        try:
            data = self.generate_all_data()
            self.save_data(data)

            print("\n" + "="*60)
            print("✅ Static data generation complete!")
            print("="*60)
            print(f"📊 Summary:")
            print(f"   • Total problems: {len(data['popular_problems'])}")
            print(f"   • Total speakers: {len(data['speakers'])}")
            print(f"   • Categories: {len(data['categories'])}")
            print(f"   • Output file: {self.output_path}")
            print(f"   • Generated: {data['metadata']['generated']}")
            print("\n🚀 Ready for GitHub Pages deployment!")

            return True

        except Exception as e:
            print(f"\n❌ Generation failed: {str(e)}")
            return False


def main():
    """Main entry point"""
    # Check for API key
    has_api_key = bool(os.getenv('ANTHROPIC_API_KEY'))
    demo_mode = not has_api_key

    if demo_mode:
        print("⚠️  No ANTHROPIC_API_KEY found. Running in demo mode with sample data.")
        print("   Set ANTHROPIC_API_KEY environment variable for real Claude responses.\n")
    else:
        print("✅ ANTHROPIC_API_KEY detected. Using Claude for real responses.\n")

    # Find transcripts directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    # Generate data
    generator = StaticDataGenerator(
        transcripts_dir=project_root,
        demo_mode=demo_mode
    )

    success = generator.run()
    exit(0 if success else 1)


if __name__ == "__main__":
    main()
