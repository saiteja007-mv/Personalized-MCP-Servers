# DataViz MCP Server - Cursor File Path Fix

## Issue Fixed

The DataViz MCP server now correctly resolves file paths when used in Cursor or other MCP clients. Previously, Windows file paths passed to the Docker container couldn't be resolved.

## What Changed

The updated server (pushed to Docker Hub) includes:

1. **Automatic Path Resolution** - The server automatically converts Windows paths to WSL/Linux format
2. **Multiple Path Format Support** - Accepts Windows, WSL, and Linux paths
3. **Better Error Messages** - Clear feedback when files can't be found
4. **New Helper Tool** - `get_file_path_help()` for path usage instructions

## How to Update

Since you're running the latest Docker image, pull the updated version:

```bash
docker pull saitejamothukuri/dataviz-mcp-server:latest
```

Then restart your Cursor application.

## File Path Usage in Cursor

### Method 1: Direct Windows Paths (Easiest)

Simply pass your Windows file path directly:

```
Load dataset: C:\Users\YourUsername\Documents\data.csv
```

The server will automatically convert it to WSL format:
- `C:\Users\YourUsername\Documents\data.csv` → `/mnt/c/Users/YourUsername/Documents/data.csv`

### Method 2: Mount Docker Volumes (Recommended)

For better performance, mount your local directory to the container.

**Update your Cursor MCP config** (`%APPDATA%\Claude\mcp.json`):

```json
{
  "mcpServers": {
    "dataviz": {
      "type": "stdio",
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "-v",
        "C:\\Users\\YourUsername\\Documents\\data:/app/data",
        "-v",
        "C:\\Users\\YourUsername\\Documents\\outputs:/app/outputs",
        "saitejamothukuri/dataviz-mcp-server:latest"
      ]
    }
  }
}
```

Then use paths like:
```
Load dataset: /app/data/file.csv
```

### Method 3: WSL Paths

If using WSL, you can pass WSL-formatted paths directly:

```
Load dataset: /mnt/c/Users/YourUsername/Documents/data.csv
```

## Supported File Types

- **CSV**: `.csv` files
- **Excel**: `.xlsx`, `.xls` files
- **SQL Database**: Via connection strings
- **MongoDB**: Via connection strings
- **Cloud Storage**: AWS S3, Google BigQuery, Azure Blob Storage

## Testing Your Setup

1. Save a CSV file somewhere on your computer
2. In Cursor, ask the DataViz MCP server to load it:

   **Prompt:**
   ```
   Please load this CSV file and tell me about its structure:
   C:\Users\YourUsername\Documents\sample.csv
   ```

3. The server should respond with:
   - Number of rows and columns
   - Column names and data types
   - Sample of the first 5 rows

## If You Still Get Path Errors

1. **Get Path Help** - Call the `get_file_path_help()` tool in Cursor to see all supported formats

2. **Check File Exists** - Make sure the file path is correct:
   ```bash
   # In Windows PowerShell or Command Prompt
   dir "C:\Users\YourUsername\Documents\data.csv"
   ```

3. **Use Container Path** - Copy the file to the mounted `/app/data` directory:
   ```bash
   # If using Method 2 with volume mounts
   cp "C:\Users\YourUsername\Documents\data.csv" "C:\Users\YourUsername\Documents\data\data.csv"
   # Then use: /app/data/data.csv
   ```

4. **Check Docker is Running** - Ensure Docker Desktop is running:
   ```bash
   docker ps
   ```

## Path Resolution Examples

| You Pass | Server Converts To | Works? |
|----------|-------------------|--------|
| `C:\Users\user\data.csv` | `/mnt/c/Users/user/data.csv` | ✅ Yes |
| `D:\Project\files\data.csv` | `/mnt/d/Project/files/data.csv` | ✅ Yes |
| `/mnt/c/Users/user/data.csv` | (used as-is) | ✅ Yes |
| `/app/data/data.csv` | (used as-is if mounted) | ✅ Yes |
| `data.csv` | (error - relative paths not supported) | ❌ No |
| `C:/Users/user/data.csv` | (converts to backslashes first) | ✅ Yes |

## New Tools Available

### get_file_path_help()

Returns detailed instructions on file path formats and methods:

```
Call this in Cursor when you need help with file paths
```

This tool provides:
- Overview of Docker container file handling
- All supported path formats
- Three different methods to load files
- Recommended approach

## Excel Files with Multiple Sheets

When loading Excel files, specify the sheet:

```
Load this Excel file: C:\Users\user\data.xlsx
From sheet: "Sales"
```

If no sheet is specified, the first sheet is used.

## Next Steps

1. **Pull the latest image**: `docker pull saitejamothukuri/dataviz-mcp-server:latest`
2. **Restart Cursor**
3. **Try loading a file** - Use the examples above
4. **Call get_file_path_help()** if you need more details

## Issues?

If you still encounter issues:

1. Check that Docker Desktop is running
2. Verify your file path is absolute (not relative)
3. Make sure the file exists on your system
4. Try copying the file to an `/app/data` mounted directory
5. Call `get_file_path_help()` for troubleshooting steps
