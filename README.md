# MCP & Model Orchestration Learning Repository

Welcome! This repository contains two complete, working examples to help you understand two important AI engineering patterns.

## 📦 What's Inside

### 1. MCP Server Example (`mcp_server_example/`)
A **real Model Context Protocol server** that exposes a sentiment analysis tool to Claude.

**Learn:** How to extend AI assistants with external tools using the MCP standard.

### 2. Model Orchestration Example (`model_orchestration_example/`)
An **orchestrator that chains two models** together (sentiment classifier → action recommender).

**Learn:** How to build AI pipelines that manage context and data flow between multiple models.

### 3. Comprehensive Tutorial (`MCP_TUTORIAL.md`)
A detailed guide explaining:
- What MCP actually is (and isn't)
- How model orchestration works
- When to use each pattern
- Conceptual deep dives with analogies
- Practical examples and next steps

## 🚀 Quick Start

### Try the Orchestrator (Recommended First)
```bash
cd model_orchestration_example
python orchestrator.py
```
No dependencies needed! See immediate results showing how models are chained.

### Try the MCP Server
```bash
cd mcp_server_example
pip install -r requirements.txt
python sentiment_server.py
```
Then configure it with Claude to give Claude sentiment analysis capabilities!

## 📚 Learning Path

1. **Start here:** Read `MCP_TUTORIAL.md` for conceptual understanding
2. **Then:** Run `model_orchestration_example/orchestrator.py` to see orchestration
3. **Finally:** Set up `mcp_server_example/sentiment_server.py` with Claude

## 🎯 Key Takeaways

- **MCP** = Connecting AI to external tools/data (AI ↔ Resources)
- **Orchestration** = Connecting multiple AI models (Model A → Model B → Model C)
- Both are important, both manage "context", but they solve different problems!

## 📖 Documentation

Each example has its own detailed README:
- `mcp_server_example/README.md` - MCP server setup and usage
- `model_orchestration_example/README.md` - Orchestration patterns and extensions

## 💡 Built For Learning

Every file is heavily commented to explain:
- **What** the code does
- **Why** it's structured that way
- **How** you can extend it

Feel free to modify, experiment, and break things - that's how you learn!

## 🤝 Questions?

Check `MCP_TUTORIAL.md` which includes:
- Detailed comparisons
- Common questions and answers
- Next steps and resources
- Real-world use cases

---

**Happy learning!** 🎉
