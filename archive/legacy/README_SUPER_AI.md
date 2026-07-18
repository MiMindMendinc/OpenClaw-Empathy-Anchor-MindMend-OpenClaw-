# 🌟 MindMend Super AI - Unified Privacy-First Youth Mental Health & Safety App

> **Combining MindMend Guardian + Eve AI + OpenClaw Empathy Anchor + Night Mode**  
> Privacy-first, offline-capable AI for youth mental health support and safety monitoring

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![Node.js](https://img.shields.io/badge/node-%3E%3D18.0.0-brightgreen.svg)](https://nodejs.org/)
[![CI/CD](https://github.com/MiMindMendinc/OpenClaw-Empathy-Anchor-MindMend-OpenClaw-/actions/workflows/ci.yml/badge.svg)](https://github.com/MiMindMendinc/OpenClaw-Empathy-Anchor-MindMend-OpenClaw-/actions)

## 🎯 Overview

**MindMend Super AI** is an all-in-one application combining:

- **🛡️ MindMend Guardian**: Offline child safety with threat detection, geofencing, parent alerts
- **💙 Eve AI**: Youth mental health empathy support with crisis detection
- **⚓ OpenClaw Empathy Anchor**: Custom OpenClaw integration for compassionate AI responses  
- **🌙 Night Mode**: Bedtime routines, sleep tracking, calming responses

### Key Features

- ✅ **Real-time Chat Empathy** for mental health support
- ✅ **Keyword/Toxicity Scanning** with NLP (spaCy or pattern matching)
- ✅ **Location Geofencing** with parent alerts
- ✅ **Async Parent Alerts** via Firebase (offline-compatible)
- ✅ **JWT Authentication** for secure access
- ✅ **Offline Capability** with local processing
- ✅ **Crisis Resources** (988 Lifeline, NAMI Michigan)
- ✅ **Donation Links** to support mental health initiatives
- ✅ **Night Mode** for bedtime safety and calming support

## 🏗️ Architecture

```
MindMend Super AI
├── Backend (Python/Flask)
│   ├── luna_safety_core.py    # Core safety & empathy logic
│   ├── app.py                  # Flask API server
│   └── tests/                  # Backend test suite
├── Frontend (Node.js/OpenClaw + Flutter option)
│   ├── index.js                # OpenClaw integration
│   ├── skills/empathy-anchor/  # Empathy skill
│   └── (Flutter app TBD)       # Mobile UI
└── CI/CD
    └── .github/workflows/ci.yml
```

### API Endpoints

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/health` | GET | Health check | No |
| `/auth/login` | POST | JWT authentication | No |
| `/chat` | POST | Empathy chat with safety scanning | Yes |
| `/location` | POST | Geofence checking | Yes |
| `/night_mode` | POST | Bedtime support & calming | Yes |
| `/alerts` | GET | Parent alert management | Yes |
| `/resources` | GET | Crisis resources & donation links | No |

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+** for backend
- **Node.js 18+** for frontend/OpenClaw
- **pip** and **npm** package managers

### Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/MiMindMendinc/OpenClaw-Empathy-Anchor-MindMend-OpenClaw-.git
cd OpenClaw-Empathy-Anchor-MindMend-OpenClaw-
```

#### 2. Backend Setup (Python/Flask)

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run backend server
python app.py
```

The backend will start on `http://localhost:5000`

#### 3. Frontend Setup (Node.js/OpenClaw)

```bash
# From root directory
npm install

# Run Node tests
npm test

# Start OpenClaw integration
npm start
```

### Environment Variables

Create a `.env` file in the `backend/` directory:

```env
# Flask Configuration
JWT_SECRET_KEY=your-secret-key-change-in-production
OFFLINE_MODE=true
DEBUG=false
PORT=5000

# Optional: Enable spaCy NLP
USE_SPACY=false

# Firebase (for production alerts)
# FIREBASE_CREDENTIALS=path/to/credentials.json
```

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest tests/ -v
```

Tests cover:
- ✅ Luna Safety Core (crisis detection, empathy responses, geofencing)
- ✅ Flask API endpoints (chat, location, night mode, auth)
- ✅ Night mode time validation
- ✅ Alert creation and management

### Frontend Tests

```bash
npm test
```

Tests cover:
- ✅ Empathy-anchor skill functionality
- ✅ OpenClaw integration
- ✅ Crisis detection in JavaScript layer

### End-to-End Testing

```bash
# Run full test suite
cd backend && pytest tests/ -v && cd .. && npm test
```

## 📱 Mobile Frontend (Flutter - In Development)

A Flutter mobile app is planned for cross-platform (iOS/Android) deployment with:

- **Chat UI** for Eve-like empathy conversations
- **GPS Integration** for geofencing
- **Auth Login** with JWT tokens
- **Push Notifications** for parent alerts
- **Night Mode UI** with bedtime reminders

*Alternative: React Native if Flutter is not preferred*

## 🛡️ Privacy & Offline Mode

**Privacy is our top priority.** MindMend Super AI operates **fully offline by default**:

- ✅ **Local Processing**: All message scanning happens on-device
- ✅ **No Data Transmission**: Conversations never leave the device in offline mode
- ✅ **No Tracking**: Zero analytics or usage monitoring
- ✅ **Parent Control**: Alerts can be queued offline and sent when online

### How Offline Mode Works

1. **Pattern Matching NLP**: Uses keyword detection (no cloud ML needed)
2. **Local LLM Fallback**: Can integrate with Ollama for advanced local AI
3. **Offline JWT**: Tokens validated locally
4. **Queued Alerts**: Parent alerts stored locally until connection available

## 🆘 Crisis Resources

**If you or someone you know is in crisis, please reach out:**

### National Resources
- **988 Suicide & Crisis Lifeline**: Call or text **988** (24/7)
- **Crisis Text Line**: Text **HELLO** to **741741** (24/7)

### Michigan Resources
- **NAMI Michigan**: **1-800-950-NAMI (6264)**
- **Michigan Crisis & Access Line**: **1-844-464-3274**

### Emergency
- **911**: For immediate life-threatening emergencies

## 💙 Support Our Mission

Help us provide free mental health tools for Michigan youth:

- **GoFundMe**: [https://gofund.me/42b8334bd](https://gofund.me/42b8334bd)
- **Cash App**: [$MichiganMindMendinc](https://cash.app/$MichiganMindMendinc)

Your support helps us continue developing privacy-first mental health resources for young people across Michigan and beyond.

## 🔧 Development

### Project Structure

```
.
├── backend/
│   ├── luna_safety_core.py      # Core safety logic
│   ├── app.py                    # Flask API
│   ├── requirements.txt          # Python dependencies
│   └── tests/                    # Backend tests
│       ├── test_luna_safety_core.py
│       └── test_app.py
├── frontend/                     # (Flutter app - TBD)
├── skills/
│   └── empathy-anchor/           # OpenClaw empathy skill
│       ├── index.js
│       └── SKILL.md
├── .github/
│   └── workflows/
│       └── ci.yml                # CI/CD pipeline
├── index.js                      # Node.js entry point
├── package.json                  # Node dependencies
├── README.md                     # This file
└── LICENSE                       # MIT License
```

### Adding New Features

1. **Backend**: Extend `luna_safety_core.py` or add new API endpoints in `app.py`
2. **Frontend**: Update `skills/empathy-anchor/` or add Flutter components
3. **Tests**: Add tests in `backend/tests/` or `test/` directories
4. **CI/CD**: Pipeline automatically runs on push to `main`, `develop`, or `copilot/**` branches

## 📊 CI/CD Pipeline

Our GitHub Actions workflow automatically:

1. ✅ Runs backend Python tests (pytest)
2. ✅ Runs frontend Node.js tests
3. ✅ Validates build and startup
4. ✅ Performs security scans (Trivy)
5. ✅ Checks code style (flake8)
6. ✅ Audits npm dependencies

## 🎯 Roadmap

### Phase 1: Core Backend ✅ (Complete)
- [x] Luna Safety Core implementation
- [x] Flask API with all endpoints
- [x] JWT authentication
- [x] Comprehensive test suite
- [x] CI/CD pipeline

### Phase 2: Enhanced Features (In Progress)
- [ ] Flutter mobile app
- [ ] Firebase push notifications
- [ ] spaCy NLP integration (optional)
- [ ] Ollama local LLM integration
- [ ] Database for alert persistence

### Phase 3: Deployment (Planned)
- [ ] Docker containerization
- [ ] Local pilot deployment (Dec 26, 2025)
- [ ] Production environment setup
- [ ] Parent dashboard web app

## 🤝 Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Add tests for new functionality
4. Ensure all tests pass (`pytest` and `npm test`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## ⚠️ Important Disclaimers

- **Not a Replacement for Professional Help**: This tool provides supportive language and resources but is **NOT** a substitute for professional mental health care.
- **Crisis Situations**: If you're in crisis, please call **988** or visit your nearest emergency room immediately.
- **Youth Safety**: Parents and guardians should supervise usage for younger users.
- **AI Limitations**: AI-based emotion detection has limitations and may not catch all nuances.

## 🙏 Acknowledgments

- **OpenClaw Team**: For the incredible open-source AI assistant framework
- **Michigan Community**: For supporting youth mental health initiatives  
- **Mental Health Professionals**: For guidance on ethical AI in mental health support
- **Crisis Organizations**: 988 Lifeline, Crisis Text Line, NAMI Michigan

---

**Built with 💙 by MiMindMendinc for youth mental health and privacy-first AI**

**Remember: You are not alone. Your feelings are valid. Help is available.**

---

## 🎯 Demo

Experience a live demo of Eve, our youth mental health AI assistant:
- **Eve AI Demo**: [https://kid-helper-ai.replit.app](https://kid-helper-ai.replit.app)

---

**For questions, support, or collaboration:**  
📧 Contact: MiMindMendinc  
🌐 Website: [Coming Soon]  
💬 Discord: [Community Coming Soon]
