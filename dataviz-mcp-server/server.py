import os
import sys
import json
import logging
from fastmcp import FastMCP
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO, BytesIO
import base64
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger("visualization-server")

mcp = FastMCP("DataViz Pro")

DATA_CACHE = {}

@mcp.tool()
def get_file_path_help():
    """Get instructions on how to provide file paths to the DataViz server when using Cursor or other MCP clients."""
    help_text = {
        "overview": "The DataViz server runs in a Docker container and needs special handling for file paths from Cursor or other clients.",
        "supported_path_formats": [
            "Windows absolute paths: C:\\Users\\username\\data\\file.csv",
            "WSL paths: /mnt/c/Users/username/data/file.csv",
            "Linux/Unix paths: /home/user/data/file.csv",
            "Container paths: /app/data/file.csv"
        ],
        "methods": {
            "method_1_use_docker_volume": {
                "description": "Mount your local directory to /app/data in the container (RECOMMENDED)",
                "steps": [
                    "1. Update your Cursor MCP config to mount volumes",
                    "2. Modify ~/.cursor/mcp.json dataviz configuration",
                    "3. Change the docker run command to include volume mounts"
                ],
                "example_config": {
                    "dataviz": {
                        "type": "stdio",
                        "command": "docker",
                        "args": [
                            "run",
                            "--rm",
                            "-i",
                            "-v",
                            "C:\\Users\\username\\Documents\\data:/app/data",
                            "saitejamothukuri/dataviz-mcp-server:latest"
                        ]
                    }
                },
                "then_use": "/app/data/file.csv in the MCP tool"
            },
            "method_2_automatic_path_resolution": {
                "description": "The server automatically converts Windows paths to WSL/Linux format",
                "how_it_works": "Pass your Windows path directly - the server will handle conversion",
                "example": "C:\\Users\\username\\Documents\\data.csv will be converted to /mnt/c/Users/username/Documents/data.csv"
            },
            "method_3_use_wsl_paths": {
                "description": "If using WSL, pass WSL-formatted paths directly",
                "example": "/mnt/c/Users/username/Documents/data.csv"
            }
        },
        "recommended_approach": "Use Method 1 (Docker volume mounting) for best performance and easier path handling"
    }

    logger.info("User requested file path help")
    return json.dumps(help_text, indent=2)

def resolve_file_path(file_path: str) -> tuple[bool, str]:
    """
    Resolve file path from Cursor or other clients.
    Handles Windows paths passed to Docker container.
    Returns (success: bool, resolved_path: str)
    """
    try:
        # Original path
        original_path = file_path.strip()
        logger.info(f"Attempting to resolve path: {original_path}")

        # Try as-is first (for Unix-like paths in container)
        if os.path.exists(original_path):
            logger.info(f"Found file at: {original_path}")
            return True, original_path

        # Convert Windows path to WSL path if needed
        if '\\' in original_path or ':' in original_path:
            # Windows path like C:\Users\... -> /mnt/c/Users/...
            if len(original_path) > 1 and original_path[1] == ':':
                drive_letter = original_path[0].lower()
                rest_of_path = original_path[2:].replace('\\', '/')
                wsl_path = f"/mnt/{drive_letter}{rest_of_path}"
                logger.info(f"Converted Windows path to WSL: {wsl_path}")

                if os.path.exists(wsl_path):
                    logger.info(f"Found file at WSL path: {wsl_path}")
                    return True, wsl_path

        # Try with forward slashes
        forward_slash_path = original_path.replace('\\', '/')
        if os.path.exists(forward_slash_path):
            logger.info(f"Found file with forward slashes: {forward_slash_path}")
            return True, forward_slash_path

        # List available directories for debugging
        available_dirs = []
        for root, dirs, files in os.walk('/'):
            if len(available_dirs) < 5:  # Limit to first 5 for logging
                available_dirs.extend([os.path.join(root, d) for d in dirs[:2]])

        error_msg = f"File not found: {original_path}. Make sure to use absolute paths or copy files to /app/data directory in the container."
        logger.error(error_msg)
        return False, error_msg

    except Exception as e:
        error_msg = f"Error resolving path {file_path}: {str(e)}"
        logger.error(error_msg)
        return False, error_msg

@mcp.tool()
def load_csv_file(file_path: str = "", delimiter: str = ",", encoding: str = "utf-8"):
    """Load a CSV file into memory for visualization. Returns dataset info including columns, row count, and sample data. Accepts absolute file paths from Windows, WSL, or Linux."""
    try:
        if not file_path:
            return "Error: file_path parameter is required"

        # Resolve the file path
        success, resolved_path = resolve_file_path(file_path)
        if not success:
            return f"Error: {resolved_path}"

        df = pd.read_csv(resolved_path, delimiter=delimiter, encoding=encoding)
        dataset_id = f"csv_{hash(resolved_path)}"
        DATA_CACHE[dataset_id] = df

        info = {
            "dataset_id": dataset_id,
            "rows": len(df),
            "columns": list(df.columns),
            "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
            "sample": df.head(5).to_dict(orient='records')
        }

        logger.info(f"Loaded CSV: {resolved_path} with {len(df)} rows")
        return json.dumps(info, indent=2)
    except Exception as e:
        logger.error(f"Error loading CSV: {str(e)}")
        return f"Error loading CSV file: {str(e)}"

@mcp.tool()
def load_excel_file(file_path: str = "", sheet_name: str = ""):
    """Load an Excel file into memory. If sheet_name is empty, loads the first sheet. Returns dataset info. Accepts absolute file paths from Windows, WSL, or Linux."""
    try:
        if not file_path:
            return "Error: file_path parameter is required"

        # Resolve the file path
        success, resolved_path = resolve_file_path(file_path)
        if not success:
            return f"Error: {resolved_path}"

        sheet = sheet_name if sheet_name else 0
        df = pd.read_excel(resolved_path, sheet_name=sheet)
        dataset_id = f"excel_{hash(resolved_path + str(sheet))}"
        DATA_CACHE[dataset_id] = df

        info = {
            "dataset_id": dataset_id,
            "rows": len(df),
            "columns": list(df.columns),
            "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
            "sample": df.head(5).to_dict(orient='records')
        }

        logger.info(f"Loaded Excel: {resolved_path}, sheet: {sheet}")
        return json.dumps(info, indent=2)
    except Exception as e:
        logger.error(f"Error loading Excel: {str(e)}")
        return f"Error loading Excel file: {str(e)}"

@mcp.tool()
def connect_sql_database(connection_string: str = "", query: str = ""):
    """Connect to SQL database and execute query. Connection string format: dialect://username:password@host:port/database. Supports PostgreSQL, MySQL, SQL Server."""
    try:
        if not connection_string or not query:
            return "Error: Both connection_string and query parameters are required"
        
        from sqlalchemy import create_engine
        engine = create_engine(connection_string)
        df = pd.read_sql(query, engine)
        dataset_id = f"sql_{hash(connection_string + query)}"
        DATA_CACHE[dataset_id] = df
        
        info = {
            "dataset_id": dataset_id,
            "rows": len(df),
            "columns": list(df.columns),
            "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
            "sample": df.head(5).to_dict(orient='records')
        }
        
        logger.info(f"Loaded SQL data: {len(df)} rows")
        return json.dumps(info, indent=2)
    except Exception as e:
        logger.error(f"Error connecting to SQL database: {str(e)}")
        return f"Error connecting to SQL database: {str(e)}"

@mcp.tool()
def connect_mongodb(connection_string: str = "", database: str = "", collection: str = "", query: str = "{}"):
    """Connect to MongoDB and fetch data. Query should be a JSON string representing MongoDB query filter."""
    try:
        if not connection_string or not database or not collection:
            return "Error: connection_string, database, and collection parameters are required"
        
        from pymongo import MongoClient
        client = MongoClient(connection_string)
        db = client[database]
        coll = db[collection]
        
        query_dict = json.loads(query) if query else {}
        cursor = coll.find(query_dict)
        df = pd.DataFrame(list(cursor))
        
        if '_id' in df.columns:
            df['_id'] = df['_id'].astype(str)
        
        dataset_id = f"mongo_{hash(connection_string + database + collection)}"
        DATA_CACHE[dataset_id] = df
        
        info = {
            "dataset_id": dataset_id,
            "rows": len(df),
            "columns": list(df.columns),
            "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
            "sample": df.head(5).to_dict(orient='records')
        }
        
        logger.info(f"Loaded MongoDB data: {len(df)} rows")
        return json.dumps(info, indent=2)
    except Exception as e:
        logger.error(f"Error connecting to MongoDB: {str(e)}")
        return f"Error connecting to MongoDB: {str(e)}"

@mcp.tool()
def load_aws_s3_file(bucket_name: str = "", file_key: str = "", aws_access_key: str = "", aws_secret_key: str = "", region: str = "us-east-1"):
    """Load a CSV or Excel file from AWS S3. Requires AWS credentials."""
    try:
        if not bucket_name or not file_key:
            return "Error: bucket_name and file_key parameters are required"
        
        import boto3
        from io import BytesIO
        
        s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key if aws_access_key else None,
            aws_secret_access_key=aws_secret_key if aws_secret_key else None,
            region_name=region
        )
        
        obj = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        file_content = obj['Body'].read()
        
        if file_key.endswith('.csv'):
            df = pd.read_csv(BytesIO(file_content))
        elif file_key.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(BytesIO(file_content))
        else:
            return "Error: Unsupported file format. Only CSV and Excel files are supported."
        
        dataset_id = f"s3_{hash(bucket_name + file_key)}"
        DATA_CACHE[dataset_id] = df
        
        info = {
            "dataset_id": dataset_id,
            "rows": len(df),
            "columns": list(df.columns),
            "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
            "sample": df.head(5).to_dict(orient='records')
        }
        
        logger.info(f"Loaded S3 file: {bucket_name}/{file_key}")
        return json.dumps(info, indent=2)
    except Exception as e:
        logger.error(f"Error loading from S3: {str(e)}")
        return f"Error loading from AWS S3: {str(e)}"

@mcp.tool()
def load_gcp_bigquery(project_id: str = "", query: str = "", credentials_json: str = ""):
    """Load data from Google BigQuery. credentials_json should be the path to service account JSON file or empty to use default credentials."""
    try:
        if not project_id or not query:
            return "Error: project_id and query parameters are required"
        
        from google.cloud import bigquery
        
        if credentials_json:
            client = bigquery.Client.from_service_account_json(credentials_json, project=project_id)
        else:
            client = bigquery.Client(project=project_id)
        
        df = client.query(query).to_dataframe()
        dataset_id = f"bigquery_{hash(project_id + query)}"
        DATA_CACHE[dataset_id] = df
        
        info = {
            "dataset_id": dataset_id,
            "rows": len(df),
            "columns": list(df.columns),
            "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
            "sample": df.head(5).to_dict(orient='records')
        }
        
        logger.info(f"Loaded BigQuery data: {len(df)} rows")
        return json.dumps(info, indent=2)
    except Exception as e:
        logger.error(f"Error loading from BigQuery: {str(e)}")
        return f"Error loading from Google BigQuery: {str(e)}"

@mcp.tool()
def load_azure_blob(account_name: str = "", container_name: str = "", blob_name: str = "", account_key: str = ""):
    """Load a CSV or Excel file from Azure Blob Storage. Requires Azure storage account credentials."""
    try:
        if not account_name or not container_name or not blob_name:
            return "Error: account_name, container_name, and blob_name parameters are required"
        
        from azure.storage.blob import BlobServiceClient
        
        connection_string = f"DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={account_key};EndpointSuffix=core.windows.net"
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        
        stream = BytesIO()
        blob_client.download_blob().readinto(stream)
        stream.seek(0)
        
        if blob_name.endswith('.csv'):
            df = pd.read_csv(stream)
        elif blob_name.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(stream)
        else:
            return "Error: Unsupported file format. Only CSV and Excel files are supported."
        
        dataset_id = f"azure_{hash(account_name + container_name + blob_name)}"
        DATA_CACHE[dataset_id] = df
        
        info = {
            "dataset_id": dataset_id,
            "rows": len(df),
            "columns": list(df.columns),
            "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
            "sample": df.head(5).to_dict(orient='records')
        }
        
        logger.info(f"Loaded Azure Blob: {container_name}/{blob_name}")
        return json.dumps(info, indent=2)
    except Exception as e:
        logger.error(f"Error loading from Azure: {str(e)}")
        return f"Error loading from Azure Blob Storage: {str(e)}"

@mcp.tool()
def list_loaded_datasets():
    """List all datasets currently loaded in memory with their IDs and basic information."""
    try:
        if not DATA_CACHE:
            return "No datasets currently loaded in memory."
        
        datasets = []
        for dataset_id, df in DATA_CACHE.items():
            datasets.append({
                "dataset_id": dataset_id,
                "rows": len(df),
                "columns": list(df.columns),
                "memory_usage_mb": round(df.memory_usage(deep=True).sum() / 1024 / 1024, 2)
            })
        
        return json.dumps({"datasets": datasets}, indent=2)
    except Exception as e:
        logger.error(f"Error listing datasets: {str(e)}")
        return f"Error listing datasets: {str(e)}"

@mcp.tool()
def preview_dataset(dataset_id: str = "", num_rows: str = "10"):
    """Preview a loaded dataset. Shows first N rows with column information."""
    try:
        if not dataset_id:
            return "Error: dataset_id parameter is required"
        
        if dataset_id not in DATA_CACHE:
            return f"Error: Dataset {dataset_id} not found. Use list_loaded_datasets to see available datasets."
        
        df = DATA_CACHE[dataset_id]
        n = int(num_rows)
        
        preview = {
            "dataset_id": dataset_id,
            "total_rows": len(df),
            "columns": list(df.columns),
            "preview_rows": df.head(n).to_dict(orient='records'),
            "statistics": df.describe().to_dict()
        }
        
        return json.dumps(preview, indent=2)
    except Exception as e:
        logger.error(f"Error previewing dataset: {str(e)}")
        return f"Error previewing dataset: {str(e)}"

@mcp.tool()
def create_bar_chart(dataset_id: str = "", x_column: str = "", y_column: str = "", title: str = "", output_path: str = "/app/outputs/bar_chart.html"):
    """Create an interactive bar chart using Plotly. Returns HTML file path."""
    try:
        if not dataset_id or not x_column or not y_column:
            return "Error: dataset_id, x_column, and y_column parameters are required"
        
        if dataset_id not in DATA_CACHE:
            return f"Error: Dataset {dataset_id} not found"
        
        df = DATA_CACHE[dataset_id]
        
        if x_column not in df.columns or y_column not in df.columns:
            return f"Error: Columns {x_column} or {y_column} not found in dataset"
        
        fig = px.bar(df, x=x_column, y=y_column, title=title if title else f"{y_column} by {x_column}")
        fig.update_layout(template="plotly_white", showlegend=True)
        fig.write_html(output_path)
        
        logger.info(f"Created bar chart: {output_path}")
        return f"Bar chart created successfully and saved to {output_path}"
    except Exception as e:
        logger.error(f"Error creating bar chart: {str(e)}")
        return f"Error creating bar chart: {str(e)}"

@mcp.tool()
def create_line_chart(dataset_id: str = "", x_column: str = "", y_column: str = "", title: str = "", output_path: str = "/app/outputs/line_chart.html"):
    """Create an interactive line chart using Plotly. Useful for time series data. Returns HTML file path."""
    try:
        if not dataset_id or not x_column or not y_column:
            return "Error: dataset_id, x_column, and y_column parameters are required"
        
        if dataset_id not in DATA_CACHE:
            return f"Error: Dataset {dataset_id} not found"
        
        df = DATA_CACHE[dataset_id]
        
        if x_column not in df.columns or y_column not in df.columns:
            return f"Error: Columns {x_column} or {y_column} not found in dataset"
        
        fig = px.line(df, x=x_column, y=y_column, title=title if title else f"{y_column} over {x_column}")
        fig.update_layout(template="plotly_white", showlegend=True)
        fig.write_html(output_path)
        
        logger.info(f"Created line chart: {output_path}")
        return f"Line chart created successfully and saved to {output_path}"
    except Exception as e:
        logger.error(f"Error creating line chart: {str(e)}")
        return f"Error creating line chart: {str(e)}"

@mcp.tool()
def create_pie_chart(dataset_id: str = "", names_column: str = "", values_column: str = "", title: str = "", output_path: str = "/app/outputs/pie_chart.html"):
    """Create an interactive pie chart using Plotly. Returns HTML file path."""
    try:
        if not dataset_id or not names_column or not values_column:
            return "Error: dataset_id, names_column, and values_column parameters are required"
        
        if dataset_id not in DATA_CACHE:
            return f"Error: Dataset {dataset_id} not found"
        
        df = DATA_CACHE[dataset_id]
        
        if names_column not in df.columns or values_column not in df.columns:
            return f"Error: Columns {names_column} or {values_column} not found in dataset"
        
        fig = px.pie(df, names=names_column, values=values_column, title=title if title else f"Distribution of {values_column}")
        fig.update_layout(template="plotly_white")
        fig.write_html(output_path)
        
        logger.info(f"Created pie chart: {output_path}")
        return f"Pie chart created successfully and saved to {output_path}"
    except Exception as e:
        logger.error(f"Error creating pie chart: {str(e)}")
        return f"Error creating pie chart: {str(e)}"

@mcp.tool()
def create_scatter_plot(dataset_id: str = "", x_column: str = "", y_column: str = "", color_column: str = "", title: str = "", output_path: str = "/app/outputs/scatter_plot.html"):
    """Create an interactive scatter plot using Plotly. Optionally color points by a third column. Returns HTML file path."""
    try:
        if not dataset_id or not x_column or not y_column:
            return "Error: dataset_id, x_column, and y_column parameters are required"
        
        if dataset_id not in DATA_CACHE:
            return f"Error: Dataset {dataset_id} not found"
        
        df = DATA_CACHE[dataset_id]
        
        if x_column not in df.columns or y_column not in df.columns:
            return f"Error: Columns {x_column} or {y_column} not found in dataset"
        
        color = color_column if color_column and color_column in df.columns else None
        
        fig = px.scatter(df, x=x_column, y=y_column, color=color, title=title if title else f"{y_column} vs {x_column}")
        fig.update_layout(template="plotly_white")
        fig.write_html(output_path)
        
        logger.info(f"Created scatter plot: {output_path}")
        return f"Scatter plot created successfully and saved to {output_path}"
    except Exception as e:
        logger.error(f"Error creating scatter plot: {str(e)}")
        return f"Error creating scatter plot: {str(e)}"

@mcp.tool()
def create_heatmap(dataset_id: str = "", title: str = "", output_path: str = "/app/outputs/heatmap.html"):
    """Create a correlation heatmap for numeric columns in the dataset using Plotly. Returns HTML file path."""
    try:
        if not dataset_id:
            return "Error: dataset_id parameter is required"
        
        if dataset_id not in DATA_CACHE:
            return f"Error: Dataset {dataset_id} not found"
        
        df = DATA_CACHE[dataset_id]
        numeric_df = df.select_dtypes(include=['number'])
        
        if numeric_df.empty:
            return "Error: No numeric columns found in dataset for correlation heatmap"
        
        corr = numeric_df.corr()
        
        fig = go.Figure(data=go.Heatmap(
            z=corr.values,
            x=corr.columns,
            y=corr.columns,
            colorscale='RdBu',
            zmid=0
        ))
        
        fig.update_layout(
            title=title if title else "Correlation Heatmap",
            template="plotly_white"
        )
        fig.write_html(output_path)
        
        logger.info(f"Created heatmap: {output_path}")
        return f"Heatmap created successfully and saved to {output_path}"
    except Exception as e:
        logger.error(f"Error creating heatmap: {str(e)}")
        return f"Error creating heatmap: {str(e)}"

@mcp.tool()
def create_histogram(dataset_id: str = "", column: str = "", bins: str = "30", title: str = "", output_path: str = "/app/outputs/histogram.html"):
    """Create an interactive histogram using Plotly. Returns HTML file path."""
    try:
        if not dataset_id or not column:
            return "Error: dataset_id and column parameters are required"
        
        if dataset_id not in DATA_CACHE:
            return f"Error: Dataset {dataset_id} not found"
        
        df = DATA_CACHE[dataset_id]
        
        if column not in df.columns:
            return f"Error: Column {column} not found in dataset"
        
        nbins = int(bins)
        
        fig = px.histogram(df, x=column, nbins=nbins, title=title if title else f"Distribution of {column}")
        fig.update_layout(template="plotly_white")
        fig.write_html(output_path)
        
        logger.info(f"Created histogram: {output_path}")
        return f"Histogram created successfully and saved to {output_path}"
    except Exception as e:
        logger.error(f"Error creating histogram: {str(e)}")
        return f"Error creating histogram: {str(e)}"

@mcp.tool()
def create_box_plot(dataset_id: str = "", y_column: str = "", x_column: str = "", title: str = "", output_path: str = "/app/outputs/box_plot.html"):
    """Create an interactive box plot using Plotly. If x_column is provided, creates grouped box plots. Returns HTML file path."""
    try:
        if not dataset_id or not y_column:
            return "Error: dataset_id and y_column parameters are required"
        
        if dataset_id not in DATA_CACHE:
            return f"Error: Dataset {dataset_id} not found"
        
        df = DATA_CACHE[dataset_id]
        
        if y_column not in df.columns:
            return f"Error: Column {y_column} not found in dataset"
        
        x = x_column if x_column and x_column in df.columns else None
        
        fig = px.box(df, y=y_column, x=x, title=title if title else f"Box Plot of {y_column}")
        fig.update_layout(template="plotly_white")
        fig.write_html(output_path)
        
        logger.info(f"Created box plot: {output_path}")
        return f"Box plot created successfully and saved to {output_path}"
    except Exception as e:
        logger.error(f"Error creating box plot: {str(e)}")
        return f"Error creating box plot: {str(e)}"

@mcp.tool()
def create_dashboard(dataset_id: str = "", title: str = "Interactive Dashboard", output_path: str = "/app/outputs/dashboard.html"):
    """Create a comprehensive dashboard with multiple visualizations for the dataset. Returns HTML file path."""
    try:
        if not dataset_id:
            return "Error: dataset_id parameter is required"
        
        if dataset_id not in DATA_CACHE:
            return f"Error: Dataset {dataset_id} not found"
        
        df = DATA_CACHE[dataset_id]
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        
        if len(numeric_cols) < 2:
            return "Error: Dataset needs at least 2 numeric columns for dashboard creation"
        
        from plotly.subplots import make_subplots
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Correlation Heatmap', 'Distribution', 'Box Plots', 'Summary Statistics'),
            specs=[[{"type": "heatmap"}, {"type": "histogram"}],
                   [{"type": "box"}, {"type": "table"}]]
        )
        
        corr = df[numeric_cols].corr()
        fig.add_trace(
            go.Heatmap(z=corr.values, x=corr.columns, y=corr.columns, colorscale='RdBu', zmid=0),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Histogram(x=df[numeric_cols[0]], name=numeric_cols[0]),
            row=1, col=2
        )
        
        for col in numeric_cols[:3]:
            fig.add_trace(
                go.Box(y=df[col], name=col),
                row=2, col=1
            )
        
        stats = df[numeric_cols].describe().round(2)
        fig.add_trace(
            go.Table(
                header=dict(values=['Statistic'] + list(stats.columns)),
                cells=dict(values=[stats.index] + [stats[col] for col in stats.columns])
            ),
            row=2, col=2
        )
        
        fig.update_layout(
            title_text=title,
            template="plotly_white",
            height=800,
            showlegend=False
        )
        
        fig.write_html(output_path)
        
        logger.info(f"Created dashboard: {output_path}")
        return f"Dashboard created successfully with multiple visualizations and saved to {output_path}"
    except Exception as e:
        logger.error(f"Error creating dashboard: {str(e)}")
        return f"Error creating dashboard: {str(e)}"

@mcp.tool()
def generate_summary_report(dataset_id: str = ""):
    """Generate a comprehensive statistical summary report of the dataset including missing values, data types, and basic statistics."""
    try:
        if not dataset_id:
            return "Error: dataset_id parameter is required"
        
        if dataset_id not in DATA_CACHE:
            return f"Error: Dataset {dataset_id} not found"
        
        df = DATA_CACHE[dataset_id]
        
        report = {
            "dataset_id": dataset_id,
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "memory_usage_mb": round(df.memory_usage(deep=True).sum() / 1024 / 1024, 2),
            "columns": {
                col: {
                    "dtype": str(df[col].dtype),
                    "missing_values": int(df[col].isnull().sum()),
                    "missing_percentage": round(df[col].isnull().sum() / len(df) * 100, 2),
                    "unique_values": int(df[col].nunique())
                }
                for col in df.columns
            },
            "numeric_summary": df.describe().to_dict() if not df.select_dtypes(include=['number']).empty else {}
        }
        
        return json.dumps(report, indent=2)
    except Exception as e:
        logger.error(f"Error generating summary report: {str(e)}")
        return f"Error generating summary report: {str(e)}"

if __name__ == "__main__":
    logger.info("Starting DataViz Pro MCP Server")
    mcp.run()