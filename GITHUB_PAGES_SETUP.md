# GitHub Pages Deployment Guide for WWLD

This guide explains how to deploy WWLD as a fully static GitHub Pages site without requiring a backend server.

## Overview

The GitHub Pages deployment uses:
- **Pre-generated responses** stored in `data.json` (updated weekly)
- **Static frontend** (`frontend_backend_integration.html`)
- **GitHub Actions** for automated weekly regeneration and deployment
- **No backend API required** - everything runs on the client side

## Setup Instructions

### Step 1: Generate Initial Data (Local)

First, generate the initial `data.json` file on your local machine:

```bash
cd backend
python generate_static_data.py
```

This will create `data.json` in the project root with responses for all 10 popular problems.

**Note:** You need `ANTHROPIC_API_KEY` environment variable set to use real Claude responses. Without it, the script runs in demo mode with sample data.

### Step 2: Configure GitHub Secrets

Add your Anthropic API key as a GitHub secret so that the weekly regeneration workflow can access it:

1. Go to your GitHub repository settings
2. Navigate to **Secrets and variables → Actions**
3. Click **New repository secret**
4. Name: `ANTHROPIC_API_KEY`
5. Value: Your actual Anthropic API key
6. Click **Add secret**

### Step 3: Enable GitHub Pages

1. Go to your repository **Settings**
2. Navigate to **Pages** (left sidebar)
3. Under "Build and deployment", select:
   - Source: **Deploy from a branch**
   - Branch: **main**
   - Folder: **/ (root)** or create a `docs` folder and select that

**Note:** The `deploy.yml` workflow will automatically create the `docs` folder and deploy from there.

### Step 4: Configure Repository Settings

Make sure your repository has:
- **Branch protection rules** disabled for `main` (so workflows can commit)
- **Allow GitHub Actions** is enabled

### Step 5: Verify Deployment

After pushing to main:

1. Go to **Actions** tab in your repository
2. Wait for the `Deploy to GitHub Pages` workflow to complete
3. Your site will be live at: `https://YOUR_USERNAME.github.io/YOUR_REPO_NAME`

## Workflows

### regenerate-data.yml

**Purpose:** Weekly regeneration of pre-cached responses

**Schedule:** Every Sunday at 2 AM UTC (configurable in the YAML)

**Triggered by:**
- Weekly schedule (automatic)
- Manual dispatch: Go to Actions → Regenerate Static Data → Run workflow

**What it does:**
1. Checks out the latest code
2. Installs Python dependencies
3. Runs `generate_static_data.py` with ANTHROPIC_API_KEY
4. Generates fresh responses for all 10 popular problems
5. Commits `data.json` back to main branch if changed
6. Pushes to GitHub (deploy workflow automatically triggers)

**Manual trigger example:**
```bash
gh workflow run regenerate-data.yml
```

### deploy.yml

**Purpose:** Builds and deploys the static site to GitHub Pages

**Triggered by:**
- Push to main branch (if `frontend_backend_integration.html` or `data.json` changed)
- Manual dispatch: Go to Actions → Deploy to GitHub Pages → Run workflow

**What it does:**
1. Checks out code
2. Creates `docs/` folder
3. Copies frontend HTML to `docs/index.html`
4. Copies `data.json` to `docs/data.json`
5. Uploads to GitHub Pages
6. Site is live at configured URL

## File Structure for GitHub Pages

The deployed site uses:

```
docs/
  ├── index.html          (copy of frontend_backend_integration.html)
  └── data.json           (pre-generated responses)
```

## Testing Locally

### Test Frontend with Static Data

1. Start a simple HTTP server:
```bash
python3 -m http.server 8001
```

2. Open browser: `http://localhost:8001/frontend_backend_integration.html`

3. The frontend will:
   - Load `data.json`
   - Display popular problems from static data
   - Allow searching pre-generated problems
   - Show error if problem not in pre-generated set

### Test with API Fallback

Add `?useAPI=true` to URL to test API mode:
```
http://localhost:8001/frontend_backend_integration.html?useAPI=true
```

## Frontend Behavior

### Static Mode (Default)

When `data.json` is available:
- Popular problems loaded from static data
- Search queries checked against pre-generated responses
- Instant responses (no API latency)
- If problem not in pre-generated set: Shows helpful message

**User Message Format:**
```
❌ "Your question" is not in our pre-generated set.
Try one of the popular problems or use API mode.
```

### API Mode (Fallback)

When `data.json` is missing or `?useAPI=true` parameter set:
- Requires backend running at `http://localhost:8000`
- Makes live API calls to Claude
- Can answer any question
- Shows "Consulting with Lenny's brain..." while loading

### Switching Modes

| Scenario | Mode | How |
|----------|------|-----|
| Normal GitHub Pages | Static | Automatic when `data.json` loaded |
| Local development (backend running) | API | Add `?useAPI=true` to URL |
| Local development (no backend) | Static | Keep `data.json`, remove API parameter |

## Deployment Checklist

- [ ] Generated initial `data.json` locally with `python backend/generate_static_data.py`
- [ ] Committed `data.json` to repository
- [ ] Added `ANTHROPIC_API_KEY` secret to GitHub repository
- [ ] Enabled GitHub Pages in repository settings
- [ ] Pushed to main branch
- [ ] Verified workflows run successfully in Actions tab
- [ ] Accessed live site at GitHub Pages URL
- [ ] Tested searching for popular problems
- [ ] Verified weekly regeneration is scheduled

## Troubleshooting

### Workflow says "No such file or directory: data.json"

**Problem:** `data.json` doesn't exist in repository root

**Solution:**
```bash
cd backend
python generate_static_data.py
git add ../data.json
git commit -m "Add initial data.json"
git push
```

### Workflow fails with "ANTHROPIC_API_KEY not found"

**Problem:** Secret not configured correctly

**Solution:**
1. Verify secret name is exactly `ANTHROPIC_API_KEY`
2. Check that the value is your full Anthropic API key
3. Wait 1 minute for secret to propagate
4. Manually trigger workflow: `gh workflow run regenerate-data.yml`

### GitHub Pages still building or not showing

**Problem:** Deployment not completed

**Solution:**
1. Check Actions tab for workflow status
2. Ensure `deploy.yml` workflow completed successfully
3. Verify Pages settings point to correct branch/folder
4. Wait up to 1 minute for GitHub to publish changes

### Frontend shows "data.json not found" in console

**Problem:** `data.json` not deployed to GitHub Pages

**Solution:**
1. Verify `data.json` exists in repository root
2. Manually trigger deploy workflow:
   ```bash
   gh workflow run deploy.yml
   ```
3. Check that `docs/` folder has `data.json` after deployment

### Popular problems not loading

**Problem:** Frontend can't find static data

**Solution:**
1. Open browser developer console (F12)
2. Check for errors loading `data.json`
3. If 404 error: File not deployed (see above)
4. If parsing error: `data.json` corrupted (regenerate it)

## Advanced Configuration

### Change Regeneration Schedule

Edit `.github/workflows/regenerate-data.yml`, line with `cron`:

```yaml
schedule:
  # Change this cron expression
  - cron: '0 2 * * 0'  # Currently: Sunday 2 AM UTC
```

Common cron expressions:
- `0 2 * * 0` - Weekly (Sunday 2 AM UTC)
- `0 0 * * *` - Daily (midnight UTC)
- `0 * * * *` - Hourly
- `0 0 1 * *` - Monthly (first day)

### Custom Domain

To use a custom domain:

1. Add `CNAME` file to `docs/` folder with your domain
2. Configure your domain registrar to point to GitHub Pages
3. Enable HTTPS in repository Pages settings

See [GitHub Pages custom domain docs](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site)

### Add More Popular Problems

To add new pre-generated problems:

1. Edit `backend/solution_generator.py`:
   ```python
   POPULAR_PROBLEMS = [
       "..existing problems...",
       "Your new problem here?"
   ]
   ```

2. Regenerate data:
   ```bash
   python backend/generate_static_data.py
   ```

3. Commit and push - deploy workflow will pick it up

## Performance Notes

| Metric | Value |
|--------|-------|
| Page load time | <1 second |
| Search response | Instant (client-side) |
| Problem lookup | <100ms (fuzzy matching) |
| Static data size | ~20-30 KB (gzipped) |
| Cache hit rate | 100% for pre-generated problems |

## Cost Savings

With GitHub Pages static deployment:
- **API costs reduced by ~95%** - Only regeneration calls (weekly, ~$0.30/week)
- **No backend hosting costs** - GitHub Pages is free
- **Faster response times** - Client-side lookups vs network latency
- **Unlimited scaling** - GitHub Pages handles traffic automatically

## Support & Debugging

### View Workflow Logs

```bash
# List recent workflows
gh workflow list

# View logs for regenerate-data workflow
gh run list -w regenerate-data.yml

# View detailed logs for a specific run
gh run view <run-id> --log
```

### Manual Data Regeneration

If you need to manually regenerate data:

```bash
cd backend
export ANTHROPIC_API_KEY="your-key-here"
python generate_static_data.py
git add ../data.json
git commit -m "Manual data regeneration"
git push
```

## Questions?

Refer to:
- `CLAUDE.md` - Project architecture and overview
- `backend/README.md` - Backend API reference
- `.github/workflows/*.yml` - Workflow definitions
- GitHub Pages docs: https://docs.github.com/en/pages
