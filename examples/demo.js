/**
 * OpenClaw Empathy Anchor - Demo Examples
 * Demonstrates the empathy-anchor skill capabilities
 */

const OpenClaw = require('../index');

console.log('╔═══════════════════════════════════════════════════════════╗');
console.log('║        OpenClaw Empathy Anchor - Demo Examples            ║');
console.log('╚═══════════════════════════════════════════════════════════╝\n');

// Initialize OpenClaw with offline mode for privacy
const openclaw = new OpenClaw({ offlineMode: true });

// Example scenarios
const examples = [
  {
    title: 'Example 1: General Anxiety',
    input: 'I\'m feeling really anxious about school tomorrow.'
  },
  {
    title: 'Example 2: Sadness and Loneliness',
    input: 'I feel so lonely and sad. Nobody understands me.'
  },
  {
    title: 'Example 3: Overwhelm',
    input: 'Everything feels like too much. I can\'t handle all this stress.'
  },
  {
    title: 'Example 4: Crisis Detection',
    input: 'I don\'t see the point anymore. I just want it all to end.'
  },
  {
    title: 'Example 5: Mixed Emotions',
    input: 'I\'m angry at myself, scared of failing, and just feeling hopeless.'
  }
];

// Run through examples
examples.forEach((example, index) => {
  console.log(`\n${'='.repeat(60)}`);
  console.log(`${example.title}`);
  console.log(`${'='.repeat(60)}\n`);
  
  console.log(`User Input: "${example.input}"\n`);
  
  // Process with empathy anchor
  const result = openclaw.chat(example.input);
  
  console.log('Response:');
  console.log(result.response);
  
  console.log('\nMetadata:');
  console.log(`- Emotions Detected: ${result.metadata.emotionsDetected.join(', ') || 'none'}`);
  console.log(`- Crisis Alert: ${result.metadata.isCrisis ? 'YES ⚠️' : 'No'}`);
  console.log(`- Intensity: ${result.metadata.intensity}`);
  console.log(`- Privacy Mode: ${result.metadata.offlineMode ? 'ENABLED 🔒' : 'Disabled'}`);
  
  if (index < examples.length - 1) {
    console.log('\n');
  }
});

console.log('\n\n╔═══════════════════════════════════════════════════════════╗');
console.log('║                    Demo Complete                          ║');
console.log('╚═══════════════════════════════════════════════════════════╝\n');

console.log('💡 Key Features Demonstrated:');
console.log('   ✓ Emotion validation and detection');
console.log('   ✓ Compassionate language wrapping');
console.log('   ✓ Crisis detection and immediate resource suggestions');
console.log('   ✓ Privacy-first offline mode');
console.log('   ✓ Youth-focused mental health support');
console.log('   ✓ 988 and other resource integration\n');

console.log('📚 To run this demo: npm run demo');
console.log('💻 To start interactive mode: npm start\n');
