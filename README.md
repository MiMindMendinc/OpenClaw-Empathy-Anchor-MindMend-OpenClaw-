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
