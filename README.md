# DefaultPython

[![CI](https://github.com/CharlesPoulin/DefaultPython/actions/workflows/ci.yml/badge.svg)](https://github.com/CharlesPoulin/DefaultPython/actions/workflows/ci.yml)
[![Python Version](https://img.shields.io/badge/python-3.13-blue.svg)](https://python.org)
[![Code Style: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)

A professional Python project template designed for modern development. It uses **[uv](https://docs.astral.sh/uv/)** for ultra-fast dependency management and includes a full suite of code quality tools.

## 🚀 Getting Started

### 1. Prerequisites

You will need `uv` installed. It replaces tools like `pip`, `poetry`, and `virtualenv`.

```powershell
# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Installation

Clone the repo and sync dependencies:

```bash
# Install all dependencies into a fresh virtual environment
uv sync
```

### 3. Running the App

```bash
# Run the command-line entry point
uv run defaultpython

# Run the API server (FastAPI) with hot-reload
uv run uvicorn defaultpython.api:app --reload
```

---

## 🛠️ Development Workflow

### Managing Dependencies

Instead of `pip install`, use `uv` to add packages. This keeps `pyproject.toml` and `uv.lock` in sync.

```bash
# Add a production dependency (e.g., pandas)
uv add pandas

# Add a development tool (e.g., pytest)
uv add --dev pytest
```

### Code Quality & Testing

We use strict tools to maintain high code quality. You should run these before pushing code.

| Tool | Purpose | Command |
| :--- | :--- | :--- |
| **Ruff** | Lints code and fixes formatting issues. | `task lint` |
| **Mypy** | Checks static types (like TypeScript for Python). | `task type-check` |
| **Bandit** | Scans for security vulnerabilities. | `task security` |
| **Pytest** | Runs your test suite. | `task test` |

### Using the Task Runner

This project uses [Task](https://taskfile.dev/) to simplify commands. It's like a modern `Make`.

```bash
# List all available commands
task

# Format code automatically (fixes imports, spacing, etc.)
task format

# Run EVERYTHING (Lint, Format, Types, Security, Tests)
# Run this before you submit a Pull Request!
task check
```

---

## 📂 Project Structure

```text
.
├── src/                # Source code
│   └── defaultpython/  # Main package
├── tests/              # Test suite (mirrors src structure)
├── .github/            # GitHub Actions (CI/CD workflows)
├── pyproject.toml      # Project configuration & dependencies
├── Taskfile.yml        # Task runner definitions
├── Dockerfile          # Production container setup
└── uv.lock             # Exact dependency versions (do not edit manually)
```

## 🔌 API Documentation

When the server is running (`task run-api`), you can view the interactive documentation:

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## 🤝 Contributing

1. **Environment Variables**: Copy `.env.example` to `.env` if you need to set secrets.
2. **Pre-commit Hooks**: We use `pre-commit` to catch errors automatically.

   ```bash
   uv run pre-commit install
   ```

3. **Commit Messages**: We use [Conventional Commits](https://www.conventionalcommits.org/) (e.g., `feat: add login`, `fix: crash on modules`). This allows us to generate changelogs automatically.
