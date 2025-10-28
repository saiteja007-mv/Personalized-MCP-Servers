# DataViz MCP Server - Docker MCP Registry Contribution Guide

## Overview

This guide walks you through contributing your DataViz MCP Server to the Docker MCP Registry, making it officially available to all Docker Desktop users and MCP clients.

## Prerequisites

Before starting, ensure you have:
- Git installed
- GitHub account
- Docker Desktop v4.40+ with MCP support
- Go v1.24+ (for local testing)
- Task runner (optional, but recommended)

## Step 1: Prepare Your Repository

Your DataViz MCP Server project needs these files at the root:

### Required Files Checklist
- ✅ `Dockerfile` - Already have this
- ✅ `server.py` - Your main MCP server code
- ✅ `requirements.txt` - Python dependencies
- ⏳ `LICENSE` - Need to add (MIT or Apache 2.0)
- ⏳ `README.md` - Need to enhance
- ⏳ `server.json` - Registry configuration
- ⏳ `tools.json` - Tool definitions (optional but recommended)

## Step 2: Add License File

Create a `LICENSE` file (MIT is recommended):

### MIT License
```
MIT License

Copyright (c) 2025 Saiteja Mothukuri

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE OR OTHERWISE
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
```

## Step 3: Create server.json

This file defines your server for the registry:

```json
{
  "name": "dataviz",
  "summary": "Interactive data visualization and analysis MCP server powered by Plotly, Pandas, and Matplotlib",
  "description": "DataViz Pro is a comprehensive MCP server for creating professional visualizations, analyzing datasets, and generating interactive dashboards. Supports CSV, Excel, SQL databases, MongoDB, AWS S3, Google BigQuery, and Azure Blob Storage.",
  "version": "1.0.0",
  "license": "MIT",
  "author": "Saiteja Mothukuri",
  "repository": "https://github.com/saiteja007-mv/dataviz-mcp-server",
  "documentationUrl": "https://github.com/saiteja007-mv/dataviz-mcp-server/blob/main/README.md",
  "type": "local",
  "docker": {
    "image": "saitejamothukuri/dataviz-mcp-server:latest",
    "buildContext": ".",
    "dockerfile": "Dockerfile"
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

## Step 4: Create tools.json (Optional but Recommended)

This file documents all available tools:

```json
{
  "tools": [
    {
      "name": "load_csv_file",
      "description": "Load a CSV file into memory for visualization. Accepts absolute file paths from Windows, WSL, or Linux.",
      "inputSchema": {
        "type": "object",
        "properties": {
          "file_path": {
            "type": "string",
            "description": "Absolute path to CSV file (Windows, WSL, or Linux format)"
          },
          "delimiter": {
            "type": "string",
            "description": "CSV delimiter character",
            "default": ","
          },
          "encoding": {
            "type": "string",
            "description": "File encoding",
            "default": "utf-8"
          }
        },
        "required": ["file_path"]
      }
    },
    {
      "name": "load_excel_file",
      "description": "Load an Excel file into memory. If sheet_name is empty, loads the first sheet.",
      "inputSchema": {
        "type": "object",
        "properties": {
          "file_path": {
            "type": "string",
            "description": "Absolute path to Excel file"
          },
          "sheet_name": {
            "type": "string",
            "description": "Sheet name to load (optional)",
            "default": ""
          }
        },
        "required": ["file_path"]
      }
    },
    {
      "name": "create_bar_chart",
      "description": "Create an interactive bar chart using Plotly",
      "inputSchema": {
        "type": "object",
        "properties": {
          "dataset_id": {
            "type": "string",
            "description": "ID of loaded dataset"
          },
          "x_column": {
            "type": "string",
            "description": "Column name for X axis"
          },
          "y_column": {
            "type": "string",
            "description": "Column name for Y axis"
          },
          "title": {
            "type": "string",
            "description": "Chart title"
          },
          "output_path": {
            "type": "string",
            "description": "Path to save HTML output",
            "default": "/app/outputs/bar_chart.html"
          }
        },
        "required": ["dataset_id", "x_column", "y_column"]
      }
    },
    {
      "name": "create_line_chart",
      "description": "Create an interactive line chart using Plotly. Useful for time series data.",
      "inputSchema": {
        "type": "object",
        "properties": {
          "dataset_id": {
            "type": "string",
            "description": "ID of loaded dataset"
          },
          "x_column": {
            "type": "string",
            "description": "Column name for X axis"
          },
          "y_column": {
            "type": "string",
            "description": "Column name for Y axis"
          },
          "title": {
            "type": "string",
            "description": "Chart title"
          },
          "output_path": {
            "type": "string",
            "description": "Path to save HTML output",
            "default": "/app/outputs/line_chart.html"
          }
        },
        "required": ["dataset_id", "x_column", "y_column"]
      }
    },
    {
      "name": "create_scatter_plot",
      "description": "Create an interactive scatter plot using Plotly. Optionally color points by a third column.",
      "inputSchema": {
        "type": "object",
        "properties": {
          "dataset_id": {
            "type": "string",
            "description": "ID of loaded dataset"
          },
          "x_column": {
            "type": "string",
            "description": "Column name for X axis"
          },
          "y_column": {
            "type": "string",
            "description": "Column name for Y axis"
          },
          "color_column": {
            "type": "string",
            "description": "Optional column for coloring points"
          },
          "title": {
            "type": "string",
            "description": "Chart title"
          },
          "output_path": {
            "type": "string",
            "description": "Path to save HTML output",
            "default": "/app/outputs/scatter_plot.html"
          }
        },
        "required": ["dataset_id", "x_column", "y_column"]
      }
    },
    {
      "name": "create_heatmap",
      "description": "Create a correlation heatmap for numeric columns in the dataset using Plotly",
      "inputSchema": {
        "type": "object",
        "properties": {
          "dataset_id": {
            "type": "string",
            "description": "ID of loaded dataset"
          },
          "title": {
            "type": "string",
            "description": "Chart title",
            "default": "Correlation Heatmap"
          },
          "output_path": {
            "type": "string",
            "description": "Path to save HTML output",
            "default": "/app/outputs/heatmap.html"
          }
        },
        "required": ["dataset_id"]
      }
    },
    {
      "name": "create_dashboard",
      "description": "Create a comprehensive dashboard with multiple visualizations for the dataset",
      "inputSchema": {
        "type": "object",
        "properties": {
          "dataset_id": {
            "type": "string",
            "description": "ID of loaded dataset"
          },
          "title": {
            "type": "string",
            "description": "Dashboard title",
            "default": "Interactive Dashboard"
          },
          "output_path": {
            "type": "string",
            "description": "Path to save HTML output",
            "default": "/app/outputs/dashboard.html"
          }
        },
        "required": ["dataset_id"]
      }
    },
    {
      "name": "list_loaded_datasets",
      "description": "List all datasets currently loaded in memory with their IDs and basic information"
    },
    {
      "name": "generate_summary_report",
      "description": "Generate a comprehensive statistical summary report of the dataset",
      "inputSchema": {
        "type": "object",
        "properties": {
          "dataset_id": {
            "type": "string",
            "description": "ID of loaded dataset"
          }
        },
        "required": ["dataset_id"]
      }
    },
    {
      "name": "get_file_path_help",
      "description": "Get instructions on how to provide file paths to the DataViz server when using Cursor or other MCP clients"
    }
  ]
}
```

## Step 5: Enhance README.md

Your existing README should include:
- Clear description of what the server does
- Installation instructions
- Usage examples
- Supported data sources
- Configuration options
- License information

## Step 6: Commit to GitHub

If not already on GitHub, push your project:

```bash
git init
git add .
git commit -m "Initial commit: DataViz MCP Server"
git remote add origin https://github.com/YOUR_USERNAME/dataviz-mcp-server
git push -u origin main
```

## Step 7: Fork Docker MCP Registry

1. Go to https://github.com/docker/mcp-registry
2. Click "Fork" button
3. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/mcp-registry
   cd mcp-registry
   ```

## Step 8: Add Your Server to Registry

Create a new directory in the registry:

```bash
mkdir -p servers/dataviz-mcp-server
cd servers/dataviz-mcp-server
```

Create `server.json` inside with the configuration from Step 3.

## Step 9: Test Locally (Optional)

If you have Task installed:

```bash
task validate
```

Or test with Docker Desktop's MCP Toolkit.

## Step 10: Submit Pull Request

1. Commit your changes:
   ```bash
   git add servers/dataviz-mcp-server/
   git commit -m "Add DataViz MCP Server to registry"
   ```

2. Push to your fork:
   ```bash
   git push origin main
   ```

3. Create a PR on https://github.com/docker/mcp-registry
   - Title: "Add DataViz MCP Server"
   - Description: Include:
     - Brief description of your server
     - Link to your GitHub repository
     - Supported platforms
     - Any special requirements

## Key Points to Remember

- Your Docker image must be publicly available on Docker Hub ✅ (done)
- Include proper documentation ✅ (have README)
- Use MIT or Apache 2.0 license ⏳ (need to add)
- All files must be at repository root
- PR review can take a few days
- All commits will be squashed by Docker team

## Example PR Description

```markdown
## Add DataViz MCP Server

This PR adds the DataViz MCP Server, a comprehensive tool for data visualization and analysis.

### Details
- **Repository**: https://github.com/saiteja007-mv/dataviz-mcp-server
- **Docker Image**: saitejamothukuri/dataviz-mcp-server:latest
- **Description**: Interactive data visualization and analysis using Plotly, Pandas, and Matplotlib
- **Supported Data Sources**: CSV, Excel, SQL, MongoDB, AWS S3, Google BigQuery, Azure Blob Storage
- **License**: MIT

### Features
- Load and analyze CSV and Excel files
- Connect to SQL databases and MongoDB
- Load data from cloud storage (AWS S3, Google BigQuery, Azure)
- Create 10+ types of interactive visualizations
- Generate comprehensive dashboards
- Automatic file path resolution for Windows/WSL/Linux
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Docker image not found | Ensure image is pushed to Docker Hub with `latest` tag |
| PR not approved | Check that all required files are present and properly formatted |
| Image fails to run | Test locally: `docker run saitejamothukuri/dataviz-mcp-server:latest` |
| License issue | Use MIT (MIT License text required) or Apache 2.0 |

## Next Steps

1. Add LICENSE file (MIT recommended)
2. Enhance README with complete documentation
3. Create server.json configuration
4. Create tools.json with tool definitions
5. Push all changes to your GitHub repository
6. Fork Docker MCP Registry
7. Add server configuration to your fork
8. Submit PR to Docker team

Good luck with your contribution! 🚀
