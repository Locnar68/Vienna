#!/bin/bash
# AWS MCP Setup Script
# This script helps you set up the AWS MCP connector with Claude

set -e

echo "============================================"
echo "AWS MCP Setup for Claude"
echo "============================================"
echo ""

# Step 1: Check AWS credentials
echo "Step 1: Checking AWS credentials..."
if [ ! -d ~/.aws ]; then
    echo "⚠️  AWS credentials not found. Creating ~/.aws directory..."
    mkdir -p ~/.aws

    echo ""
    echo "Please configure your AWS credentials. You have two options:"
    echo ""
    echo "Option A: Use AWS CLI (recommended)"
    echo "  Run: aws configure"
    echo ""
    echo "Option B: Manual configuration"
    echo "  1. Create ~/.aws/credentials with:"
    echo "     [default]"
    echo "     aws_access_key_id = YOUR_ACCESS_KEY"
    echo "     aws_secret_access_key = YOUR_SECRET_KEY"
    echo ""
    echo "  2. Create ~/.aws/config with:"
    echo "     [default]"
    echo "     region = us-east-1"
    echo ""
    read -p "Press Enter after configuring AWS credentials..."
fi

if [ -f ~/.aws/credentials ]; then
    echo "✅ AWS credentials found"
else
    echo "❌ AWS credentials still not found. Please configure them first."
    exit 1
fi

# Step 2: Clone aws-mcp repository
echo ""
echo "Step 2: Cloning aws-mcp repository..."
cd /home/user
if [ -d "aws-mcp" ]; then
    echo "⚠️  aws-mcp directory already exists. Updating..."
    cd aws-mcp
    git pull
else
    git clone https://github.com/RafalWilinski/aws-mcp.git
    cd aws-mcp
fi

# Step 3: Install dependencies
echo ""
echo "Step 3: Installing dependencies..."
npm install

# Step 4: Get the installation path
AWS_MCP_PATH=$(pwd)
echo ""
echo "✅ AWS MCP installed at: $AWS_MCP_PATH"

# Step 5: Configure Claude Desktop
echo ""
echo "Step 4: Configuring Claude Desktop..."

# Find Claude config location (varies by system)
if [ "$(uname)" == "Darwin" ]; then
    # macOS
    CLAUDE_CONFIG_DIR="$HOME/Library/Application Support/Claude"
elif [ "$(uname)" == "Linux" ]; then
    # Linux
    CLAUDE_CONFIG_DIR="$HOME/.config/Claude"
else
    CLAUDE_CONFIG_DIR="$HOME/.config/Claude"
fi

mkdir -p "$CLAUDE_CONFIG_DIR"
CONFIG_FILE="$CLAUDE_CONFIG_DIR/claude_desktop_config.json"

echo "Claude config file: $CONFIG_FILE"

# Create or update config
if [ -f "$CONFIG_FILE" ]; then
    echo "⚠️  Existing Claude config found. Backing up..."
    cp "$CONFIG_FILE" "$CONFIG_FILE.backup"
    echo "Backup saved to: $CONFIG_FILE.backup"
fi

# Create new config
cat > "$CONFIG_FILE" << EOF
{
  "mcpServers": {
    "aws": {
      "command": "npm",
      "args": [
        "--silent",
        "--prefix",
        "$AWS_MCP_PATH",
        "start"
      ]
    }
  }
}
EOF

echo "✅ Claude config updated"

# Summary
echo ""
echo "============================================"
echo "Setup Complete! 🎉"
echo "============================================"
echo ""
echo "Next steps:"
echo "1. Restart Claude Desktop"
echo "2. Ask Claude: 'What AWS resources do I have?'"
echo "3. Try queries like:"
echo "   - 'List all my S3 buckets'"
echo "   - 'Show me EC2 instances'"
echo "   - 'What Lambda functions are deployed?'"
echo ""
echo "Troubleshooting:"
echo "  View logs: tail -f ~/Library/Logs/Claude/mcp-server-aws.log"
echo "             (or $HOME/.config/Claude/logs/mcp-server-aws.log on Linux)"
echo ""
echo "Configuration file: $CONFIG_FILE"
echo "AWS MCP path: $AWS_MCP_PATH"
echo ""
