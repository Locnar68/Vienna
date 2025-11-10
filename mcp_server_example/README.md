# MCP Server Example: Sentiment Analyzer

## What is This?

This is a **real MCP server** that exposes a sentiment analysis tool to Claude (or any MCP-compatible AI).

## How MCP Works

```
┌─────────┐         ┌──────────────┐         ┌──────────────┐
│  Claude │◄───────►│  MCP Server  │◄───────►│ External     │
│   (AI)  │  stdio  │   (Python)   │         │ Resources    │
└─────────┘         └──────────────┘         └──────────────┘
```

1. **Claude** discovers available tools by calling `list_tools()`
2. **Claude** calls a tool with `call_tool(name, arguments)`
3. **MCP Server** executes the tool and returns results
4. **Claude** uses the results to respond to the user

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Make the server executable
chmod +x sentiment_server.py
```

## Usage

### Option 1: Test the server directly (for development)

```bash
# Run the server (it will wait for stdio input)
python sentiment_server.py
```

### Option 2: Configure it with Claude Code (the real use case!)

Add this to your MCP configuration file (usually `~/.config/claude/mcp.json`):

```json
{
  "mcpServers": {
    "sentiment-analyzer": {
      "command": "python",
      "args": ["/home/user/Vienna/mcp_server_example/sentiment_server.py"]
    }
  }
}
```

Then restart Claude Code, and you'll be able to ask Claude to analyze sentiment!

## Example Conversation with Claude

**You:** "Can you analyze the sentiment of this customer review: 'This product is terrible and I hate it'"

**Claude:** *[Calls the analyze_sentiment tool via MCP]* "The review has negative sentiment with high confidence..."

## Key Concepts Demonstrated

1. **Server Setup**: Creating an MCP server with `Server("name")`
2. **Tool Declaration**: Using `@app.list_tools()` to tell Claude what's available
3. **Tool Implementation**: Using `@app.call_tool()` to execute the logic
4. **Stdio Transport**: Communicating via stdin/stdout (the standard way)
5. **Structured Responses**: Returning results in MCP's TextContent format

## What Makes This "MCP"?

- ✅ Follows the MCP specification
- ✅ Uses the official MCP Python SDK
- ✅ Can be discovered and called by any MCP client (like Claude)
- ✅ Uses standard transport (stdio)
- ✅ Returns structured responses

This is the **real deal** - a production-ready MCP server pattern!
