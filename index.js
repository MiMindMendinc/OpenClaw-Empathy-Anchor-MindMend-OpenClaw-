/**
 * MindMend Empathy Anchor — Node entry point
 * Privacy-first, offline-capable response layer for youth-support demos.
 *
 * Compatibility: the exported class name `OpenClaw` is retained as an alias
 * so existing require('./index') demos keep working. Public product name is
 * MindMend Empathy Anchor.
 */

const readline = require('node:readline');
const EmpathyAnchor = require('./skills/empathy-anchor');

class MindMendEmpathyAnchor {
  constructor(config = {}) {
    this.config = {
      offlineMode: config.offlineMode !== false,
      ...config,
    };

    this.empathyAnchor = new EmpathyAnchor({
      offlineMode: this.config.offlineMode,
      storeRawText: this.config.storeRawText === true,
      includeResources: this.config.includeResources !== false,
    });
  }

  chat(message, aiResponse = null) {
    return this.empathyAnchor.process(message, aiResponse);
  }

  checkCrisis(message) {
    return this.empathyAnchor.isCrisisDetected(message);
  }

  validateEmotions(message) {
    return this.empathyAnchor.validateEmotions(message);
  }
}

// Compatibility alias for existing demos/tests
const OpenClaw = MindMendEmpathyAnchor;

function printBanner(app) {
  console.log('\nMindMend Empathy Anchor');
  console.log('Local-first safety signal / supportive response layer');
  console.log(`Offline mode: ${app.config.offlineMode ? 'enabled' : 'disabled'}`);
  console.log('Type "exit" to quit.\n');
}

function startCli() {
  const app = new MindMendEmpathyAnchor({ offlineMode: true });
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });

  printBanner(app);

  const promptUser = () => {
    rl.question('You: ', (input) => {
      if (input.trim().toLowerCase() === 'exit') {
        console.log('\nTake care. You matter, and real support is worth reaching for when things feel heavy.\n');
        rl.close();
        return;
      }

      const result = app.chat(input);
      console.log(`\nMindMend:\n${result.response}\n`);

      if (result.metadata.isCrisis) {
        console.log('Safety note: crisis language detected. Please contact a real person or emergency resource now.\n');
      }

      promptUser();
    });
  };

  promptUser();
}

module.exports = OpenClaw;
module.exports.MindMendEmpathyAnchor = MindMendEmpathyAnchor;
module.exports.OpenClaw = OpenClaw;

if (require.main === module) {
  startCli();
}
