#!/bin/bash

# WWLD Browser Testing Script
# This script opens the application in your browser and provides testing instructions

echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                            ║"
echo "║                     🚀 OPENING WWLD IN YOUR BROWSER 🚀                    ║"
echo "║                                                                            ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Check if servers are running
echo "🔍 Checking servers..."
echo ""

# Check backend
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend: Running on http://localhost:8000"
    BACKEND_RUNNING=true
else
    echo "❌ Backend: NOT running (http://localhost:8000)"
    BACKEND_RUNNING=false
fi

# Check frontend
if curl -s http://localhost:8001/frontend_backend_integration.html > /dev/null 2>&1; then
    echo "✅ Frontend: Running on http://localhost:8001"
    FRONTEND_RUNNING=true
else
    echo "❌ Frontend: NOT running (http://localhost:8001)"
    FRONTEND_RUNNING=false
fi

echo ""

# If both servers running, open browser
if [ "$BACKEND_RUNNING" = true ] && [ "$FRONTEND_RUNNING" = true ]; then
    echo "✨ Both servers running! Opening browser..."
    echo ""

    URL="http://localhost:8001/frontend_backend_integration.html"

    # Open in browser (macOS)
    if [[ "$OSTYPE" == "darwin"* ]]; then
        open "$URL"
        echo "🌐 Browser opened: $URL"
    # Open in browser (Linux)
    elif command -v xdg-open &> /dev/null; then
        xdg-open "$URL"
        echo "🌐 Browser opened: $URL"
    # Open in browser (Windows Git Bash)
    elif command -v start &> /dev/null; then
        start "$URL"
        echo "🌐 Browser opened: $URL"
    else
        echo "📋 Manually open in your browser:"
        echo "   $URL"
    fi

    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "🧪 QUICK TEST CHECKLIST"
    echo ""
    echo "Follow these steps to test all features:"
    echo ""
    echo "1️⃣  TEST PROBLEM HISTORY (1 min)"
    echo "    • Type: 'How do I prioritize?'"
    echo "    • Click: ASK"
    echo "    • See: Results appear"
    echo "    • See: History panel shows at top"
    echo "    • Type: 'How do I hire?'"
    echo "    • Click: ASK"
    echo "    • See: History shows 2 items"
    echo "    • Press: F5 to refresh"
    echo "    • See: History still there ✅"
    echo ""
    echo "2️⃣  TEST FAVORITES (1 min)"
    echo "    • Click: ★ star on any solution"
    echo "    • See: Star turns gold ⭐"
    echo "    • Scroll: Down to see 'Saved Insights' panel"
    echo "    • Click: Another star on different solution"
    echo "    • Press: F5 to refresh"
    echo "    • See: Both favorites still there ✅"
    echo ""
    echo "3️⃣  TEST EXPORT (1 min)"
    echo "    • Click: '📥 Export' button (top-right)"
    echo "    • Modal: Opens with export options"
    echo "    • Click: '📄 Export as JSON'"
    echo "    • See: File downloads (check Downloads folder)"
    echo "    • Click: '📥 Export' again"
    echo "    • Click: '📝 Export as Text'"
    echo "    • See: Another file downloads ✅"
    echo ""
    echo "4️⃣  TEST SHARE (1 min)"
    echo "    • Click: '🔗 Share' button (top-right)"
    echo "    • Modal: Opens with share URL"
    echo "    • Click: '📋 Copy Link'"
    echo "    • See: 'Copied!' message"
    echo "    • Open: New browser tab"
    echo "    • Paste: The URL"
    echo "    • See: Same results appear in new tab ✅"
    echo ""
    echo "5️⃣  CHECK STORAGE (Developer Tools)"
    echo "    • Press: F12 (Developer Tools)"
    echo "    • Go to: Application → Storage → Local Storage"
    echo "    • Select: http://localhost:8001"
    echo "    • See: 'problemHistory' key (your saved problems)"
    echo "    • See: 'favorites' key (your starred solutions) ✅"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "📊 EXPECTED RESULTS"
    echo ""
    echo "After testing, you should have:"
    echo "  ✅ History panel showing your questions"
    echo "  ✅ Favorites panel showing starred solutions"
    echo "  ✅ Downloaded export files (JSON and Text)"
    echo "  ✅ Copied share URL that works in new tab"
    echo "  ✅ Data persisting after F5 refresh"
    echo "  ✅ localStorage keys visible in DevTools"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "🎯 TOTAL TEST TIME: ~5 minutes"
    echo ""
    echo "🔗 Direct URLs:"
    echo "   Browser: http://localhost:8001/frontend_backend_integration.html"
    echo "   API:     http://localhost:8000"
    echo ""
    echo "📚 Documentation:"
    echo "   • START_TESTING_NOW.md - Quick reference"
    echo "   • TESTING_GUIDE.md - Comprehensive (46+ scenarios)"
    echo "   • GITHUB_DEPLOYMENT_GUIDE.md - Full deployment guide"
    echo ""

else
    echo "❌ ERROR: Not all servers are running"
    echo ""
    echo "Please start them in two separate terminals:"
    echo ""
    echo "Terminal 1 (Backend):"
    echo "  cd /Users/jeevan.patil/Downloads/Lenny/backend"
    echo "  export ANTHROPIC_API_KEY=\"your-api-key\""
    echo "  python main.py"
    echo ""
    echo "Terminal 2 (Frontend):"
    echo "  cd /Users/jeevan.patil/Downloads/Lenny"
    echo "  python3 -m http.server 8001"
    echo ""
    exit 1
fi

echo "✨ Browser test script complete!"
