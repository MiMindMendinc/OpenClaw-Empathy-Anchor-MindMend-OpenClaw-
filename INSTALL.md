# 🚀 MindMend Super AI - Installation & Deployment Guide

Complete guide for installing, testing, and deploying the MindMend Super AI unified application.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Running the Application](#running-the-application)
5. [Testing](#testing)
6. [Deployment](#deployment)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software

- **Python 3.11 or higher** - Backend/API server
  - Check: `python --version` or `python3 --version`
  - Download: [python.org](https://www.python.org/downloads/)

- **Node.js 18 or higher** - Frontend/OpenClaw
  - Check: `node --version`
  - Download: [nodejs.org](https://nodejs.org/)

- **pip** - Python package manager
  - Usually comes with Python
  - Check: `pip --version` or `pip3 --version`

- **npm** - Node package manager
  - Comes with Node.js
  - Check: `npm --version`

### Optional Software

- **Git** - Version control (for cloning the repo)
- **virtualenv** - Python virtual environments (recommended)
- **Docker** - For containerized deployment (future)

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/MiMindMendinc/OpenClaw-Empathy-Anchor-MindMend-OpenClaw-.git
cd OpenClaw-Empathy-Anchor-MindMend-OpenClaw-
```

### 2. Backend Setup (Python/Flask)

```bash
cd backend

# Create a virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Verify installation
python -c "import flask; print('Flask installed successfully')"
```

### 3. Frontend Setup (Node.js/OpenClaw)

```bash
# Go back to root directory
cd ..

# Install Node.js dependencies
npm install

# Verify installation
npm list --depth=0
```

---

## Configuration

### Backend Configuration

Create a `.env` file in the `backend/` directory:

```bash
cd backend
cp .env.example .env  # If .env.example exists, otherwise create manually
```

Edit `.env` with your settings:

```env
# Flask Configuration
JWT_SECRET_KEY=your-secret-key-change-in-production
OFFLINE_MODE=true
DEBUG=false
PORT=5000

# Optional: Enable spaCy NLP (requires installation)
USE_SPACY=false

# Firebase (for production push notifications - future)
# FIREBASE_CREDENTIALS=path/to/firebase-credentials.json
```

**Important Security Notes:**
- ⚠️ Change `JWT_SECRET_KEY` to a strong, random value in production
- ⚠️ Set `DEBUG=false` in production
- ⚠️ Never commit `.env` file to version control

### Frontend Configuration

The frontend uses the existing `openclaw.config.json` and `.env.example` files.

For offline mode, set environment variable:

```bash
export OFFLINE_MODE=true
```

---

## Running the Application

### Start Backend Server

```bash
cd backend
source venv/bin/activate  # If using virtual environment
python app.py
```

Expected output:
```
INFO:luna_safety_core:Luna Safety Core initialized - Offline: True, NLP: False
INFO:__main__:MindMend Super AI Backend Started - Offline Mode: True
 * Running on http://0.0.0.0:5000
```

The API will be available at `http://localhost:5000`

### Start Frontend (OpenClaw)

In a new terminal:

```bash
npm start
```

This starts the OpenClaw empathy anchor integration.

### Test API Endpoints

Using `curl`:

```bash
# Health check
curl http://localhost:5000/health

# Login to get JWT token
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test_user"}'

# Use the token from above in subsequent requests
TOKEN="your-jwt-token-here"

# Chat endpoint
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"message": "I feel anxious"}'

# Get crisis resources
curl http://localhost:5000/resources
```

---

## Testing

### Run All Tests

```bash
# Backend tests (from backend directory)
cd backend
pytest tests/ -v

# Frontend tests (from root directory)
cd ..
npm test

# Run both
cd backend && pytest tests/ -v && cd .. && npm test
```

### Run Specific Test Suites

```bash
# Luna Safety Core tests only
cd backend
pytest tests/test_luna_safety_core.py -v

# Flask API tests only
pytest tests/test_app.py -v

# With coverage report
pytest tests/ -v --cov=. --cov-report=html
```

### Expected Test Results

**Backend Tests:**
- ✅ 19 tests in `test_luna_safety_core.py`
- ✅ 17 tests in `test_app.py`
- **Total: 36 passing tests**

**Frontend Tests:**
- Tests from existing `test/` and `tests/` directories

---

## Deployment

### Local Development Deployment

Already covered in "Running the Application" section above.

### Production Deployment Options

#### Option 1: Traditional Server (Linux VPS)

```bash
# Install system dependencies
sudo apt update
sudo apt install python3.11 python3-pip nginx

# Clone and setup app
git clone <repo-url>
cd OpenClaw-Empathy-Anchor-MindMend-OpenClaw-
cd backend
pip install -r requirements.txt

# Use gunicorn for production
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

#### Option 2: Docker (Future)

```bash
# Build Docker image
docker build -t mindmend-super-ai .

# Run container
docker run -p 5000:5000 -e OFFLINE_MODE=true mindmend-super-ai
```

#### Option 3: Cloud Platform (Heroku, Railway, etc.)

1. **Heroku:**
   ```bash
   heroku create mindmend-super-ai
   git push heroku main
   ```

2. **Railway:**
   - Connect GitHub repository
   - Set environment variables
   - Deploy automatically on push

#### Option 4: Raspberry Pi (Offline Mode - Owosso Deployment)

Perfect for privacy-first offline deployment:

```bash
# On Raspberry Pi 4 or newer
sudo apt update
sudo apt install python3 python3-pip nodejs npm

# Clone and setup
git clone <repo-url>
cd OpenClaw-Empathy-Anchor-MindMend-OpenClaw-
cd backend
pip3 install -r requirements.txt

# Run with systemd for auto-start
sudo cp mindmend.service /etc/systemd/system/
sudo systemctl enable mindmend
sudo systemctl start mindmend
```

---

## Troubleshooting

### Common Issues

#### Backend Issues

**Issue: `ModuleNotFoundError: No module named 'flask'`**
```bash
# Solution: Install dependencies
cd backend
pip install -r requirements.txt
```

**Issue: `Permission denied` when binding to port 5000**
```bash
# Solution: Use a different port or run with sudo
PORT=8000 python app.py
# Or on Linux/Mac:
sudo python app.py  # Not recommended
```

**Issue: Tests fail with import errors**
```bash
# Solution: Ensure you're in the right directory
cd backend
python -m pytest tests/ -v
```

#### Frontend Issues

**Issue: `npm install` fails**
```bash
# Solution: Clear cache and retry
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

**Issue: OpenClaw not found**
```bash
# Solution: Install OpenClaw CLI
npm run install-openclaw
```

### Getting Help

- **GitHub Issues**: [Create an issue](https://github.com/MiMindMendinc/OpenClaw-Empathy-Anchor-MindMend-OpenClaw-/issues)
- **Documentation**: See README_SUPER_AI.md
- **OpenClaw Docs**: [docs.openclaw.ai](https://docs.openclaw.ai)

---

## Performance Tips

### Backend Optimization

1. **Use Gunicorn** with multiple workers in production
2. **Enable caching** for repeated scans
3. **Install spaCy** for better NLP (optional):
   ```bash
   pip install spacy
   python -m spacy download en_core_web_sm
   ```

### Frontend Optimization

1. **Minimize dependencies** for faster startup
2. **Use production build** for Node.js apps
3. **Enable compression** in nginx if using reverse proxy

---

## Next Steps

After successful installation:

1. ✅ Review API documentation in README_SUPER_AI.md
2. ✅ Test all endpoints with sample data
3. ✅ Set up Firebase for push notifications (optional)
4. ✅ Configure geofencing safe zones
5. ✅ Customize crisis resources for your region
6. ✅ Plan production deployment

---

## Deployment Checklist

Before deploying to production:

- [ ] Change JWT secret key
- [ ] Disable debug mode
- [ ] Set up HTTPS/SSL
- [ ] Configure firewall rules
- [ ] Set up monitoring/logging
- [ ] Create backup strategy
- [ ] Test all endpoints
- [ ] Load test the API
- [ ] Document deployment architecture
- [ ] Train users on the system

---

**Questions or issues?** Please open an issue on GitHub or contact the MindMend team.

**Remember:** This application handles sensitive mental health data. Always prioritize privacy and security.

---

Built with 💙 by MiMindMendinc for youth mental health and safety.
