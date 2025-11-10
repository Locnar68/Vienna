# AWS MCP Setup Guide for Claude

This guide will help you connect Claude to your AWS account using the Model Context Protocol (MCP).

## 🎯 What You'll Be Able to Do

Once configured, you can ask Claude:
- "List all my EC2 instances in us-east-1"
- "Show me my S3 buckets with their sizes"
- "What Lambda functions do I have deployed?"
- "Describe my VPC configuration"
- "Show me CloudWatch alarms that are in ALARM state"

Claude will query your AWS account in real-time and give you accurate answers!

## 📋 Prerequisites

You need:
- ✅ Node.js (you have v22.21.1)
- ✅ npm (you have v10.9.4)
- ✅ Claude Desktop installed
- ⚠️ AWS credentials (we'll set this up below)

## 🚀 Setup Steps

### Step 1: Get AWS Credentials

You need AWS access credentials. Here's how to get them:

#### Option A: Use Existing Credentials
If you already have AWS credentials, skip to Step 2.

#### Option B: Create New IAM User (Recommended)

1. **Log into AWS Console**: https://console.aws.amazon.com/
2. **Go to IAM** → Users → Create User
3. **User name**: `claude-mcp-user`
4. **Permissions**: Attach policies based on what you want Claude to access:
   - `ReadOnlyAccess` - Safe option, can read but not modify
   - Or specific policies like `AmazonS3ReadOnlyAccess`, `AmazonEC2ReadOnlyAccess`
5. **Create access key**:
   - Go to Security credentials tab
   - Create access key → Choose "Command Line Interface (CLI)"
   - **Download the credentials** (you'll need them in Step 2)

⚠️ **Security Note**: Start with read-only access. You can add write permissions later.

### Step 2: Configure AWS Credentials

Create the AWS credentials file:

```bash
# Create the directory
mkdir -p ~/.aws

# Create credentials file
cat > ~/.aws/credentials << 'EOF'
[default]
aws_access_key_id = YOUR_ACCESS_KEY_HERE
aws_secret_access_key = YOUR_SECRET_KEY_HERE
EOF

# Create config file
cat > ~/.aws/config << 'EOF'
[default]
region = us-east-1
output = json
EOF

# Set proper permissions (important for security!)
chmod 600 ~/.aws/credentials
chmod 600 ~/.aws/config
```

**Replace**:
- `YOUR_ACCESS_KEY_HERE` with your actual AWS Access Key ID
- `YOUR_SECRET_KEY_HERE` with your actual AWS Secret Access Key
- `us-east-1` with your preferred AWS region

### Step 3: Install AWS MCP

Run the automated setup script:

```bash
cd /home/user/Vienna
./aws-mcp-setup.sh
```

Or do it manually:

```bash
# Clone the repository
cd /home/user
git clone https://github.com/RafalWilinski/aws-mcp.git
cd aws-mcp

# Install dependencies
npm install

# Note the full path (you'll need it next)
pwd
```

### Step 4: Configure Claude Desktop

Find your Claude config file location:
- **Linux**: `~/.config/Claude/claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

Create or edit the config file:

```json
{
  "mcpServers": {
    "aws": {
      "command": "npm",
      "args": [
        "--silent",
        "--prefix",
        "/home/user/aws-mcp",
        "start"
      ]
    }
  }
}
```

⚠️ **Important**: Replace `/home/user/aws-mcp` with the actual path from Step 3.

### Step 5: Restart Claude Desktop

1. Completely quit Claude Desktop (not just close the window)
2. Reopen Claude Desktop
3. The AWS MCP server should now be connected!

## ✅ Testing Your Setup

Ask Claude these questions to verify it's working:

### Basic Test
```
Can you list my AWS profiles?
```

### S3 Test
```
What S3 buckets do I have in my account?
```

### EC2 Test
```
List all EC2 instances in us-east-1
```

### Lambda Test
```
Show me all Lambda functions in my default region
```

## 🔍 Troubleshooting

### Check if MCP server is running

**Linux:**
```bash
tail -f ~/.config/Claude/logs/mcp-server-aws.log
```

**macOS:**
```bash
tail -f ~/Library/Logs/Claude/mcp-server-aws.log
```

### Common Issues

#### Issue: "AWS credentials not found"
**Solution**: Verify credentials file exists and has correct format:
```bash
cat ~/.aws/credentials
cat ~/.aws/config
```

#### Issue: "Permission denied"
**Solution**: Check file permissions:
```bash
chmod 600 ~/.aws/credentials
chmod 600 ~/.aws/config
```

#### Issue: Claude doesn't see AWS MCP
**Solutions**:
1. Verify the path in `claude_desktop_config.json` is correct
2. Make sure you completely restarted Claude Desktop
3. Check logs for error messages
4. Verify `npm start` works in the aws-mcp directory:
   ```bash
   cd /home/user/aws-mcp
   npm start
   ```

#### Issue: "Access Denied" errors
**Solution**: Your IAM user needs appropriate permissions. Add policies in IAM console.

## 🎓 What You Can Ask Claude

### Information Queries
- "What's the total size of all my S3 buckets?"
- "Show me EC2 instances that are currently running"
- "List Lambda functions with their runtime versions"
- "What RDS databases do I have?"
- "Show me CloudFormation stacks"

### Resource Details
- "Describe the configuration of my VPC"
- "What's the status of CloudWatch alarm X?"
- "Show me tags for EC2 instance i-xxxxx"
- "What's the IAM policy attached to role X?"

### Cost Analysis
- "Which S3 buckets are using the most storage?"
- "Show me EC2 instances by instance type"

## 🔐 Security Best Practices

1. **Use Read-Only Access First**: Start with `ReadOnlyAccess` policy
2. **Use IAM User, Not Root**: Never use root account credentials
3. **Rotate Credentials**: Regularly rotate access keys
4. **Monitor Usage**: Check CloudTrail logs for API calls
5. **Least Privilege**: Only grant permissions Claude actually needs

## 📚 Advanced Configuration

### Multiple AWS Profiles

If you have multiple AWS accounts, configure profiles:

**~/.aws/credentials:**
```ini
[default]
aws_access_key_id = KEY1
aws_secret_access_key = SECRET1

[production]
aws_access_key_id = KEY2
aws_secret_access_key = SECRET2

[staging]
aws_access_key_id = KEY3
aws_secret_access_key = SECRET3
```

**~/.aws/config:**
```ini
[default]
region = us-east-1

[profile production]
region = us-west-2

[profile staging]
region = eu-west-1
```

Then ask Claude: "List EC2 instances using the production profile"

### Custom Region Configuration

Set default region in `~/.aws/config` or ask Claude:
```
List S3 buckets in eu-west-1 region
```

## 🎉 Success!

You now have Claude connected to AWS! This is MCP in action - you've:
1. Set up an MCP server (aws-mcp)
2. Configured it with your context (AWS credentials)
3. Connected it to Claude via the MCP protocol

Try asking Claude about your AWS resources and see the magic happen! 🚀

## 📖 More Resources

- **AWS MCP GitHub**: https://github.com/RafalWilinski/aws-mcp
- **MCP Documentation**: https://modelcontextprotocol.io
- **AWS IAM Best Practices**: https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html

---

**Need help?** Check the logs or ask Claude: "What AWS MCP servers are available?"
