#!/usr/bin/env node

/**
 * Demonstration of MindMend Empathy Anchor (Node skill).
 */

const { MindMendEmpathyAnchor } = require('./index');

console.log('\nMindMend Empathy Anchor — Node skill demonstration');
console.log('Technical demonstration. Not clinical software. Not 988/911.\n');

const app = new MindMendEmpathyAnchor({ offlineMode: true });

const scenarios = [
  {
    title: 'Anxiety',
    message: "I'm feeling really anxious about my exams tomorrow",
  },
  {
    title: 'Sadness',
    message: 'I feel so sad and lonely lately',
  },
  {
    title: 'Crisis language',
    message: 'I am feeling suicidal',
  },
  {
    title: 'Neutral',
    message: 'I had a tough day',
  },
];

for (const scenario of scenarios) {
  console.log('='.repeat(64));
  console.log(scenario.title);
  console.log(`User: "${scenario.message}"\n`);
  const result = app.chat(scenario.message);
  console.log(result.response);
  console.log('\nEmotions:', (result.metadata.emotionsDetected || []).join(', ') || 'none');
  console.log('Crisis:', result.metadata.isCrisis ? 'yes' : 'no');
  console.log('Intensity:', result.metadata.intensity);
  console.log();
}

console.log('Interactive CLI: npm start');
console.log('Tests: npm test');
console.log('Live API showcase: make demo\n');
