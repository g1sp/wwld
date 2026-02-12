"""
SolutionGenerator - Use Claude to extract relevant wisdom from transcripts
Uses AWS Bedrock for Claude API access
"""

import boto3
import json
import re
from transcript_processor import TranscriptProcessor
from typing import Optional, Dict, List

class SolutionGenerator:
    """Generate solutions by asking Claude to search transcripts"""

    # Map of problem keywords to relevant episodes
    PROBLEM_CATEGORIES = {
        "product-market-fit": [
            "Sean Ellis",
            "Brian Balfour",
            "Marty Cagan",
            "Sean Ellis",
            "Andrew Wilkinson"
        ],
        "product-eng-conflict": [
            "Brian Chesky",
            "Marty Cagan",
            "Will Larson",
            "Camille Fournier"
        ],
        "prioritization": [
            "Marty Cagan",
            "Richard Rumelt",
            "Jake Knapp + John Zeratsky",
            "Itamar Gilad"
        ],
        "team-burnout": [
            "Andy Johns",
            "Jason Fried",
            "Jerry Colonna",
            "Eric Ries"
        ],
        "go-to-market": [
            "Jason M Lemkin",
            "April Dunford",
            "Andy Raskin",
            "Sean Ellis"
        ],
        "building-teams": [
            "Marty Cagan",
            "Ken Norton",
            "Melissa Perri",
            "Camille Fournier"
        ],
        "data-driven": [
            "Ronny Kohavi",
            "Nicole Forsgren",
            "Patrick Campbell",
            "Sean Ellis"
        ],
        "communication": [
            "Nancy Duarte",
            "Kim Scott",
            "Matt Abrahams",
            "Andy Raskin"
        ],
        "scaling": [
            "Eric Ries",
            "Bill Carr",
            "Boz",
            "Shishir Mehrotra"
        ],
        "pricing": [
            "Jason M Lemkin",
            "Madhavan Ramanujam",
            "Eli Schwartz",
            "Patrick Campbell"
        ]
    }

    # Popular problems for discovery
    POPULAR_PROBLEMS = [
        "How do I know if we have product-market fit?",
        "My engineering and product team don't get along. How do I fix this?",
        "How do I prioritize what to build next?",
        "We're burning out our team. What should we do?",
        "How do we launch and market a new product?",
        "How do I build a high-performing product team?",
        "How do I make data-driven decisions?",
        "How do I communicate better with my CEO?",
        "How do we scale without losing culture?",
        "What's the right pricing strategy?"
    ]

    def __init__(self, transcript_processor: TranscriptProcessor, demo_mode: bool = False):
        self.processor = transcript_processor
        self.demo_mode = demo_mode
        if not demo_mode:
            self.bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1')

    def get_popular_problems(self) -> List[str]:
        """Return list of popular problems"""
        return self.POPULAR_PROBLEMS

    def categorize_problem(self, problem: str) -> str:
        """
        Categorize a problem to find relevant episodes

        Uses keyword matching and Claude if needed
        """
        problem_lower = problem.lower()

        # Direct keyword matching
        keyword_map = {
            "product-market fit": ["pmf", "product market", "fit", "traction", "growth accelerates"],
            "product-eng-conflict": ["product eng", "engineering", "team", "conflict", "collaboration"],
            "prioritization": ["prioriti", "what to build", "roadmap", "focus", "build"],
            "team-burnout": ["burnout", "team", "mental health", "stress", "unsustainable"],
            "go-to-market": ["launch", "marketing", "gtm", "go-to-market", "distribution"],
            "building-teams": ["building team", "hiring", "structure", "org", "people"],
            "data-driven": ["data", "metrics", "analytics", "measurement", "experiment"],
            "communication": ["communicat", "messaging", "story", "pitch", "influence"],
            "scaling": ["scale", "growth", "large", "organizational", "complexity"],
            "pricing": ["pricing", "monetiz", "price", "revenue", "unit economics"]
        }

        for category, keywords in keyword_map.items():
            if any(kw in problem_lower for kw in keywords):
                return category

        # Fallback to "product-market-fit" as default
        return "product-market-fit"

    def generate_solutions(
        self,
        problem: str,
        num_solutions: int = 3,
        category: Optional[str] = None
    ) -> Dict:
        """
        Generate solutions for a problem by extracting insights from transcripts

        Returns structured solutions with real quotes
        """
        # Categorize problem if not provided
        if not category:
            category = self.categorize_problem(problem)

        # Get relevant speakers/episodes for this problem
        relevant_speakers = self.PROBLEM_CATEGORIES.get(category, [])

        # Extract insights from relevant episodes
        solutions = []

        for i, speaker_name in enumerate(relevant_speakers[:num_solutions]):
            try:
                # Get transcript for this speaker
                episodes = self.processor.get_speaker_episodes(speaker_name)
                if not episodes:
                    continue

                # Use the first/largest episode for this speaker
                episode_name = episodes[0]
                transcript = self.processor.get_transcript_content(episode_name)
                role = self.processor.get_speaker_role(speaker_name)

                if not transcript:
                    continue

                # Use Claude to extract relevant insight
                insight = self._extract_insight_with_claude(
                    problem=problem,
                    speaker_name=speaker_name,
                    transcript=transcript,
                    episode_name=episode_name
                )

                if insight:
                    solutions.append({
                        "speaker": speaker_name,
                        "speaker_role": role,
                        "icon": self._get_speaker_icon(speaker_name),
                        "insight": insight["quote"],
                        "framework": insight["framework1"],
                        "framework2": insight["framework2"],
                        "episode_name": episode_name,
                        "episode_timestamp": insight.get("timestamp", ""),
                        "confidence": 0.85
                    })

            except Exception as e:
                print(f"⚠️  Error generating solution for {speaker_name}: {str(e)}")
                continue

        return {
            "problem": problem,
            "category": category,
            "solutions": solutions
        }

    def _extract_insight_with_claude(
        self,
        problem: str,
        speaker_name: str,
        transcript: str,
        episode_name: str
    ) -> Optional[Dict]:
        """
        Use Claude to extract a relevant insight/quote from a transcript
        In demo mode, returns sample insights without API calls

        Returns structured insight with quote and frameworks
        """
        if self.demo_mode:
            return self._get_demo_insight(problem, speaker_name, episode_name)

        # Limit transcript to first 8000 chars to avoid token limits
        truncated_transcript = transcript[:8000]

        prompt = f"""
You are an expert at extracting actionable advice from podcast transcripts.

PROBLEM: {problem}

TRANSCRIPT FROM {speaker_name}:
{truncated_transcript}

Your task:
1. Find the most relevant insight or quote from {speaker_name} that directly addresses the problem
2. Extract a concise, actionable quote (1-3 sentences max) that {speaker_name} actually said
3. Identify 1-2 frameworks or concepts mentioned
4. If you find a timestamp, include it (format: MM:SS or HH:MM:SS)

IMPORTANT:
- Only include actual quotes from the transcript, NOT paraphrased versions
- The quote must be verbatim or nearly verbatim from the text
- If no relevant content exists, respond with null

Respond in this exact JSON format (no markdown, just JSON):
{{
    "quote": "exact quote from transcript addressing the problem",
    "framework1": "framework or concept name",
    "framework2": "second framework or concept",
    "timestamp": "HH:MM:SS or null",
    "confidence": 0.85
}}

If no relevant insight found, respond with:
{{"quote": null}}
"""

        try:
            response = self.bedrock_client.invoke_model(
                modelId="anthropic.claude-instant-v1:2:100k",
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-06-01",
                    "max_tokens": 500,
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                })
            )

            response_body = json.loads(response['body'].read())
            response_text = response_body['content'][0]['text'].strip()

            # Parse JSON response
            result = json.loads(response_text)

            if result.get("quote"):
                return result
            else:
                return None

        except json.JSONDecodeError as e:
            print(f"⚠️  JSON parsing error: {str(e)}")
            if 'response_text' in locals():
                print(f"   Response was: {response_text[:200]}")
            return None
        except Exception as e:
            print(f"⚠️  Claude API error: {str(e)}")
            return None

    def _get_demo_insight(self, problem: str, speaker_name: str, episode_name: str) -> Optional[Dict]:
        """Return sample insights for demo mode without API calls"""
        demo_insights = {
            "Marty Cagan": {
                "quote": "Focus on the outcomes you want to achieve, not just shipping features. The best teams start with the customer problem and work backwards.",
                "framework1": "Problem-First Product Design",
                "framework2": "Outcome-Driven Roadmap",
                "timestamp": "12:34"
            },
            "Jake Knapp + John Zeratsky 2.0": {
                "quote": "Use the sprint methodology to make faster decisions. When you're faced with too many options, timeboxing forces you to make choices.",
                "framework1": "Design Sprint Framework",
                "framework2": "Time-Boxed Decision Making",
                "timestamp": "08:15"
            },
            "Richard Rumelt": {
                "quote": "Good strategy is about focusing on what truly matters. You can't do everything, so be clear about your constraints and priorities.",
                "framework1": "Strategic Focus",
                "framework2": "Constraint-Based Planning",
                "timestamp": "15:42"
            },
            "Sean Ellis": {
                "quote": "Product-market fit is when your customers love what you built so much they tell their friends. If you're not growing, you haven't found it yet.",
                "framework1": "Product-Market Fit Definition",
                "framework2": "Growth as Validation Signal",
                "timestamp": "05:20"
            }
        }

        # Return demo insight if speaker exists, otherwise generic
        if speaker_name in demo_insights:
            return demo_insights[speaker_name]

        return {
            "quote": f"Thoughtful approach to {problem.lower()} is key. Understanding your audience and iterating based on feedback helps you make better decisions.",
            "framework1": "Iterative Problem Solving",
            "framework2": "Customer-Centric Approach",
            "timestamp": "10:00"
        }

    def _get_speaker_icon(self, speaker_name: str) -> str:
        """Return an appropriate emoji icon for a speaker based on their expertise"""
        icon_map = {
            "Sean Ellis": "📈",
            "Brian Balfour": "🎯",
            "Marty Cagan": "🚀",
            "Brian Chesky": "🤝",
            "Will Larson": "⚙️",
            "Jake Knapp + John Zeratsky": "🎪",
            "Richard Rumelt": "🎪",
            "Itamar Gilad": "🔍",
            "Andy Johns": "❤️",
            "Jason Fried": "🏢",
            "Jerry Colonna": "🧘",
            "Jason M Lemkin": "📢",
            "April Dunford": "🎤",
            "Andy Raskin": "💬",
            "Ken Norton": "🎓",
            "Melissa Perri": "⚙️",
            "Ronny Kohavi": "📊",
            "Nicole Forsgren": "📊",
            "Nancy Duarte": "🎤",
            "Kim Scott": "💭",
            "Eric Ries": "🔬",
            "Bill Carr": "📚",
            "Boz": "👥",
            "Madhavan Ramanujam": "💰",
            "Eli Schwartz": "💰",
        }

        return icon_map.get(speaker_name, "💡")

    def _safe_json_parse(self, text: str) -> Dict:
        """Safely parse JSON from Claude response"""
        # Try direct parsing first
        try:
            return json.loads(text)
        except:
            pass

        # Try extracting JSON from code blocks
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except:
                pass

        # Try finding JSON object directly
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(0))
            except:
                pass

        return {}
