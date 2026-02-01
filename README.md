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
# OpenClaw Empathy Anchor - MindMend

Customized OpenClaw.ai with empathy anchor for ethical, offline AI supporting youth mental health and safety in Michigan. Privacy-first tools for families.

# OpenClaw Empathy Anchor - MindMend

Customized OpenClaw.ai with empathy anchor for ethical, offline AI supporting youth mental health and safety in Michigan. Privacy-first tools for families in Owosso.

## 🌟 About

The Empathy Anchor skill is a youth-focused mental health support tool that:

- **Validates emotions** - Acknowledges and normalizes what young people are feeling
- **Triggers on all messages** - Provides compassionate support throughout conversations
- **Suggests Michigan resources** - Connects youth to NAMI Michigan, 988 Suicide & Crisis Lifeline, and other local support
- **Privacy-first** - Detects offline mode and respects user privacy
- **Privacy-first** - Detects offline mode and respects user privacy (especially important for youth in Owosso)
- **Youth-appropriate** - Uses language and approaches designed for young people

## 🚀 Installation

### Prerequisites

- Node.js 18.0.0 or higher
- npm (comes with Node.js)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/MiMindMendinc/OpenClaw-Empathy-Anchor-MindMend-OpenClaw-.git
   cd OpenClaw-Empathy-Anchor-MindMend-OpenClaw-
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Run tests**
   ```bash
   npm test
   ```

### Using the Skill

The empathy-anchor skill is located in `skills/empathy-anchor/` and can be integrated into any OpenClaw installation:

1. Copy the `skills/empathy-anchor` directory to your OpenClaw skills folder
2. The skill will automatically trigger on all messages
3. Configure offline mode via environment variable if needed:
   ```bash
   export OFFLINE_MODE=true
   ```

## 📚 Skill Features

### Emotional Detection

The skill analyzes messages for:
- Crisis keywords (suicide, self-harm, etc.)
- Distress keywords (anxiety, depression, loneliness, etc.)
- Neutral messages

### Michigan Mental Health Resources

#### 988 Suicide & Crisis Lifeline
- **Call or Text**: 988
- **Available**: 24/7
- **Services**: Free, confidential crisis support

#### NAMI Michigan
- **Website**: [https://namimi.org](https://namimi.org)
- **Helpline**: 1-800-950-NAMI (6264)
- **Services**: Support groups, education, advocacy

#### Crisis Text Line
- **Text**: "HELLO" to 741741
- **Available**: 24/7

#### Teen Line
- **Call**: 1-800-TLC-TEEN (852-8336)
- **Services**: Peer support for teens
#### Emergency
- **Call**: 911
- **When**: Immediate danger or life-threatening emergency

### Privacy Protection

The skill checks for offline mode through:
- Context system flags (`context.system.offlineMode`, `context.system.offline`, `context.system.networkStatus`)
- Environment variable (`OFFLINE_MODE=true`)

When offline mode is detected, responses include a privacy notice.
When offline mode is detected, responses include a privacy notice: "🔒 Privacy Mode: Your conversation is staying private"

This is especially important for youth AI users in Owosso and across Michigan who need assurance that their conversations remain confidential.

## 🧪 Testing

Run the comprehensive test suite:

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
Tests cover:
- Module exports and structure
- Emotional content analysis
- Offline mode detection
- Resource formatting
- Main skill execution
- Michigan resource availability
- All-message triggering

## 🎯 Demo & Support

### Try the Demo
Experience a live demo of Eve, our youth mental health AI assistant:
- **Eve Demo**: [https://kid-helper-ai.replit.app](https://kid-helper-ai.replit.app)

### Support MindMend

Help us continue developing privacy-first mental health tools for Michigan youth:

- **GoFundMe**: [https://gofund.me/42b8334bd](https://gofund.me/42b8334bd)
- **Cash App**: [$MichiganMindMendinc](https://cash.app/$MichiganMindMendinc)

Your support helps us provide free, accessible mental health resources to young people across Michigan.

## 📖 Documentation

### SKILL.md

See `skills/empathy-anchor/SKILL.md` for detailed skill documentation including:
- When to use the skill
- Core principles
- Response guidelines
- Implementation notes
- Example responses

### API

The skill exports a main `run` function:

```javascript
const result = await run(context, params);
```

**Parameters:**
- `context`: OpenClaw execution context (includes system info, offline status)
- `params`: Object with `message`, `text`, or `content` property

**Returns:**
```javascript
{
  success: boolean,
  empathyLevel: 'crisis' | 'distress' | 'neutral' | 'none',
  hasResources: boolean,
  offline: boolean,
  response: string,
  metadata: {
    triggeredOn: 'all-messages',
    privacyMode: boolean,
    resourcesShared: boolean,
    emotionLevel: string
  }
}
```

## 🤝 Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass (`npm test`)
5. Submit a pull request

## 📄 License

ISC License - see LICENSE file for details

## 🏥 Crisis Resources

**If you or someone you know is in crisis, please reach out:**

- **988 Suicide & Crisis Lifeline**: Call or text 988 (24/7)
- **Crisis Text Line**: Text "HELLO" to 741741 (24/7)
- **NAMI Michigan**: 1-800-950-NAMI (6264)
- **Emergency**: Call 911

## 🙏 Acknowledgments

Built with love for Michigan youth and families by MiMindMendinc.

Special thanks to the OpenClaw.ai community for creating an open-source framework that enables privacy-first AI assistance.

---

**Remember: You are not alone. Your feelings are valid. Help is available.**

The Empathy Anchor skill is a youth-focused mental health support tool that:

- **Validates emotions** - Acknowledges and normalizes what young people are feeling
- **Triggers on all messages** - Provides compassionate support throughout conversations
- **Suggests Michigan resources** - Connects youth to NAMI Michigan, 988 Suicide & Crisis Lifeline, and other local support
- **Privacy-first** - Detects offline mode and respects user privacy (especially important for youth in Owosso)
- **Youth-appropriate** - Uses language and approaches designed for young people

## 🚀 Installation

### Prerequisites

- Node.js 18.0.0 or higher
- npm (comes with Node.js)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/MiMindMendinc/OpenClaw-Empathy-Anchor-MindMend-OpenClaw-.git
   cd OpenClaw-Empathy-Anchor-MindMend-OpenClaw-
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Run tests**
   ```bash
   npm test
   ```

### Using the Skill

The empathy-anchor skill is located in `skills/empathy-anchor/` and can be integrated into any OpenClaw installation:

1. Copy the `skills/empathy-anchor` directory to your OpenClaw skills folder
2. The skill will automatically trigger on all messages
3. Configure offline mode via environment variable if needed:
   ```bash
   export OFFLINE_MODE=true
   ```

## 📚 Skill Features

### Emotional Detection

The skill analyzes messages for:
- Crisis keywords (suicide, self-harm, etc.)
- Distress keywords (anxiety, depression, loneliness, etc.)
- Neutral messages

### Michigan Mental Health Resources

#### 988 Suicide & Crisis Lifeline
- **Call or Text**: 988
- **Available**: 24/7
- **Services**: Free, confidential crisis support

#### NAMI Michigan
- **Website**: [https://namimi.org](https://namimi.org)
- **Helpline**: 1-800-950-NAMI (6264)
- **Services**: Support groups, education, advocacy

#### Crisis Text Line
- **Text**: "HELLO" to 741741
- **Available**: 24/7

#### Emergency
- **Call**: 911
- **When**: Immediate danger or life-threatening emergency

### Privacy Protection

The skill checks for offline mode through:
- Context system flags (`context.system.offlineMode`, `context.system.offline`, `context.system.networkStatus`)
- Environment variable (`OFFLINE_MODE=true`)

When offline mode is detected, responses include a privacy notice: "🔒 Privacy Mode: Your conversation is staying private"

This is especially important for youth AI users in Owosso and across Michigan who need assurance that their conversations remain confidential. When running offline on a Raspberry Pi or similar device, no data is sent to the cloud, ensuring complete privacy.

## 🧪 Testing

Run the comprehensive test suite:

```bash
npm test
```

Tests cover:
- Module exports and structure
- Emotional content analysis
- Offline mode detection
- Resource formatting
- Main skill execution
- Michigan resource availability
- All-message triggering

## 🎯 Demo & Support

### Try the Demo
Experience a live demo of Eve, our youth mental health AI assistant:
- **Eve Demo**: [https://kid-helper-ai.replit.app](https://kid-helper-ai.replit.app)

### Support MindMend

Help us continue developing privacy-first mental health tools for Michigan youth:

- **GoFundMe**: [https://gofund.me/42b8334bd](https://gofund.me/42b8334bd)
- **Cash App**: [$MichiganMindMendinc](https://cash.app/$MichiganMindMendinc)

Your support helps us provide free, accessible mental health resources to young people across Michigan.

## 📖 Documentation

### SKILL.md

See `skills/empathy-anchor/SKILL.md` for detailed skill documentation including:
- When to use the skill
- Core principles
- Response guidelines
- Implementation notes
- Example responses

### API

The skill exports a main `run` function:

```javascript
const result = await run(context, params);
```

**Parameters:**
- `context`: OpenClaw execution context (includes system info, offline status)
- `params`: Object with `message`, `text`, or `content` property

**Returns:**
```javascript
{
  success: boolean,
  empathyLevel: 'crisis' | 'distress' | 'neutral' | 'none',
  hasResources: boolean,
  offline: boolean,
  response: string,
  metadata: {
    triggeredOn: 'all-messages',
    privacyMode: boolean,
    resourcesShared: boolean,
    emotionLevel: string
  }
}
```

## 🤝 Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass (`npm test`)
5. Submit a pull request

## 📄 License

ISC License - see LICENSE file for details

## 🏥 Crisis Resources

**If you or someone you know is in crisis, please reach out:**

- **988 Suicide & Crisis Lifeline**: Call or text 988 (24/7)
- **Crisis Text Line**: Text "HELLO" to 741741 (24/7)
- **NAMI Michigan**: 1-800-950-NAMI (6264)
- **Emergency**: Call 911

## 🙏 Acknowledgments

Built with love for Michigan youth and families by MiMindMendinc.

Special thanks to the OpenClaw.ai community for creating an open-source framework that enables privacy-first AI assistance.

---

**Remember: You are not alone. Your feelings are valid. Help is available.**
## About

This repository integrates the [OpenClaw](https://github.com/openclaw/openclaw) personal AI assistant with a custom **Empathy Anchor** skill designed specifically for youth mental health support. It provides:

- 🧠 **Compassionate AI**: Responses infused with emotional intelligence and empathy
- 🔒 **Privacy-First**: Local-first architecture, data stays on your device
- 🆘 **Crisis Awareness**: Automatic detection and response to mental health crises
- 👥 **Youth-Centered**: Age-appropriate language and understanding
- 📱 **Multi-Channel**: Works with WhatsApp, Telegram, Discord, and more

## Prerequisites

- **Node.js** 22 or higher
- **npm** or **pnpm**
- An API key from [Anthropic](https://anthropic.com) (recommended) or [OpenAI](https://openai.com)

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/MiMindMendinc/OpenClaw-Empathy-Anchor-MindMend-OpenClaw.git
cd OpenClaw-Empathy-Anchor-MindMend-OpenClaw-
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Install OpenClaw CLI
```bash
npm run install-openclaw
```

### 4. Configure Environment
Copy the example environment file and add your API keys:
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY or OPENAI_API_KEY
```

### 5. Run Setup Wizard
```bash
npm run setup
```

The OpenClaw onboarding wizard will guide you through:
- Choosing your AI model provider
- Configuring channels (WhatsApp, Telegram, etc.)
- Setting up your workspace
- Loading the Empathy Anchor skill

### 6. Start the Assistant
```bash
npm start
```

Or use OpenClaw directly:
```bash
openclaw gateway
```

## Empathy Anchor Skill

The **Empathy Anchor** is the core skill that provides compassionate, youth-focused mental health support.

### Features

- ✅ **Active Listening**: Validates feelings and experiences
- ✅ **Emotional Safety**: Non-judgmental, supportive responses
- ✅ **Crisis Detection**: Recognizes signs of distress and provides resources
- ✅ **Privacy**: All conversations stay private and local
- ✅ **Resource Awareness**: Knows when to provide hotline numbers and professional help

See [skills/empathy-anchor/SKILL.md](./skills/empathy-anchor/SKILL.md) for detailed documentation.

### Crisis Resources

The skill provides these resources when needed:

**National:**
- 988 Suicide & Crisis Lifeline (call or text)
- Crisis Text Line: Text HOME to 741741
- Trevor Project (LGBTQ+ Youth): 1-866-488-7386

**Michigan:**
- Michigan Crisis & Access Line: 1-844-464-3274

## Configuration

The repository includes:
- `openclaw.config.json` - OpenClaw configuration with Empathy Anchor enabled
- `.env.example` - Environment variables template
- `skills/empathy-anchor/` - Custom skill directory

### Customizing the Skill

Edit `openclaw.config.json` to adjust:
- Crisis detection sensitivity
- Response templates
- Resource lists
- Privacy settings

## Architecture

This integration works by:

1. **Using OpenClaw as a dependency**: The full OpenClaw assistant framework
2. **Custom Skills**: The Empathy Anchor skill in `./skills/empathy-anchor/`
3. **Configuration Override**: Custom config that enables empathy-focused features
4. **Local-First**: Data and conversations stay on your device

```
┌─────────────────────────────────────────────┐
│         Your Application (index.js)         │
│  - Loads OpenClaw                          │
│  - Applies Empathy Anchor configuration    │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│         OpenClaw Core Framework             │
│  - Gateway (communication hub)             │
│  - Agent (AI processing)                   │
│  - Skills Loader                           │
│  - Channels (WhatsApp, Telegram, etc.)     │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│       Custom Empathy Anchor Skill           │
│  - Emotional intelligence guidelines       │
│  - Crisis detection & response             │
│  - Youth-appropriate communication         │
│  - Resource provision                      │
└─────────────────────────────────────────────┘
```

## Development

### Project Structure
```
.
├── index.js                   # Main entry point
├── package.json              # Dependencies and scripts
├── openclaw.config.json      # OpenClaw configuration
├── .env.example              # Environment template
├── skills/
│   └── empathy-anchor/       # Custom empathy skill
│       └── SKILL.md          # Skill documentation
└── README.md                 # This file
```

### Available Scripts

- `npm start` - Start the assistant
- `npm run setup` - Run OpenClaw onboarding wizard
- `npm run install-openclaw` - Install OpenClaw CLI globally
- `npm run dev` - Start in development mode

## OpenClaw Integration

This repository integrates with [OpenClaw](https://github.com/openclaw/openclaw), which provides:

- 🌐 **Gateway**: Communication hub for all channels
- 🤖 **Agent**: AI processing and conversation management
- 🔌 **Skills System**: Extensible skill loader
- 📡 **Channels**: WhatsApp, Telegram, Discord, Slack, and more
- 🎨 **Canvas**: Visual content rendering
- 💾 **Memory**: Conversation history and context

For full OpenClaw documentation, visit [docs.openclaw.ai](https://docs.openclaw.ai).

## Privacy & Ethics

This project prioritizes:

- **Privacy**: Data stays local, no unnecessary cloud services
- **Safety**: Crisis detection and appropriate resource provision
- **Ethics**: AI should support, not replace, human connection
- **Transparency**: Open source, auditable code
- **Youth Protection**: Age-appropriate, safe interactions

## Support & Contribution

This project is developed by Michigan MindMend Inc. to support youth mental health in Owosso and beyond.

### Get Help
- Try Eve demo: https://kid-helper-ai.replit.app
- OpenClaw docs: https://docs.openclaw.ai
- OpenClaw Discord: https://discord.gg/clawd

### Donate
Support mental health initiatives in Michigan:
- GoFundMe: https://gofund.me/42b8334bd
- Cash App: https://cash.app/$MichiganMindMendinc

### Developer
By Lyle Perrien II, Michigan MindMend Inc.

## License

MIT License - See [LICENSE](./LICENSE) file for details.

This project uses [OpenClaw](https://github.com/openclaw/openclaw) which is also MIT licensed.

## Important Disclaimers

⚠️ **This AI assistant is NOT a replacement for professional mental health care.**

- Always seek professional help for serious mental health concerns
- In emergencies, call 911 or go to your nearest emergency room
- Crisis resources are provided, but the AI cannot provide therapy
- Parents/guardians should supervise youth usage

## Acknowledgments

- **OpenClaw Team**: For the incredible open-source AI assistant framework
- **Michigan Community**: For supporting youth mental health initiatives
- **Mental Health Professionals**: For guidance on ethical AI in mental health support
