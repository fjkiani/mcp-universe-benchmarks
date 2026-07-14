"""Model registry — loads model definitions from models.yaml."""
from pathlib import Path
from typing import Optional
import yaml


class ModelRegistry:
    def __init__(self, registry_path: Path):
        self.registry_path = registry_path
        self._models = None
        self._defaults = None

    def _load(self):
        if self._models is not None:
            return
        with open(self.registry_path) as f:
            data = yaml.safe_load(f)
        self._models = data.get("models", [])
        self._defaults = data.get("defaults", {})

    def list_models(self, provider: Optional[str] = None, tier: Optional[str] = None) -> list[dict]:
        self._load()
        result = self._models
        if provider:
            result = [m for m in result if m.get("provider") == provider]
        if tier:
            result = [m for m in result if m.get("tier") == tier]
        return result

    def get_model(self, slug: str) -> Optional[dict]:
        self._load()
        for m in self._models:
            if m["slug"] == slug:
                return m
        return None

    def get_default_judge(self) -> str:
        self._load()
        return self._defaults.get("judge_model", "openrouter/openai/gpt-oss-20b:free")

    def get_default_agent(self) -> str:
        self._load()
        return self._defaults.get("agent_model", "openrouter/meta-llama/llama-3.3-70b-instruct:free")
