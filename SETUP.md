# Setup Guide

This guide will help you set up the OpenClaw Empathy Anchor assistant from scratch.

## System Requirements

### Required
- **Operating System**: macOS, Linux, or Windows (via WSL2)
- **Node.js**: Version 22 or higher
- **npm**: Version 9 or higher (comes with Node.js)
- **RAM**: At least 4GB available
- **Disk Space**: 1GB for installation

### Recommended
- **Internet Connection**: For initial setup and AI model access
- **Terminal/Shell**: Basic command line knowledge
- **API Access**: Anthropic Claude API (recommended) or OpenAI API

## Step-by-Step Installation

### 1. Install Node.js

If you don't have Node.js 22+, install it:

**macOS (using Homebrew):**
```bash
brew install node@22
```

**Linux (using nvm):**
```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 22
nvm use 22
```

**Windows:**
- Install WSL2 first: https://docs.microsoft.com/en-us/windows/wsl/install
- Then follow Linux instructions inside WSL2

Verify installation:
```bash
node --version  # Should show v22.x.x or higher
npm --version   # Should show 9.x.x or higher
```

### 2. Clone the Repository

```bash
git clone https://github.com/MiMindMendinc/OpenClaw-Empathy-Anchor-MindMend-OpenClaw.git
cd OpenClaw-Empathy-Anchor-MindMend-OpenClaw-
```

### 3. Install Project Dependencies

```bash
npm install
```

This will install the lightweight wrapper dependencies.

### 4. Install OpenClaw CLI

```bash
npm run install-openclaw
```

Or manually:
```bash
npm install -g openclaw@latest
```

Verify OpenClaw is installed:
```bash
openclaw --version
```

### 5. Get API Keys

You'll need an API key from one of these providers:

#### Option A: Anthropic (Recommended)
1. Go to https://console.anthropic.com
2. Sign up or log in
3. Navigate to API Keys
4. Create a new API key
5. Copy the key (starts with `sk-ant-`)

#### Option B: OpenAI
1. Go to https://platform.openai.com
2. Sign up or log in
3. Navigate to API Keys
4. Create a new API key
5. Copy the key (starts with `sk-`)

### 6. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your preferred text editor:
```bash
nano .env
# or
code .env
# or
vim .env
```

Add your API key:
```env
# For Anthropic (recommended)
ANTHROPIC_API_KEY=sk-ant-your-key-here

# OR for OpenAI
# OPENAI_API_KEY=sk-your-key-here
```

Save and close the file.

### 7. Run OpenClaw Onboarding

```bash
npm run setup
```

Or directly:
```bash
openclaw onboard
```

The wizard will ask you:

1. **Workspace location**: Press Enter for default (`~/.openclaw`)
2. **Model provider**: Choose Anthropic or OpenAI
3. **API key**: Enter the key from step 5
4. **Channels**: Choose which messaging platforms to enable
   - WhatsApp (requires phone number)
   - Telegram (requires bot token)
   - Discord (requires bot token)
   - Or skip for local testing
5. **Skills**: Confirm loading skills from `./skills`

### 8. Verify Configuration

Check that the config file was created:
```bash
cat ~/.openclaw/openclaw.json
```

It should include your model settings and skills configuration.

### 9. Start the Assistant

```bash
npm start
```

You should see:
```
╔═══════════════════════════════════════════════════════════════╗
║  OpenClaw Empathy Anchor - Michigan MindMend Inc.            ║
║  Privacy-first AI for youth mental health support            ║
╚═══════════════════════════════════════════════════════════════╝
```

If everything is configured correctly, you'll see:
```
OpenClaw loaded successfully!
```

### 10. Test the Assistant

#### Option A: Local Testing
```bash
openclaw chat
```

This opens an interactive chat in your terminal.

#### Option B: Connect a Channel

If you configured WhatsApp/Telegram/Discord:
```bash
openclaw gateway
```

The gateway will start and connect to your configured channels.

## Common Issues & Solutions

### "OpenClaw not found"
**Solution**: Install OpenClaw globally
```bash
npm install -g openclaw@latest
```

### "API key invalid"
**Solution**: Double-check your API key in `.env`
- Ensure no extra spaces
- Verify the key is active in your provider's console
- Make sure you're using the right key format

### "Node version too old"
**Solution**: Update Node.js
```bash
# macOS
brew upgrade node

# Linux (using nvm)
nvm install 22
nvm use 22
```

### "Port already in use"
**Solution**: Change the port in `openclaw.config.json`
```json
{
  "gateway": {
    "port": 18791  // Changed from default 18790
  }
}
```

### Skills not loading
**Solution**: Verify skills directory in config
```json
{
  "skills": {
    "load": {
      "extraDirs": [
        "./skills/empathy-anchor"
      ]
    }
  }
}
```

## Channel-Specific Setup

### WhatsApp
1. During onboarding, choose WhatsApp
2. Scan the QR code with your phone
3. Keep the gateway running to stay connected

### Telegram
1. Create a bot: Talk to @BotFather on Telegram
2. Get your bot token
3. Add token during onboarding or in `.env`

### Discord
1. Create a Discord application: https://discord.com/developers
2. Create a bot and get the token
3. Add token during onboarding or in `.env`

## Next Steps

1. **Test the Empathy Anchor**: See [Testing Guide](./docs/TESTING.md)
2. **Customize Responses**: Edit `skills/empathy-anchor/SKILL.md`
3. **Add Local Resources**: Update crisis resources in `openclaw.config.json`
4. **Explore OpenClaw**: Visit https://docs.openclaw.ai

## Getting Help

- **OpenClaw Documentation**: https://docs.openclaw.ai
- **OpenClaw Discord**: https://discord.gg/clawd
- **Issues**: https://github.com/MiMindMendinc/OpenClaw-Empathy-Anchor-MindMend-OpenClaw/issues

## Support the Project

- Try Eve demo: https://kid-helper-ai.replit.app
- Donate: https://gofund.me/42b8334bd
- Cash App: https://cash.app/$MichiganMindMendinc

---

**Developed by Lyle Perrien II, Michigan MindMend Inc.**
