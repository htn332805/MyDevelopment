from orchestrator.context import Context
from typing import Dict, Any

class BaseScriptlet:
    def validate(self, ctx: Context, params: Dict[str, Any]):
        raise NotImplementedError

    def run(self, ctx: Context, params: Dict[str, Any]) -> int:
        raise NotImplementedError
