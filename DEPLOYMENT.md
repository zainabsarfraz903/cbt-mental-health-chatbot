# Deployment Guide

## Table of Contents
1. [GitHub Actions Setup](#github-actions-setup)
2. [Hetzner Cloud VPS Setup](#hetzner-cloud-vps-setup)
3. [Vercel Deployment](#vercel-deployment)

---

## GitHub Actions Setup

### Prerequisites
- GitHub repository with GitHub Actions enabled
- Docker Hub account (for pushing images)

### Configuration Steps

1. **Set GitHub Secrets**
   - Go to: Settings → Secrets and variables → Actions
   - Add the following secrets:
     ```
     DOCKER_USERNAME = your_dockerhub_username
     DOCKER_PASSWORD = your_dockerhub_token
     ```

2. **How It Works**
   - **On every push to `main` or `develop`:**
     - Runs unit tests on Python 3.9, 3.10, 3.11
     - Runs linting checks (black, isort, flake8)
     - Generates coverage reports
   - **On successful tests + merge to `main`:**
     - Builds Docker image
     - Pushes to Docker Hub

3. **View Workflow Status**
   - Go to: Actions tab in your GitHub repo
   - See real-time progress of all CI/CD stages

---

## Hetzner Cloud VPS Setup

### 1. Create VPS Instance

**Steps:**
- Log in to [Hetzner Cloud Console](https://console.hetzner.cloud/)
- Create new server:
  - **Image:** Ubuntu 22.04
  - **Type:** CPX11 (2 vCPU, 4GB RAM) - minimum recommended
  - **Location:** Pick closest region
  - **Add SSH key** for secure access

### 2. Initial Server Setup

SSH into your server:
```bash
ssh root@your_server_ip
```

Run initial setup:
```bash
# Update packages
apt update && apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Create non-root user
useradd -m -s /bin/bash cbotuser
usermod -aG docker cbotuser
su - cbotuser
```

### 3. Deploy Using Docker

**Option A: Pull from Docker Hub**
```bash
docker run -d \
  --name cbt-chatbot \
  -p 8000:8000 \
  -p 8501:8501 \
  -e ENVIRONMENT=production \
  your_dockerhub_username/cbt-chatbot:latest
```

**Option B: Using Docker Compose (Recommended)**

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  cbt-api:
    image: your_dockerhub_username/cbt-chatbot:latest
    container_name: cbt-api
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=production
    restart: unless-stopped
    volumes:
      - ./data:/app/data
      - ./models:/app/models

  nginx:
    image: nginx:alpine
    container_name: nginx-reverse-proxy
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - cbt-api
    restart: unless-stopped
```

Run:
```bash
docker-compose up -d
```

### 4. Set Up SSL Certificate (Let's Encrypt)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get certificate
sudo certbot certonly --standalone -d your_domain.com

# Auto-renew (runs daily)
sudo systemctl enable certbot.timer
```

### 5. Monitor Your Application

```bash
# Check running containers
docker ps

# View logs
docker logs cbt-api

# Restart service
docker restart cbt-api

# Stop service
docker stop cbt-api
docker remove cbt-api
```

### 6. Automated Deployments (Optional)

Create deployment webhook to auto-update when Docker image changes:

```bash
# Install webhook tool
sudo apt install webhook -y

# Create hooks.json
cat > hooks.json << 'EOF'
[
  {
    "id": "deploy-cbt",
    "execute-command": "/home/cbotuser/deploy.sh",
    "command-working-directory": "/home/cbotuser"
  }
]
EOF

# Create deploy script
cat > deploy.sh << 'EOF'
#!/bin/bash
cd /home/cbotuser/cbt-chatbot
docker-compose pull
docker-compose up -d
EOF

chmod +x deploy.sh
```

---

## Vercel Deployment

**Note:** Vercel is best for frontend-only deployments. For your project:

### Option 1: Deploy Streamlit Frontend to Vercel (Limited)

Streamlit doesn't work well on Vercel (it's server-side). Instead:

1. Use **Streamlit Cloud** (recommended):
   ```bash
   # Push your repo to GitHub
   # Go to share.streamlit.io
   # Connect GitHub repo
   # Select your branch and frontend/app.py
   ```

### Option 2: Deploy Next.js Frontend + FastAPI Backend

If you create a Next.js frontend:

**Frontend on Vercel:**
```bash
# Create frontend folder with Next.js
npx create-next-app@latest frontend-web

# Connect to Vercel
npm i -g vercel
vercel
```

**Backend on Hetzner** (use instructions above)

**Connect frontend to backend:**
```javascript
// In your Next.js API routes or frontend
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'https://api.yourdomain.com'
const response = await fetch(`${API_URL}/chat`, { /* ... */ })
```

Set environment variable in Vercel dashboard:
```
NEXT_PUBLIC_API_URL=https://your_hetzner_server.com:8000
```

---

## Cost Estimates

| Service | Plan | Cost/Month |
|---------|------|-----------|
| Hetzner Cloud | CPX11 | €4-5 |
| SSL Certificate | Let's Encrypt | FREE |
| Vercel | Hobby | FREE |
| Docker Hub | Free | FREE |
| GitHub Actions | Free (5000 min/mo) | FREE |

---

## Monitoring & Logs

### Hetzner Server Monitoring
```bash
# System resources
htop

# Disk usage
df -h

# Docker container resources
docker stats
```

### Log Management
```bash
# View application logs
docker logs -f cbt-api

# Save logs to file
docker logs cbt-api > app.log 2>&1
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| 502 Bad Gateway | Check if API container is running: `docker ps` |
| Port already in use | Change port in docker-compose.yml or stop conflicting service |
| Certificate error | Renew: `sudo certbot renew --force-renewal` |
| Out of memory | Upgrade server or increase swap: `fallocate -l 4G /swapfile` |

---

## Next Steps

1. ✅ Set up GitHub Actions secrets
2. ✅ Push code to trigger first workflow
3. ✅ Create Hetzner account and VPS
4. ✅ Deploy Docker image to VPS
5. ✅ Set up SSL certificate
6. ✅ Monitor logs and performance
