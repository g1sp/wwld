#!/bin/bash

# WWLD Backend Setup Script
# Automatically installs dependencies and validates setup

set -e

echo "🚀 WWLD Backend Setup"
echo "===================="
echo ""

# Check Python version
echo "✓ Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "  Python version: $python_version"

if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 9) else 1)"; then
    echo "❌ Python 3.9+ required"
    exit 1
fi

# Check for API key
echo ""
echo "✓ Checking ANTHROPIC_API_KEY..."
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "❌ ANTHROPIC_API_KEY not set"
    echo ""
    echo "Set it with:"
    echo "  export ANTHROPIC_API_KEY='your-key-here'"
    echo ""
    echo "Get your key at: https://console.anthropic.com/api_keys"
    exit 1
else
    echo "  ✅ API key found"
fi

# Install dependencies
echo ""
echo "✓ Installing dependencies..."
pip install -q -r requirements.txt
echo "  ✅ Dependencies installed"

# Verify transcripts
echo ""
echo "✓ Checking transcripts..."
TRANSCRIPTS_DIR="${TRANSCRIPTS_DIR:-.}"
transcript_count=$(ls "$TRANSCRIPTS_DIR"/*.txt 2>/dev/null | wc -l)
echo "  Found: $transcript_count transcript files"

if [ $transcript_count -lt 100 ]; then
    echo "⚠️  Warning: Only $transcript_count transcripts found (expected ~300)"
fi

# Test imports
echo ""
echo "✓ Testing imports..."
python3 -c "from transcript_processor import TranscriptProcessor; print('  ✅ TranscriptProcessor OK')" || exit 1
python3 -c "from solution_generator import SolutionGenerator; print('  ✅ SolutionGenerator OK')" || exit 1
python3 -c "from cache_manager import CacheManager; print('  ✅ CacheManager OK')" || exit 1
python3 -c "from anthropic import Anthropic; print('  ✅ Anthropic SDK OK')" || exit 1

# Create cache directory
echo ""
echo "✓ Creating cache directory..."
mkdir -p .cache
echo "  ✅ Cache directory ready"

# Summary
echo ""
echo "===================="
echo "✅ Setup Complete!"
echo "===================="
echo ""
echo "Next steps:"
echo ""
echo "1. Start the backend:"
echo "   python main.py"
echo ""
echo "2. In another terminal, test it:"
echo "   python test_backend.py"
echo ""
echo "3. Open frontend in browser:"
echo "   Set TRANSCRIPTS_DIR env var, then open frontend_backend_integration.html"
echo ""
echo "4. View API docs:"
echo "   http://localhost:8000/docs"
echo ""
echo "5. Set TRANSCRIPTS_DIR environment variable:"
echo "   export TRANSCRIPTS_DIR='/path/to/transcripts'"
echo ""
