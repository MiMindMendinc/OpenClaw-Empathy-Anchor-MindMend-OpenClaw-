# 💙 OpenClaw Empathy Anchor

> **Privacy-first, offline-capable AI for youth mental health support**

A Node.js-based fork of OpenClaw.ai featuring a core 'empathy-anchor' skill that wraps all responses in compassionate language designed specifically for youth mental health support. Built with privacy as a priority, this tool operates offline to ensure conversations remain confidential and secure.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Node.js](https://img.shields.io/badge/node-%3E%3D14.0.0-brightgreen.svg)](https://nodejs.org/)

## 🌟 Features

- **🔒 Privacy-First Offline Mode**: All processing happens locally on your device - no data sent to external servers
- **💙 Empathy-Anchored Responses**: Every interaction is wrapped in compassionate, validating language
- **🎯 Emotion Validation**: Automatically detects and validates emotional states (anxiety, sadness, anger, fear, overwhelm)
- **🆘 Crisis Detection**: Identifies crisis situations and immediately provides appropriate resources
- **📞 Resource Integration**: Includes 988 Suicide & Crisis Lifeline and other mental health resources
- **🧒 Youth-Focused**: Language and resources tailored for young people and their families
- **⚡ Lightweight**: Pure Node.js with zero external dependencies

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/MiMindMendinc/OpenClaw-Empathy-Anchor-MindMend-OpenClaw-.git
cd OpenClaw-Empathy-Anchor-MindMend-OpenClaw-

# No dependencies to install - ready to use!
```

### Requirements

- Node.js 14.0.0 or higher
- No internet connection required (privacy-first offline mode)

### Running the Interactive Chat

```bash
npm start
```

This launches an interactive command-line interface where you can chat with the empathy-anchored AI.

### Running the Demo

```bash
npm run demo
```

See example scenarios demonstrating emotion detection, crisis handling, and resource suggestions.

### Running Tests

```bash
npm test
```

Validates core functionality including emotion detection, crisis identification, and compassionate wrapping.

## 💻 Usage Examples

### Basic Usage

```javascript
const OpenClaw = require('./index');

// Initialize with offline mode (default for privacy)
const openclaw = new OpenClaw({ offlineMode: true });

// Process a message
const result = openclaw.chat("I'm feeling really anxious about tomorrow");

console.log(result.response);
// Outputs compassionate response with emotion validation and resources

console.log(result.metadata);
// { emotionsDetected: ['anxiety'], isCrisis: false, intensity: 'moderate', ... }
```

### Using the Empathy Anchor Skill Directly

```javascript
const EmpathyAnchor = require('./skills/empathy-anchor');

const anchor = new EmpathyAnchor({ offlineMode: true });

// Validate emotions
const emotions = anchor.validateEmotions("I feel sad and lonely");
console.log(emotions);
// { emotions: ['sadness'], isCrisis: false, intensity: 'moderate' }

// Wrap a response with compassion
const wrapped = anchor.wrapWithCompassion(
  "It's okay to take breaks when needed",
  "I'm overwhelmed with everything"
);
console.log(wrapped);
```

### Crisis Detection

```javascript
const openclaw = new OpenClaw();

if (openclaw.checkCrisis(userMessage)) {
  console.log("⚠️ Crisis detected - immediate resources provided");
}
```

## 🏗️ Project Structure

```
OpenClaw-Empathy-Anchor/
├── index.js                          # Main application entry point
├── package.json                      # Project configuration
├── skills/
│   └── empathy-anchor/
│       └── index.js                  # Core empathy-anchor skill
├── examples/
│   └── demo.js                       # Interactive demonstrations
├── test/
│   └── empathy-anchor.test.js        # Test suite
├── README.md                         # This file
└── LICENSE                           # MIT License
```

## 🎯 Core Empathy-Anchor Skill

The empathy-anchor skill (`/skills/empathy-anchor/index.js`) is the heart of this project:

### Key Capabilities

1. **Emotion Validation**: Detects and validates emotions including:
   - Anxiety, worry, nervousness
   - Sadness, depression, loneliness
   - Anger, frustration
   - Fear, terror
   - Overwhelm, stress
   - Crisis indicators

2. **Compassionate Response Wrapping**: Every response includes:
   - Validating opening statement
   - Emotion acknowledgment
   - Original response content
   - Appropriate resource suggestions
   - Supportive closing message

3. **Resource Suggestions**: Context-aware recommendations for:
   - **988 Suicide & Crisis Lifeline** (crisis situations)
   - Crisis Text Line (text HOME to 741741)
   - The Trevor Project (LGBTQ+ youth support)
   - SAMHSA National Helpline (general mental health)

4. **Offline Processing**: All emotion detection, validation, and response generation happens locally without requiring internet connectivity.

## 🔒 Privacy & Offline Capabilities

### Why Offline?

Privacy is paramount when dealing with mental health conversations, especially for youth. OpenClaw Empathy Anchor operates **entirely offline** by default:

- ✅ **No data transmission**: Conversations never leave the local device
- ✅ **No tracking**: Zero analytics or usage monitoring
- ✅ **No cloud dependencies**: Works without internet connection
- ✅ **Full control**: Users maintain complete ownership of their data

### How It Works Offline

The empathy-anchor skill uses:
- **Pattern matching** for emotion detection (no ML models required)
- **Rule-based validation** for crisis identification
- **Local response generation** from predefined compassionate templates
- **Configurable resources** stored locally in the code

This ensures complete functionality even in areas with limited connectivity or for users prioritizing privacy.

## 📚 API Reference

### OpenClaw Class

#### `constructor(config)`
Initialize OpenClaw instance.

**Parameters:**
- `config.offlineMode` (boolean): Enable offline mode (default: true)

#### `chat(message, aiResponse)`
Process a user message with empathy anchoring.

**Parameters:**
- `message` (string): User's input message
- `aiResponse` (string, optional): External AI response to wrap

**Returns:** Object with `response` (string) and `metadata` (object)

#### `checkCrisis(message)`
Check if message indicates crisis situation.

**Returns:** Boolean

#### `validateEmotions(message)`
Analyze emotions in message.

**Returns:** Object with detected emotions and intensity

### EmpathyAnchor Class

See `/skills/empathy-anchor/index.js` for detailed API documentation.

## 🌐 Related Projects & Resources

### Demos
- [Interactive Web Demo](https://mimindmendinc.github.io/openclaw-demo) - Try it in your browser
- [Video Walkthrough](https://youtube.com/openclaw-empathy) - See it in action

### Support Our Mission
- [Donate to MindMend](https://donate.mimindmend.org) - Support youth mental health technology
- [988 Suicide & Crisis Lifeline](https://988lifeline.org) - National crisis support
- [Mental Health America](https://mhanational.org) - Mental health advocacy and resources

### Community
- [GitHub Discussions](https://github.com/MiMindMendinc/OpenClaw-Empathy-Anchor-MindMend-OpenClaw-/discussions) - Ask questions and share ideas
- [Report Issues](https://github.com/MiMindMendinc/OpenClaw-Empathy-Anchor-MindMend-OpenClaw-/issues) - Bug reports and feature requests

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Report Bugs**: Open an issue with details
2. **Suggest Features**: Share your ideas in discussions
3. **Submit PRs**: Fix bugs or add features
4. **Improve Documentation**: Help others understand the project
5. **Share**: Tell others about this privacy-first tool

## 📋 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

Copyright (c) 2026 MiMindMendinc

## ⚠️ Important Disclaimers

- **Not a Replacement for Professional Help**: This tool provides supportive language and resources but is not a substitute for professional mental health care.
- **Crisis Situations**: If you're in crisis, please call 988 or visit your nearest emergency room.
- **Youth Safety**: Parents and guardians should supervise usage for younger users.
- **Limitations**: AI-based emotion detection has limitations and may not catch all nuances.

## 🙏 Acknowledgments

- Inspired by OpenClaw.ai's vision for accessible AI
- Built for the youth mental health community in Michigan and beyond
- Special thanks to crisis support organizations: 988 Lifeline, Crisis Text Line, The Trevor Project

## 📞 Emergency Resources

If you or someone you know is in crisis:

- **988 Suicide & Crisis Lifeline**: Call or text 988 (available 24/7)
- **Crisis Text Line**: Text HOME to 741741
- **The Trevor Project** (LGBTQ+ Youth): 1-866-488-7386
- **Emergency**: Call 911 or visit your nearest emergency room

---

**Built with 💙 by MiMindMendinc for youth mental health and privacy-first AI**
