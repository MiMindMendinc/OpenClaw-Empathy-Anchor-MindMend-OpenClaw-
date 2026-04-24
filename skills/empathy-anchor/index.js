/**
 * OpenClaw Empathy Anchor
 *
 * A small, privacy-first response layer for youth-support and wellness demos.
 * This module is intentionally offline-capable, deterministic by default, and
 * transparent about safety boundaries. It is not a therapist, medical device,
 * emergency service, or crisis hotline.
 */

const crypto = require('node:crypto');

const MICHIGAN_RESOURCES = Object.freeze({
  suicide988: {
    name: '988 Suicide & Crisis Lifeline',
    contact: 'Call or Text 988',
    availability: '24/7',
    description: 'Free, confidential crisis support in the United States.',
  },
  crisisTextLine: {
    name: 'Crisis Text Line',
    contact: 'Text HOME to 741741',
    availability: '24/7',
    description: 'Free crisis support by text message.',
  },
  namiMichigan: {
    name: 'NAMI Michigan',
    helpline: '1-800-950-NAMI',
    website: 'https://namimi.org',
    description: 'Michigan mental health education, advocacy, and support resources.',
  },
  teenLine: {
    name: 'Teen Line',
    contact: 'Text TEEN to 839863',
    website: 'https://www.teenline.org',
    description: 'Teen-to-teen support and youth mental health resources.',
  },
});

const DEFAULT_RESOURCES = Object.freeze({
  crisis: {
    name: MICHIGAN_RESOURCES.suicide988.name,
    number: MICHIGAN_RESOURCES.suicide988.contact,
    description: MICHIGAN_RESOURCES.suicide988.description,
  },
  text: {
    name: MICHIGAN_RESOURCES.crisisTextLine.name,
    number: MICHIGAN_RESOURCES.crisisTextLine.contact,
    description: MICHIGAN_RESOURCES.crisisTextLine.description,
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
    /\b(suicidal|self\s*harm|hurt\s+myself|cut\s+myself|better\s+off\s+dead|end\s+it\s+all)\b/i,
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

function analyzeEmotionalContent(text) {
  const input = String(text || '');
  const detected = [];

  for (const [emotion, patterns] of Object.entries(EMOTION_PATTERNS)) {
    if (patterns.some((pattern) => pattern.test(input))) {
      detected.push(emotion);
    }
  }

  const hasCrisis = detected.includes('crisis');
  const hasDistress = detected.some((emotion) => emotion !== 'crisis');
  let emotionLevel = 'neutral';

  if (hasCrisis) emotionLevel = 'crisis';
  else if (hasDistress) emotionLevel = 'distress';

  return {
    hasCrisis,
    hasDistress,
    emotions: detected,
    emotionLevel,
    suggestResources: emotionLevel !== 'neutral',
    inputHash: stableHash(input),
  };
}

function isOfflineMode(context = {}) {
  if (process.env.OFFLINE_MODE === 'true') return true;
  if (process.env.MINDMEND_OFFLINE === 'true') return true;

  const system = context.system || {};
  if (system.offlineMode === true) return true;
  if (system.offline === true) return true;
  if (String(system.networkStatus || '').toLowerCase() === 'offline') return true;

  return false;
}

function generateValidation() {
  return 'Your feelings are valid. You deserve support, safety, and a real person you can trust when things feel heavy.';
}

function formatResourceSuggestions(level) {
  if (level === 'crisis') {
    return [
      'Immediate Support:',
      `- ${MICHIGAN_RESOURCES.suicide988.name}: ${MICHIGAN_RESOURCES.suicide988.contact}`,
      `- ${MICHIGAN_RESOURCES.crisisTextLine.name}: ${MICHIGAN_RESOURCES.crisisTextLine.contact}`,
    ].join('\n');
  }

  if (level === 'distress') {
    return [
      'Support Resources:',
      `- ${MICHIGAN_RESOURCES.suicide988.name}: ${MICHIGAN_RESOURCES.suicide988.contact}`,
      `- NAMI Michigan: ${MICHIGAN_RESOURCES.namiMichigan.website} / ${MICHIGAN_RESOURCES.namiMichigan.helpline}`,
      `- Teen Line: ${MICHIGAN_RESOURCES.teenLine.contact}`,
    ].join('\n');
  }

  return '';
}

async function run(context = {}, params = {}) {
  const message = String(params.message ?? params.text ?? params.content ?? '').trim();
  const offline = isOfflineMode(context);

  if (!message) {
    return {
      success: true,
      response: '',
      empathyLevel: 'none',
      hasResources: false,
      offline,
      metadata: {
        triggeredOn: 'all-messages',
        privacyMode: offline,
        resourcesShared: false,
        emotionLevel: 'none',
      },
    };
  }

  const anchor = new EmpathyAnchor({ offlineMode: offline });
  const analysis = analyzeEmotionalContent(message);
  const processed = anchor.process(message);
  const resources = formatResourceSuggestions(analysis.emotionLevel);
  const privacyPrefix = offline ? 'Privacy Mode: local/offline support path active.\n\n' : '';
  const response = `${privacyPrefix}${processed.response}${resources ? `\n\n${resources}` : ''}`;

  return {
    success: true,
    response,
    empathyLevel: analysis.emotionLevel,
    hasResources: Boolean(resources),
    offline,
    metadata: {
      triggeredOn: 'all-messages',
      privacyMode: offline,
      resourcesShared: Boolean(resources),
      emotionLevel: analysis.emotionLevel,
      inputHash: analysis.inputHash,
    },
  };
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

  validateEmotions(text) {
    const input = String(text || '');
    const analysis = analyzeEmotionalContent(input);
    const detected = {
      emotions: analysis.emotions,
      isCrisis: analysis.hasCrisis,
      intensity: 'low',
      inputHash: analysis.inputHash,
    };

    if (analysis.hasCrisis) {
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

  generateSupportiveResponse(emotionData) {
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
module.exports.MICHIGAN_RESOURCES = MICHIGAN_RESOURCES;
module.exports.stableHash = stableHash;
module.exports.analyzeEmotionalContent = analyzeEmotionalContent;
module.exports.isOfflineMode = isOfflineMode;
module.exports.generateValidation = generateValidation;
module.exports.formatResourceSuggestions = formatResourceSuggestions;
module.exports.run = run;
