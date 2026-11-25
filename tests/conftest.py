import sys
from pathlib import Path

# The server is a single module at the repository root, not an installed package.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
