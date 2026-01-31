# Quick Start Guide

## Running OpenClaw Empathy Anchor

### Option 1: Interactive Chat Mode
Start a conversation with the empathy-anchored AI:

```bash
npm start
```

Example interaction:
```
You: I'm feeling really stressed about my exams
OpenClaw: [Compassionate response with emotion validation and resources]
```

Type `exit` to quit.

### Option 2: Run Demo Examples
See 5 example scenarios demonstrating different emotional states and crisis detection:

```bash
npm run demo
```

### Option 3: Run Tests
Validate all functionality works correctly:

```bash
npm test
```

### Option 4: Use as a Library
Integrate into your own Node.js application:

```javascript
const OpenClaw = require('./index');
const openclaw = new OpenClaw({ offlineMode: true });

const result = openclaw.chat("I'm having a hard day");
console.log(result.response);
```

## Key Features

✅ **100% Offline** - No internet required, complete privacy  
✅ **Emotion Detection** - Recognizes anxiety, sadness, anger, fear, overwhelm  
✅ **Crisis Detection** - Immediately identifies crisis situations  
✅ **Resource Integration** - Suggests 988 and other appropriate resources  
✅ **Youth-Focused** - Language and support tailored for young people  
✅ **Zero Dependencies** - Pure Node.js, no external packages needed  

## Privacy Guarantee

- ✅ All processing happens locally on your device
- ✅ No data is sent to external servers
- ✅ No tracking or analytics
- ✅ Complete user control and ownership of conversations

## Emergency Resources

**If you're in crisis:**
- Call or text **988** (24/7 Suicide & Crisis Lifeline)
- Text **HOME to 741741** (Crisis Text Line)
- Call **911** or visit nearest emergency room

---

For more details, see [README.md](README.md)
