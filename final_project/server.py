"""
Flask server for emotion detection web application.

This module provides a web interface for emotion detection using
the EmotionDetection package and Watson NLP services.
"""

import os
import sys
from flask import Flask, render_template, request

# Add parent directory to path to import EmotionDetection package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from EmotionDetection import emotion_detector
except ImportError:
    # Handle import error gracefully
    emotion_detector = None

app = Flask(__name__)


@app.route('/')
def index():
    """
    Main page route.

    Returns:
        str: Rendered HTML template for the main page.
    """
    return render_template('index.html')


@app.route('/emotionDetector', methods=['POST'])
def analyze_emotion():
    """
    Endpoint for emotion analysis.

    Returns:
        str: Formatted emotion analysis result or error message.
    """
    if emotion_detector is None:
        return "Error: Emotion detection service not available"

    try:
        # Get text from form data
        text_to_analyze = request.form.get('textToAnalyze', '')

        if not text_to_analyze or text_to_analyze.strip() == '':
            return "Invalid text! Please try again!"

        # Analyze emotions
        result = emotion_detector(text_to_analyze)

        if not result:
            return "Invalid text! Please try again!"

        # Check if dominant_emotion is None (error case)
        if result['dominant_emotion'] is None:
            return "Invalid text! Please try again!"

        # Format the response as specified
        response_text = (
            f"For the given statement, the system response is "
            f"'anger': {result['anger']}, 'disgust': {result['disgust']}, "
            f"'fear': {result['fear']}, 'joy': {result['joy']} and "
            f"'sadness': {result['sadness']}. "
            f"The dominant emotion is {result['dominant_emotion']}."
        )

        return response_text

    except (ValueError, KeyError, TypeError) as e:
        return f"Error processing request: {str(e)}"


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
