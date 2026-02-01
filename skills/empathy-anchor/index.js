/**
 * Empathy Anchor Skill for OpenClaw
 * Privacy-first, offline-capable AI skill for youth mental health support
 * 
 * This skill wraps all responses in compassionate language and provides
 * emotion validation and mental health resource suggestions.
 */

class EmpathyAnchor {
  constructor(config = {}) {
    this.config = {
      offlineMode: config.offlineMode !== false, // Default to offline for privacy
      compassionLevel: config.compassionLevel || 'high',
      crisisHotline: config.crisisHotline || '988', // 988 Suicide & Crisis Lifeline
      ...config
    };

    // Emotion validation patterns
    this.emotionPatterns = {
      anxiety: ['anxious', 'worried', 'nervous', 'scared', 'afraid', 'panic', 'stress'],
      sadness: ['sad', 'depressed', 'down', 'unhappy', 'hopeless', 'lonely', 'empty'],
      anger: ['angry', 'mad', 'frustrated', 'annoyed', 'upset', 'furious'],
      fear: ['terrified', 'frightened', 'fearful', 'scared', 'afraid'],
      overwhelm: ['overwhelmed', 'too much', 'cannot handle', 'drowning', 'stuck'],
      crisis: ['suicide', 'suicidal', 'kill myself', 'end it all', 'want it all to end', 'want to die', 'better off dead', 'no point', "don't want to live", 'hurt myself', 'self-harm', 'cut myself', 'end my life', 'take my life']
    };

    // Compassionate response templates
    this.compassionateFrames = {
      opening: [
        "I hear you, and what you're feeling is valid.",
        "Thank you for sharing that with me. Your feelings matter.",
        "I'm here to listen, and I want you to know you're not alone.",
        "It takes courage to express how you're feeling. I'm here for you."
      ],
      validation: [
        "It's completely okay to feel this way.",
        "Your emotions are real and important.",
        "Many people experience similar feelings, and they're all valid.",
        "What you're going through is significant, and you deserve support."
      ],
      supportive: [
        "You deserve compassion and understanding.",
        "Taking care of your mental health is important and brave.",
        "Remember, reaching out for help is a sign of strength.",
        "You're worth the care and support you need."
      ]
    };

    // Mental health resources
    this.resources = {
      crisis: {
        name: '988 Suicide & Crisis Lifeline',
        number: '988',
        description: 'Free, confidential support 24/7 for people in distress'
      },
      text: {
        name: 'Crisis Text Line',
        number: 'Text HOME to 741741',
        description: 'Free, 24/7 crisis support via text'
      },
      trevor: {
        name: 'The Trevor Project',
        number: '1-866-488-7386',
        description: 'LGBTQ+ youth crisis support'
      },
      general: {
        name: 'SAMHSA National Helpline',
        number: '1-800-662-4357',
        description: 'Substance abuse and mental health services'
      }
    };
  }

  /**
   * Validates and identifies emotions in user input
   * @param {string} text - User's message
   * @returns {object} Detected emotions and crisis indicators
   */
  validateEmotions(text) {
    const lowerText = text.toLowerCase();
    const detected = {
      emotions: [],
      isCrisis: false,
      intensity: 'moderate'
    };

    // Check for each emotion pattern
    for (const [emotion, patterns] of Object.entries(this.emotionPatterns)) {
      for (const pattern of patterns) {
        if (lowerText.includes(pattern)) {
          detected.emotions.push(emotion);
          
          // Crisis detection
          if (emotion === 'crisis') {
            detected.isCrisis = true;
            detected.intensity = 'critical';
          }
          break;
        }
      }
    }

    // Remove duplicates
    detected.emotions = [...new Set(detected.emotions)];

    // Determine intensity based on multiple emotions
    if (detected.emotions.length > 3 && !detected.isCrisis) {
      detected.intensity = 'high';
    }

    return detected;
  }

  /**
   * Suggests appropriate resources based on detected emotions
   * @param {object} emotionData - Result from validateEmotions
   * @returns {array} Relevant resources
   */
  suggestResources(emotionData) {
    const suggestions = [];

    // Always suggest crisis resources if crisis detected
    if (emotionData.isCrisis) {
      suggestions.push({
        ...this.resources.crisis,
        urgent: true,
        message: 'If you\'re in crisis, please reach out immediately:'
      });
      suggestions.push(this.resources.text);
      return suggestions;
    }

    // Suggest based on intensity
    if (emotionData.intensity === 'high' || emotionData.emotions.length > 2) {
      suggestions.push({
        ...this.resources.crisis,
        message: 'If you need immediate support, these resources are available 24/7:'
      });
    }

    // Always include general resource
    suggestions.push({
      ...this.resources.general,
      message: 'For ongoing support and resources:'
    });

    return suggestions;
  }

  /**
   * Wraps a response with compassionate, empathetic language
   * @param {string} originalResponse - The original AI response
   * @param {string} userInput - The user's original message
   * @returns {string} Compassionately wrapped response
   */
  wrapWithCompassion(originalResponse, userInput) {
    // Validate emotions in user input
    const emotionData = this.validateEmotions(userInput);

    // Select random compassionate frames
    const opening = this.compassionateFrames.opening[
      Math.floor(Math.random() * this.compassionateFrames.opening.length)
    ];
    const validation = this.compassionateFrames.validation[
      Math.floor(Math.random() * this.compassionateFrames.validation.length)
    ];

    // Build compassionate response
    let compassionateResponse = `${opening}\n\n`;

    // Add emotion validation if emotions detected
    if (emotionData.emotions.length > 0) {
      compassionateResponse += `${validation}\n\n`;
    }

    // Add the original response
    compassionateResponse += `${originalResponse}\n\n`;

    // Add resources if appropriate
    const resources = this.suggestResources(emotionData);
    if (resources.length > 0) {
      compassionateResponse += '\n**Resources for Support:**\n\n';
      
      resources.forEach(resource => {
        if (resource.message) {
          compassionateResponse += `${resource.message}\n`;
        }
        compassionateResponse += `- **${resource.name}**: ${resource.number}\n`;
        compassionateResponse += `  ${resource.description}\n\n`;
      });
    }

    // Add supportive closing
    const supportive = this.compassionateFrames.supportive[
      Math.floor(Math.random() * this.compassionateFrames.supportive.length)
    ];
    compassionateResponse += `${supportive}`;

    return compassionateResponse;
  }

  /**
   * Process user input with empathy-anchor skill (offline-capable)
   * @param {string} userInput - User's message
   * @param {string} aiResponse - Optional AI response to wrap
   * @returns {object} Processed response with empathy anchoring
   */
  process(userInput, aiResponse = null) {
    const emotionData = this.validateEmotions(userInput);

    // If no AI response provided, generate a supportive acknowledgment
    const baseResponse = aiResponse || this.generateSupportiveResponse(emotionData);

    return {
      response: this.wrapWithCompassion(baseResponse, userInput),
      metadata: {
        emotionsDetected: emotionData.emotions,
        isCrisis: emotionData.isCrisis,
        intensity: emotionData.intensity,
        offlineMode: this.config.offlineMode,
        timestamp: new Date().toISOString()
      }
    };
  }

  /**
   * Generate a supportive response when no AI response is available (offline mode)
   * @param {object} emotionData - Detected emotion data
   * @returns {string} Supportive response
   */
  generateSupportiveResponse(emotionData) {
    if (emotionData.isCrisis) {
      return `Your life has value, and you deserve support right now. Please don't face this alone.`;
    }

    if (emotionData.emotions.length === 0) {
      return `I'm here to listen and support you. Would you like to share more about what's on your mind?`;
    }

    const emotionList = emotionData.emotions.join(', ');
    return `I understand you're experiencing feelings of ${emotionList}. These emotions are valid, and it's important to acknowledge them. Would you like to talk more about what you're going through?`;
  }

  /**
   * Check if input indicates a crisis situation
   * @param {string} text - User's message
   * @returns {boolean} True if crisis detected
   */
  isCrisisDetected(text) {
    return this.validateEmotions(text).isCrisis;
  }
}

// Export for use in Node.js
if (typeof module !== 'undefined' && module.exports) {
  module.exports = EmpathyAnchor;
}
 * 
 * Youth-focused empathy skill that validates emotions and provides 
 * Michigan mental health resources with privacy-first approach.
 */

/**
 * Michigan mental health resources
 * 
 * Comprehensive list of Michigan-specific mental health support resources
 * including crisis hotlines, support organizations, and peer support services.
 * 
 * @type {Object}
 * @property {Object} suicide988 - 988 Suicide & Crisis Lifeline (national, 24/7)
 * @property {Object} namiMichigan - National Alliance on Mental Illness Michigan chapter
 * @property {Object} crisisTextLine - Text-based crisis support
 * @property {Object} teenLine - Peer support specifically for teens
 */
const MICHIGAN_RESOURCES = {
  suicide988: {
    name: '988 Suicide & Crisis Lifeline',
    contact: 'Call or Text 988',
    availability: '24/7',
    description: 'Free, confidential crisis support'
  },
  namiMichigan: {
    name: 'NAMI Michigan',
    website: 'https://namimi.org',
    helpline: '1-800-950-NAMI (6264)',
    description: 'Support groups, education, and advocacy'
  },
  crisisTextLine: {
    name: 'Michigan Crisis Text Line',
    contact: 'Text "HELLO" to 741741',
    availability: '24/7',
    description: 'Text-based crisis support'
  },
  teenLine: {
    name: 'Teen Line',
    contact: '1-800-TLC-TEEN (852-8336)',
    description: 'Peer support for teens'
  }
};

/**
 * Keywords that suggest emotional distress or need for support
 * 
 * Used for pattern matching in emotional content analysis to identify when
 * users may benefit from empathetic validation and resource suggestions.
 * Matching is case-insensitive. These keywords indicate moderate emotional
 * distress that warrants supportive resources but not immediate crisis intervention.
 * 
 * @type {string[]}
 */
const DISTRESS_KEYWORDS = [
  'anxious', 'anxiety', 'worried', 'stress', 'stressed',
  'sad', 'sadness', 'depressed', 'depression', 'lonely', 'alone',
  'scared', 'afraid', 'fear', 'panic', 'overwhelmed',
  'hurt', 'pain', 'crying', 'upset', 'angry', 'frustrated',
  'hopeless', 'helpless', 'worthless', 'suicide', 'self-harm',
  'nobody understands', 'nobody cares', 'give up', 'end it'
];

/**
 * Crisis keywords that require immediate resource sharing
 * 
 * These keywords indicate severe emotional distress or immediate risk and trigger
 * urgent crisis resource presentation (988, Crisis Text Line) with emphasis on
 * immediate availability. Crisis keywords take precedence over distress keywords
 * in the response urgency hierarchy. Matching is case-insensitive.
 * 
 * @type {string[]}
 */
const CRISIS_KEYWORDS = [
  'suicide', 'suicidal', 'kill myself', 'want to die', 'end my life',
  'self-harm', 'hurt myself', 'cutting', 'overdose'
];

/**
 * Empathetic validation phrases
 * 
 * Youth-appropriate, non-judgmental phrases for emotional validation.
 * One phrase is randomly selected when generating empathy responses to
 * acknowledge and normalize users' feelings. Designed to create a safe,
 * supportive environment for young people to express emotions.
 * 
 * @type {string[]}
 */
const VALIDATION_PHRASES = [
  "It's completely okay to feel that way",
  "Your feelings are valid, and it's brave to share them",
  "Many young people experience similar emotions",
  "Thank you for trusting me with this",
  "I hear you, and what you're feeling matters",
  "It takes courage to express these feelings",
  "You're not alone in feeling this way"
];

/**
 * Check if the system is in offline mode
 * @param {Object} context - The skill execution context
 * @returns {boolean} True if offline mode is active
 */
function isOfflineMode(context) {
  // Check for offline mode indicators in context
  if (context && context.system) {
    return context.system.offlineMode === true || 
           context.system.offline === true ||
           context.system.networkStatus === 'offline';
  }
  
  // Check environment variable
  if (process.env.OFFLINE_MODE === 'true' || process.env.OFFLINE_MODE === '1') {
    return true;
  }
  
  return false;
}

/**
 * Detect if message contains emotional distress
 * @param {string} message - The user's message
 * @returns {Object} Analysis of emotional content
 */
function analyzeEmotionalContent(message) {
  const lowerMessage = message.toLowerCase();
  
  const hasCrisis = CRISIS_KEYWORDS.some(keyword => 
    lowerMessage.includes(keyword)
  );
  
  const hasDistress = DISTRESS_KEYWORDS.some(keyword => 
    lowerMessage.includes(keyword)
  );
  
  const emotionLevel = hasCrisis ? 'crisis' : hasDistress ? 'distress' : 'neutral';
  
  return {
    hasCrisis,
    hasDistress,
    emotionLevel,
    suggestResources: hasCrisis || hasDistress
  };
}

/**
 * Generate empathetic validation
 * @returns {string} A random validation phrase
 */
function generateValidation() {
  const index = Math.floor(Math.random() * VALIDATION_PHRASES.length);
  return VALIDATION_PHRASES[index];
}

/**
 * Format resource suggestions based on emotion level
 * @param {string} emotionLevel - 'crisis', 'distress', or 'neutral'
 * @returns {string} Formatted resource information
 */
function formatResourceSuggestions(emotionLevel) {
  if (emotionLevel === 'crisis') {
    return `\n\n**Immediate Support Available:**\n` +
           `🆘 **${MICHIGAN_RESOURCES.suicide988.name}**: ${MICHIGAN_RESOURCES.suicide988.contact} (${MICHIGAN_RESOURCES.suicide988.availability})\n` +
           `💬 **${MICHIGAN_RESOURCES.crisisTextLine.name}**: ${MICHIGAN_RESOURCES.crisisTextLine.contact}\n` +
           `\nYou don't have to go through this alone. These resources are here to help right now.`;
  }
  
  if (emotionLevel === 'distress') {
    return `\n\n**Michigan Resources for Support:**\n` +
           `• **${MICHIGAN_RESOURCES.suicide988.name}**: ${MICHIGAN_RESOURCES.suicide988.contact} (${MICHIGAN_RESOURCES.suicide988.availability})\n` +
           `• **${MICHIGAN_RESOURCES.namiMichigan.name}**: ${MICHIGAN_RESOURCES.namiMichigan.helpline} - ${MICHIGAN_RESOURCES.namiMichigan.description}\n` +
           `• **${MICHIGAN_RESOURCES.teenLine.name}**: ${MICHIGAN_RESOURCES.teenLine.contact}\n` +
           `\nThese resources are free, confidential, and here for you.`;
  }
  
  return '';
}

/**
 * Generate empathetic response
 * @param {string} message - The user's message
 * @param {Object} analysis - Emotional content analysis
 * @param {boolean} offline - Whether offline mode is active
 * @returns {string} Empathetic response with resources
 */
function generateEmpathyResponse(message, analysis, offline) {
  let response = '';
  
  // Add validation if emotional content detected
  if (analysis.hasDistress || analysis.hasCrisis) {
    response += generateValidation() + '. ';
  }
  
  // Add privacy notice if offline
  if (offline) {
    response += '\n\n🔒 **Privacy Mode**: Your conversation is staying private on your device. ';
  }
  
  // Add resources if needed
  if (analysis.suggestResources) {
    response += formatResourceSuggestions(analysis.emotionLevel);
  }
  
  return response.trim();
}

/**
 * Main skill execution function
 * @param {Object} context - Skill execution context from OpenClaw
 * @param {Object} params - Parameters including the user's message
 * @returns {Object} Skill execution result
 */
async function run(context, params) {
  try {
    // Extract message from params
    const message = params.message || params.text || params.content || '';
    
    if (!message) {
      return {
        success: true,
        empathyLevel: 'none',
        response: ''
      };
    }
    
    // Check offline mode for privacy
    const offline = isOfflineMode(context);
    
    // Analyze emotional content
    const analysis = analyzeEmotionalContent(message);
    
    // Generate empathetic response
    const response = generateEmpathyResponse(message, analysis, offline);
    
    return {
      success: true,
      empathyLevel: analysis.emotionLevel,
      hasResources: analysis.suggestResources,
      offline: offline,
      response: response,
      metadata: {
        triggeredOn: 'all-messages',
        privacyMode: offline,
        resourcesShared: analysis.suggestResources,
        emotionLevel: analysis.emotionLevel
      }
    };
  } catch (error) {
    return {
      success: false,
      error: error.message,
      response: ''
    };
  }
}

// Export for OpenClaw
module.exports = {
  run,
  // Export internals for testing
  analyzeEmotionalContent,
  isOfflineMode,
  generateValidation,
  formatResourceSuggestions,
  MICHIGAN_RESOURCES,
  DISTRESS_KEYWORDS,
  CRISIS_KEYWORDS
};
