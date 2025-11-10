# Model Orchestration Example: Sentiment → Action Bridge

## What is This?

This demonstrates **your original vision**: a bridge/orchestrator that manages data flow and context between two models:

1. **Sentiment Classifier** - analyzes text sentiment
2. **Action Recommender** - recommends actions based on sentiment

This is **NOT an MCP** (see the other example for that), but it's a valuable pattern for building AI pipelines!

## The Architecture

```
User Input
    ↓
┌─────────────────────────────────────────┐
│      MODEL ORCHESTRATOR (Bridge)        │
│                                         │
│  ┌────────────────────────────────┐   │
│  │  Context Management            │   │
│  │  - Track state                 │   │
│  │  - Pass data between models    │   │
│  │  - Handle errors               │   │
│  └────────────────────────────────┘   │
│                                         │
│  Step 1: Sentiment Classification      │
│         ↓                               │
│  Context updated with sentiment         │
│         ↓                               │
│  Step 2: Action Recommendation          │
│         ↓                               │
│  Context updated with action            │
│                                         │
└─────────────────────────────────────────┘
    ↓
Final Result (Context with all data)
```

## Key Concepts

### 1. **Context Management**
```python
@dataclass
class OrchestratorContext:
    original_input: str
    sentiment_result: SentimentResult | None = None
    action_result: ActionRecommendation | None = None
```

The context flows through the pipeline, accumulating information from each model.

### 2. **Sequential Processing**
```python
# Step 1: Classify sentiment
context.sentiment_result = classifier.classify(user_input)

# Step 2: Recommend action (uses result from step 1!)
context.action_result = recommender.recommend(context.sentiment_result)
```

Each model depends on the previous one's output - the orchestrator manages this dependency.

### 3. **Type Safety**
```python
@dataclass
class SentimentResult:
    text: str
    sentiment: Literal["positive", "negative", "neutral"]
    confidence: float
```

Strong typing makes the data flow explicit and catches errors early.

## Running the Demo

```bash
# No installation needed - uses Python 3.10+ standard library!
python orchestrator.py
```

You'll see:
- Each model processing in sequence
- Context being built up with data
- Final recommendations with reasoning

## Example Output

```
Input: "This product is absolutely wonderful! I love it!"

😊 Sentiment Analysis:
   Sentiment: positive
   Confidence: 90%

🎯 Recommended Action:
   Action: send_thank_you
   Reasoning: Customer is satisfied - reinforce positive experience
   Priority: medium
```

## How This Differs from MCP

| Aspect | This Orchestrator | MCP Server |
|--------|------------------|------------|
| Purpose | Chain multiple models | Connect AI to external tools |
| Components | Model → Model | Claude → MCP Server → Resources |
| Communication | In-process Python | Stdio protocol |
| Use Case | AI pipeline orchestration | Extending Claude's capabilities |

## When to Use This Pattern

✅ **Use orchestration when:**
- You need to chain multiple AI models
- Output of model A feeds into model B
- You need complex context management
- You're building an AI pipeline

❌ **Don't use this when:**
- You just need to give Claude access to tools (use MCP!)
- Models can run independently
- No context sharing needed

## Extending This Example

Want to make it more powerful? Try:

1. **Add real ML models:**
   ```python
   # Replace simple sentiment with transformers
   from transformers import pipeline
   sentiment_model = pipeline("sentiment-analysis")
   ```

2. **Add more stages:**
   ```python
   # Add a language detection stage
   context.language = language_detector.detect(user_input)

   # Add a priority scorer
   context.priority = priority_scorer.score(context)
   ```

3. **Add async processing:**
   ```python
   # Run models in parallel when possible
   async def process_parallel(self, input: str):
       results = await asyncio.gather(
           self.model_a.process(input),
           self.model_b.process(input)
       )
   ```

4. **Add error handling and retries:**
   ```python
   for attempt in range(3):
       try:
           result = await model.process(input)
           break
       except Exception as e:
           if attempt == 2:
               raise
           await asyncio.sleep(2 ** attempt)
   ```

## Real-World Use Cases

This pattern is perfect for:

- **Customer support automation** (sentiment → routing → response)
- **Content moderation** (detect → classify → action)
- **Document processing** (extract → analyze → summarize)
- **Multi-agent systems** (agent A → agent B → agent C)

The key insight: **The orchestrator is the intelligent glue that makes independent models work together seamlessly.**
