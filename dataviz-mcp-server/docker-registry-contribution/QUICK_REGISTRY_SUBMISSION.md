# Quick Registry Submission - 5 Minute Setup

## TL;DR - Just the Commands

### 1. Prepare Your Local Repository

```bash
# Navigate to your project
cd D:\MCP Servers\dataviz-mcp-server

# Commit all changes
git add .
git commit -m "Prepare for Docker MCP Registry submission"
git push origin main
```

### 2. Fork and Clone Docker MCP Registry

```bash
# Visit https://github.com/docker/mcp-registry and click Fork

# Clone your fork (replace YOUR_USERNAME)
git clone https://github.com/YOUR_USERNAME/mcp-registry
cd mcp-registry
```

### 3. Add Your Server Configuration

```bash
# Create directory
mkdir -p servers/dataviz-mcp-server

# Create server.json (copy from below)
cd servers/dataviz-mcp-server
```

**Create `server.json`:**
```json
{
  "name": "dataviz",
  "summary": "Interactive data visualization and analysis MCP server powered by Plotly, Pandas, and Matplotlib",
  "description": "DataViz Pro is a comprehensive MCP server for creating professional visualizations, analyzing datasets, and generating interactive dashboards. Supports CSV, Excel, SQL databases, MongoDB, AWS S3, Google BigQuery, and Azure Blob Storage with automatic file path resolution for Windows/WSL/Linux environments.",
  "version": "1.0.0",
  "license": "MIT",
  "author": "Saiteja Mothukuri",
  "repository": "https://github.com/saiteja007-mv/dataviz-mcp-server",
  "documentationUrl": "https://github.com/saiteja007-mv/dataviz-mcp-server/blob/main/Readme.md",
  "type": "local",
  "docker": {
    "image": "saitejamothukuri/dataviz-mcp-server:latest"
  },
  "tags": [
    "visualization",
    "data-analysis",
    "plotly",
    "pandas",
    "charts",
    "dashboards",
    "csv",
    "excel",
    "sql",
    "mongodb",
    "aws-s3",
    "google-bigquery",
    "azure-blob"
  ]
}
```

### 4. Commit and Push

```bash
# Go back to registry root
cd ../..

# Commit
git add servers/dataviz-mcp-server/
git commit -m "Add DataViz MCP Server to registry"
git push origin main
```

### 5. Create Pull Request

1. Visit https://github.com/docker/mcp-registry
2. Click "Pull requests" tab
3. Click "New pull request"
4. Select your fork as source
5. Fill in title and description (see below)

**PR Title:**
```
Add DataViz MCP Server
```

**PR Description:**
```markdown
## Add DataViz MCP Server

Comprehensive MCP server for data visualization and analysis using Plotly, Pandas, and Matplotlib.

**Details:**
- Repository: https://github.com/saiteja007-mv/dataviz-mcp-server
- Docker Image: saitejamothukuri/dataviz-mcp-server:latest
- License: MIT
- Supports: CSV, Excel, SQL, MongoDB, AWS S3, Google BigQuery, Azure Blob
- Features: 20 visualization and analysis tools with automatic path resolution
```

---

## Files You Already Have

✅ `Dockerfile` - Done
✅ `server.py` - Done
✅ `requirements.txt` - Done
✅ `LICENSE` - Done (MIT)
✅ `server.json` - Done
✅ `tools.json` - Done
✅ `Readme.md` - Done

## Files in Registry (Just server.json)

The Docker MCP Registry only needs `server.json` in the `servers/dataviz-mcp-server/` directory. It points to your GitHub repository for everything else.

## Validation

```bash
# Check JSON is valid
python -m json.tool servers/dataviz-mcp-server/server.json
```

## Status After Submission

- **Submission**: PR created and submitted
- **Review**: Docker team reviews (1-5 days)
- **Feedback**: May request minor changes
- **Merge**: All commits squashed and merged
- **Result**: Your server appears in Docker Desktop's MCP registry!

## What Happens Next?

1. Docker team reviews your PR
2. May ask for clarifications or minor changes
3. Once approved, they merge and squash commits
4. Your server becomes available in Docker Desktop
5. Users can install directly from the registry

---

## Need Help?

- **Path Issues?** Check `CURSOR_PATH_FIX.md`
- **Registry Details?** See `MCP_REGISTRY_GUIDE.md`
- **Full Checklist?** Review `REGISTRY_SUBMISSION_CHECKLIST.md`

Good luck! 🚀
