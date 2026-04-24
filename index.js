/**
 * OpenClaw Empathy Anchor - Main Entry Point
 * Privacy-first, offline-capable response layer for youth-support AI demos.
 */

const readline = require('node:readline');
const EmpathyAnchor = require('./skills/empathy-anchor');

class OpenClaw {
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

function printBanner(openclaw) {
  console.log('\nOpenClaw Empathy Anchor');
  console.log('Privacy-first offline youth-support response layer');
  console.log(`Offline mode: ${openclaw.config.offlineMode ? 'enabled' : 'disabled'}`);
  console.log('Type "exit" to quit.\n');
}

function startCli() {
  const openclaw = new OpenClaw({ offlineMode: true });
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });

  printBanner(openclaw);

  const promptUser = () => {
    rl.question('You: ', (input) => {
      if (input.trim().toLowerCase() === 'exit') {
        console.log('\nTake care. You matter, and real support is worth reaching for when things feel heavy.\n');
        rl.close();
        return;
      }

      const result = openclaw.chat(input);
      console.log(`\nOpenClaw:\n${result.response}\n`);

      if (result.metadata.isCrisis) {
        console.log('Safety note: crisis language detected. Please contact a real person or emergency resource now.\n');
      }

      promptUser();
    });
  };

  promptUser();
}

module.exports = OpenClaw;

if (require.main === module) {
  startCli();
}
