"""
CacheManager - Cache solutions to avoid repeated Claude API calls
"""

import json
from pathlib import Path
import hashlib
from datetime import datetime

class CacheManager:
    """Simple file-based caching for solutions"""

    def __init__(self, cache_dir: Path = None):
        self.cache_dir = cache_dir or Path(__file__).parent / ".cache"
        self.cache_dir.mkdir(exist_ok=True)
        self.index_file = self.cache_dir / "index.json"
        self.index = self._load_index()

    def _get_cache_key(self, problem: str, category: str) -> str:
        """Generate cache key from problem and category"""
        key_str = f"{problem.lower()}:{category}".encode()
        return hashlib.md5(key_str).hexdigest()

    def get(self, problem: str, category: str) -> dict or None:
        """Retrieve cached solution"""
        key = self._get_cache_key(problem, category)
        cache_file = self.cache_dir / f"{key}.json"

        if cache_file.exists():
            try:
                with open(cache_file, 'r') as f:
                    return json.load(f)
            except:
                pass

        return None

    def set(self, problem: str, category: str, solution: dict) -> None:
        """Cache a solution"""
        key = self._get_cache_key(problem, category)
        cache_file = self.cache_dir / f"{key}.json"

        try:
            with open(cache_file, 'w') as f:
                json.dump(solution, f)

            self.index[key] = {
                "problem": problem,
                "category": category,
                "timestamp": datetime.now().isoformat()
            }
            self._save_index()
        except Exception as e:
            print(f"⚠️  Cache write error: {str(e)}")

    def _load_index(self) -> dict:
        """Load cache index"""
        if self.index_file.exists():
            try:
                with open(self.index_file, 'r') as f:
                    return json.load(f)
            except:
                pass

        return {}

    def _save_index(self) -> None:
        """Save cache index"""
        try:
            with open(self.index_file, 'w') as f:
                json.dump(self.index, f, indent=2)
        except Exception as e:
            print(f"⚠️  Index write error: {str(e)}")

    def clear(self) -> None:
        """Clear all cache"""
        for cache_file in self.cache_dir.glob("*.json"):
            if cache_file.name != "index.json":
                cache_file.unlink()

        self.index = {}
        self._save_index()

    def get_stats(self) -> dict:
        """Get cache statistics"""
        cache_files = list(self.cache_dir.glob("*.json"))
        return {
            "cached_solutions": len([f for f in cache_files if f.name != "index.json"]),
            "cache_dir": str(self.cache_dir),
            "index": self.index
        }
