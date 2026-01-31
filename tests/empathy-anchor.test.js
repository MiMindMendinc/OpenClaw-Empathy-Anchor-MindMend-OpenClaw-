/**
 * Unit tests for Empathy Anchor Skill
 */

const test = require('node:test');
const assert = require('node:assert');
const path = require('path');

// Import the skill
const empathyAnchor = require('../skills/empathy-anchor/index.js');

test('Empathy Anchor Skill - Module Exports', () => {
  assert.ok(empathyAnchor.run, 'run function should be exported');
  assert.ok(empathyAnchor.analyzeEmotionalContent, 'analyzeEmotionalContent should be exported');
  assert.ok(empathyAnchor.isOfflineMode, 'isOfflineMode should be exported');
  assert.ok(empathyAnchor.MICHIGAN_RESOURCES, 'MICHIGAN_RESOURCES should be exported');
});

test('Empathy Anchor Skill - Emotional Content Analysis', async (t) => {
  await t.test('should detect crisis keywords', () => {
    const analysis = empathyAnchor.analyzeEmotionalContent('I want to kill myself');
    assert.strictEqual(analysis.hasCrisis, true, 'should detect crisis');
    assert.strictEqual(analysis.emotionLevel, 'crisis', 'emotion level should be crisis');
    assert.strictEqual(analysis.suggestResources, true, 'should suggest resources');
  });

  await t.test('should detect distress keywords', () => {
    const analysis = empathyAnchor.analyzeEmotionalContent('I feel so anxious and stressed');
    assert.strictEqual(analysis.hasDistress, true, 'should detect distress');
    assert.strictEqual(analysis.emotionLevel, 'distress', 'emotion level should be distress');
    assert.strictEqual(analysis.suggestResources, true, 'should suggest resources');
  });

  await t.test('should handle neutral messages', () => {
    const analysis = empathyAnchor.analyzeEmotionalContent('Hello, how are you?');
    assert.strictEqual(analysis.hasCrisis, false, 'should not detect crisis');
    assert.strictEqual(analysis.hasDistress, false, 'should not detect distress');
    assert.strictEqual(analysis.emotionLevel, 'neutral', 'emotion level should be neutral');
    assert.strictEqual(analysis.suggestResources, false, 'should not suggest resources');
  });

  await t.test('should be case-insensitive', () => {
    const analysis = empathyAnchor.analyzeEmotionalContent('I AM SO ANXIOUS');
    assert.strictEqual(analysis.hasDistress, true, 'should detect distress in uppercase');
  });

  await t.test('should detect multiple distress keywords', () => {
    const analysis = empathyAnchor.analyzeEmotionalContent('I feel sad, lonely, and depressed');
    assert.strictEqual(analysis.hasDistress, true, 'should detect distress with multiple keywords');
  });
});

test('Empathy Anchor Skill - Offline Mode Detection', async (t) => {
  await t.test('should detect offline mode from context.system.offlineMode', () => {
    const context = { system: { offlineMode: true } };
    assert.strictEqual(empathyAnchor.isOfflineMode(context), true);
  });

  await t.test('should detect offline mode from context.system.offline', () => {
    const context = { system: { offline: true } };
    assert.strictEqual(empathyAnchor.isOfflineMode(context), true);
  });

  await t.test('should detect offline mode from context.system.networkStatus', () => {
    const context = { system: { networkStatus: 'offline' } };
    assert.strictEqual(empathyAnchor.isOfflineMode(context), true);
  });

  await t.test('should detect offline mode from environment variable', () => {
    const originalEnv = process.env.OFFLINE_MODE;
    process.env.OFFLINE_MODE = 'true';
    assert.strictEqual(empathyAnchor.isOfflineMode({}), true);
    process.env.OFFLINE_MODE = originalEnv;
  });

  await t.test('should return false when not offline', () => {
    const context = { system: { offlineMode: false } };
    const originalEnv = process.env.OFFLINE_MODE;
    delete process.env.OFFLINE_MODE;
    assert.strictEqual(empathyAnchor.isOfflineMode(context), false);
    process.env.OFFLINE_MODE = originalEnv;
  });
});

test('Empathy Anchor Skill - Validation Generation', () => {
  const validation = empathyAnchor.generateValidation();
  assert.ok(typeof validation === 'string', 'should return a string');
  assert.ok(validation.length > 0, 'validation should not be empty');
});

test('Empathy Anchor Skill - Resource Formatting', async (t) => {
  await t.test('should format crisis resources', () => {
    const resources = empathyAnchor.formatResourceSuggestions('crisis');
    assert.ok(resources.includes('988'), 'should include 988 in crisis resources');
    assert.ok(resources.includes('Immediate Support'), 'should indicate immediate support');
    assert.ok(resources.includes('Crisis Text Line'), 'should include crisis text line');
  });

  await t.test('should format distress resources', () => {
    const resources = empathyAnchor.formatResourceSuggestions('distress');
    assert.ok(resources.includes('988'), 'should include 988 in distress resources');
    assert.ok(resources.includes('NAMI Michigan'), 'should include NAMI Michigan');
    assert.ok(resources.includes('Teen Line'), 'should include Teen Line');
  });

  await t.test('should return empty for neutral', () => {
    const resources = empathyAnchor.formatResourceSuggestions('neutral');
    assert.strictEqual(resources, '', 'should return empty string for neutral');
  });
});

test('Empathy Anchor Skill - Main Run Function', async (t) => {
  await t.test('should handle crisis message', async () => {
    const context = {};
    const params = { message: 'I want to hurt myself' };
    const result = await empathyAnchor.run(context, params);
    
    assert.strictEqual(result.success, true, 'should succeed');
    assert.strictEqual(result.empathyLevel, 'crisis', 'should identify crisis level');
    assert.strictEqual(result.hasResources, true, 'should include resources');
    assert.ok(result.response.includes('988'), 'response should include 988');
  });

  await t.test('should handle distress message', async () => {
    const context = {};
    const params = { message: 'I feel really anxious about school' };
    const result = await empathyAnchor.run(context, params);
    
    assert.strictEqual(result.success, true, 'should succeed');
    assert.strictEqual(result.empathyLevel, 'distress', 'should identify distress level');
    assert.strictEqual(result.hasResources, true, 'should include resources');
    assert.ok(result.response.length > 0, 'should have a response');
  });

  await t.test('should handle neutral message', async () => {
    const context = {};
    const params = { message: 'What is the weather today?' };
    const result = await empathyAnchor.run(context, params);
    
    assert.strictEqual(result.success, true, 'should succeed');
    assert.strictEqual(result.empathyLevel, 'neutral', 'should identify neutral level');
    assert.strictEqual(result.hasResources, false, 'should not include resources');
  });

  await t.test('should handle offline mode', async () => {
    const context = { system: { offlineMode: true } };
    const params = { message: 'I feel sad' };
    const result = await empathyAnchor.run(context, params);
    
    assert.strictEqual(result.success, true, 'should succeed');
    assert.strictEqual(result.offline, true, 'should detect offline mode');
    assert.ok(result.response.includes('Privacy Mode'), 'should mention privacy mode');
  });

  await t.test('should handle empty message', async () => {
    const context = {};
    const params = { message: '' };
    const result = await empathyAnchor.run(context, params);
    
    assert.strictEqual(result.success, true, 'should succeed');
    assert.strictEqual(result.empathyLevel, 'none', 'should have none level');
    assert.strictEqual(result.response, '', 'should have empty response');
  });

  await t.test('should handle message in different param names', async () => {
    const context = {};
    
    // Test with 'text' param
    let result = await empathyAnchor.run(context, { text: 'I feel anxious' });
    assert.strictEqual(result.success, true, 'should succeed with text param');
    assert.ok(result.response.length > 0, 'should have response for text param');
    
    // Test with 'content' param
    result = await empathyAnchor.run(context, { content: 'I feel anxious' });
    assert.strictEqual(result.success, true, 'should succeed with content param');
    assert.ok(result.response.length > 0, 'should have response for content param');
  });

  await t.test('should include metadata in response', async () => {
    const context = {};
    const params = { message: 'I feel anxious' };
    const result = await empathyAnchor.run(context, params);
    
    assert.ok(result.metadata, 'should include metadata');
    assert.strictEqual(result.metadata.triggeredOn, 'all-messages', 'should trigger on all messages');
    assert.ok('privacyMode' in result.metadata, 'should include privacy mode in metadata');
    assert.ok('resourcesShared' in result.metadata, 'should include resourcesShared in metadata');
    assert.ok('emotionLevel' in result.metadata, 'should include emotionLevel in metadata');
  });
});

test('Empathy Anchor Skill - Michigan Resources', () => {
  assert.ok(empathyAnchor.MICHIGAN_RESOURCES.suicide988, 'should have 988 resource');
  assert.ok(empathyAnchor.MICHIGAN_RESOURCES.namiMichigan, 'should have NAMI Michigan resource');
  assert.ok(empathyAnchor.MICHIGAN_RESOURCES.crisisTextLine, 'should have Crisis Text Line resource');
  assert.ok(empathyAnchor.MICHIGAN_RESOURCES.teenLine, 'should have Teen Line resource');
  
  // Verify 988 resource details
  assert.strictEqual(empathyAnchor.MICHIGAN_RESOURCES.suicide988.contact, 'Call or Text 988');
  assert.strictEqual(empathyAnchor.MICHIGAN_RESOURCES.suicide988.availability, '24/7');
  
  // Verify NAMI Michigan resource details
  assert.strictEqual(empathyAnchor.MICHIGAN_RESOURCES.namiMichigan.website, 'https://namimi.org');
  assert.ok(empathyAnchor.MICHIGAN_RESOURCES.namiMichigan.helpline.includes('1-800-950-NAMI'));
});

test('Empathy Anchor Skill - Triggers on All Messages', async () => {
  const context = {};
  const testMessages = [
    'Hello',
    'I need help',
    'What time is it?',
    'I feel anxious',
    '',
    '12345'
  ];
  
  for (const message of testMessages) {
    const result = await empathyAnchor.run(context, { message });
    assert.strictEqual(result.success, true, `should successfully process message: "${message}"`);
  }
});
