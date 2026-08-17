/**
 * MindMend Empathy Anchor — Node skill examples
 */

const { MindMendEmpathyAnchor } = require('../index');

console.log('MindMend Empathy Anchor — examples\n');

const app = new MindMendEmpathyAnchor({ offlineMode: true });

const examples = [
  { title: 'Anxiety', input: "I'm feeling really anxious about school tomorrow." },
  { title: 'Sadness', input: 'I feel so lonely and sad. Nobody understands me.' },
  { title: 'Overwhelm', input: "Everything feels like too much. I can't handle all this stress." },
  { title: 'Crisis language', input: "I don't see the point anymore. I just want it all to end." },
];

for (const example of examples) {
  console.log('='.repeat(60));
  console.log(example.title);
  console.log(`User: "${example.input}"\n`);
  const result = app.chat(example.input);
  console.log(result.response);
  console.log('\nEmotions:', (result.metadata.emotionsDetected || []).join(', ') || 'none');
  console.log('Crisis:', result.metadata.isCrisis ? 'yes' : 'no');
  console.log();
}

console.log('Live API showcase: make demo');
