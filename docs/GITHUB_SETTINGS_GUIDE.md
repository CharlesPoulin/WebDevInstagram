# 🚀 GitHub Repository Settings Guide (2026 Best Practices)

> **Quick-reference guide for optimizing your Python project's GitHub configuration.**

---

## 📋 Table of Contents

- [Repository Settings](#-repository-settings)
- [Branch Protection Rules](#-branch-protection-rules)
- [Merge Settings](#-merge-settings)
- [Actions & Automation](#-actions--automation)
- [Security Settings](#-security-settings)
- [Dependabot Configuration](#-dependabot-configuration)
- [Quick Checklist](#-quick-checklist)

---

## ⚙️ Repository Settings

### General Settings

| Setting | Recommended Value | Why |
|---------|-------------------|-----|
| **Default Branch** | `main` | Industry standard since 2020 |
| **Template Repository** | ✅ Enable if reusable | Create new repos from this template |
| **Wikis** | ❌ Disable | Use `/docs` folder instead (better versioning) |
| **Issues** | ✅ Enable | Essential for tracking work |
| **Sponsorships** | Optional | Support open-source maintainers |
| **Discussions** | ✅ Enable for OSS | Community Q&A without cluttering issues |

### Features to Disable

- [ ] **Projects** (unless actively used) — reduces clutter
- [ ] **Preserve this repository** — only for archival purposes

---

## 🔒 Branch Protection Rules

> **Settings → Branches → Add rule for `main`**

### Essential Protections ✅

```
☑ Require a pull request before merging
  └─ ☑ Require approvals: 1 (or 2 for critical projects)
  └─ ☑ Dismiss stale PR approvals when new commits are pushed
  └─ ☑ Require review from Code Owners

☑ Require status checks to pass before merging
  └─ ☑ Require branches to be up to date before merging
  └─ Status checks: ci, lint, test, security

☑ Require conversation resolution before merging

☑ Require signed commits (if team uses GPG/SSH signing)

☑ Require linear history (enables clean git log)

☑ Do not allow bypassing the above settings
```

### Advanced Protections

| Setting | Recommendation |
|---------|----------------|
| **Lock branch** | ❌ Only for release branches |
| **Allow force pushes** | ❌ Never on main |
| **Allow deletions** | ❌ Never on protected branches |
| **Restrict who can push** | ✅ Only bots/admins for releases |

---

## 🔀 Merge Settings

> **Settings → General → Pull Requests**

### Merge Button Options

```
☑ Allow squash merging ← RECOMMENDED DEFAULT
  └─ Default commit message: "Pull request title and description"

☐ Allow merge commits (disable for clean history)

☐ Allow rebase merging (can cause issues with PRs)
```

### 🌟 Auto-Delete Branches

```
☑ Automatically delete head branches ← MUST ENABLE
```

**Why?** Prevents stale branch accumulation, keeps repo clean.

### Other Options

```
☑ Always suggest updating pull request branches
☑ Allow auto-merge ← Enable for Dependabot PRs
```

---

## 🤖 Actions & Automation

### Workflow Permissions
>
> **Settings → Actions → General**

```
Workflow permissions:
☑ Read and write permissions (for auto-releases)
☑ Allow GitHub Actions to create and approve PRs
```

### Recommended Workflows

#### 1. CI Pipeline (`.github/workflows/ci.yml`)

```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
      - run: uv run ruff check .
      - run: uv run ruff format --check .

  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12", "3.13"]
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
      - run: uv run pytest --cov

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
      - run: uv run bandit -r src/

  type-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
      - run: uv run mypy src/
```

#### 2. Auto-Merge Dependabot (`.github/workflows/dependabot-auto-merge.yml`)

```yaml
name: Dependabot Auto-Merge
on: pull_request

permissions:
  contents: write
  pull-requests: write

jobs:
  auto-merge:
    runs-on: ubuntu-latest
    if: github.actor == 'dependabot[bot]'
    steps:
      - name: Auto-merge minor/patch updates
        run: gh pr merge --auto --squash "$PR_URL"
        env:
          PR_URL: ${{ github.event.pull_request.html_url }}
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

---

## 🛡️ Security Settings

### Code Security & Analysis
>
> **Settings → Code security and analysis**

| Feature | Status | Notes |
|---------|--------|-------|
| **Dependency graph** | ✅ Enable | Visualize dependencies |
| **Dependabot alerts** | ✅ Enable | Vulnerability notifications |
| **Dependabot security updates** | ✅ Enable | Auto-PRs for security fixes |
| **Dependabot version updates** | ✅ Enable | Keep dependencies fresh |
| **Code scanning** | ✅ Enable | CodeQL for Python |
| **Secret scanning** | ✅ Enable | Detect leaked secrets |
| **Push protection** | ✅ Enable | Block secret pushes |

### Secret Scanning

```
☑ Enable secret scanning
☑ Push protection ← CRITICAL: blocks commits with secrets
☑ Validity checks (GitHub tokens)
```

## 📝 Required Files Checklist

```
📁 .github/
├── 📄 CODEOWNERS              # Define code ownership
├── 📄 dependabot.yml          # Dependency updates
├── 📄 PULL_REQUEST_TEMPLATE.md
├── 📁 ISSUE_TEMPLATE/
│   ├── 📄 bug_report.yml
│   ├── 📄 feature_request.yml
│   └── 📄 config.yml
└── 📁 workflows/
    ├── 📄 ci.yml
    ├── 📄 release.yml
    └── 📄 dependabot-auto-merge.yml

📁 Root files
├── 📄 README.md               # Project overview with badges
├── 📄 LICENSE                 # MIT / Apache 2.0
├── 📄 CONTRIBUTING.md         # Contribution guidelines
├── 📄 CHANGELOG.md            # Version history
├── 📄 SECURITY.md             # Security policy
├── 📄 CODE_OF_CONDUCT.md      # Community guidelines
├── 📄 .editorconfig           # Editor consistency
├── 📄 .pre-commit-config.yaml # Pre-commit hooks
└── 📄 .gitignore              # Ignore patterns
```

---

## ✅ Quick Checklist

### Immediate Actions (5 min)

- [ ] Enable **auto-delete head branches**
- [ ] Enable **Dependabot alerts**
- [ ] Enable **secret scanning with push protection**
- [ ] Set **squash merge as default**

### Branch Protection (10 min)

- [ ] Require PR reviews
- [ ] Require status checks
- [ ] Require linear history

### Automation (15 min)

- [ ] Set up CI workflow
- [ ] Configure Dependabot
- [ ] Add auto-merge for Dependabot
- [ ] Add CODEOWNERS file

### Security (10 min)

- [ ] Enable CodeQL scanning
- [ ] Enable dependency graph
- [ ] Add SECURITY.md policy
- [ ] Configure security advisories

---

## 🔗 Quick Links

- [GitHub Branch Protection Docs](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches)
- [Dependabot Configuration](https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/configuration-options-for-the-dependabot.yml-file)
- [CodeQL Setup](https://docs.github.com/en/code-security/code-scanning/creating-an-advanced-setup-for-code-scanning)
- [Secret Scanning](https://docs.github.com/en/code-security/secret-scanning/about-secret-scanning)

---

**Last Updated:** January 2026 | **Python Version:** 3.11+
