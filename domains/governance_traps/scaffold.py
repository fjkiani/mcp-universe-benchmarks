"""
Governance Traps Domain — 4 Adversarial Pillars
Creates the governance_traps domain following the exact schema of grant_application.

Run this script from the project root to scaffold the domain:
  python3 domains/governance_traps/scaffold.py
"""

import os
import json
import yaml
from pathlib import Path

ROOT = Path(__file__).parent


def scaffold():
    """Scaffold the governance_traps domain."""
    print("Scaffolding governance_traps domain...")
    (ROOT / "tasks").mkdir(exist_ok=True)
    (ROOT / "evaluators").mkdir(exist_ok=True)
    print("✅ Directories created")


if __name__ == "__main__":
    scaffold()
