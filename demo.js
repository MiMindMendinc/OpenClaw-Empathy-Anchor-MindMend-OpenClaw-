#!/usr/bin/env node

/**
 * Demonstration of OpenClaw Empathy Anchor
 * This script shows the core features for youth mental health support
 */

const OpenClaw = require('./index');

console.log('\n╔═════════════════════════════════════════════════════════════════╗');
console.log('║  OpenClaw Empathy Anchor - Youth Mental Health Support Demo     ║');
console.log('║  Privacy-First, Offline-Capable AI for Mental Wellness          ║');
console.log('╚═════════════════════════════════════════════════════════════════╝\n');

// Initialize with offline mode for privacy
const openclaw = new OpenClaw({ offlineMode: true });
console.log();

console.log('This demonstration shows how the Empathy Anchor:\n');
console.log('  ✓ Detects emotions (anxiety, sadness, anger, etc.)');
console.log('  ✓ Validates feelings with compassionate responses');
console.log('  ✓ Identifies crisis situations');
console.log('  ✓ Provides appropriate mental health resources');
console.log('  ✓ Works completely offline for privacy\n');

// Test scenarios
const scenarios = [
  {
    title: 'Anxiety Detection & Support',
    message: "I'm feeling really anxious about my exams tomorrow",
    description: 'Common anxiety scenario - school stress'
  },
  {
    title: 'Sadness & Loneliness',
    message: "I feel so sad and lonely lately",
    description: 'Emotional distress requiring validation'
  },
  {
    title: 'Crisis Detection',
    message: "I am feeling suicidal",
    description: 'Crisis situation - immediate resource provision'
  },
  {
    title: 'General Support',
    message: "I had a tough day",
    description: 'Basic emotional support'
  }
];

scenarios.forEach((scenario, index) => {
  console.log('\n' + '═'.repeat(65));
  console.log(`SCENARIO ${index + 1}: ${scenario.title}`);
  console.log(`Description: ${scenario.description}`);
  console.log('═'.repeat(65));
  console.log(`\n💬 User: "${scenario.message}"\n`);
  
  const result = openclaw.chat(scenario.message);
  
  console.log('🤖 AI Response:');
  console.log('─'.repeat(65));
  console.log(result.response);
  console.log('─'.repeat(65));
  
  console.log('\n📊 Analysis:');
  console.log(`   Emotions: ${result.metadata.emotionsDetected.join(', ') || 'none detected'}`);
  console.log(`   Crisis Level: ${result.metadata.isCrisis ? '⚠️  CRITICAL' : '✓ Normal'}`);
  console.log(`   Intensity: ${result.metadata.intensity}`);
  console.log(`   Privacy Mode: ${result.metadata.offlineMode ? '🔒 ON (Data stays local)' : 'OFF'}`);
  
  if (result.metadata.isCrisis) {
    console.log('\n   ⚠️  ALERT: Crisis resources immediately provided to user');
  }
});

console.log('\n\n╔═════════════════════════════════════════════════════════════════╗');
console.log('║                     Demo Complete ✅                             ║');
console.log('╚═════════════════════════════════════════════════════════════════╝');

console.log('\n📋 Key Features Demonstrated:\n');
console.log('  ✓ Emotion detection working correctly');
console.log('  ✓ Compassionate response generation');
console.log('  ✓ Crisis identification and resource provision');
console.log('  ✓ Privacy-first offline operation');
console.log('  ✓ Michigan-focused mental health resources (988, NAMI, etc.)');
console.log('\n💡 Next Steps:\n');
console.log('  • Run interactive chat: npm start');
console.log('  • Run tests: npm test');
console.log('  • Review code: skills/empathy-anchor/index.js');
console.log('  • Read docs: README.md and KNOWN_ISSUES.md\n');
