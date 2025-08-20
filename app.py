from flask import Flask, render_template, request, jsonify
import re
from typing import Dict, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)


class EmotionDetector:
    """Emotion detection class using rule-based approach (Watson NLP simulation)"""

    def __init__(self):
        # Emotion keywords and patterns
        self.emotion_patterns = {
            "joy": [
                r"\b(happy|joy|excited|thrilled|delighted|pleased|great|wonderful|amazing|fantastic)\b",
                r"\b(love|adore|enjoy|like|favorite|best|excellent|outstanding|brilliant)\b",
                r"\b(smile|laugh|fun|enjoyment|pleasure|satisfaction|contentment)\b",
            ],
            "sadness": [
                r"\b(sad|unhappy|disappointed|depressed|miserable|sorrow|grief|melancholy)\b",
                r"\b(upset|hurt|broken|defeated|hopeless|lonely|isolated|abandoned)\b",
                r"\b(cry|tears|weep|mourn|regret|remorse|guilt|shame)\b",
            ],
            "anger": [
                r"\b(angry|mad|furious|enraged|irritated|annoyed|frustrated|outraged)\b",
                r"\b(hate|despise|loathe|disgust|contempt|rage|wrath|fury)\b",
                r"\b(yell|scream|shout|explode|boil|steam|fume|seethe)\b",
            ],
            "fear": [
                r"\b(afraid|scared|terrified|frightened|panicked|anxious|worried|nervous)\b",
                r"\b(horror|dread|terror|panic|alarm|distress|unease|apprehension)\b",
                r"\b(threat|danger|risk|hazard|peril|menace|intimidation)\b",
            ],
            "disgust": [
                r"\b(disgust|disgusting|repulsed|revolted|sickened|nauseated|appalled|horrified)\b",
                r"\b(gross|nasty|filthy|dirty|contaminated|polluted|corrupt)\b",
                r"\b(abhor|detest|loathe|despise|abominate|execrate)\b",
            ],
        }

        # Emotion intensity modifiers
        self.intensity_modifiers = {
            "very": 1.5,
            "really": 1.4,
            "extremely": 1.8,
            "incredibly": 1.7,
            "absolutely": 1.6,
            "slightly": 0.7,
            "somewhat": 0.8,
            "kind of": 0.6,
        }

    def detect_emotions(self, text: str) -> Dict[str, float]:
        """
        Detect emotions in the given text and return confidence scores

        Args:
            text (str): Input text to analyze

        Returns:
            Dict[str, float]: Emotion scores for each detected emotion
        """
        if not text or not text.strip():
            return {}

        text = text.lower().strip()
        emotion_scores = {emotion: 0.0 for emotion in self.emotion_patterns.keys()}

        # Check for intensity modifiers
        intensity_multiplier = 1.0
        for modifier, multiplier in self.intensity_modifiers.items():
            if modifier in text:
                intensity_multiplier = multiplier
                break

        # Analyze text for each emotion
        for emotion, patterns in self.emotion_patterns.items():
            score = 0.0
            for pattern in patterns:
                matches = re.findall(pattern, text)
                if matches:
                    score += len(matches) * 0.3  # Base score per match

            if score > 0:
                score *= intensity_multiplier
                emotion_scores[emotion] = min(score, 1.0)  # Cap at 1.0

        # Filter out emotions with zero scores
        return {k: round(v, 3) for k, v in emotion_scores.items() if v > 0}

    def get_primary_emotion(self, emotions: Dict[str, float]) -> Tuple[str, float]:
        """
        Get the primary (strongest) emotion from the detected emotions

        Args:
            emotions (Dict[str, float]): Dictionary of emotion scores

        Returns:
            Tuple[str, float]: Primary emotion and its score
        """
        if not emotions:
            return "neutral", 0.0

        primary_emotion = max(emotions.items(), key=lambda x: x[1])
        return primary_emotion[0], primary_emotion[1]

    def analyze_feedback(self, text: str) -> Dict:
        """
        Complete analysis of customer feedback

        Args:
            text (str): Customer feedback text

        Returns:
            Dict: Complete analysis results
        """
        try:
            emotions = self.detect_emotions(text)
            primary_emotion, confidence = self.get_primary_emotion(emotions)

            # Determine overall sentiment
            if primary_emotion in ["joy"]:
                sentiment = "positive"
            elif primary_emotion in ["sadness", "anger", "fear", "disgust"]:
                sentiment = "negative"
            else:
                sentiment = "neutral"

            return {
                "success": True,
                "text": text,
                "emotions": emotions,
                "primary_emotion": primary_emotion,
                "confidence": confidence,
                "sentiment": sentiment,
                "analysis_timestamp": None,  # Would be datetime.now() in production
            }

        except Exception as e:
            logger.error(f"Error analyzing feedback: {str(e)}")
            return {"success": False, "error": str(e), "text": text}


# Initialize emotion detector
emotion_detector = EmotionDetector()


@app.route("/")
def index():
    """Main page route"""
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze_emotion():
    """API endpoint for emotion analysis"""
    try:
        data = request.get_json()
        if not data or "text" not in data:
            return jsonify({"success": False, "error": "No text provided"}), 400

        text = data["text"].strip()
        if not text:
            return jsonify({"success": False, "error": "Empty text provided"}), 400

        # Perform emotion analysis
        result = emotion_detector.analyze_feedback(text)

        return jsonify(result)

    except Exception as e:
        logger.error(f"Error in analyze endpoint: {str(e)}")
        return (
            jsonify({"success": False, "error": f"Internal server error: {str(e)}"}),
            500,
        )


@app.route("/health")
def health_check():
    """Health check endpoint"""
    return jsonify(
        {"status": "healthy", "service": "Emotion Detection API", "version": "1.0.0"}
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
