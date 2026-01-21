# Ugram

[![Python Version](https://img.shields.io/badge/python-3.13-blue.svg)](https://python.org)
[![Code Style: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

An Instagram-like web application built with **FastAPI** and **PostgreSQL**. Uses **[uv](https://docs.astral.sh/uv/)** for fast dependency management.

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.13+**
- **Docker** (for the database)
- **uv** — Install it with:

```bash
# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/ugram.git
cd ugram

# Install dependencies
uv sync
```

### Running the Application

```bash
# 1. Start the database
docker compose -f backend/docker-compose.yml up -d db

# 2. Start the backend server (with hot-reload)
cd backend
uv run uvicorn src.main:app --reload --port 8000
```

The API will be available at **http://localhost:8000**

---

## 📖 API Documentation

Once the server is running, explore the API:

| Documentation | URL |
| :--- | :--- |
| **Swagger UI** | [http://localhost:8000/docs](http://localhost:8000/docs) |
| **ReDoc** | [http://localhost:8000/redoc](http://localhost:8000/redoc) |

---

## 📂 Project Structure

```
ugram/
├── backend/                 # FastAPI backend
│   ├── src/                 # Source code
│   │   ├── adapters/        # Database & external service adapters
│   │   ├── application/     # Business logic & configuration
│   │   ├── domain/          # Domain models & entities
│   │   └── main.py          # Application entry point
│   ├── tests/               # Test suite
│   ├── docker-compose.yml   # Database container
│   └── pyproject.toml       # Backend dependencies
├── pyproject.toml           # Workspace configuration
├── Taskfile.yml             # Task runner commands
└── README.md
```

---

## 🛠️ Development

### Available Commands

This project uses [Task](https://taskfile.dev/) as a task runner:

```bash
# List all available commands
task

# Start the database
task start-db

# Start the backend server
task start-backend

# Run tests
task test

# Lint code
task lint

# Format code
task format

# Run all checks (CI)
task check
```

### Managing Dependencies

```bash
# Add a production dependency
cd backend
uv add <package>

# Add a development dependency (from root)
uv add --dev <package>
```

---

## 🤝 Contributing

1. Copy `.env.example` to `.env` and configure your environment variables
2. Install pre-commit hooks:
   ```bash
   uv run pre-commit install
   ```
3. Use [Conventional Commits](https://www.conventionalcommits.org/) for commit messages:
   - `feat: add user profile page`
   - `fix: resolve login redirect issue`
   - `docs: update README`

---

## 📄 License

This project is developed as part of a university course.
