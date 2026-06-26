"""
Brain Router - Operating system scheduler for DBTT
"""

import networkx as nx
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from dbtt.core.interfaces import BrainModule, Thought, ThoughtGraph as ThoughtGraphInterface, Priority, Status, app_logger, app_config
from dbtt.core.thought_graph import ThoughtGraph


class ExecutionResult:
    """Result of executing a brain module"""

    def __init__(self, module_name: str, success: bool, result: Optional[ThoughtGraph] = None,
                 execution_time: Optional[float] = None, error: Optional[str] = None):
        self.module_name = module_name
        self.success = success
        self.result = result
        self.execution_time = execution_time
        self.error = error

    def to_dict(self) -> Dict[str, Any]:
        return {
            "module_name": self.module_name,
            "success": self.success,
            "has_result": self.result is not None,
            "execution_time": self.execution_time,
            "error": self.error
        }


class ResourceAllocation:
    """Represents resource allocation for modules"""

    def __init__(self, module_name: str, max_threads: int = 1, timeout: int = 60):
        self.module_name = module_name
        self.max_threads = max_threads
        self.timeout = timeout


class BrainRouter:
    """Operating system scheduler that decides which modules execute"""

    def __init__(self):
        self.modules: Dict[str, BrainModule] = {}
        self.resource_allocations: Dict[str, ResourceAllocation] = {}
        self.execution_order: List[str] = []
        self.pending_modules: List[str] = []
        self.executing_modules: List[str] = []
        self.completed_modules: List[str] = []
        self.failed_modules: List[str] = []
        self.config = app_config.config

    def register_module(self, module: BrainModule, allocation: Optional[ResourceAllocation] = None) -> None:
        """Register a brain module"""
        self.modules[module.name] = module
        if allocation:
            self.resource_allocations[module.name] = allocation
        app_logger.info(f"Registered module: {module.name}")

    def determine_execution_order(self, thought_graph: ThoughtGraph) -> List[str]:
        """Determine which modules to execute and in what order"""
        order = []

        # Analyze current thought graph state
        root_thoughts = thought_graph.get_root_thoughts()
        if not root_thoughts:
            return order

        # Evaluate modules based on thought graph characteristics
        for module_name in self.modules:
            if self._should_execute_module(module_name, thought_graph, root_thoughts):
                order.append(module_name)

        # Apply priority and dependency constraints
        order = self._apply_execution_constraints(order, thought_graph)

        app_logger.debug(f"Determined execution order: {order}")
        return order

    def _should_execute_module(self, module_name: str, thought_graph: ThoughtGraph,
                              root_thoughts: List[Thought]) -> bool:
        """Check if a module should be executed"""
        module = self.modules[module_name]

        # Check if module has been executed recently
        if module_name in self.completed_modules:
            return self._should_re_execute(module_name, thought_graph)

        # Check if module is already executing or completed
        if module_name in self.executing_modules or module_name in self.completed_modules:
            return False

        # Check if module should be executed based on thought graph
        return self._evaluate_module_need(module_name, thought_graph, root_thoughts)

    def _should_re_execute(self, module_name: str, thought_graph: ThoughtGraph) -> bool:
        """Check if a module should be re-executed"""
        # Implementation logic for re-execution decision
        # Consider factors like confidence scores, thought changes, etc.
        return True

    def _evaluate_module_need(self, module_name: str, thought_graph: ThoughtGraph,
                             root_thoughts: List[Thought]) -> bool:
        """Evaluate if a module needs to be executed"""
        # Default implementation - execute all modules
        # Subclasses can override to implement more sophisticated logic
        return True

    def _apply_execution_constraints(self, order: List[str], thought_graph: ThoughtGraph) -> List[str]:
        """Apply priority and dependency constraints"""
        # Sort by priority
        order_by_priority = sorted(
            order,
            key=lambda x: self.resource_allocations[x].timeout
        )

        # Apply dependency constraints
        return order_by_priority

    def execute_modules(self, thought_graph: ThoughtGraph) -> Tuple[List[ExecutionResult], ThoughtGraph]:
        """Execute registered modules in order"""
        results = []
        current_thought_graph = thought_graph

        # Determine execution order
        execution_order = self.determine_execution_order(current_thought_graph)

        for module_name in execution_order:
            module = self.modules[module_name]
            app_logger.info(f"Executing module: {module_name}")

            try:
                # Execute module with timeout
                import asyncio
                start_time = datetime.now()
                result_thought_graph = asyncio.run(
                    asyncio.wait_for(
                        self._execute_module_async(module, current_thought_graph),
                        timeout=self.resource_allocations[module_name].timeout
                    )
                )
                execution_time = (datetime.now() - start_time).total_seconds()

                self.completed_modules.append(module_name)
                results.append(ExecutionResult(
                    module_name=module_name,
                    success=True,
                    result=result_thought_graph,
                    execution_time=execution_time
                ))

                current_thought_graph = result_thought_graph

            except Exception as e:
                app_logger.error(f"Module {module_name} execution failed: {str(e)}")
                self.failed_modules.append(module_name)
                results.append(ExecutionResult(
                    module_name=module_name,
                    success=False,
                    error=str(e)
                ))

        return results, current_thought_graph

    async def _execute_module_async(self, module: BrainModule, thought_graph: ThoughtGraph) -> ThoughtGraph:
        """Execute module asynchronously"""
        return module.process(thought_graph)

    def get_module_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all modules"""
        status = {}
        for module_name in self.modules:
            status[module_name] = {
                "name": module_name,
                "executing": module_name in self.executing_modules,
                "completed": module_name in self.completed_modules,
                "failed": module_name in self.failed_modules,
                "allocation": self.resource_allocations[module_name].to_dict()
            }
        return status

    def reset(self) -> None:
        """Reset execution state"""
        self.pending_modules = []
        self.executing_modules = []
        self.completed_modules = []
        self.failed_modules = []
