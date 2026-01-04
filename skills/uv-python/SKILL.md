---
name: "UV Python Workflow"
tags: ["uv", "python", "pip", "pytest", "jupyter", "dependency", "virtualenv", "package", "run"]
intent: "Use UV package manager for all Python operations. When running Python scripts, use 'uv run python' instead of 'python'. When installing packages, use 'uv add'. When running tests, use 'uv run pytest'. When starting Jupyter, use 'uv run jupyter'. Triggers on working with Python code, running Python scripts, installing packages, executing tests, or managing Python dependencies in any project location. Use for any Python-related task where you would normally use python, pip, pytest, or other Python tools."
version: "1.0.0"
languages: ["python", "bash"]
---

# UV Python Workflow

## Usage

This skill teaches you to use UV commands instead of traditional Python commands for all Python operations. UV is a fast, modern Python package manager written in Rust that's 10-100x faster than pip and provides better dependency resolution.

**Key Principle:** Always use UV commands instead of traditional Python commands, regardless of project location.

## When to Use

**Use this skill whenever:**
- User wants to run Python scripts
- User asks to install Python packages
- User wants to run tests with pytest
- User needs to start Jupyter or other Python tools
- User is working with any Python project (in any directory)
- User mentions dependency management or virtual environments

**Key indicators:**
- Commands involving `python`, `pip`, `pytest`, `jupyter`
- Python package installation requests
- Virtual environment setup
- Running Python scripts or modules
- Any Python development task

**Important:** This skill works with projects in ANY location, not just specific directories. The UV workflow applies universally to all Python projects.

## Core Command Mapping

When the user needs to run Python commands, translate them to UV:

| Traditional Command | UV Command |
|-------------------|------------|
| `python script.py` | `uv run python script.py` |
| `python -m module` | `uv run python -m module` |
| `pytest` | `uv run pytest` |
| `pytest tests/` | `uv run pytest tests/` |
| `jupyter lab` | `uv run jupyter lab` |
| `ipython` | `uv run ipython` |
| `black .` | `uv run black .` |
| `ruff check` | `uv run ruff check` |
| `mypy src/` | `uv run mypy src/` |
| `pip install requests` | `uv add requests` |
| `pip install -e .` | `uv sync` |
| `pip uninstall requests` | `uv remove requests` |

## Essential UV Commands

### Project Initialization

```bash
# Initialize UV in existing project (creates pyproject.toml)
uv init

# Initialize with specific Python version
uv init --python 3.11
```

### Dependency Management

```bash
# Add runtime dependency
uv add requests

# Add multiple dependencies
uv add requests pandas numpy

# Add development dependency
uv add --dev pytest black ruff

# Add with version constraint
uv add "requests>=2.31.0"

# Remove dependency
uv remove requests

# Sync dependencies from pyproject.toml (creates/updates .venv)
uv sync

# Sync only production dependencies (no dev)
uv sync --no-dev
```

### Running Code

```bash
# Run Python script
uv run python script.py

# Run Python module
uv run python -m mypackage

# Run with arguments
uv run python script.py --arg1 value --arg2 value

# Run tests
uv run pytest
uv run pytest tests/test_specific.py
uv run pytest -v --cov

# Run Jupyter
uv run jupyter lab
uv run jupyter notebook

# Run interactive Python
uv run ipython
uv run python
```

### One-off Commands (without adding to dependencies)

```bash
# Run tool without installing permanently
uvx ruff check .
uvx black .
uvx mypy src/

# Run script with inline dependencies
uv run --with requests python script.py
```

## Common Workflows

### Scenario 1: User wants to run a Python script

```bash
# User says: "Run my script.py"
# You should use:
uv run python script.py
```

### Scenario 2: User wants to install a package

```bash
# User says: "Install the requests library"
# You should use:
uv add requests
```

### Scenario 3: User wants to run tests

```bash
# User says: "Run the tests"
# You should use:
uv run pytest
```

### Scenario 4: User wants to start Jupyter

```bash
# User says: "Start Jupyter Lab"
# You should:
uv add --dev jupyter  # If not already added
uv run jupyter lab
```

### Scenario 5: User has requirements.txt

```bash
# User says: "Install dependencies from requirements.txt"
# You should use:
cat requirements.txt | xargs -I {} uv add {}
# Or for dev dependencies:
cat requirements-dev.txt | xargs -I {} uv add --dev {}
```

### Scenario 6: User wants to use a tool temporarily

```bash
# User says: "Format my code with black"
# You should use:
uvx black .
# Not: uv add black (unless they want it permanent)
```

## Project Workflow

### Starting with Existing Project

When user has an existing Python project:

```bash
# 1. Navigate to project
cd /path/to/existing/project

# 2. Initialize UV (if no pyproject.toml)
uv init

# 3. Add existing dependencies (if they have requirements.txt)
cat requirements.txt | xargs -I {} uv add {}

# 4. Or manually add dependencies
uv add package1 package2 package3

# 5. Run the project
uv run python main.py
```

### Creating New Project

```bash
# 1. Create and navigate to directory
mkdir my-project
cd my-project

# 2. Initialize UV
uv init

# 3. Add dependencies
uv add requests pandas

# 4. Create script
cat > main.py << 'EOF'
import requests
print("Hello from UV!")
EOF

# 5. Run it
uv run python main.py
```

## How UV Works

### Virtual Environment

- UV automatically creates `.venv/` in your project directory
- You **don't need to manually activate** the venv
- `uv run` automatically uses the project's `.venv`
- Dependencies are installed to `.venv/`

### Dependency Resolution

- Dependencies are defined in `pyproject.toml`
- Lock file `uv.lock` ensures reproducible installs
- UV resolves dependencies faster than pip
- Handles version conflicts intelligently

### Python Version Management

```bash
# List available Python versions
uv python list

# Install specific Python version
uv python install 3.11

# Pin Python version for project
uv python pin 3.11
```

## Important Rules

1. **Always prefer `uv run` over plain commands** when executing Python code
2. **Always use `uv add` over `pip install`** when installing dependencies
3. **Work with projects in place** - don't require migration to specific directory
4. **Create pyproject.toml if missing** using `uv init`
5. **Use `uvx` for one-off tools** (formatters, linters) unless user wants them permanent
6. **Check for existing pyproject.toml** before running `uv init`
7. **Use `uv sync` after manually editing pyproject.toml**

## pyproject.toml Structure

After `uv init`, the file looks like:

```toml
[project]
name = "my-project"
version = "0.1.0"
description = "Add your description here"
requires-python = ">=3.11"
dependencies = []

[tool.uv]
dev-dependencies = []
```

When you add dependencies with `uv add requests`:

```toml
[project]
name = "my-project"
version = "0.1.0"
description = "Add your description here"
requires-python = ">=3.11"
dependencies = [
    "requests>=2.31.0",
]

[tool.uv]
dev-dependencies = []
```

## Troubleshooting

### "Command not found: uv"

UV is not installed. Install with:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### "No pyproject.toml found"

Initialize UV in the project:
```bash
uv init
```

### "Module not found" errors

Sync dependencies:
```bash
uv sync
```

### Dependencies not updating

Remove lock file and resync:
```bash
rm uv.lock
uv sync
```

### Want to see what's installed

```bash
uv tree  # Show dependency tree
uv pip list  # List installed packages
```

## When NOT to Use UV

- User explicitly asks for virtual environment activation
- User is working in a specific activated environment already
- User explicitly uses `pip` or `conda` in their question
- System-level Python operations

In these cases, respect the user's explicit choices.

## Quick Reference

```bash
# Setup
uv init                          # Initialize project
uv add <package>                 # Add dependency
uv sync                          # Install dependencies

# Run
uv run python script.py          # Run script
uv run pytest                    # Run tests
uv run jupyter lab               # Start Jupyter

# Temporary tools
uvx black .                      # Run without installing
uvx ruff check .                 # Run linter

# Info
uv tree                          # Show dependencies
uv pip list                      # List packages
```

## Examples

User: "Run my data_processor.py script"
Agent: Execute `uv run python data_processor.py` to run the script using the project's UV-managed environment.

User: "I need pandas and numpy for my analysis"
Agent: Run `uv add pandas numpy` to add both packages as project dependencies. UV will update pyproject.toml and install the packages to the local .venv.

User: "Run the test suite"
Agent: Execute `uv run pytest` to run tests using the UV-managed environment. Add flags as needed: `uv run pytest -v --cov` for verbose output with coverage.

User: "Open Jupyter Lab"
Agent: First check if jupyter is in dependencies. If not, run `uv add --dev jupyter` to add it as a dev dependency. Then execute `uv run jupyter lab` to start Jupyter.

User: "I have a project with a requirements.txt, set it up with UV"
Agent: Navigate to the project directory. Run `uv init` if no pyproject.toml exists. Then migrate dependencies with `cat requirements.txt | xargs -I {} uv add {}`. The project is now UV-managed with all dependencies tracked in pyproject.toml.

## Integration with Codex Workflows

This skill integrates seamlessly with other Codex skills:

- **time-awareness**: For time-based scheduling and deadlines
- **document-parser**: For processing Python documentation

**Key Principle:** This skill provides universal UV workflow for any Python project in any location.

## Verification Checklist

Before completing a Python task, verify:
- [ ] Used `uv run` for Python script execution (not plain `python`)
- [ ] Used `uv add` for package installation (not `pip install`)
- [ ] Checked for existing `pyproject.toml` before running `uv init`
- [ ] Used `uvx` for one-off tools (not permanent installation)
- [ ] Ran `uv sync` if manually editing `pyproject.toml`

---

**Remember:** UV is the modern Python workflow. Always use `uv run`, `uv add`, and `uvx` instead of traditional commands. Works with any Python project in any location.
