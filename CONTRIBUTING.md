# Contributing to OpenClaw Empathy Anchor

Thank you for your interest in contributing to this mental health support project! This guide will help you get started.

## Mission

Our mission is to provide privacy-first, compassionate AI support for youth mental health in Michigan and beyond. All contributions should align with this mission.

## How to Contribute

### 1. Report Issues

Found a bug or have a suggestion?
- Check existing issues first
- Create a new issue with a clear description
- For security issues, email directly (don't create public issues)

### 2. Improve Documentation

Documentation is crucial for mental health tools:
- Fix typos or unclear instructions
- Add examples or use cases
- Translate to other languages
- Update crisis resources

### 3. Enhance the Empathy Anchor Skill

- Improve conversation templates
- Add new response patterns
- Expand crisis detection
- Include more local resources

### 4. Test and Provide Feedback

- Test with different scenarios
- Report edge cases
- Share what works well
- Suggest improvements

## Code of Conduct

This project deals with sensitive topics. We expect all contributors to:

✅ Be respectful and professional
✅ Prioritize user safety and privacy
✅ Avoid judgment or stigma
✅ Follow ethical AI practices
✅ Maintain confidentiality

❌ Never share user conversations
❌ Don't minimize mental health concerns
❌ Avoid making medical claims
❌ Don't promote harmful content

## Development Setup

1. Fork the repository
2. Clone your fork
3. Follow the [SETUP.md](../SETUP.md) guide
4. Create a feature branch
5. Make your changes
6. Test thoroughly
7. Submit a pull request

## Skill Development Guidelines

When modifying the Empathy Anchor skill:

### Required Testing
- Test emotional support responses
- Verify crisis detection
- Check resource provision
- Ensure age-appropriate language
- Validate privacy measures

### Response Quality
Responses should:
- Validate feelings first
- Use clear, simple language
- Avoid jargon or technical terms
- Provide actionable support
- Know when to escalate

### Safety Checks
Before submitting:
- ✅ Crisis situations are handled appropriately
- ✅ Resources are accurate and current
- ✅ Privacy is maintained
- ✅ No harmful advice
- ✅ Professional help is encouraged when needed

## Pull Request Process

1. **Branch Naming**: Use descriptive names
   - `feature/add-local-resources`
   - `fix/crisis-detection`
   - `docs/usage-examples`

2. **Commit Messages**: Be clear and specific
   ```
   Add Owosso community mental health resources
   
   - Added local crisis line
   - Updated youth center contact
   - Included school counselor info
   ```

3. **PR Description**: Include
   - What changed and why
   - How to test
   - Any new dependencies
   - Screenshots if relevant

4. **Review Process**
   - Maintainer will review
   - May request changes
   - Must pass safety review
   - Needs approval before merge

## Priority Contributions

We especially welcome:

### High Priority
- 🔥 Accurate crisis resource updates
- 🔥 Bug fixes affecting safety
- 🔥 Privacy/security improvements

### Medium Priority
- 📚 Documentation improvements
- 🌐 Localization/translation
- 🎨 Example conversations
- 🧪 Test cases

### Low Priority
- ✨ Feature enhancements
- 🎯 Performance optimizations
- 🔧 Code refactoring

## Style Guidelines

### Markdown Files
- Use clear headers
- Include examples
- Keep paragraphs short
- Use bullet points
- Check spelling

### Code
- Follow OpenClaw conventions
- Comment complex logic
- Use meaningful variable names
- Keep functions focused

### Conversation Examples
- Use realistic scenarios
- Show both user and assistant
- Demonstrate best practices
- Include various situations

## Resource Guidelines

When adding or updating crisis resources:

### Required Information
- ✅ Organization name
- ✅ Phone number (verified)
- ✅ Hours of operation
- ✅ Type of support provided
- ✅ Geographic coverage
- ✅ Language support

### Verification
- Call the number to verify it works
- Check the website for accuracy
- Note if 24/7 or limited hours
- Confirm it's free/low-cost

### Format
```json
{
  "resource_name": {
    "name": "988 Suicide & Crisis Lifeline",
    "contact": "Call or text 988",
    "hours": "24/7",
    "type": "crisis",
    "coverage": "national",
    "verified": "2024-02-01"
  }
}
```

## Testing Checklist

Before submitting changes:

- [ ] Tested basic conversations
- [ ] Verified crisis detection
- [ ] Checked resource accuracy
- [ ] Reviewed for harmful content
- [ ] Ensured privacy compliance
- [ ] Validated with different scenarios
- [ ] Checked spelling and grammar
- [ ] Updated documentation if needed

## Questions?

- **General**: Create an issue
- **Security**: Email maintainers
- **OpenClaw**: Visit https://docs.openclaw.ai
- **Community**: Join https://discord.gg/clawd

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Support the Project

- **Try Eve demo**: https://kid-helper-ai.replit.app
- **Donate**: https://gofund.me/42b8334bd
- **Cash App**: https://cash.app/$MichiganMindMendinc

---

**Thank you for helping make mental health support more accessible and compassionate!**

Developed by Lyle Perrien II, Michigan MindMend Inc.
