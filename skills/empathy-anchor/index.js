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
