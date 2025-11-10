#!/usr/bin/env python3
"""
Model Orchestration Bridge Example

This demonstrates what you originally envisioned:
- A sentiment classifier model
- An action recommender model
- A bridge/orchestrator that manages context and data flow between them

This is NOT an MCP, but it's a valuable pattern for chaining models!
"""

from dataclasses import dataclass
from typing import Literal, Dict, Any
import json


# ============================================================================
# DATA MODELS (for type safety and clarity)
# ============================================================================

@dataclass
class SentimentResult:
    """Output from the sentiment classification model"""
    text: str
    sentiment: Literal["positive", "negative", "neutral"]
    confidence: float
    metadata: Dict[str, Any]


@dataclass
class ActionRecommendation:
    """Output from the action recommendation model"""
    action: str
    reasoning: str
    priority: Literal["low", "medium", "high"]
    confidence: float


@dataclass
class OrchestratorContext:
    """
    The "Context" that flows through the pipeline.

    This is the key insight: we maintain state as data flows
    from one model to the next.
    """
    original_input: str
    sentiment_result: SentimentResult | None = None
    action_result: ActionRecommendation | None = None
    metadata: Dict[str, Any] | None = None


# ============================================================================
# MODEL 1: Sentiment Classifier
# ============================================================================

class SentimentClassifier:
    """
    Simulates a sentiment analysis model.

    In production, this could be:
    - A call to OpenAI API
    - A local transformer model (huggingface)
    - A cloud ML service (AWS Comprehend, etc.)
    """

    def __init__(self):
        self.model_name = "simple-sentiment-v1"

    def classify(self, text: str) -> SentimentResult:
        """
        Analyze the sentiment of input text.

        This is a simple rule-based implementation for demonstration.
        In production, you'd use a real ML model.
        """
        print(f"[SentimentClassifier] Analyzing: '{text}'")

        # Simple keyword-based sentiment analysis
        positive_words = ["good", "great", "excellent", "happy", "love", "wonderful", "fantastic", "thanks", "appreciate"]
        negative_words = ["bad", "terrible", "awful", "hate", "horrible", "poor", "worst", "angry", "upset"]

        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)

        # Determine sentiment
        if positive_count > negative_count:
            sentiment = "positive"
            confidence = min(0.95, 0.6 + (positive_count * 0.1))
        elif negative_count > positive_count:
            sentiment = "negative"
            confidence = min(0.95, 0.6 + (negative_count * 0.1))
        else:
            sentiment = "neutral"
            confidence = 0.5

        result = SentimentResult(
            text=text,
            sentiment=sentiment,
            confidence=confidence,
            metadata={
                "positive_signals": positive_count,
                "negative_signals": negative_count,
                "model": self.model_name
            }
        )

        print(f"[SentimentClassifier] Result: {sentiment} (confidence: {confidence:.2f})")
        return result


# ============================================================================
# MODEL 2: Action Recommender
# ============================================================================

class ActionRecommender:
    """
    Recommends actions based on sentiment.

    This simulates a second ML model that takes sentiment as input
    and outputs recommended actions.
    """

    def __init__(self):
        self.model_name = "action-recommender-v1"

        # Action mapping rules (in production, this could be learned from data)
        self.action_rules = {
            "positive": {
                "action": "send_thank_you",
                "reasoning": "Customer is satisfied - reinforce positive experience",
                "priority": "medium"
            },
            "negative": {
                "action": "escalate_to_manager",
                "reasoning": "Customer is dissatisfied - requires immediate attention",
                "priority": "high"
            },
            "neutral": {
                "action": "monitor",
                "reasoning": "Customer is neutral - no immediate action needed",
                "priority": "low"
            }
        }

    def recommend(self, sentiment_result: SentimentResult) -> ActionRecommendation:
        """
        Recommend an action based on sentiment analysis.

        Note how this model DEPENDS on the output of the previous model!
        This is where orchestration becomes important.
        """
        print(f"[ActionRecommender] Processing sentiment: {sentiment_result.sentiment}")

        # Get base recommendation
        rule = self.action_rules[sentiment_result.sentiment]

        # Adjust confidence based on sentiment confidence
        # If sentiment is uncertain, action should be less confident too
        confidence = sentiment_result.confidence * 0.9  # Scale down slightly

        # Adjust priority based on confidence
        if sentiment_result.confidence < 0.6:
            priority = "low"  # Not confident enough for high priority
        else:
            priority = rule["priority"]

        result = ActionRecommendation(
            action=rule["action"],
            reasoning=rule["reasoning"],
            priority=priority,
            confidence=confidence
        )

        print(f"[ActionRecommender] Recommended action: {result.action} (priority: {priority})")
        return result


# ============================================================================
# THE ORCHESTRATOR: The "Bridge" Between Models
# ============================================================================

class ModelOrchestrator:
    """
    The Orchestrator manages:
    1. Data flow between models
    2. Context/state management
    3. Error handling and fallbacks
    4. Logging and observability

    This is the "glue" that makes multiple models work together!
    """

    def __init__(self):
        # Initialize our models
        self.sentiment_classifier = SentimentClassifier()
        self.action_recommender = ActionRecommender()

        print("[Orchestrator] Initialized with 2 models")

    def process(self, user_input: str) -> OrchestratorContext:
        """
        The main orchestration pipeline.

        This is where the magic happens:
        1. Create context
        2. Pass through model 1 → update context
        3. Pass through model 2 → update context
        4. Return enriched context
        """
        print(f"\n{'='*60}")
        print(f"[Orchestrator] Starting pipeline for input: '{user_input}'")
        print(f"{'='*60}\n")

        # Step 1: Initialize context
        context = OrchestratorContext(
            original_input=user_input,
            metadata={"pipeline_version": "1.0"}
        )

        # Step 2: Run sentiment classification
        try:
            context.sentiment_result = self.sentiment_classifier.classify(user_input)
        except Exception as e:
            print(f"[Orchestrator] ERROR in sentiment classification: {e}")
            # In production: implement fallback logic
            raise

        # Step 3: Run action recommendation (uses output from step 2!)
        try:
            context.action_result = self.action_recommender.recommend(
                context.sentiment_result
            )
        except Exception as e:
            print(f"[Orchestrator] ERROR in action recommendation: {e}")
            # In production: implement fallback logic
            raise

        print(f"\n[Orchestrator] Pipeline complete!\n")
        return context

    def process_batch(self, inputs: list[str]) -> list[OrchestratorContext]:
        """
        Process multiple inputs through the pipeline.

        Demonstrates how the orchestrator can handle batching.
        """
        print(f"[Orchestrator] Processing batch of {len(inputs)} items")
        return [self.process(input_text) for input_text in inputs]


# ============================================================================
# UTILITY: Pretty printing results
# ============================================================================

def print_results(context: OrchestratorContext):
    """Pretty print the orchestration results"""
    print("\n" + "="*60)
    print("ORCHESTRATION RESULTS")
    print("="*60)

    print(f"\n📝 Input:")
    print(f"   {context.original_input}")

    print(f"\n😊 Sentiment Analysis:")
    if context.sentiment_result:
        print(f"   Sentiment: {context.sentiment_result.sentiment}")
        print(f"   Confidence: {context.sentiment_result.confidence:.2%}")
        print(f"   Positive signals: {context.sentiment_result.metadata['positive_signals']}")
        print(f"   Negative signals: {context.sentiment_result.metadata['negative_signals']}")

    print(f"\n🎯 Recommended Action:")
    if context.action_result:
        print(f"   Action: {context.action_result.action}")
        print(f"   Reasoning: {context.action_result.reasoning}")
        print(f"   Priority: {context.action_result.priority}")
        print(f"   Confidence: {context.action_result.confidence:.2%}")

    print("\n" + "="*60 + "\n")


# ============================================================================
# DEMO: See it in action!
# ============================================================================

def main():
    """
    Demonstrate the orchestrator with example customer feedback.
    """
    print("\n🚀 Model Orchestration Demo\n")

    # Create the orchestrator
    orchestrator = ModelOrchestrator()

    # Test cases
    test_inputs = [
        "This product is absolutely wonderful! I love it and would highly recommend it.",
        "This is the worst service I've ever experienced. Completely terrible.",
        "The product arrived on time and looks okay.",
    ]

    # Process each input through the pipeline
    for user_input in test_inputs:
        context = orchestrator.process(user_input)
        print_results(context)


if __name__ == "__main__":
    main()
