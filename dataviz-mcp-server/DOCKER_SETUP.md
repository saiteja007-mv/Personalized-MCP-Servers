# DataViz MCP Server - Docker Hub Setup Guide

Your DataViz MCP Server is now published to Docker Hub and can be accessed from anywhere!

**Docker Hub Repository:** `saitejamothukuri/dataviz-mcp-server:latest`

## Quick Start with Docker Compose

Use the `compose.public.yaml` file to run the server:

```bash
docker compose -f compose.public.yaml up
```

## Configuration for Different MCP Clients

### 1. Claude Desktop Configuration

Edit your Claude Desktop config file:
- **macOS/Linux:** `~/.config/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

Add the following configuration:

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

### 2. Cursor Configuration

For Cursor IDE, add to your MCP settings:

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

### 3. Claude Mobile App

The mobile app currently supports MCP servers through:
1. Claude.com web interface - Configure via your account settings
2. Desktop sync - Use Claude Desktop configuration (will sync to mobile)

To use the server on mobile:
1. Set it up in Claude Desktop first
2. Sync your configuration
3. Or access the server through claude.com using the Docker method

### 4. Docker Compose for Advanced Setup

For production or advanced setups with data persistence:

```yaml
version: '3.8'
services:
  dataviz-server:
    image: saitejamothukuri/dataviz-mcp-server:latest
    container_name: dataviz-mcp-server
    volumes:
      - ./data:/app/data
      - ./outputs:/app/outputs
    environment:
      - PYTHONUNBUFFERED=1
    stdin_open: true
    tty: false
    restart: "no"
    ports:
      - "8000:8000"  # If you add a web interface later
```

## Usage

Once configured in your MCP client, you can use the DataViz Pro tools:

- **load_csv_file** - Load CSV files for visualization
- **create_line_chart** - Create interactive line charts
- **create_bar_chart** - Create bar charts
- **create_scatter_plot** - Create scatter plots
- **create_heatmap** - Create heatmaps
- And many more visualization tools!

## Pulling the Latest Version

Whenever you want to update to the latest version:

```bash
docker pull saitejamothukuri/dataviz-mcp-server:latest
```

## Troubleshooting

### Permission Issues on macOS/Linux
If you encounter permission issues, ensure Docker daemon is running:
```bash
docker ps
```

### Windows WSL Issues
Make sure Docker Desktop for Windows is running and WSL integration is enabled.

### No Data Persistence
When running with `docker run`, use volumes to persist data:
```bash
docker run -v $(pwd)/data:/app/data -v $(pwd)/outputs:/app/outputs saitejamothukuri/dataviz-mcp-server:latest
```

## Build a Custom Version

If you need to modify the server, you can:

1. Clone or download your source code
2. Modify as needed
3. Build locally:
   ```bash
   docker build -t saitejamothukuri/dataviz-mcp-server:v1.0.0 .
   docker push saitejamothukuri/dataviz-mcp-server:v1.0.0
   ```
4. Update your client configs to use the new tag

## Support

For issues or improvements, check your GitHub repository or Docker Hub repository page.
