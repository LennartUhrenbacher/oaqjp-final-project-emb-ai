/**
 * AI Emotion Detection Web Application
 * JavaScript functionality for emotion analysis
 */

// Global variables
let isAnalyzing = false;

/**
 * Main function to analyze emotions in customer feedback
 */
async function analyzeEmotions() {
    const feedbackText = document.getElementById('feedbackText').value.trim();
    const analyzeBtn = document.getElementById('analyzeBtn');
    const loading = document.getElementById('loading');
    const errorMessage = document.getElementById('errorMessage');
    const resultSection = document.getElementById('resultSection');
    
    // Input validation
    if (!feedbackText) {
        showError('Please enter some text to analyze.');
        return;
    }
    
    if (isAnalyzing) {
        return; // Prevent multiple simultaneous requests
    }
    
    // Reset UI state
    hideError();
    hideResults();
    showLoading();
    disableAnalyzeButton();
    isAnalyzing = true;
    
    try {
        // Make API call to Flask backend
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: feedbackText })
        });
        
        const result = await response.json();
        
        if (response.ok && result.success) {
            displayResults(result);
        } else {
            const errorMsg = result.error || 'Failed to analyze emotions. Please try again.';
            showError(errorMsg);
        }
        
    } catch (error) {
        console.error('Error during analysis:', error);
        showError('Network error. Please check your connection and try again.');
    } finally {
        hideLoading();
        enableAnalyzeButton();
        isAnalyzing = false;
    }
}

/**
 * Display emotion analysis results
 */
function displayResults(result) {
    const resultSection = document.getElementById('resultSection');
    const primaryEmotion = document.getElementById('primaryEmotion');
    const confidenceScore = document.getElementById('confidenceScore');
    const confidenceBar = document.getElementById('confidenceBar');
    const overallSentiment = document.getElementById('overallSentiment');
    const emotionsList = document.getElementById('emotionsList');
    
    // Set primary emotion and confidence
    primaryEmotion.textContent = capitalizeFirstLetter(result.primary_emotion);
    confidenceScore.textContent = `${(result.confidence * 100).toFixed(1)}%`;
    confidenceBar.style.width = `${result.confidence * 100}%`;
    
    // Set overall sentiment with appropriate styling
    const sentimentElement = overallSentiment;
    sentimentElement.textContent = capitalizeFirstLetter(result.sentiment);
    sentimentElement.className = 'mb-0';
    
    // Add sentiment-specific styling
    if (result.sentiment === 'positive') {
        sentimentElement.style.color = '#28a745';
        sentimentElement.innerHTML = '<i class="fas fa-smile"></i> ' + capitalizeFirstLetter(result.sentiment);
    } else if (result.sentiment === 'negative') {
        sentimentElement.style.color = '#dc3545';
        sentimentElement.innerHTML = '<i class="fas fa-frown"></i> ' + capitalizeFirstLetter(result.sentiment);
    } else {
        sentimentElement.style.color = '#6c757d';
        sentimentElement.innerHTML = '<i class="fas fa-meh"></i> ' + capitalizeFirstLetter(result.sentiment);
    }
    
    // Display all detected emotions
    displayEmotionsList(result.emotions, emotionsList);
    
    // Show results section
    resultSection.style.display = 'block';
    
    // Smooth scroll to results
    resultSection.scrollIntoView({ behavior: 'smooth' });
}

/**
 * Display list of detected emotions with scores
 */
function displayEmotionsList(emotions, container) {
    if (!emotions || Object.keys(emotions).length === 0) {
        container.innerHTML = '<p class="text-muted">No specific emotions detected.</p>';
        return;
    }
    
    // Sort emotions by confidence score (descending)
    const sortedEmotions = Object.entries(emotions)
        .sort(([,a], [,b]) => b - a);
    
    let emotionsHTML = '';
    sortedEmotions.forEach(([emotion, score]) => {
        const percentage = (score * 100).toFixed(1);
        const emotionIcon = getEmotionIcon(emotion);
        
        emotionsHTML += `
            <div class="d-flex justify-content-between align-items-center mb-2">
                <span>
                    ${emotionIcon} ${capitalizeFirstLetter(emotion)}
                </span>
                <div class="d-flex align-items-center">
                    <div class="confidence-bar me-2" style="width: 100px;">
                        <div class="confidence-fill" style="width: ${percentage}%"></div>
                    </div>
                    <span class="emotion-score">${percentage}%</span>
                </div>
            </div>
        `;
    });
    
    container.innerHTML = emotionsHTML;
}

/**
 * Get appropriate icon for each emotion
 */
function getEmotionIcon(emotion) {
    const emotionIcons = {
        'joy': '<i class="fas fa-laugh text-warning"></i>',
        'sadness': '<i class="fas fa-sad-tear text-info"></i>',
        'anger': '<i class="fas fa-angry text-danger"></i>',
        'fear': '<i class="fas fa-fearful text-warning"></i>',
        'disgust': '<i class="fas fa-dizzy text-secondary"></i>',
        'neutral': '<i class="fas fa-meh text-muted"></i>'
    };
    
    return emotionIcons[emotion] || '<i class="fas fa-question text-muted"></i>';
}

/**
 * Utility function to capitalize first letter
 */
function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

/**
 * Show error message
 */
function showError(message) {
    const errorMessage = document.getElementById('errorMessage');
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
}

/**
 * Hide error message
 */
function hideError() {
    const errorMessage = document.getElementById('errorMessage');
    errorMessage.style.display = 'none';
}

/**
 * Show loading spinner
 */
function showLoading() {
    const loading = document.getElementById('loading');
    loading.style.display = 'block';
}

/**
 * Hide loading spinner
 */
function hideLoading() {
    const loading = document.getElementById('loading');
    loading.style.display = 'none';
}

/**
 * Show results section
 */
function showResults() {
    const resultSection = document.getElementById('resultSection');
    resultSection.style.display = 'block';
}

/**
 * Hide results section
 */
function hideResults() {
    const resultSection = document.getElementById('resultSection');
    resultSection.style.display = 'none';
}

/**
 * Disable analyze button
 */
function disableAnalyzeButton() {
    const analyzeBtn = document.getElementById('analyzeBtn');
    analyzeBtn.disabled = true;
    analyzeBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';
}

/**
 * Enable analyze button
 */
function enableAnalyzeButton() {
    const analyzeBtn = document.getElementById('analyzeBtn');
    analyzeBtn.disabled = false;
    analyzeBtn.innerHTML = '<i class="fas fa-magic"></i> Analyze Emotions';
}

/**
 * Clear all results and reset form
 */
function clearResults() {
    document.getElementById('feedbackText').value = '';
    hideError();
    hideResults();
    hideLoading();
    enableAnalyzeButton();
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    // Add enter key support for textarea
    const feedbackText = document.getElementById('feedbackText');
    feedbackText.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && e.ctrlKey) {
            analyzeEmotions();
        }
    });
    
    // Add clear button functionality
    const clearBtn = document.createElement('button');
    clearBtn.className = 'btn btn-outline-secondary ms-2';
    clearBtn.innerHTML = '<i class="fas fa-times"></i> Clear';
    clearBtn.onclick = clearResults;
    
    const buttonContainer = document.querySelector('.text-center');
    buttonContainer.appendChild(clearBtn);
});

// Legacy function for backward compatibility
function RunSentimentAnalysis() {
    analyzeEmotions();
}
