/**
 * Empathy Anchor Skill for OpenClaw
 * 
 * Youth-focused empathy skill that validates emotions and provides 
 * Michigan mental health resources with privacy-first approach.
 */

/**
 * Michigan mental health resources
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
 */
const CRISIS_KEYWORDS = [
  'suicide', 'suicidal', 'kill myself', 'want to die', 'end my life',
  'self-harm', 'hurt myself', 'cutting', 'overdose'
];

/**
 * Empathetic validation phrases
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
