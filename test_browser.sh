#!/bin/bash

echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║                   🚀 WWLD IN BROWSER - TESTING 🚀                         ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Check backend
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend: Running on http://localhost:8000"
    BACKEND=true
else
    echo "❌ Backend: NOT running"
    BACKEND=false
fi

# Check frontend
if curl -s http://localhost:8001 > /dev/null 2>&1; then
    echo "✅ Frontend: Running on http://localhost:8001"
    FRONTEND=true
else
    echo "❌ Frontend: NOT running"
    FRONTEND=false
fi

echo ""

if [ "$BACKEND" = true ] && [ "$FRONTEND" = true ]; then
    URL="http://localhost:8001/frontend_backend_integration.html"
    echo "🌐 Opening browser: $URL"
    echo ""
    
    open "$URL" 2>/dev/null || xdg-open "$URL" 2>/dev/null || echo "📋 Open in browser: $URL"
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "✨ QUICK TEST CHECKLIST (5 minutes)"
    echo ""
    echo "📚 PROBLEM HISTORY TEST:"
    echo "   1. Type: 'How do I prioritize?'"
    echo "   2. Click: ASK"
    echo "   3. See history panel appear above input ✅"
    echo "   4. Ask another question"
    echo "   5. History shows 2 items"
    echo "   6. Press F5 → History persists ✅"
    echo ""
    echo "⭐ FAVORITES TEST:"
    echo "   1. Click ★ star on any solution"
    echo "   2. Star turns gold ⭐"
    echo "   3. Scroll down → 'Saved Insights' appears ✅"
    echo "   4. Star another solution"
    echo "   5. Press F5 → Favorites persist ✅"
    echo ""
    echo "📥 EXPORT TEST:"
    echo "   1. Click '📥 Export' button"
    echo "   2. Choose 'JSON' → File downloads ✅"
    echo "   3. Click Export again"
    echo "   4. Choose 'Text' → File downloads ✅"
    echo ""
    echo "🔗 SHARE TEST:"
    echo "   1. Click '🔗 Share' button"
    echo "   2. Click '📋 Copy Link'"
    echo "   3. See 'Copied!' message ✅"
    echo "   4. Open new tab and paste URL"
    echo "   5. Same results appear ✅"
    echo ""
    echo "🔍 VERIFY STORAGE (F12 → Application → Storage → Local Storage):"
    echo "   • problemHistory - Your saved problems"
    echo "   • favorites - Your starred solutions ✅"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "✅ All systems running! Test in your browser now!"
    echo ""
else
    echo "❌ ERROR: Not all servers running"
fi
