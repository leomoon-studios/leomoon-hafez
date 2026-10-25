from __future__ import annotations

import os
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = PROJECT_ROOT / "src"

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
sys.path.insert(0, str(SOURCE_ROOT))
