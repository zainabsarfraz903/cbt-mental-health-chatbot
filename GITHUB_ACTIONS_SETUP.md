# GitHub Actions - Quick Setup Guide

## 1. Set GitHub Secrets

These credentials are needed for Docker Hub integration:

**Step-by-step:**
1. Go to your GitHub repo → **Settings** → **Secrets and variables** → **Actions**
2. Click **"New repository secret"** and add:

| Secret Name | Value |
|-------------|-------|
| `DOCKER_USERNAME` | Your Docker Hub username |
| `DOCKER_PASSWORD` | Your Docker Hub Personal Access Token |

**How to get Docker Hub token:**
- Login to [Docker Hub](https://hub.docker.com)
- Go to Account Settings → Security
- Click "New Access Token"
- Copy the token and paste it as `DOCKER_PASSWORD`

## 2. Workflow Triggers

The CI/CD pipeline automatically triggers on:

✅ **Push to `main` or `develop` branch**
✅ **Pull requests** to `main` or `develop`

On merge to `main`, after all tests pass:
- ✅ Docker image is built
- ✅ Image is pushed to Docker Hub
- ✅ Two tags created: `latest` and commit SHA

## 3. Monitor Workflow

1. Go to your repo → **Actions** tab
2. See all workflow runs listed
3. Click any run to see detailed logs:
   - Test results per Python version
   - Code coverage report
   - Linting results
   - Docker build status

## 4. Workflow Stages Explained

### Stage 1: **Test** (Runs always)
```
✓ Checkout code
✓ Set up Python 3.9, 3.10, 3.11
✓ Install dependencies
✓ Run pytest with coverage
✓ Upload coverage to Codecov
```

### Stage 2: **Lint** (Runs always)
```
✓ Check code formatting (black)
✓ Check import order (isort)
✓ Lint with flake8
```

### Stage 3: **Build & Push** (Runs only on main after tests pass)
```
✓ Setup Docker Buildx
✓ Login to Docker Hub
✓ Build multi-stage Docker image
✓ Push to: docker.io/username/cbt-chatbot:latest
✓ Push to: docker.io/username/cbt-chatbot:{commit-hash}
```

## 5. Example Workflow

When you push to main:

```
📌 main branch (push event)
    ↓
🧪 Tests
    ├─ Python 3.9 tests ✓
    ├─ Python 3.10 tests ✓
    ├─ Python 3.11 tests ✓
    └─ Coverage report ✓
    ↓
🔍 Linting
    ├─ Black formatting ✓
    ├─ Import sorting ✓
    └─ Flake8 lint ✓
    ↓
📦 Build Docker (if all pass)
    ├─ Build image ✓
    ├─ Push to Docker Hub ✓
    └─ Tag: latest, {commit-sha} ✓
```

## 6. Pull Request Workflow

When you create a PR:

```
🔀 Pull Request to main
    ↓
🧪 Tests run (3 versions) ✓
    ↓
🔍 Linting checks ✓
    ↓
✅ Green check = Safe to merge!
    ↓
📌 Merge to main
    ↓
📦 Build & Push Docker
```

## 7. Troubleshooting

### ❌ Tests failing?
- Click the failed run
- Scroll to "Run tests" section
- See exact error message
- Fix locally and push again

### ❌ Docker push fails?
- Verify `DOCKER_USERNAME` secret is correct
- Verify `DOCKER_PASSWORD` is a valid token (not password!)
- Check if token has push permissions

### ❌ Linting fails?
- Run locally:
  ```bash
  pip install black isort flake8
  black src/ api/ frontend/ tests/
  isort src/ api/ frontend/ tests/
  flake8 src/ api/ frontend/ tests/
  ```
- Fix issues and push again

## 8. View Docker Image

After successful build, find your image on Docker Hub:

1. Go to [Docker Hub](https://hub.docker.com)
2. Search for `your_username/cbt-chatbot`
3. See all available tags
4. Pull locally:
   ```bash
   docker pull your_username/cbt-chatbot:latest
   ```

## 9. Deploy to Hetzner

Once Docker image is built and pushed:

```bash
# SSH to your Hetzner server
ssh root@your_server_ip

# Pull latest image
docker pull your_username/cbt-chatbot:latest

# Run container
docker-compose up -d

# Check status
docker ps
docker logs cbt-api
```

## 10. GitHub Actions Badge

Add this to your README.md to show CI status:

```markdown
[![CI/CD Pipeline](https://github.com/zainabsarfraz903/cbt-mental-health-chatbot/workflows/CI%2FCD%20Pipeline/badge.svg)](https://github.com/zainabsarfraz903/cbt-mental-health-chatbot/actions)
```

---

## Quick Reference Commands

```bash
# View secrets (they're hidden)
# Navigate: Settings → Secrets

# Manually trigger workflow (no action needed - automatic on push)

# Check specific Python version test results
# Go to Actions → Latest Run → Test Job → Python 3.10

# Re-run a failed workflow
# Go to Actions → Failed Run → "Re-run failed jobs"

# Delete workflow history
# Only GitHub admins can do this via API
```
