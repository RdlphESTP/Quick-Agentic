import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

from quick_agentic.generate_code import generate_code

with open("user_graph.json", "r") as f:
    user_graph = json.load(f)

generated_code = generate_code(user_graph)
output_path = Path("template") / "src" / "template" / "graph.py"
output_path.write_text(generated_code, encoding="utf-8")

# Run ruff to format the generated code
if shutil.which("ruff"):
    ruff_command = ["ruff", "check", "--fix", str(output_path)]
elif shutil.which("uvx"):
    ruff_command = ["uvx", "ruff", "check", "--fix", str(output_path)]
elif importlib.util.find_spec("ruff") is not None:
    ruff_command = [sys.executable, "-m", "ruff", "check", "--fix", str(output_path)]
else:
    raise FileNotFoundError(
        "Ruff is not available. Install it or make sure `ruff`/`uvx` is on PATH."
    )

subprocess.run(ruff_command, check=True)
