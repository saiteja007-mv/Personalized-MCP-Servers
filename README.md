# Creating MCP Servers with Claude - One Prompt Solution

This repository demonstrates how to create complete, working MCP (Model Context Protocol) servers using Claude AI with just a single, well-crafted prompt.

## 🚀 The Magic Prompt

Simply use this prompt with Claude to generate a complete MCP server:

```
You are an expert MCP (Model Context Protocol) server developer. You will create a complete, working MCP server based on the user's requirements.

<About the MCP Server>

CLARIFICATION PROCESS
Before generating the server, ensure you have:
1. Service name and description - Clear understanding of what the server does
2. API documentation - If integrating with external services, fetch and review API docs
3. Tool requirements - Specific list of tools/functions needed
4. Authentication needs - API keys, OAuth tokens, or other auth requirements
5. Output preferences - Any specific formatting or response requirements
If any critical information is missing, ASK THE USER for clarification before proceeding.

YOUR OUTPUT STRUCTURE
You must organize your response in TWO distinct sections:

SECTION 1: FILES TO CREATE
Generate EXACTLY these 5 files with complete content that the user can copy and save.
DO NOT create duplicate files or variations. Each file should appear ONCE with its complete content.

SECTION 2: INSTALLATION INSTRUCTIONS FOR THE USER
Provide step-by-step commands the user needs to run on their computer.
Present these as a clean, numbered list without creating duplicate instruction sets.

CRITICAL RULES FOR CODE GENERATION
1. NO `@mcp.prompt()` decorators - They break Claude Desktop
2. NO `prompt` parameter to FastMCP() - It breaks Claude Desktop
3. NO type hints from typing module - No `Optional`, `Union`, `List[str]`, etc.
4. NO complex parameter types - Use `param: str = ""` not `param: str = None`
5. SINGLE-LINE DOCSTRINGS ONLY - Multi-line docstrings cause gateway panic errors
6. DEFAULT TO EMPTY STRINGS - Use `param: str = ""` never `param: str = None`
7. ALWAYS return strings from tools - All tools must return formatted strings
8. ALWAYS use Docker - The server must run in a Docker container
9. ALWAYS log to stderr - Use the logging configuration provided
10. ALWAYS handle errors gracefully - Return user-friendly error messages
```

## 📁 What You Get

When you use this prompt, Claude will generate exactly 5 files:

1. **`server.py`** - The main MCP server implementation
2. **`requirements.txt`** - Python dependencies
3. **`Dockerfile`** - Container configuration
4. **`compose.yaml`** - Docker Compose setup
5. **`README.md`** - Project-specific documentation

## 🛠️ How It Works

### Step 1: Describe Your MCP Server
Tell Claude what you want your MCP server to do. For example:
- "Create an MCP server that integrates with GitHub API to manage repositories"
- "Build a weather MCP server that fetches current conditions and forecasts"
- "Make a file management MCP server for organizing documents"

### Step 2: Claude Generates Everything
Claude will:
- Ask clarifying questions if needed
- Generate all 5 required files
- Provide installation instructions
- Ensure the code follows MCP best practices

### Step 3: Deploy and Use
Follow the provided installation instructions to:
- Set up the Docker environment
- Configure any required API keys
- Start your MCP server
- Connect it to Claude Desktop

## 🎯 Key Features

- **Zero Configuration**: Just describe what you want and get a working server
- **Docker Ready**: All servers run in containers for consistency
- **Claude Desktop Compatible**: Follows all MCP protocol requirements
- **Error Handling**: Graceful error handling and user-friendly messages
- **Logging**: Proper logging to stderr for debugging
- **Type Safe**: Uses proper parameter types without breaking Claude Desktop

## 📋 Example Usage

### Example 1: GitHub Integration
```
I want an MCP server that can:
- List my GitHub repositories
- Create new repositories
- Manage issues and pull requests
- Search for code across repositories
```

### Example 2: Weather Service
```
Create a weather MCP server that:
- Gets current weather for any city
- Provides 5-day forecasts
- Shows weather alerts
- Converts between temperature units
```

### Example 3: File Management
```
Build a file management MCP server that can:
- Organize files by type and date
- Search for files by content
- Create folder structures
- Generate file reports
```

## 🔧 Technical Requirements

- Docker and Docker Compose
- Python 3.8+
- Claude Desktop with MCP support
- Internet connection (for external API integrations)

## 📚 Best Practices

1. **Be Specific**: The more detailed your requirements, the better the generated server
2. **Include APIs**: If you need external data, mention the specific APIs
3. **Authentication**: Specify what auth methods you need (API keys, OAuth, etc.)
4. **Error Handling**: Mention any specific error handling requirements
5. **Output Format**: Specify how you want data formatted (JSON, markdown, etc.)

## 🚨 Common Issues

- **Claude Desktop Crashes**: Usually caused by type hints or decorators - the prompt handles this
- **Docker Build Fails**: Check that all dependencies are in requirements.txt
- **API Errors**: Ensure API keys are properly configured
- **Permission Issues**: Make sure Docker has proper permissions

## 🎉 Success Stories

This approach has been used to create:
- Data visualization MCP servers
- API integration servers
- File management tools
- Database query servers
- Content generation tools

## 🤝 Contributing

If you create an interesting MCP server using this prompt, consider:
- Sharing your use case
- Contributing improvements to the prompt
- Documenting any new patterns you discover

## 📖 Learn More

- [MCP Protocol Documentation](https://modelcontextprotocol.io/)
- [Claude Desktop Setup](https://claude.ai/desktop)
- [Docker Documentation](https://docs.docker.com/)

---

**Ready to create your MCP server?** Just copy the prompt above and describe what you want to build! 🚀