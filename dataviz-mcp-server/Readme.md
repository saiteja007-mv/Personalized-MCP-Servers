# DataViz Pro - MCP Server

Interactive data visualization and analysis MCP server powered by Plotly, Pandas, and Matplotlib.

## 🚀 Quick Setup

### Add to Claude Desktop

Edit your Claude Desktop config file:

**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
**macOS/Linux:** `~/.config/Claude/claude_desktop_config.json`

Add this configuration:

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

### Add to Cursor

In Cursor MCP settings, add:

```json
{
  "dataviz": {
    "type": "stdio",
    "command": "docker",
    "args": ["run", "--rm", "-i", "saitejamothukuri/dataviz-mcp-server:latest"]
  }
}
```

### Restart Your Client

Restart Claude Desktop or Cursor to load the MCP server.

## 📊 What You Can Do

### Load Data
- CSV files
- Excel (XLSX, XLS)
- PostgreSQL, MySQL, SQL Server
- MongoDB
- AWS S3, Google BigQuery, Azure Blob Storage

### Create Visualizations
- Bar charts
- Line charts
- Pie charts
- Scatter plots
- Heatmaps
- Histograms
- Box plots
- Interactive dashboards

### Analyze Data
- Generate statistical reports
- Preview datasets
- Calculate correlations
- Explore data structure

## 💡 Usage Examples

```
"Load C:\Users\username\data\sales.csv and create a bar chart"

"Connect to my PostgreSQL database and show a summary report"

"Load data from S3 and create a dashboard"
```

## 📂 Project Structure

```
dataviz-mcp-server/
├── server.py              (20 MCP tools)
├── Dockerfile             (Container image)
├── requirements.txt       (Python packages)
├── LICENSE               (MIT)
├── README.md             (This file)
├── compose.public.yaml   (Docker Compose setup)
├── data/                 (Your data files)
└── outputs/              (Generated visualizations)
```

## 🔧 With File Access (Volume Mounting)

To load local files, update your config to mount a volume:

```json
{
  "dataviz": {
    "type": "stdio",
    "command": "docker",
    "args": [
      "run",
      "--rm",
      "-i",
      "-v",
      "C:\\Users\\YourName\\Documents\\data:/app/data",
      "saitejamothukuri/dataviz-mcp-server:latest"
    ]
  }
}
```

Then use paths like `/app/data/file.csv` in your MCP client.

## 🐳 Docker Hub

**Image:** `saitejamothukuri/dataviz-mcp-server:latest`

Pull latest version:
```bash
docker pull saitejamothukuri/dataviz-mcp-server:latest
```

## ✨ 20 Tools Available

**Data Loading (7 tools)**
- load_csv_file
- load_excel_file
- connect_sql_database
- connect_mongodb
- load_aws_s3_file
- load_gcp_bigquery
- load_azure_blob

**Visualization (8 tools)**
- create_bar_chart
- create_line_chart
- create_pie_chart
- create_scatter_plot
- create_heatmap
- create_histogram
- create_box_plot
- create_dashboard

**Analysis (4 tools)**
- list_loaded_datasets
- preview_dataset
- generate_summary_report
- get_file_path_help

## 🆘 File Path Formats

The server automatically handles:
- Windows: `C:\Users\username\data.csv` ✅
- WSL: `/mnt/c/Users/username/data.csv` ✅
- Linux: `/home/user/data.csv` ✅

## 📖 More Information

- **GitHub:** https://github.com/saiteja007-mv/Personalized-MCP-Servers/tree/main/dataviz-mcp-server
- **Docker Hub:** https://hub.docker.com/r/saitejamothukuri/dataviz-mcp-server
- **MCP Protocol:** https://modelcontextprotocol.io

## 📄 License

MIT License - See LICENSE file

---

**Ready to visualize your data?** Add the configuration above and start using in your MCP client! 📊
