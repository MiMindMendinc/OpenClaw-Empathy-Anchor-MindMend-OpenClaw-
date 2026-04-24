/**
 * OpenClaw Empathy Anchor
 *
 * A small, privacy-first response layer for youth-support and wellness demos.
 * This module is intentionally offline-capable, deterministic by default, and
 * transparent about safety boundaries. It is not a therapist, medical device,
 * emergency service, or crisis hotline.
 */

const crypto = require('node:crypto');

const DEFAULT_RESOURCES = Object.freeze({
  crisis: {
    name: '988 Suicide & Crisis Lifeline',
    number: 'Call or text 988',
    description: 'Free, confidential support 24/7 in the United States.',
  },
  text: {
    name: 'Crisis Text Line',
    number: 'Text HOME to 741741',
    description: 'Free, 24/7 crisis support by text.',
  },
  general: {
    name: 'SAMHSA National Helpline',
    number: '1-800-662-4357',
    description: 'Mental health and substance-use support referrals.',
  },
});

const EMOTION_PATTERNS = Object.freeze({
  anxiety: [/\b(anxious|worried|nervous|panic|stressed?|afraid)\b/i],
  sadness: [/\b(sad|depressed|down|hopeless|lonely|empty)\b/i],
  anger: [/\b(angry|mad|frustrated|furious|upset)\b/i],
  fear: [/\b(terrified|frightened|scared|unsafe)\b/i],
  overwhelm: [/\b(overwhelmed|too much|cannot handle|can't handle|drowning|stuck)\b/i],
  bullying: [/\b(bullied|bullying|harassed|picked on|threatened)\b/i],
  crisis: [
    /\b(i\s+want\s+to\s+die|kill\s+myself|end\s+my\s+life|take\s+my\s+life)\b/i,
    /\b(suicidal|self\s*harm|hurt\s+myself|cut\s+myself|better\s+off\s+dead)\b/i,
  ],
});

const RESPONSE_FRAMES = Object.freeze({
  opening: [
    "I hear you, and what you're feeling matters.",
    "Thank you for trusting me with that.",
    "I'm here with you, and you do not have to carry this alone.",
    "That sounds heavy. I'm glad you said something.",
  ],
  validation: [
    "Your emotions are real, and they deserve care.",
    "It makes sense to want support when things feel this hard.",
    "You deserve patience, safety, and help from people you trust.",
    "This moment matters, and so do you.",
  ],
  grounding: [
    'Take one slow breath in and one slow breath out.',
    'Name five things you can see around you.',
    'Put both feet on the floor and notice the room you are in.',
    'Try to move closer to a safe, trusted person if you can.',
  ],
});

function stableHash(value) {
  return crypto.createHash('sha256').update(String(value || '')).digest('hex');
}

function pickDeterministic(items, seed) {
  const hash = stableHash(seed);
  const index = Number.parseInt(hash.slice(0, 8), 16) % items.length;
  return items[index];
}

class EmpathyAnchor {
  constructor(config = {}) {
    this.config = {
      offlineMode: config.offlineMode !== false,
      crisisHotline: config.crisisHotline || '988',
      storeRawText: config.storeRawText === true,
      includeResources: config.includeResources !== false,
      ...config,
    };

    this.resources = {
      ...DEFAULT_RESOURCES,
      ...(config.resources || {}),
    };
  }

  /**
   * Identify broad emotional/safety signals in user text.
   * This is rules-based support logic, not diagnosis.
   */
  validateEmotions(text) {
    const input = String(text || '');
    const detected = {
      emotions: [],
      isCrisis: false,
      intensity: 'low',
      inputHash: stableHash(input),
    };

    for (const [emotion, patterns] of Object.entries(EMOTION_PATTERNS)) {
      if (patterns.some((pattern) => pattern.test(input))) {
        detected.emotions.push(emotion);
      }
    }

    detected.isCrisis = detected.emotions.includes('crisis');

    if (detected.isCrisis) {
      detected.intensity = 'critical';
    } else if (detected.emotions.includes('bullying') || detected.emotions.length >= 3) {
      detected.intensity = 'high';
    } else if (detected.emotions.length > 0) {
      detected.intensity = 'moderate';
    }

    return detected;
  }

  suggestResources(emotionData) {
    if (!this.config.includeResources) return [];

    if (emotionData.isCrisis) {
      return [
        {
          ...this.resources.crisis,
          urgent: true,
          message: "If you might hurt yourself or someone else, contact a real person immediately:",
        },
        this.resources.text,
      ];
    }

    if (emotionData.intensity === 'high') {
      return [
        {
          ...this.resources.crisis,
          urgent: false,
          message: 'If this becomes urgent or unsafe, support is available 24/7:',
        },
        this.resources.general,
      ];
    }

    return [];
  }

  generateSupportiveResponse(emotionData, userInput = '') {
    if (emotionData.isCrisis) {
      return (
        'Your life has value, and this needs support from a real person right now. ' +
        'Please call/text 988, contact emergency services, or move near a trusted adult immediately.'
      );
    }

    if (emotionData.intensity === 'high') {
      return (
        'This sounds serious, and you should not have to handle it alone. ' +
        'Please consider telling a trusted adult, counselor, caregiver, or local support person.'
      );
    }

    if (emotionData.emotions.length > 0) {
      return (
        `I noticed signals of ${emotionData.emotions.join(', ')}. ` +
        'A small grounding step may help while you decide who you can talk to next.'
      );
    }

    return "I'm here to listen. You can share more at your own pace.";
  }

  wrapWithCompassion(originalResponse, userInput) {
    const emotionData = this.validateEmotions(userInput);
    const seed = `${userInput}:${originalResponse}`;
    const opening = pickDeterministic(RESPONSE_FRAMES.opening, `${seed}:opening`);
    const validation = pickDeterministic(RESPONSE_FRAMES.validation, `${seed}:validation`);
    const grounding = pickDeterministic(RESPONSE_FRAMES.grounding, `${seed}:grounding`);

    const sections = [opening];

    if (emotionData.emotions.length > 0) {
      sections.push(validation);
    }

    sections.push(originalResponse);

    if (!emotionData.isCrisis) {
      sections.push(`Grounding step: ${grounding}`);
    }

    const resources = this.suggestResources(emotionData);
    if (resources.length > 0) {
      const resourceText = resources
        .map((resource) => {
          const prefix = resource.message ? `${resource.message}\n` : '';
          return `${prefix}- ${resource.name}: ${resource.number}\n  ${resource.description}`;
        })
        .join('\n\n');
      sections.push(`Resources for support:\n\n${resourceText}`);
    }

    sections.push('Reminder: this tool is supportive software, not a replacement for a trusted adult, clinician, crisis worker, or emergency services.');

    return sections.join('\n\n');
  }

  process(userInput, aiResponse = null) {
    const input = String(userInput || '').trim();

    if (!input) {
      return {
        response: "I'm here to listen. Please share what's on your mind when you're ready.",
        metadata: {
          error: 'empty_input',
          offlineMode: this.config.offlineMode,
          timestamp: new Date().toISOString(),
        },
      };
    }

    const emotionData = this.validateEmotions(input);
    const baseResponse = aiResponse || this.generateSupportiveResponse(emotionData, input);

    return {
      response: this.wrapWithCompassion(baseResponse, input),
      metadata: {
        emotionsDetected: emotionData.emotions,
        isCrisis: emotionData.isCrisis,
        intensity: emotionData.intensity,
        inputHash: emotionData.inputHash,
        rawInput: this.config.storeRawText ? input : undefined,
        offlineMode: this.config.offlineMode,
        timestamp: new Date().toISOString(),
      },
    };
  }

  isCrisisDetected(text) {
    return this.validateEmotions(text).isCrisis;
  }
}

module.exports = EmpathyAnchor;
module.exports.DEFAULT_RESOURCES = DEFAULT_RESOURCES;
module.exports.EMOTION_PATTERNS = EMOTION_PATTERNS;
module.exports.RESPONSE_FRAMES = RESPONSE_FRAMES;
module.exports.stableHash = stableHash;
