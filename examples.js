/**
 * Example usage of the Empathy Anchor Skill
 * 
 * This file demonstrates how to use the empathy-anchor skill
 * in different scenarios.
 */

const empathyAnchor = require('./skills/empathy-anchor/index.js');

/**
 * Example 1: Crisis message
 */
async function exampleCrisis() {
  console.log('\n=== Example 1: Crisis Message ===');
  
  const context = {};
  const params = { message: 'I feel like I want to hurt myself' };
  
  const result = await empathyAnchor.run(context, params);
  
  console.log('Input:', params.message);
  console.log('Empathy Level:', result.empathyLevel);
  console.log('Response:', result.response);
}

/**
 * Example 2: Distress message
 */
async function exampleDistress() {
  console.log('\n=== Example 2: Distress Message ===');
  
  const context = {};
  const params = { message: 'I am feeling really anxious about school tomorrow' };
  
  const result = await empathyAnchor.run(context, params);
  
  console.log('Input:', params.message);
  console.log('Empathy Level:', result.empathyLevel);
  console.log('Response:', result.response);
}

/**
 * Example 3: Neutral message
 */
async function exampleNeutral() {
  console.log('\n=== Example 3: Neutral Message ===');
  
  const context = {};
  const params = { message: 'What is the weather like today?' };
  
  const result = await empathyAnchor.run(context, params);
  
  console.log('Input:', params.message);
  console.log('Empathy Level:', result.empathyLevel);
  console.log('Response:', result.response || '(No empathy response needed)');
}

/**
 * Example 4: Offline mode
 */
async function exampleOffline() {
  console.log('\n=== Example 4: Offline Mode with Distress ===');
  
  const context = { 
    system: { 
      offlineMode: true 
    } 
  };
  const params = { message: 'I feel so lonely and sad' };
  
  const result = await empathyAnchor.run(context, params);
  
  console.log('Input:', params.message);
  console.log('Offline Mode:', result.offline);
  console.log('Empathy Level:', result.empathyLevel);
  console.log('Response:', result.response);
}

/**
 * Example 5: Multiple messages (triggers on all)
 */
async function exampleMultiple() {
  console.log('\n=== Example 5: Multiple Messages ===');
  
  const messages = [
    'Hello!',
    'I am worried about my grades',
    'Can you help me with homework?',
    'I feel really stressed'
  ];
  
  const context = {};
  
  for (const message of messages) {
    const result = await empathyAnchor.run(context, { message });
    console.log(`\nInput: "${message}"`);
    console.log(`Level: ${result.empathyLevel}, Has Resources: ${result.hasResources}`);
    if (result.response) {
      console.log(`Response: ${result.response.substring(0, 100)}...`);
    }
  }
}

/**
 * Run all examples
 */
async function runExamples() {
  console.log('╔════════════════════════════════════════════════════════╗');
  console.log('║   Empathy Anchor Skill - Usage Examples               ║');
  console.log('╚════════════════════════════════════════════════════════╝');
  
  await exampleCrisis();
  await exampleDistress();
  await exampleNeutral();
  await exampleOffline();
  await exampleMultiple();
  
  console.log('\n=== Examples Complete ===\n');
}

// Run if called directly
if (require.main === module) {
  runExamples().catch(console.error);
}

module.exports = { runExamples };
