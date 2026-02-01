#!/usr/bin/env node

/**
 * OpenClaw Empathy Anchor - MindMend Integration
 * 
 * This is a wrapper around OpenClaw that integrates the empathy-anchor skill
 * for ethical, offline AI supporting youth mental health and safety.
 */

import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

console.log(`
╔═══════════════════════════════════════════════════════════════╗
║  OpenClaw Empathy Anchor - Michigan MindMend Inc.            ║
║  Privacy-first AI for youth mental health support            ║
╚═══════════════════════════════════════════════════════════════╝

Setting up OpenClaw with empathy-anchor skill...

Skills directory: ${join(__dirname, 'skills')}

To get started:
1. Run: npm run setup (to configure OpenClaw)
2. Run: npm start (to start the assistant)

For empathy-anchor skill configuration, see skills/empathy-anchor/SKILL.md
`);

// Import and run OpenClaw
try {
  const openclaw = await import('openclaw');
  console.log('OpenClaw loaded successfully!');
  console.log('\nRun "openclaw onboard" to set up your assistant.');
} catch (error) {
  console.error('Error loading OpenClaw:', error.message);
  console.log('\nPlease install OpenClaw first:');
  console.log('  npm run install-openclaw');
  process.exit(1);
}
