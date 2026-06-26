"""
Prompt Builder for DBTT Cognitive Operating System
"""

from typing import Dict, Any, Optional
from dbtt.models import Context
from dbtt.core.thought_graph import ThoughtGraph
from dbtt.core.logger import get_logger

app_logger = get_logger(__name__)


class PromptBuilder:
    """Builds prompts for the LLM layer"""

    def __init__(self):
        self.templates = {}
        self.default_config = {
            "include_system_context": True,
            "include_verified_thoughts": True,
            "include_memory": True,
            "include_goals": True,
            "max_thoughts": 10,
            "thought_confidence_threshold": 0.7
        }

    def build_prompt(
        self,
        thought_graph: ThoughtGraph,
        context: Context,
        config: Dict[str, Any] = None,
        additional_context: Dict[str, Any] = None
    ) -> str:
        """Build a comprehensive prompt for the LLM"""
        prompt_parts = []

        # Add system context
        if config is None:
            config = self.default_config

        if config.get("include_system_context", True):
            prompt_parts.append(self._build_system_context())

        # Add verified thoughts
        if config.get("include_verified_thoughts", True):
            prompt_parts.append(self._build_verified_thoughts(thought_graph, config))

        # Add memory
        if config.get("include_memory", True):
            prompt_parts.append(self._build_memory(context))

        # Add goals and reasoning
        if config.get("include_goals", True):
            prompt_parts.append(self._build_goals(context))

        # Add user query if present
        if additional_context and "user_query" in additional_context:
            prompt_parts.append(f"\nUser Query: {additional_context['user_query']}")

        # Combine all prompt parts
        prompt = "\n".join(prompt_parts)

        app_logger.debug(f"Built prompt of length {len(prompt)}")
        return prompt

    def _build_system_context(self) -> str:
        """Build system context section"""
        return """You are DBTT, a Digital Brain That Thinks. You are an intelligent cognitive operating system designed to process information, reason logically, and provide thoughtful responses.

Key capabilities:
- Logical reasoning and analysis
- Strategic planning
- Creative problem solving
- Memory-based knowledge retrieval
- Context-aware response generation

Your role is to:
1. Process information from multiple thought paths
2. Consider diverse perspectives and possibilities
3. Verify information through multiple sources
4. Make well-reasoned decisions
5. Respond in a natural, helpful manner

Respond based only on the verified information provided below, and cite your reasoning when appropriate.
"""

    def _build_verified_thoughts(self, thought_graph: ThoughtGraph, config: Dict[str, Any]) -> str:
        """Build verified thoughts section"""
        max_thoughts = config.get("max_thoughts", 10)
        confidence_threshold = config.get("thought_confidence_threshold", 0.7)

        # Get thoughts above confidence threshold, sorted by confidence
        verified_thoughts = [
            t for t in thought_graph.thoughts.values()
            if t.confidence >= confidence_threshold
        ]
        sorted_thoughts = sorted(verified_thoughts, key=lambda t: t.confidence, reverse=True)[:max_thoughts]

        if not sorted_thoughts:
            return "\nNo verified thoughts available."

        thoughts_section = "\nVerified Reasoning Paths:\n"
        for thought in sorted_thoughts:
            thoughts_section += f"\n- {thought.content}"
            thoughts_section += f"\n  Confidence: {thought.confidence:.2f}"
            if thought.source:
                thoughts_section += f"\n  Source: {thought.source}"

        return thoughts_section

    def _build_memory(self, context: Context) -> str:
        """Build memory section"""
        memory_section = "\nRelevant Past Experiences and Knowledge:\n"
        memory_section += "Based on past interactions and knowledge, relevant information includes:\n"

        # Add memory entries - would normally retrieve from memory layer
        memory_section += "- Previous solutions to similar problems\n"
        memory_section += "- Established best practices\n"
        memory_section += "- Historical patterns and outcomes\n"
        memory_section += "- Learned strategies and techniques\n"

        return memory_section

    def _build_goals(self, context: Context) -> str:
        """Build goals and reasoning section"""
        goals_section = "Current Goals and Reasoning:\n"
        goals_section += "The goal is to provide a helpful, accurate, and well-reasoned response based on the cognitive processing above.\n"
        goals_section += "Key reasoning steps:\n"
        goals_section += "1. Process information from multiple cognitive modules\n"
        goals_section += "2. Verify information through multiple sources\n"
        goals_section += "3. Consider different perspectives and alternatives\n"
        goals_section += "4. Make decisions based on highest confidence reasoning\n"
        goals_section += "5. Provide clear, structured response to user\n"

        return goals_section

    def update_template(self, name: str, template: str) -> None:
        """Update or add a template"""
        self.templates[name] = template

    def get_template(self, name: str) -> Optional[str]:
        """Get a template by name"""
        return self.templates.get(name)
