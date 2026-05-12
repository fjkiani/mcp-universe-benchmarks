"""Base domain class for LBX MCP Universe benchmarks."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class DomainTask(BaseModel):
    """Base class for domain tasks."""

    task_id: str = Field(..., description="Unique task identifier")
    description: str = Field(..., description="Task description")
    difficulty: str = Field(default="medium", description="Task difficulty level")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class DomainVariation(BaseModel):
    """Base class for domain variations."""

    variation_id: str = Field(..., description="Unique variation identifier")
    name: str = Field(..., description="Variation name")
    description: str = Field(..., description="Variation description")
    tasks: List[DomainTask] = Field(default_factory=list, description="Tasks in this variation")


class BaseDomain(ABC):
    """Abstract base class for domain implementations."""

    def __init__(self, domain_name: str):
        """Initialize the domain.

        Args:
            domain_name: Name of the domain
        """
        self.domain_name = domain_name
        self.variations: Dict[str, DomainVariation] = {}

    @abstractmethod
    def load_data(self) -> None:
        """Load domain-specific data.

        This method should load all necessary data for the domain,
        including tasks, rules, and any reference data.
        """
        pass

    @abstractmethod
    def validate_structure(self) -> bool:
        """Validate the domain structure.

        Returns:
            True if structure is valid, False otherwise
        """
        pass

    def add_variation(self, variation: DomainVariation) -> None:
        """Add a variation to the domain.

        Args:
            variation: Domain variation to add
        """
        self.variations[variation.variation_id] = variation

    def get_variation(self, variation_id: str) -> Optional[DomainVariation]:
        """Get a specific variation.

        Args:
            variation_id: ID of the variation to retrieve

        Returns:
            DomainVariation if found, None otherwise
        """
        return self.variations.get(variation_id)

    def list_variations(self) -> List[str]:
        """List all variation IDs.

        Returns:
            List of variation IDs
        """
        return list(self.variations.keys())

    def get_task_count(self, variation_id: Optional[str] = None) -> int:
        """Get total task count.

        Args:
            variation_id: Optional variation ID to count tasks for

        Returns:
            Total number of tasks
        """
        if variation_id:
            variation = self.get_variation(variation_id)
            return len(variation.tasks) if variation else 0

        return sum(len(v.tasks) for v in self.variations.values())

    def validate_completeness(self, min_tasks: int = 100) -> bool:
        """Validate that domain has minimum required tasks.

        Args:
            min_tasks: Minimum number of tasks required (default: 100)

        Returns:
            True if domain meets minimum task requirement
        """
        total_tasks = self.get_task_count()
        return total_tasks >= min_tasks

    def __repr__(self) -> str:
        """String representation of the domain."""
        return f"<{self.__class__.__name__} domain='{self.domain_name}' variations={len(self.variations)}>"

