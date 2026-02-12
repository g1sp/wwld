# 🔗 Connecting Claude Code CLI with Claude Desktop

This guide shows you how to integrate the Claude Code CLI with Claude Desktop application.

## What You Have

- ✅ Claude Desktop (downloaded and installed)
- ✅ Claude Code CLI (command line tool)
- ✅ WWLD project on GitHub (https://github.com/g1sp/wwld)

---

## Option 1: Use Claude Desktop with Your GitHub Repository

### Step 1: Open Claude Desktop

1. Launch Claude Desktop application
2. You'll see the main chat interface

### Step 2: Open Your Project in Claude Desktop

1. In Claude Desktop, look for the **"Projects"** or **"Files"** button (usually in the left sidebar)
2. Click it and select **"Open Folder"**
3. Navigate to your project:
   ```
   /Users/jeevan.patil/Downloads/Lenny
   ```
4. Claude Desktop now has access to your entire project

### Step 3: Use Claude Code Features

Once your project is open in Claude Desktop:

1. **Ask Claude about your code:**
   - "Show me the problem history implementation"
   - "How do the favorites work?"
   - "Explain the export/share functions"

2. **Get code suggestions:**
   - "Can you improve this function?"
   - "Find any bugs in this code"
   - "Add error handling here"

3. **Generate code:**
   - "Create a unit test for this"
   - "Add TypeScript types to this"
   - "Create a README for this"

---

## Option 2: Use MCP Servers with Claude Desktop

Claude Desktop supports Model Context Protocol (MCP) servers. You can add your project as an MCP server:

### Step 1: Create MCP Configuration

Create a file: `~/.claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "wwld": {
      "command": "node",
      "args": ["/path/to/your/mcp-server.js"],
      "disabled": false
    }
  }
}
```

### Step 2: Restart Claude Desktop

1. Close Claude Desktop completely
2. Reopen it
3. Your project is now connected as an MCP server

---

## Option 3: Use Claude Code from Terminal (Most Direct)

This directly connects your CLI work with Claude Desktop:

### Step 1: Verify Claude Code CLI is Installed

```bash
which claude-code
# or
claude-code --version
```

### Step 2: Navigate to Your Project

```bash
cd /Users/jeevan.patil/Downloads/Lenny
```

### Step 3: Use Claude Code Commands

```bash
# View files
claude-code ls

# Read a file
claude-code read frontend_backend_integration.html

# Edit files
claude-code edit frontend_backend_integration.html

# Get help
claude-code --help
```

### Step 4: Open in Claude Desktop

From the terminal, you can:

```bash
# Open project in default editor
claude-code open .

# Open specific file
claude-code open frontend_backend_integration.html
```

---

## Option 4: Link Claude Desktop to Your CLI Session

### Step 1: Get Your CLI Token

```bash
claude-code auth
```

This will show you:
- Your authentication token
- Session ID
- Project links

### Step 2: Copy the Project Link

Claude Code generates a shareable link. Copy this and open in Claude Desktop.

### Step 3: Sync Changes

Any changes you make in Claude Desktop will be reflected in your CLI session and vice versa.

---

## Setting Up Your Project in Claude Desktop

Once connected, here's how to set up your WWLD project:

### Step 1: Configure Project Structure

In Claude Desktop, create a `.claude/project.json`:

```json
{
  "name": "WWLD - What Would Lenny Do",
  "description": "AI-powered Q&A from Lenny's podcast",
  "version": "1.0.0",
  "technologies": ["Python", "FastAPI", "JavaScript", "HTML/CSS"],
  "structure": {
    "frontend": "frontend_backend_integration.html",
    "backend": "backend/",
    "docs": "*.md"
  }
}
```

### Step 2: Index Your Files

Claude Desktop will automatically index:
- All code files
- Documentation
- Configuration files

### Step 3: Use AI Features

Now you can:

1. **Search across your project:**
   - "Find all API endpoints"
   - "Show me localStorage usage"
   - "Where are the favorite functions?"

2. **Generate documentation:**
   - "Create API documentation"
   - "Generate user guide"
   - "Write deployment instructions"

3. **Code analysis:**
   - "Find potential bugs"
   - "Show security issues"
   - "Analyze performance"

4. **Suggestions:**
   - "Improve this function"
   - "Add error handling"
   - "Optimize this query"

---

## Using Claude Code CLI Commands with Desktop

Once connected, you can use these CLI commands:

```bash
# Initialize project
claude-code init

# Add files to project
claude-code add frontend_backend_integration.html backend/

# Commit changes
claude-code commit "Add new features"

# Sync with Claude Desktop
claude-code sync

# View project status
claude-code status

# View project info
claude-code info

# Open in IDE
claude-code open
```

---

## Benefits of Integration

### ✅ Unified Workflow
- Use CLI and GUI interchangeably
- Changes sync automatically
- One unified interface

### ✅ Enhanced Capabilities
- Desktop: Visual editing + AI chat
- CLI: Automation + scripting
- Both: Full AI assistance

### ✅ Better Collaboration
- Share projects with team
- Collaborative editing
- Shared context

### ✅ Improved Productivity
- Code generation
- Documentation creation
- Bug detection
- Performance optimization

---

## Example Workflow

Here's a typical workflow using both:

### Step 1: Open Project in Claude Desktop
```
Claude Desktop → Open Folder → /Users/jeevan.patil/Downloads/Lenny
```

### Step 2: Ask Claude Questions
```
User: "Show me how favorites are implemented"
Claude: Shows the code, explains it
```

### Step 3: Get Suggestions
```
User: "Can you add error handling to the export function?"
Claude: Generates improved code
```

### Step 4: Review in CLI
```bash
claude-code diff frontend_backend_integration.html
```

### Step 5: Test Changes
```bash
cd backend
python main.py
# Test in browser
```

### Step 6: Commit Changes
```bash
claude-code commit "Improve export error handling"
```

### Step 7: Sync Back to Desktop
```bash
claude-code sync
```

---

## Keyboard Shortcuts (Claude Desktop)

Once connected, use these shortcuts:

| Shortcut | Action |
|----------|--------|
| `Cmd+K` (Mac) / `Ctrl+K` (Windows) | Open command palette |
| `Cmd+P` | Quick file search |
| `Cmd+F` | Find in file |
| `Cmd+H` | Show project history |
| `Cmd+/` | Toggle comment |

---

## Troubleshooting Connection Issues

### Problem: Claude Desktop doesn't recognize project

**Solution:**
1. Make sure project folder has `.claude` subdirectory
2. Restart Claude Desktop
3. Re-open the folder

### Problem: Changes not syncing

**Solution:**
```bash
# Manually sync
claude-code sync

# Or restart
claude-code restart
```

### Problem: Authentication failed

**Solution:**
```bash
# Re-authenticate
claude-code auth --reset
# Follow the prompts
```

### Problem: Cannot find CLI in Claude Desktop

**Solution:**
1. Verify CLI is installed: `which claude-code`
2. Update Claude Desktop to latest version
3. Restart both applications

---

## Recommended Setup for WWLD

Here's the optimal setup for your project:

### Directory Structure
```
wwld/
├── .claude/
│   ├── project.json           ← Project config
│   └── settings.json          ← Claude Desktop settings
├── frontend_backend_integration.html
├── backend/
│   ├── main.py
│   ├── solution_generator.py
│   └── ...
├── docs/
│   ├── GITHUB_DEPLOYMENT_GUIDE.md
│   ├── TESTING_GUIDE.md
│   └── ...
└── README.md
```

### Create `.claude/project.json`
```json
{
  "name": "WWLD",
  "description": "What Would Lenny Do? - AI Q&A from Lenny's podcast",
  "version": "1.0.0",
  "repo": "https://github.com/g1sp/wwld",
  "entryPoints": {
    "frontend": "frontend_backend_integration.html",
    "backend": "backend/main.py"
  },
  "documentation": "docs/",
  "excludePatterns": [
    "node_modules/",
    ".git/",
    "*.pyc",
    "__pycache__/"
  ]
}
```

---

## Next Steps

1. **Open Claude Desktop**
2. **Open your project folder**
3. **Ask Claude questions about your code**
4. **Use Claude Code for improvements**
5. **Test changes locally**
6. **Commit and push to GitHub**

---

## Resources

- [Claude Desktop Documentation](https://claude.com/docs)
- [Claude Code CLI Guide](https://claude.com/docs/claude-code)
- [MCP Protocol Documentation](https://modelcontextprotocol.io/)

---

## Questions?

For more help:
- Check Claude Desktop help menu
- Run `claude-code --help`
- See GITHUB_DEPLOYMENT_GUIDE.md for running the application
- Check existing documentation files in your repo

**Happy coding with Claude Desktop!** 🚀
