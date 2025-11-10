#!/usr/bin/env python3
"""
A Simple MCP Server Example: Sentiment Analysis Tool

This MCP server exposes a sentiment analysis tool that Claude can call.
It demonstrates the core concepts of MCP:
- Server setup
- Tool definition
- Tool execution
- Response formatting
"""

import asyncio
from mcp.server import Server
from mcp.types import Tool, TextContent
from mcp.server.stdio import stdio_server

# Create an MCP server instance
app = Server("sentiment-analyzer")


# Define what tools this server provides
@app.list_tools()
async def list_tools() -> list[Tool]:
    """
    Tell Claude what tools are available.

    This is like publishing an API specification - Claude can see
    what tools exist and how to call them.
    """
    return [
        Tool(
            name="analyze_sentiment",
            description="Analyzes the sentiment of text and returns positive, negative, or neutral",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to analyze for sentiment"
                    }
                },
                "required": ["text"]
            }
        )
    ]


# Implement the actual tool logic
@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """
    Execute the tool when Claude calls it.

    This is where the actual work happens - Claude sends a tool name
    and arguments, and we return results.
    """
    if name != "analyze_sentiment":
        raise ValueError(f"Unknown tool: {name}")

    text = arguments["text"]

    # Simple sentiment analysis logic (you could use ML models here!)
    positive_words = ["good", "great", "excellent", "happy", "love", "wonderful", "fantastic"]
    negative_words = ["bad", "terrible", "awful", "hate", "horrible", "poor", "worst"]

    text_lower = text.lower()
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)

    if positive_count > negative_count:
        sentiment = "positive"
        confidence = min(0.9, 0.5 + (positive_count * 0.1))
    elif negative_count > positive_count:
        sentiment = "negative"
        confidence = min(0.9, 0.5 + (negative_count * 0.1))
    else:
        sentiment = "neutral"
        confidence = 0.5

    result = {
        "sentiment": sentiment,
        "confidence": confidence,
        "positive_signals": positive_count,
        "negative_signals": negative_count,
        "text_analyzed": text
    }

    # Return results in MCP format
    return [
        TextContent(
            type="text",
            text=f"Sentiment Analysis Result:\n"
                 f"Sentiment: {sentiment}\n"
                 f"Confidence: {confidence:.2f}\n"
                 f"Positive signals: {positive_count}\n"
                 f"Negative signals: {negative_count}"
        )
    ]


async def main():
    """
    Run the MCP server using stdio transport.

    Stdio (standard input/output) is the most common way to run MCP servers.
    Claude communicates with the server through stdin/stdout.
    """
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
