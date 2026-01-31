# API Documentation

## OpenClaw Class

The main entry point for the OpenClaw Empathy Anchor application.

### Constructor

```javascript
new OpenClaw(config)
```

**Parameters:**
- `config` (Object, optional)
  - `offlineMode` (Boolean): Enable offline privacy-first mode. Default: `true`
  - `skills` (Array): Additional skills to load. Default: `[]`

**Example:**
```javascript
const OpenClaw = require('./index');
const openclaw = new OpenClaw({ offlineMode: true });
```

### Methods

#### `chat(message, aiResponse)`

Process a user message with empathy anchoring.

**Parameters:**
- `message` (String): User's input message
- `aiResponse` (String, optional): External AI response to wrap with compassion

**Returns:** Object
```javascript
{
  response: String,      // Compassionately wrapped response
  metadata: {
    emotionsDetected: Array,  // List of detected emotions
    isCrisis: Boolean,        // True if crisis detected
    intensity: String,        // 'moderate', 'high', or 'critical'
    offlineMode: Boolean,     // Privacy mode status
    timestamp: String         // ISO timestamp
  }
}
```

**Example:**
```javascript
const result = openclaw.chat("I'm feeling overwhelmed");
console.log(result.response);
console.log(result.metadata.emotionsDetected); // ['overwhelm']
```

#### `checkCrisis(message)`

Check if a message indicates a crisis situation.

**Parameters:**
- `message` (String): User's input message

**Returns:** Boolean - `true` if crisis detected, `false` otherwise

**Example:**
```javascript
if (openclaw.checkCrisis(userMessage)) {
  console.log("Crisis detected - immediate help needed");
}
```

#### `validateEmotions(message)`

Analyze and validate emotions in a message.

**Parameters:**
- `message` (String): User's input message

**Returns:** Object
```javascript
{
  emotions: Array,      // List of detected emotions
  isCrisis: Boolean,    // True if crisis detected
  intensity: String     // 'moderate', 'high', or 'critical'
}
```

**Example:**
```javascript
const emotions = openclaw.validateEmotions("I'm scared and sad");
console.log(emotions.emotions); // ['fear', 'sadness']
```

---

## EmpathyAnchor Class

The core skill for emotion validation and compassionate response generation.

### Constructor

```javascript
new EmpathyAnchor(config)
```

**Parameters:**
- `config` (Object, optional)
  - `offlineMode` (Boolean): Enable offline mode. Default: `true`
  - `compassionLevel` (String): Level of compassion. Default: `'high'`
  - `crisisHotline` (String): Crisis hotline number. Default: `'988'`

**Example:**
```javascript
const EmpathyAnchor = require('./skills/empathy-anchor');
const anchor = new EmpathyAnchor({ offlineMode: true });
```

### Methods

#### `validateEmotions(text)`

Validates and identifies emotions in user input using pattern matching.

**Parameters:**
- `text` (String): User's message to analyze

**Returns:** Object
```javascript
{
  emotions: Array,      // Detected emotions
  isCrisis: Boolean,    // Crisis indicator
  intensity: String     // 'moderate', 'high', or 'critical'
}
```

**Detected Emotion Types:**
- `anxiety`: worried, nervous, scared, stressed, panic
- `sadness`: sad, depressed, lonely, hopeless, empty
- `anger`: angry, mad, frustrated, upset
- `fear`: terrified, frightened, fearful
- `overwhelm`: overwhelmed, too much, can't handle
- `crisis`: suicide, self-harm, want to die (triggers crisis response)

**Example:**
```javascript
const result = anchor.validateEmotions("I'm anxious and scared");
console.log(result);
// { emotions: ['anxiety', 'fear'], isCrisis: false, intensity: 'moderate' }
```

#### `suggestResources(emotionData)`

Suggests appropriate mental health resources based on detected emotions.

**Parameters:**
- `emotionData` (Object): Result from `validateEmotions()`

**Returns:** Array of resource objects
```javascript
[{
  name: String,         // Resource name
  number: String,       // Contact number or text instructions
  description: String,  // Resource description
  urgent: Boolean,      // Only present if crisis
  message: String       // Context message
}]
```

**Available Resources:**
- **988 Suicide & Crisis Lifeline**: For crisis situations (24/7)
- **Crisis Text Line**: Text HOME to 741741 (24/7)
- **The Trevor Project**: LGBTQ+ youth support
- **SAMHSA National Helpline**: General mental health services

**Example:**
```javascript
const emotionData = { isCrisis: true, emotions: ['crisis'], intensity: 'critical' };
const resources = anchor.suggestResources(emotionData);
console.log(resources[0].name); // "988 Suicide & Crisis Lifeline"
```

#### `wrapWithCompassion(originalResponse, userInput)`

Wraps a response with compassionate, empathetic language.

**Parameters:**
- `originalResponse` (String): The response to wrap
- `userInput` (String): User's original message (for emotion detection)

**Returns:** String - Compassionately wrapped response

**Response Structure:**
1. Validating opening statement
2. Emotion acknowledgment (if emotions detected)
3. Original response content
4. Mental health resources (if appropriate)
5. Supportive closing statement

**Example:**
```javascript
const wrapped = anchor.wrapWithCompassion(
  "Take breaks when you need them",
  "I'm feeling overwhelmed"
);
console.log(wrapped);
// Returns multi-paragraph compassionate response
```

#### `process(userInput, aiResponse)`

Main processing method - combines emotion validation with compassionate wrapping.

**Parameters:**
- `userInput` (String): User's message
- `aiResponse` (String, optional): AI response to wrap. If not provided, generates supportive acknowledgment

**Returns:** Object (same structure as `OpenClaw.chat()`)

**Example:**
```javascript
const result = anchor.process("I feel alone");
console.log(result.response);
console.log(result.metadata.emotionsDetected);
```

#### `generateSupportiveResponse(emotionData)`

Generates supportive response when no AI response is available (offline mode).

**Parameters:**
- `emotionData` (Object): Result from `validateEmotions()`

**Returns:** String - Context-appropriate supportive message

**Example:**
```javascript
const emotionData = { emotions: ['anxiety', 'fear'], isCrisis: false };
const response = anchor.generateSupportiveResponse(emotionData);
console.log(response);
// "I understand you're experiencing feelings of anxiety, fear..."
```

#### `isCrisisDetected(text)`

Convenience method to quickly check for crisis indicators.

**Parameters:**
- `text` (String): User's message

**Returns:** Boolean

**Example:**
```javascript
if (anchor.isCrisisDetected(userMessage)) {
  // Immediately show crisis resources
}
```

---

## Configuration Options

### Offline Mode (Privacy-First)

Both classes default to offline mode for maximum privacy:

```javascript
const openclaw = new OpenClaw({ offlineMode: true });
```

**In offline mode:**
- No external API calls
- No data transmission
- All processing happens locally
- Pattern-based emotion detection
- Template-based response generation

### Custom Crisis Hotline

Override the default 988 hotline if needed:

```javascript
const anchor = new EmpathyAnchor({ 
  crisisHotline: '1-800-XXX-XXXX' 
});
```

### Compassion Level

Adjust the level of compassionate framing (future enhancement):

```javascript
const anchor = new EmpathyAnchor({ 
  compassionLevel: 'high' // or 'medium', 'low'
});
```

---

## Integration Examples

### Express.js API

```javascript
const express = require('express');
const OpenClaw = require('./index');

const app = express();
const openclaw = new OpenClaw({ offlineMode: true });

app.use(express.json());

app.post('/chat', (req, res) => {
  const { message } = req.body;
  const result = openclaw.chat(message);
  res.json(result);
});

app.listen(3000, () => {
  console.log('OpenClaw API running on port 3000');
});
```

### Discord Bot

```javascript
const OpenClaw = require('./index');
const openclaw = new OpenClaw({ offlineMode: true });

client.on('messageCreate', async (message) => {
  if (message.author.bot) return;
  
  const result = openclaw.chat(message.content);
  
  if (result.metadata.isCrisis) {
    // Send urgent DM with resources
    await message.author.send('⚠️ Crisis resources: ...');
  }
  
  await message.reply(result.response);
});
```

### CLI Application

See `index.js` for full interactive CLI implementation.

---

## Error Handling

The library handles errors gracefully:

```javascript
const result = openclaw.chat(''); // Empty input
console.log(result.metadata.error); // "Empty input"
console.log(result.response); // "I'm here to listen..."
```

No exceptions are thrown - all edge cases return safe default responses.

---

## Testing

Run the test suite:

```bash
npm test
```

Test coverage includes:
- Emotion detection for all categories
- Crisis detection and resource suggestions
- Compassionate wrapping
- Offline mode functionality
- Edge cases (empty input, no emotions, etc.)

---

## License

MIT License - See LICENSE file for details.

---

## Support

For issues, questions, or contributions:
- GitHub Issues: https://github.com/MiMindMendinc/OpenClaw-Empathy-Anchor-MindMend-OpenClaw-/issues
- Discussions: https://github.com/MiMindMendinc/OpenClaw-Empathy-Anchor-MindMend-OpenClaw-/discussions
