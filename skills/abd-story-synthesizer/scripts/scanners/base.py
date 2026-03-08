"""Base scanner — works with markdown content; no grammar or AST required."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class Violation:
    """A single validation violation."""
    rule_id: str
    message: str
    location: str
    severity: str = "warning"
    snippet: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "message": self.message,
            "location": self.location,
            "severity": self.severity,
            "snippet": self.snippet,
        }


class BaseScanner(ABC):
    """Base for all scanners. Uses regex and native Python only — no grammar, no AST."""

    rule_id: str = ""

    def __init__(self, rule_id: str = ""):
        self.rule_id = rule_id or self.rule_id

    @abstractmethod
    def scan(self, content: str, source_path: str | Path | None = None) -> list[Violation]:
        """Scan markdown content; return list of violations."""
        pass
