# Known Issues and Resolutions

## Node.js Version Requirements

### Issue
The project requires **Node.js 22.0.0 or higher** due to the OpenClaw dependency requirements.

### Resolution
- Update to Node.js 22.0.0 or higher from [nodejs.org](https://nodejs.org/)
- The package.json now correctly specifies `"node": ">=22.0.0"` in the engines field

### What Works
- **Basic functionality** (`npm start`, `npm test`): Empathy-anchor core features
- **OpenClaw CLI commands** (`npm run setup`, `npm run dev`, `npm run install-openclaw`): Full OpenClaw integration

## Security Warnings During Installation

### Issue
npm install shows security warnings about vulnerabilities in transitive dependencies:
```
4 high severity vulnerabilities
```

These warnings come from:
- `openclaw` → `node-llama-cpp` → `cmake-js` → `tar`

### Resolution
**No action required for core functionality.** 

These vulnerabilities exist in the OpenClaw package's deep dependency chain and do not affect the empathy-anchor skill, which:
- Uses only Node.js built-in modules (`readline`, etc.)
- Operates completely independently of the vulnerable packages
- Does not use cmake-js, node-llama-cpp, or tar directly

The empathy-anchor skill's core features (emotion detection, crisis detection, compassionate response generation) work perfectly without these dependencies.

### If You Need to Use OpenClaw CLI
If you need the full OpenClaw CLI functionality and want to address the security warnings, you would need to wait for the OpenClaw maintainers to update their dependencies. However, for the youth mental health support features of this project, the warnings can be safely ignored.

## Script Functionality

### What Works ✅
- `npm install` - Installs all dependencies successfully
- `npm test` - All 14 tests pass
- `npm start` - Interactive empathy-anchor chat works perfectly

### What Requires Node 22+ ⚠️
- `npm run install-openclaw` - Installs OpenClaw CLI globally
- `npm run setup` - OpenClaw onboarding wizard
- `npm run dev` - OpenClaw development mode

## Summary

**For Youth Mental Health Support (Primary Use Case):**
- ✅ All core features work perfectly
- ✅ No security concerns for standalone empathy-anchor usage
- ✅ Ready to demonstrate and use

**For Full OpenClaw Integration (Advanced Use Case):**
- ⚠️ Requires Node.js 22.0.0+
- ⚠️ Security warnings in dependencies (can be safely ignored for this use case)
- ⚠️ CLI commands require proper Node version

## Recommendations

1. **For basic usage**: Use `npm start` to run the empathy-anchor chat interface
2. **For testing**: Use `npm test` to verify all functionality
3. **For Node version**: Ensure you have Node.js 22.0.0 or higher installed
4. **For security warnings**: Safe to ignore for empathy-anchor standalone usage
