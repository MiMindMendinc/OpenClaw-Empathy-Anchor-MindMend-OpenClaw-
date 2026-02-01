/**
 * OpenClaw Empathy Anchor - Main Entry Point
 * Privacy-first, offline-capable AI for youth mental health support
 */

const EmpathyAnchor = require('./skills/empathy-anchor');

/**
 * OpenClaw class - Main application interface
 */
class OpenClaw {
  constructor(config = {}) {
    this.config = {
      offlineMode: config.offlineMode !== false, // Default to offline for privacy
      skills: config.skills || [],
      ...config
    };

    // Initialize empathy anchor skill
    this.empathyAnchor = new EmpathyAnchor({
      offlineMode: this.config.offlineMode
    });

    console.log('🔒 OpenClaw Empathy Anchor initialized');
    console.log(`📴 Offline mode: ${this.config.offlineMode ? 'ENABLED (Privacy-first)' : 'Disabled'}`);
  }

  /**
   * Process user message with empathy anchoring
   * @param {string} message - User's message
   * @param {string} aiResponse - Optional AI response to wrap
   * @returns {object} Processed response
   */
  chat(message, aiResponse = null) {
    if (!message || message.trim() === '') {
      return {
        response: `I'm here to listen. Please share what's on your mind.`,
        metadata: { error: 'Empty input' }
      };
    }

    // Process through empathy anchor
    const result = this.empathyAnchor.process(message, aiResponse);

    return result;
  }

  /**
   * Check for crisis indicators in message
   * @param {string} message - User's message
   * @returns {boolean} True if crisis detected
   */
  checkCrisis(message) {
    return this.empathyAnchor.isCrisisDetected(message);
  }

  /**
   * Validate emotions in message
   * @param {string} message - User's message
   * @returns {object} Emotion validation data
   */
  validateEmotions(message) {
    return this.empathyAnchor.validateEmotions(message);
  }
}

// Export for use in other modules
module.exports = OpenClaw;

// CLI interface if run directly
if (require.main === module) {
  const readline = require('readline');
  
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  const openclaw = new OpenClaw({ offlineMode: true });

  console.log('\n╔═══════════════════════════════════════════════════════════╗');
  console.log('║     OpenClaw Empathy Anchor - Youth Mental Health Support  ║');
  console.log('║              Privacy-First Offline AI                      ║');
  console.log('╚═══════════════════════════════════════════════════════════╝\n');
  console.log('💙 I\'m here to listen and support you.');
  console.log('🔒 All conversations stay private on your device.\n');
  console.log('Type "exit" to quit.\n');

  const promptUser = () => {
    rl.question('You: ', (input) => {
      if (input.toLowerCase() === 'exit') {
        console.log('\n💙 Take care of yourself. Remember, you\'re not alone.\n');
        rl.close();
        return;
      }

      const result = openclaw.chat(input);
      console.log(`\nOpenClaw: ${result.response}\n`);
      
      if (result.metadata.isCrisis) {
        console.log('⚠️  CRISIS ALERT: Please reach out to the resources mentioned above immediately.\n');
      }

      promptUser();
    });
  };

  promptUser();
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
