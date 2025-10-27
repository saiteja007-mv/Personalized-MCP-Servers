# DataViz Pro MCP Server

A powerful Model Context Protocol (MCP) server for creating interactive data visualizations and dashboards from multiple data sources.

## 📋 Original Request

> "This MCP server should be for tools like powerBI which can generate visualizations, reports, dashboards from a cleaned datasets using User prompts. I would choose alternate resources like Python Based Visualization server, The data sources should be anything like CSV, Excels, Databases like SQL server, MySQL, MongoDB, AWS Cloud, GCP, Azure and all other types"

## 🎯 Overview

DataViz Pro is a Python-based visualization MCP server that provides an alternative to Power BI by generating interactive visualizations, reports, and dashboards using Plotly, Matplotlib, and Seaborn. It supports multiple data sources including local files, databases, and cloud storage.

## ✨ Features

### Data Source Support

- **Local Files**: CSV, Excel (XLSX, XLS)
- **Databases**: PostgreSQL, MySQL, SQL Server, MongoDB
- **Cloud Storage**:
  - AWS S3
  - Google Cloud BigQuery
  - Azure Blob Storage

### Visualization Types

- Bar Charts
- Line Charts
- Pie Charts
- Scatter Plots
- Histograms
- Box Plots
- Correlation Heatmaps
- Multi-panel Dashboards

### Analysis Tools

- Dataset preview and exploration
- Statistical summary reports
- Memory-efficient data caching
- Interactive HTML outputs

## 📦 Installation

### Prerequisites

- Docker Desktop installed and running
- Claude Desktop application
- Windows/macOS/Linux

### Step 1: Create Project Structure

```bash
mkdir dataviz-mcp-server
cd dataviz-mcp-server
mkdir data outputs
```

### Step 2: Create Required Files

Create the following 5 files in your project directory:*I*

#### 1. `Dockerfile`

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY server.py .

# Create directories for data and outputs
RUN mkdir -p /app/data /app/outputs

CMD ["python", "server.py"]
```

#### 2. `requirements.txt`

```txt
fastmcp
pandas
numpy
plotly
matplotlib
seaborn
openpyxl
xlrd
sqlalchemy
pymongo
psycopg2-binary
mysql-connector-python
boto3
google-cloud-bigquery
google-cloud-storage
azure-storage-blob
azure-identity
pyarrow
kaleido
```

#### 3. `server.py`

See the complete server.py code in the installation package.

#### 4. `compose.yaml`

```yaml
services:
  dataviz-server:
    build: .
    container_name: dataviz-mcp-server
    volumes:
      - ./data:/app/data
      - ./outputs:/app/outputs
    environment:
      - PYTHONUNBUFFERED=1
    stdin_open: true
    tty: false
    restart: "no"
```

### Step 3: Build Docker Image

```bash
docker compose build
```

### Step 4: Configure Claude Desktop

#### On Windows:

```bash
notepad %APPDATA%\Claude\claude_desktop_config.json
```

#### On macOS:

```bash
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

#### Configuration Content:

**Windows:**

```json
{
  "mcpServers": {
    "dataviz-pro": {
      "command": "docker",
      "args": [
        "compose",
        "-f",
        "C:\\Users\\YOUR_USERNAME\\dataviz-mcp-server\\compose.yaml",
        "run",
        "--rm",
        "-i",
        "dataviz-server"
      ]
    }
  }
}
```

**macOS/Linux:**

```json
{
  "mcpServers": {
    "dataviz-pro": {
      "command": "docker",
      "args": [
        "compose",
        "-f",
        "/absolute/path/to/dataviz-mcp-server/compose.yaml",
        "run",
        "--rm",
        "-i",
        "dataviz-server"
      ]
    }
  }
}
```

**⚠️ Important:** Replace the path with your actual project folder path!

### Step 5: Restart Claude Desktop

1. Completely quit Claude Desktop (not just close)
2. Restart the application
3. Look for the 🔌 icon in the bottom right
4. Verify "dataviz-pro" appears with available tools

## 🚀 Usage Examples

### Example 1: Load and Visualize CSV Data

```
Load the file /app/data/sales.csv and create a bar chart showing total_sales by month
```

### Example 2: Connect to SQL Database

```
Connect to my PostgreSQL database at postgresql://user:password@localhost:5432/mydb 
and run the query: SELECT * FROM sales WHERE year = 2024
Then create a line chart showing revenue over time
```

### Example 3: Load from AWS S3

```
Load the file sales-2024.csv from my S3 bucket "my-data-bucket" 
using access key AKIA... and secret key abc123...
Then create a pie chart of revenue by region
```

### Example 4: MongoDB Data Analysis

```
Connect to MongoDB at mongodb://localhost:27017
Database: analytics, Collection: user_events
Query: {"event_type": "purchase"}
Create a histogram of purchase amounts
```

### Example 5: Create Comprehensive Dashboard

```
Load /app/data/customer_data.csv and create a dashboard with multiple visualizations
```

### Example 6: Generate Summary Report

```
List all loaded datasets and generate a summary report for the CSV dataset
```

## 📊 Available Tools

### Data Loading Tools

1. **load_csv_file** - Load CSV files with custom delimiters
2. **load_excel_file** - Load Excel files (with sheet selection)
3. **connect_sql_database** - Connect to SQL databases (PostgreSQL, MySQL, SQL Server)
4. **connect_mongodb** - Fetch data from MongoDB
5. **load_aws_s3_file** - Load files from AWS S3 buckets
6. **load_gcp_bigquery** - Query Google BigQuery
7. **load_azure_blob** - Load files from Azure Blob Storage

### Dataset Management Tools

8. **list_loaded_datasets** - View all datasets in memory
9. **preview_dataset** - Preview dataset rows and statistics
10. **generate_summary_report** - Comprehensive statistical analysis

### Visualization Tools

11. **create_bar_chart** - Interactive bar charts
12. **create_line_chart** - Time series and trend analysis
13. **create_pie_chart** - Distribution visualization
14. **create_scatter_plot** - Relationship analysis with optional coloring
15. **create_histogram** - Distribution analysis
16. **create_box_plot** - Statistical distribution with outliers
17. **create_heatmap** - Correlation analysis
18. **create_dashboard** - Multi-panel comprehensive dashboard

## 📁 File Structure

```
dataviz-mcp-server/
├── Dockerfile
├── requirements.txt
├── server.py
├── compose.yaml
├── data/                 # Place your data files here
│   ├── sales.csv
│   └── customers.xlsx
└── outputs/              # Generated visualizations saved here
    ├── bar_chart.html
    ├── dashboard.html
    └── ...
```

## 🔧 Configuration

### Data Access Paths

When loading local files, use these path formats:

- **Inside Docker**: `/app/data/yourfile.csv`
- **Your Computer**: `./data/yourfile.csv` (files placed in the data folder)

### Database Connection Strings

**PostgreSQL:**

```
postgresql://username:password@host:5432/database
```

**MySQL:**

```
mysql+pymysql://username:password@host:3306/database
```

**SQL Server:**

```
mssql+pyodbc://username:password@host/database?driver=ODBC+Driver+17+for+SQL+Server
```

**MongoDB:**

```
mongodb://username:password@host:27017/
```

### Cloud Storage Credentials

**AWS S3:**

- `aws_access_key`: Your AWS access key ID
- `aws_secret_key`: Your AWS secret access key
- `region`: AWS region (default: us-east-1)

**Google BigQuery:**

- `credentials_json`: Path to service account JSON file
- `project_id`: GCP project ID

**Azure Blob:**

- `account_name`: Storage account name
- `account_key`: Storage account key

## 🐛 Troubleshooting

### Server Not Appearing in Claude Desktop

1. **Check Docker is running:**

   ```bash
   docker ps
   ```
2. **Verify configuration path:**

   - Ensure the path in `claude_desktop_config.json` is absolute
   - Use double backslashes `\\` on Windows
   - Use forward slashes `/` on macOS/Linux
3. **Check Claude Desktop logs:**

   - Windows: `%APPDATA%\Claude\logs\`
   - macOS: `~/Library/Logs/Claude/`
4. **Test server manually:**

   ```bash
   docker compose run --rm dataviz-server
   ```

   Should start without errors (press Ctrl+C to stop)

### "No configuration file provided: not found"

This means Docker can't find `compose.yaml`. Solutions:

- Use absolute path in `claude_desktop_config.json`
- Verify file is named `compose.yaml` (not `docker-compose.yml`)
- Ensure the `-f` flag points to the correct file

### Output Files Not Accessible

1. **Check volumes are mounted:**

   ```bash
   docker compose config
   ```
2. **Verify folder permissions:**

   ```bash
   # Windows
   icacls outputs /grant Users:F

   # macOS/Linux
   chmod 755 outputs
   ```
3. **Check file was created:**

   ```bash
   ls outputs/
   ```

### Memory Issues with Large Datasets

- Datasets are kept in memory during the session
- For very large files (>1GB), consider:
  - Loading only necessary columns
  - Filtering data at source (SQL WHERE clause)
  - Processing in chunks
  - Closing Claude to clear memory cache

## 🔒 Security Notes

### Credentials Management

- **Never commit credentials** to version control
- Use environment variables for sensitive data
- Consider using Docker secrets for production

### Network Access

- Server runs in isolated Docker container
- Only has access to mounted volumes (`./data` and `./outputs`)
- Database connections go through Docker network

### Data Privacy

- All data processing happens locally in Docker
- No data is sent to external services (except cloud data sources you configure)
- Generated visualizations are saved locally in `./outputs`

## 📈 Performance Tips

1. **Optimize data loading:**

   - Filter data at source when possible
   - Load only required columns
   - Use appropriate data types
2. **Visualization performance:**

   - Limit data points in scatter plots (<10k points)
   - Aggregate data before visualization
   - Use appropriate chart types for data size
3. **Memory management:**

   - Clear unused datasets periodically
   - Restart Claude Desktop to free memory
   - Monitor Docker container resources

## 🔄 Updates and Maintenance

### Rebuild After Changes

```bash
docker compose build --no-cache
```

### Update Dependencies

Edit `requirements.txt` and rebuild:

```bash
docker compose build
```

### View Logs

```bash
docker compose logs dataviz-server
```

### Clean Up

```bash
# Remove containers
docker compose down

# Remove images
docker compose down --rmi all

# Remove volumes
docker compose down -v
```

## 📚 Additional Resources

- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [Plotly Documentation](https://plotly.com/python/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)

## 🤝 Contributing

This is a custom MCP server. To modify:

1. Edit `server.py` to add new tools
2. Update `requirements.txt` for new dependencies
3. Rebuild Docker image
4. Restart Claude Desktop

## 📝 License

This project is provided as-is for use with Claude Desktop.

## 💡 Tips

- **Start Simple**: Test with a small CSV file first
- **Check Data**: Always preview datasets before visualization
- **Use Appropriate Charts**: Match visualization type to data type
- **Save Work**: Generated HTML files can be opened in any browser
- **Experiment**: Try different chart types to find the best representation

## 🎯 Best Practices

1. **Data Preparation**: Clean your data before loading
2. **Naming Conventions**: Use clear, descriptive column names
3. **File Organization**: Keep data files in the `data/` folder
4. **Output Management**: Regularly review and clean the `outputs/` folder
5. **Error Handling**: Check tool responses for error messages
6. **Performance**: Monitor memory usage with large datasets

---

**Date:** October 27, 2025
**Version:** 1.0.0
**MCP Protocol:** 2025-06-18
