"""
Calculator Tool for DBTT Cognitive Operating System
"""

from tools.base_tool import BaseTool, ToolResult
from typing import Dict, Any


class CalculatorTool(BaseTool):
    """Advanced calculator tool that supports various mathematical operations"""

    def __init__(self):
        super().__init__("calculator")

    def execute(self, parameters: Dict[str, Any]) -> ToolResult:
        operation = parameters.get("operation", "add")
        operands = parameters.get("operands", [])

        try:
            if operation == "add":
                result = sum(operands)
                formula = " + ".join(str(x) for x in operands)
            elif operation == "subtract":
                if len(operands) >= 2:
                    result = operands[0] - sum(operands[1:])
                    formula = f"{operands[0]} - ({") + f" + ".join(str(x) for x in operands[1:]) + ")"
                else:
                    raise ValueError("Subtraction requires at least 2 operands")
            elif operation == "multiply":
                result = 1
                for operand in operands:
                    result *= operand
                formula = " * ".join(str(x) for x in operands)
            elif operation == "divide":
                if len(operands) >= 2:
                    result = operands[0]
                    for operand in operands[1:]:
                        if operand == 0:
                            raise ValueError("Division by zero")
                        result /= operand
                    formula = f"{operands[0]} / ({") + f" * ".join(str(x) for x in operands[1:]) + ")"
                else:
                    raise ValueError("Division requires at least 2 operands")
            elif operation == "power":
                if len(operands) >= 2:
                    result = operands[0] ** operands[1]
                    formula = f"{operands[0]} ^ {operands[1]}"
                else:
                    raise ValueError("Power operation requires at least 2 operands")
            elif operation == "sqrt":
                import math
                if len(operands) < 1:
                    raise ValueError("Square root requires 1 operand")
                result = math.sqrt(operands[0])
                formula = f"sqrt({operands[0]})"
            elif operation == "mod":
                if len(operands) >= 2:
                    result = operands[0] % operands[1]
                    formula = f"{operands[0]} % {operands[1]}"
                else:
                    raise ValueError("Modulo operation requires 2 operands")
            else:
                raise ValueError(f"Unsupported operation: {operation}")

            return ToolResult(
                success=True,
                result={
                    "value": result,
                    "formula": formula,
                    "operation": operation,
                    "operands": operands
                }
            )

        except Exception as e:
            return ToolResult(success=False, error=str(e))
