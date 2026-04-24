'use strict';

const assert = require('node:assert/strict');
const test = require('node:test');

const EmpathyAnchor = require('../skills/empathy-anchor');
const OpenClaw = require('../index');

test('EmpathyAnchor initializes in offline mode by default', () => {
  const anchor = new EmpathyAnchor();

  assert.equal(anchor.config.offlineMode, true);
  assert.equal(anchor.config.crisisHotline, '988');
});

test('validateEmotions detects anxiety signals', () => {
  const anchor = new EmpathyAnchor();
  const result = anchor.validateEmotions('I feel really anxious and worried.');

  assert.equal(result.emotions.includes('anxiety'), true);
  assert.equal(result.isCrisis, false);
  assert.equal(result.intensity, 'moderate');
});

test('validateEmotions detects crisis language', () => {
  const anchor = new EmpathyAnchor();
  const result = anchor.validateEmotions('I want to die and I need help.');

  assert.equal(result.emotions.includes('crisis'), true);
  assert.equal(result.isCrisis, true);
  assert.equal(result.intensity, 'critical');
});

test('suggestResources includes urgent resources for crisis language', () => {
  const anchor = new EmpathyAnchor();
  const emotionData = anchor.validateEmotions('I want to hurt myself.');
  const resources = anchor.suggestResources(emotionData);

  assert.equal(resources.length >= 2, true);
  assert.equal(resources[0].urgent, true);
  assert.equal(resources.some((resource) => resource.number.includes('988')), true);
});

test('process returns metadata without raw input by default', () => {
  const anchor = new EmpathyAnchor();
  const result = anchor.process('I feel sad today.');

  assert.equal(typeof result.response, 'string');
  assert.equal(result.metadata.rawInput, undefined);
  assert.equal(typeof result.metadata.inputHash, 'string');
  assert.equal(result.metadata.emotionsDetected.includes('sadness'), true);
});

test('process can store raw input only when explicitly configured', () => {
  const anchor = new EmpathyAnchor({ storeRawText: true });
  const result = anchor.process('I feel sad today.');

  assert.equal(result.metadata.rawInput, 'I feel sad today.');
});

test('wrapWithCompassion is deterministic for the same input', () => {
  const anchor = new EmpathyAnchor();
  const first = anchor.wrapWithCompassion('Base response.', 'I feel anxious.');
  const second = anchor.wrapWithCompassion('Base response.', 'I feel anxious.');

  assert.equal(first, second);
});

test('OpenClaw chat processes messages', () => {
  const openclaw = new OpenClaw();
  const result = openclaw.chat('I feel overwhelmed.');

  assert.equal(typeof result.response, 'string');
  assert.equal(result.metadata.emotionsDetected.includes('overwhelm'), true);
});

test('OpenClaw handles empty input safely', () => {
  const openclaw = new OpenClaw();
  const result = openclaw.chat('');

  assert.equal(result.metadata.error, 'empty_input');
});

test('OpenClaw crisis check returns true for crisis language', () => {
  const openclaw = new OpenClaw();

  assert.equal(openclaw.checkCrisis('I want to end my life.'), true);
  assert.equal(openclaw.checkCrisis('I had a good day.'), false);
});
