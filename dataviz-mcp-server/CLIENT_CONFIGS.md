# Quick Client Configuration Guide

## 1. Claude Desktop

### macOS/Linux
```bash
# Edit config file
nano ~/.config/Claude/claude_desktop_config.json
```

### Windows
```bash
# Edit config file (use Notepad or your editor)
%APPDATA%\Claude\claude_desktop_config.json
```

### Configuration JSON
```json
{
  "mcpServers": {
    "dataviz": {
      "type": "stdio",
      "command": "docker",
      "args": ["run", "--rm", "-i", "saitejamothukuri/dataviz-mcp-server:latest"]
    }
  }
}
```

**After saving:** Restart Claude Desktop for changes to take effect.

---

## 2. Cursor IDE

1. Open Cursor settings
2. Go to **Features** → **MCP** section
3. Add new MCP server with:

```json
{
  "name": "dataviz",
  "type": "stdio",
  "command": "docker",
  "args": ["run", "--rm", "-i", "saitejamothukuri/dataviz-mcp-server:latest"]
}
```

**Note:** Restart Cursor after configuration changes.

---

## 3. Claude Web (claude.com)

Currently, Docker-based MCP servers work best through:
1. **Claude Desktop** → Files interface (sync your data)
2. **Direct API usage** if you expose the server to an HTTP endpoint

---

## 4. Claude Mobile App

**Option 1: Via Claude Desktop Sync**
- Configure in Claude Desktop (see above)
- Sign in with same Anthropic account
- Configuration syncs automatically

**Option 2: Via Cloud Storage**
- Upload data to cloud (S3, Google Cloud Storage, Azure Blob)
- Access through Claude Mobile directly

---

## 5. Running as Always-On Docker Service

For persistent access across all clients:

```bash
# Run in background
docker run -d \
  --name dataviz-mcp-server \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/outputs:/app/outputs \
  --restart unless-stopped \
  saitejamothukuri/dataviz-mcp-server:latest

# Check logs
docker logs -f dataviz-mcp-server

# Stop when done
docker stop dataviz-mcp-server
```

---

## Environment Variables (Optional)

You can pass custom environment variables to the Docker container:

```bash
docker run -e PYTHONUNBUFFERED=1 -e LOG_LEVEL=INFO saitejamothukuri/dataviz-mcp-server:latest
```

---

## Verifying Your Setup

After configuration, test with a simple prompt in your MCP client:

**Test Prompt:**
```
Can you help me load a CSV file and create a visualization?
My file is at /app/data/sample.csv with columns: name, value, date
```

The server should respond with available visualization functions.

---

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| `docker: command not found` | Install Docker Desktop for your OS |
| `Cannot connect to Docker daemon` | Start Docker Desktop application |
| `Permission denied` | Run with `sudo` or add user to docker group: `sudo usermod -aG docker $USER` |
| `Image not found` | Ensure you have internet connection and Docker can pull from Docker Hub |
| `Port already in use` | Change port mapping in docker run command |

---

## Updating to Latest Version

```bash
# Pull latest image
docker pull saitejamothukuri/dataviz-mcp-server:latest

# Recreate running container (if using always-on setup)
docker stop dataviz-mcp-server
docker rm dataviz-mcp-server
docker run -d --name dataviz-mcp-server ... # (repeat your docker run command)
```
