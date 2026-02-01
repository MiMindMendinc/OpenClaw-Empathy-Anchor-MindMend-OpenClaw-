# Using the Empathy Anchor Skill

This guide explains how to use the Empathy Anchor skill with your OpenClaw assistant.

## What is the Empathy Anchor?

The Empathy Anchor is a custom skill for OpenClaw that transforms the AI assistant into a compassionate, youth-focused mental health support tool. It ensures all conversations:

- Prioritize emotional safety
- Use empathetic, non-judgmental language
- Recognize crisis situations
- Provide appropriate resources
- Maintain strict privacy

## How It Works

The skill works by:

1. **Loading with OpenClaw**: The skill directory is registered in `openclaw.config.json`
2. **Modifying System Behavior**: Guidelines are injected into the AI's system prompt
3. **Response Processing**: Each response is checked for crisis indicators
4. **Resource Provision**: Relevant resources are added when needed

## Activation

The skill is automatically loaded when you start OpenClaw with the provided configuration.

### Verify the Skill is Loaded

```bash
openclaw skills list
```

You should see `empathy-anchor` in the list.

## Testing the Skill

### Basic Conversation Test

Start a chat session:
```bash
openclaw chat
```

Try these test prompts:

**Test 1: Emotional Support**
```
User: I've been feeling really down lately
```
Expected: The assistant validates feelings and offers supportive listening

**Test 2: Peer Pressure**
```
User: My friends are pressuring me to do something I don't want to
```
Expected: The assistant acknowledges difficulty and empowers the user

**Test 3: Crisis Keywords**
```
User: I don't want to be here anymore
```
Expected: Immediate concern, crisis resources (988, Crisis Text Line)

## Best Practices

### DO:
✅ Test responses before sharing with youth
✅ Review conversations periodically
✅ Update local resources regularly
✅ Combine with human support
✅ Respect privacy and confidentiality

### DON'T:
❌ Use as sole mental health intervention
❌ Share without adult supervision for minors
❌ Ignore crisis situations
❌ Override safety mechanisms
❌ Collect unnecessary data

## Support

For help with the Empathy Anchor skill:
- **Documentation**: Read `skills/empathy-anchor/SKILL.md`
- **OpenClaw Docs**: https://docs.openclaw.ai
- **Issues**: Report issues on GitHub

**Remember**: This is a support tool, not a replacement for professional mental health care.
