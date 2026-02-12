"""
TranscriptProcessor - Load and parse Lenny's podcast transcripts
"""

from pathlib import Path
from typing import List, Dict, Optional
import re
from collections import defaultdict

class TranscriptProcessor:
    """Load and index all transcripts for efficient searching"""

    def __init__(self, transcripts_dir: Path):
        self.transcripts_dir = Path(transcripts_dir)
        self.transcripts = {}  # {filename: content}
        self.speakers = {}  # {speaker_name: [episodes]}
        self.episodes = {}  # {episode_name: {speaker, content, etc}}
        self.speaker_roles = {}  # {speaker_name: role description}

        self._load_all_transcripts()
        self._extract_speakers()

    def _load_all_transcripts(self):
        """Load all .txt transcript files"""
        print("📖 Loading transcripts...")

        txt_files = list(self.transcripts_dir.glob("*.txt"))
        print(f"   Found {len(txt_files)} transcript files")

        for file_path in txt_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if content.strip():
                        episode_name = file_path.stem
                        self.transcripts[episode_name] = content
                        self.episodes[episode_name] = {
                            "name": episode_name,
                            "file_path": str(file_path),
                            "content": content,
                            "size_kb": len(content) / 1024
                        }
            except Exception as e:
                print(f"   ⚠️  Failed to load {file_path.name}: {str(e)}")

        print(f"   ✅ Loaded {len(self.transcripts)} transcripts successfully")

    def _extract_speakers(self):
        """Extract speaker names and roles from transcripts"""
        print("🎤 Extracting speakers...")

        for episode_name, content in self.transcripts.items():
            # Extract speaker name from filename (usually "Speaker Name.txt")
            speaker_name = episode_name

            if speaker_name not in self.speakers:
                self.speakers[speaker_name] = []

            self.speakers[speaker_name].append(episode_name)

            # Try to extract role from content
            if speaker_name not in self.speaker_roles:
                role = self._extract_role_from_content(content, speaker_name)
                self.speaker_roles[speaker_name] = role

        print(f"   ✅ Found {len(self.speakers)} unique speakers")

    def _extract_role_from_content(self, content: str, speaker_name: str) -> str:
        """
        Try to extract speaker's role from transcript intro

        Pattern: Usually appears in first 1000 chars with titles like:
        "CEO of X", "VP of Y", "Founder of Z", "Growth Expert", etc.
        """
        # Look for common patterns in first 2000 characters
        intro = content[:2000]

        patterns = [
            r"(?:CEO|President|Founder|VP|Head|Director|Chief|Co-founder|Partner)",
            r"(?:Manager|Leader|Expert|Strategist|Engineer|Designer)",
            r"(?:at|of)\s+([A-Za-z\s&]+?)(?:\.|,|;)",
        ]

        for pattern in patterns:
            match = re.search(pattern, intro, re.IGNORECASE)
            if match:
                return match.group(0)

        # Default fallback
        return "Podcast Guest & Expert"

    @property
    def transcript_count(self) -> int:
        """Total number of transcripts loaded"""
        return len(self.transcripts)

    def get_all_speakers(self) -> List[str]:
        """Get list of all speakers"""
        return list(self.speakers.keys())

    def get_transcript_names(self) -> List[str]:
        """Get list of all transcript names"""
        return list(self.transcripts.keys())

    def get_speaker_episodes(self, speaker_name: str) -> List[str]:
        """Get all episodes featuring a speaker"""
        return self.speakers.get(speaker_name, [])

    def get_speaker_role(self, speaker_name: str) -> str:
        """Get speaker's role description"""
        return self.speaker_roles.get(speaker_name, "Podcast Guest")

    def get_transcript_content(self, episode_name: str) -> str:
        """Get full transcript content for an episode"""
        return self.transcripts.get(episode_name, "")

    def get_episode_info(self, episode_name: str) -> dict:
        """Get episode metadata"""
        return self.episodes.get(episode_name, {})

    def search_transcripts(self, keyword: str, limit: int = 5) -> List[Dict]:
        """
        Search transcripts for keyword matches

        Returns list of matching segments with context
        """
        results = []
        keyword_lower = keyword.lower()

        for episode_name, content in self.transcripts.items():
            if keyword_lower in content.lower():
                # Find all occurrences
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if keyword_lower in line.lower():
                        # Get context (previous and next line)
                        context_start = max(0, i - 1)
                        context_end = min(len(lines), i + 2)
                        context = ' '.join(lines[context_start:context_end])

                        results.append({
                            "episode": episode_name,
                            "speaker": episode_name,
                            "match": line.strip(),
                            "context": context.strip(),
                            "relevance": 0.8  # Placeholder
                        })

                if len(results) >= limit:
                    return results[:limit]

        return results

    def get_relevant_segments(self, topic: str, episode_name: str, max_segments: int = 5) -> List[Dict]:
        """
        Get relevant segments from an episode based on topic

        Uses keyword matching and heuristics to find relevant quotes
        """
        content = self.get_transcript_content(episode_name)
        if not content:
            return []

        # Split by speaker (heuristic: lines starting with names/timestamps)
        segments = re.split(r'\n(?=[A-Z][a-z\s]+\s*\()', content)

        relevant = []
        topic_lower = topic.lower()

        for segment in segments:
            # Check if segment is relevant to topic
            if topic_lower in segment.lower():
                # Extract speaker name
                speaker_match = re.match(r'([^(]+)\s*\(', segment)
                speaker = speaker_match.group(1).strip() if speaker_match else episode_name

                # Extract timestamp
                time_match = re.search(r'\((\d{2}:\d{2}:\d{2})\)', segment)
                timestamp = time_match.group(1) if time_match else None

                # Clean up segment text
                clean_text = re.sub(r'\([^)]*\)', '', segment).strip()
                if len(clean_text) > 50:  # Only include substantial segments
                    relevant.append({
                        "speaker": speaker,
                        "timestamp": timestamp,
                        "text": clean_text[:500],  # First 500 chars
                        "relevance": 0.85
                    })

            if len(relevant) >= max_segments:
                break

        return relevant

    def get_transcript_stats(self) -> dict:
        """Get statistics about all transcripts"""
        total_chars = sum(len(content) for content in self.transcripts.values())
        avg_chars = total_chars / len(self.transcripts) if self.transcripts else 0

        return {
            "total_transcripts": len(self.transcripts),
            "total_speakers": len(self.speakers),
            "total_characters": total_chars,
            "average_transcript_length": avg_chars,
            "largest_episode": max(
                self.episodes.items(),
                key=lambda x: len(x[1]["content"])
            )[0] if self.episodes else None
        }
