"""
Response Parser for DBTT Cognitive Operating System
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass
from dbtt.models import Response
from dbtt.core.logger import get_logger

app_logger = get_logger(__name__)


class ResponseParser:
    """Parses LLM responses and formats them for the user"""

    def __init__(self):
        self.parsers = {}
        self.formatters = {}

    def parse_response(self, response: str, metadata: Dict[str, Any] = None) -> Response:
        """Parse a raw LLM response into a structured Response object"""
        if metadata is None:
            metadata = {}

        response_id = metadata.get("response_id", f"resp_{len(str(datetime.now()))}")
        confidence = metadata.get("confidence", 0.5)
        source = metadata.get("source", "llm")

        parsed_response = Response(
            id=response_id,
            content=response,
            confidence=confidence,
            source=source,
            metadata=metadata
        )

        app_logger.debug(f"Parsed LLM response with confidence: {confidence}")
        return parsed_response

    def format_response(self, response: Response, format_type: str = "text") -> str:
        """Format a Response object for display"""
        if format_type == "text":
            return self._format_as_text(response)
        elif format_type == "structured":
            return self._format_as_structured(response)
        elif format_type == "concise":
            return self._format_as_concise(response)
        else:
            return response.content

    def _format_as_text(self, response: Response) -> str:
        """Format response as natural text"""
        formatted = response.content

        if response.confidence >= 0.8:
            formatted = f"I'm confident that: {formatted}"
        elif response.confidence >= 0.6:
            formatted = f"Based on my analysis, {formatted}"
        elif response.confidence >= 0.4:
            formatted = f"After considering various perspectives, {formatted}"
        else:
            formatted = f"Here's what I found: {formatted}"

        return formatted

    def _format_as_structured(self, response: Response) -> str:
        """Format response with metadata"""
        structured = f"Response (Confidence: {response.confidence:.2f}, Source: {response.source})\n"
        structured += f"{'=' * 50}\n"
        structured += response.content
        structured += f"\n{'=' * 50}\n"

        if response.metadata:
            structured += f"Metadata: {response.metadata}\n"

        return structured

    def _format_as_concise(self, response: Response) -> str:
        """Format response concisely"""
        words = response.content.split()
        if len(words) > 20:
            concise = " ".join(words[:20]) + "..."
            return concise
        return response.content

    def extract_key_information(self, response: Response) -> Dict[str, Any]:
        """Extract key information from a response"""
        return {
            "summary": self._extract_summary(response),
            "key_points": self._extract_key_points(response),
            "confidence": response.confidence,
            "source": response.source
        }

    def _extract_summary(self, response: Response) -> str:
        """Extract a summary of the response"""
        sentences = response.content.split('.')
        if len(sentences) > 1:
            summary = '. '.join(sentences[:2]) + '.'
            if len(summary) > 100:
                summary = summary[:97] + "..."
            return summary
        return response.content

    def _extract_key_points(self, response: Response) -> List[str]:
        """Extract key points from the response"""
        words = response.content.split()
        return [word for word in words if len(word) > 6 and word[0].isupper()]
