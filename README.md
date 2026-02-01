# OpenClaw Empathy Anchor - MindMend

Customized OpenClaw.ai with empathy anchor for ethical, offline AI supporting youth mental health and safety in Michigan. Privacy-first tools for families in Owosso.

## 🌟 About

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
