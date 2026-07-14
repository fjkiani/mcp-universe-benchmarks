"""
Compatibility shim for evaluator decorators.

Provides `compare_func`, `eval_func`, `FunctionResult`, and `Context` that previously
came from the private `lbx_cli.mcpuniverse.evaluator.functions` module.

When lbx_cli is available (live evaluation pipeline), the real decorators
are used. When it's not (local development, CI without private submodules),
these stubs provide the same interface so evaluators can be imported and
tested without the private dependency.
"""

import os
from typing import Any, Callable, Optional


class FunctionResult:
    """Mock of the Pydantic FunctionResult wrapper from lbx_cli."""

    def __init__(self, result: Any = None, **kwargs):
        self.result = result
        for k, v in kwargs.items():
            setattr(self, k, v)

    def model_dump(self) -> dict:
        return {"result": self.result}

    def dict(self) -> dict:
        return {"result": self.result}


class Context:
    """Mock of lbx_cli.mcpuniverse.common.context.Context."""

    def __init__(self, **kwargs):
        self._env = {}
        self._kwargs = kwargs

    def get_env(self, key: str, default: Optional[str] = None) -> Optional[str]:
        return os.environ.get(key, default)

    def set_env(self, key: str, value: str) -> None:
        os.environ[key] = value


def compare_func(name: Optional[str] = None) -> Callable:
    """Decorator that registers an evaluator function with a given op name."""

    def decorator(fn: Callable) -> Callable:
        fn._evaluator_name = name
        fn._evaluator_type = "compare_func"
        return fn

    return decorator


def eval_func(name: Optional[str] = None) -> Callable:
    """Decorator that registers an evaluator function with a given op name."""

    def decorator(fn: Callable) -> Callable:
        fn._evaluator_name = name
        fn._evaluator_type = "eval_func"
        return fn

    return decorator
