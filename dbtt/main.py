"""
Main entry point for DBTT Cognitive Operating System
"""

import asyncio
import signal
import sys
from datetime import datetime
from typing import Dict, Any
from dbtt.core.logger import get_logger
from dbtt.core.config import app_config
from dbtt.brain.brain_router import BrainRouter
from dbtt.llm.qwen import QwenLLM
from dbtt.core.interfaces import ThoughtGraph, Thought, Priority
from dbtt.core.system_config import SystemConfig

app_logger = get_logger(__name__)


class DBTT:
    """Main orchestrator for DBTT Cognitive Operating System"""

    def __init__(self, config_path: str = None):
        self.config_path = config_path
        self.thought_graph = ThoughtGraph()
        self.brain_router = BrainRouter()
        self.llm = None
        self.running = False
        self.system_config = SystemConfig(app_config.config)

        # Initialize modules
        self._initialize_modules()

    def _initialize_modules(self) -> None:
        """Initialize all modules and register them"""
        # Load configuration
        if self.config_path:
            app_config.load(self.config_path)

        app_logger.info(f"Initializing DBTT v{app_config.config.version}")

        # Register specialized brains
        self._register_brains()

        # Initialize LLM
        self._initialize_llm()

        app_logger.info("DBTT initialization complete")

    def _register_brains(self) -> None:
        """Register all brain modules"""
        from dbtt.brain.logic import LogicBrain
        from dbtt.brain.planning import PlanningBrain
        from dbtt.brain.creativity import CreativityBrain
        from dbtt.brain.curiosity import CuriosityBrain
        from dbtt.brain.emotion import EmotionBrain
        from dbtt.brain.simulation import SimulationBrain
        from dbtt.brain.reflection import ReflectionEngine
        from dbtt.brain.debate import DebateEngine
        from dbtt.brain.verification import VerificationEngine
        from dbtt.brain.decision import DecisionEngine

        brains = [
            LogicBrain(),
            PlanningBrain(),
            CreativityBrain(),
            CuriosityBrain(),
            EmotionBrain(),
            SimulationBrain(),
            ReflectionEngine(),
            DebateEngine(),
            VerificationEngine(),
            DecisionEngine()
        ]

        for brain in brains:
            self.brain_router.register_module(brain)

        app_logger.info(f"Registered {len(brains)} brain modules")

    def _initialize_llm(self) -> None:
        """Initialize the LLM layer"""
        self.llm = QwenLLM()
        self.llm.initialize(app_config.config.to_dict())

    async def process(self, user_input: str, context: Dict[str, Any] = None) -> str:
        """Process user input through the entire cognitive pipeline"""
        if context is None:
            context = {}

        app_logger.info(f"Processing user input: {user_input[:100]}...")

        try:
            # Create initial thought from user input
            thought_id = f"user_input_{len(str(datetime.now()))}"
            from dbtt.models.thought import Thought, Priority

            initial_thought = Thought(
                id=thought_id,
                content=f"User input: {user_input}",
                confidence=0.9,
                priority=Priority.HIGH,
                source="user_input"
            )
            self.thought_graph.add_thought(initial_thought)

            # Execute brain modules in order
            results, updated_graph = self.brain_router.execute_modules(self.thought_graph)
            self.thought_graph = updated_graph

            # Build prompt for LLM
            from dbtt.llm.prompt_builder import PromptBuilder
            prompt_builder = PromptBuilder()
            from dbtt.models.context import Context

            prompt_context = Context(id="main_context", thought_ids=list(self.thought_graph.thoughts.keys()))
            prompt = prompt_builder.build_prompt(
                self.thought_graph,
                prompt_context,
                additional_context={"user_query": user_input}
            )

            # Generate response using LLM
            from dbtt.llm.response_parser import ResponseParser
            response_parser = ResponseParser()

            llm_response = await self.llm.generate_response(prompt, {})
            parsed_response = response_parser.parse_response(
                llm_response.content,
                {"source": "llm", "confidence": llm_response.response_time / 30.0}
            )

            formatted_response = response_parser.format_response(parsed_response, "text")

            app_logger.info(f"Generated response: {formatted_response[:100]}...")
            return formatted_response

        except Exception as e:
            app_logger.error(f"Error processing user input: {str(e)}")
            raise

    async def shutdown(self) -> None:
        """Shutdown all components"""
        app_logger.info("Shutting down DBTT components")
        self.running = False

        if self.llm:
            self.llm.shutdown()

        app_logger.info("DBTT shutdown complete")

    async def health_check(self) -> Dict[str, Any]:
        """Perform a health check of all components"""
        health_status = {
            "status": "healthy",
            "components": {}
        }

        # Check LLM health
        if self.llm:
            llm_health = await self.llm.health_check()
            health_status["components"]["llm"] = {
                "status": "healthy" if llm_health else "unhealthy",
                "name": self.llm.name
            }

        # Check brain modules
        module_status = self.brain_router.get_module_status()
        health_status["components"]["brain_modules"] = module_status

        # Check overall system
        if self.llm and await self.llm.health_check():
            app_logger.info("All components are healthy")
        else:
            app_logger.warning("Some components are unhealthy")
            health_status["status"] = "degraded"

        return health_status

    def save_thought_graph(self, path: str) -> None:
        """Save the current thought graph to a file"""
        import json
        with open(path, 'w') as f:
            json.dump(self.thought_graph.to_dict(), f, indent=2)
        app_logger.info(f"Saved thought graph to {path}")

    def load_thought_graph(self, path: str) -> None:
        """Load a thought graph from a file"""
        import json
        with open(path, 'r') as f:
            data = json.load(f)
        self.thought_graph.from_dict(data)
        app_logger.info(f"Loaded thought graph from {path}")

    async def run_async(self) -> None:
        """Run the main event loop"""
        self.running = True
        app_logger.info("DBTT is running")

        while self.running:
            # Main processing loop
            await asyncio.sleep(1)

    def run(self) -> None:
        """Run DBTT synchronously"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        async def main():
            await self.run_async()

        try:
            loop.run_until_complete(main())
        except KeyboardInterrupt:
            app_logger.info("Keyboard interrupt received, shutting down")
        finally:
            loop.run_until_complete(self.shutdown())
            loop.close()


# Signal handler for graceful shutdown
signal.signal(signal.SIGINT, lambda sig, frame: sys.exit(0))
signal.signal(signal.SIGTERM, lambda sig, frame: sys.exit(0))
