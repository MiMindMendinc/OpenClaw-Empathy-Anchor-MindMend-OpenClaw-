/**
 * Basic tests for OpenClaw Empathy Anchor
 */

const EmpathyAnchor = require('../skills/empathy-anchor');
const OpenClaw = require('../index');

console.log('Running OpenClaw Empathy Anchor Tests...\n');

let testsPassed = 0;
let testsFailed = 0;

function test(description, testFn) {
  try {
    testFn();
    console.log(`✓ ${description}`);
    testsPassed++;
  } catch (error) {
    console.log(`✗ ${description}`);
    console.log(`  Error: ${error.message}`);
    testsFailed++;
  }
}

function assertEqual(actual, expected, message) {
  if (actual !== expected) {
    throw new Error(`${message}: Expected ${expected}, got ${actual}`);
  }
}

function assertTrue(value, message) {
  if (!value) {
    throw new Error(message);
  }
}

function assertContains(array, value, message) {
  if (!array.includes(value)) {
    throw new Error(`${message}: Array does not contain ${value}`);
  }
}

// Test EmpathyAnchor class
console.log('Testing EmpathyAnchor Class:\n');

test('EmpathyAnchor initializes with default config', () => {
  const anchor = new EmpathyAnchor();
  assertTrue(anchor.config.offlineMode, 'Should default to offline mode');
  assertEqual(anchor.config.crisisHotline, '988', 'Should have 988 hotline');
});

test('Detects anxiety emotions', () => {
  const anchor = new EmpathyAnchor();
  const result = anchor.validateEmotions('I feel really anxious and worried');
  assertContains(result.emotions, 'anxiety', 'Should detect anxiety');
});

test('Detects sadness emotions', () => {
  const anchor = new EmpathyAnchor();
  const result = anchor.validateEmotions('I am so sad and depressed');
  assertContains(result.emotions, 'sadness', 'Should detect sadness');
});

test('Detects crisis situations', () => {
  const anchor = new EmpathyAnchor();
  const result = anchor.validateEmotions('I want to hurt myself');
  assertTrue(result.isCrisis, 'Should detect crisis');
  assertEqual(result.intensity, 'critical', 'Should mark as critical');
});

test('Suggests crisis resources for crisis situations', () => {
  const anchor = new EmpathyAnchor();
  const emotionData = { isCrisis: true, emotions: ['crisis'], intensity: 'critical' };
  const resources = anchor.suggestResources(emotionData);
  assertTrue(resources.length > 0, 'Should suggest resources');
  assertTrue(resources[0].urgent, 'Should mark as urgent');
  assertTrue(resources[0].number.includes('988'), 'Should include 988');
});

test('Wraps response with compassion', () => {
  const anchor = new EmpathyAnchor();
  const wrapped = anchor.wrapWithCompassion('Here is some advice', 'I feel anxious');
  assertTrue(wrapped.includes('Here is some advice'), 'Should include original response');
  assertTrue(wrapped.length > 'Here is some advice'.length, 'Should add compassionate framing');
});

test('Process method returns proper structure', () => {
  const anchor = new EmpathyAnchor();
  const result = anchor.process('I feel worried about tomorrow');
  assertTrue(result.response, 'Should have response');
  assertTrue(result.metadata, 'Should have metadata');
  assertTrue(result.metadata.offlineMode, 'Should indicate offline mode');
  assertTrue(Array.isArray(result.metadata.emotionsDetected), 'Should have emotions array');
});

test('Generates supportive response in offline mode', () => {
  const anchor = new EmpathyAnchor();
  const emotionData = { emotions: ['anxiety'], isCrisis: false, intensity: 'moderate' };
  const response = anchor.generateSupportiveResponse(emotionData);
  assertTrue(response.includes('anxiety'), 'Should mention detected emotion');
  assertTrue(response.length > 0, 'Should generate response');
});

test('isCrisisDetected returns boolean', () => {
  const anchor = new EmpathyAnchor();
  const crisis = anchor.isCrisisDetected('I want to end it all');
  const notCrisis = anchor.isCrisisDetected('I had a good day');
  assertTrue(crisis === true, 'Should detect crisis');
  assertTrue(notCrisis === false, 'Should not detect crisis in normal message');
});

// Test OpenClaw class
console.log('\nTesting OpenClaw Main Class:\n');

test('OpenClaw initializes correctly', () => {
  const openclaw = new OpenClaw();
  assertTrue(openclaw.empathyAnchor, 'Should have empathy anchor');
  assertTrue(openclaw.config.offlineMode, 'Should default to offline');
});

test('OpenClaw chat processes messages', () => {
  const openclaw = new OpenClaw();
  const result = openclaw.chat('I feel sad');
  assertTrue(result.response, 'Should return response');
  assertTrue(result.metadata, 'Should return metadata');
});

test('OpenClaw handles empty input', () => {
  const openclaw = new OpenClaw();
  const result = openclaw.chat('');
  assertTrue(result.metadata.error, 'Should indicate error for empty input');
});

test('OpenClaw checkCrisis works', () => {
  const openclaw = new OpenClaw();
  const crisis = openclaw.checkCrisis('suicide');
  assertTrue(crisis, 'Should detect crisis keyword');
});

test('OpenClaw validateEmotions works', () => {
  const openclaw = new OpenClaw();
  const emotions = openclaw.validateEmotions('I am scared and nervous');
  assertTrue(Array.isArray(emotions.emotions), 'Should return emotions array');
  assertTrue(emotions.emotions.length > 0, 'Should detect emotions');
});

// Summary
console.log('\n' + '='.repeat(50));
console.log('Test Results:');
console.log('='.repeat(50));
console.log(`✓ Passed: ${testsPassed}`);
console.log(`✗ Failed: ${testsFailed}`);
console.log(`Total: ${testsPassed + testsFailed}`);
console.log('='.repeat(50));

if (testsFailed > 0) {
  console.log('\n❌ Some tests failed!');
  process.exit(1);
} else {
  console.log('\n✅ All tests passed!');
  process.exit(0);
}
