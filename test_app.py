"""
Unit tests for AI Emotion Detection Application
Tests the EmotionDetector class and Flask endpoints
"""

import unittest
import json
import sys
import os
from unittest.mock import patch

# Add the current directory to Python path to import app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, EmotionDetector


class TestEmotionDetector(unittest.TestCase):
    """Test cases for EmotionDetector class"""

    def setUp(self):
        """Set up test fixtures"""
        self.detector = EmotionDetector()
        self.app = app.test_client()
        self.app.testing = True

    def test_initialization(self):
        """Test EmotionDetector initialization"""
        self.assertIsNotNone(self.detector.emotion_patterns)
        self.assertIsNotNone(self.detector.intensity_modifiers)
        self.assertIn("joy", self.detector.emotion_patterns)
        self.assertIn("sadness", self.detector.emotion_patterns)
        self.assertIn("anger", self.detector.emotion_patterns)
        self.assertIn("fear", self.detector.emotion_patterns)
        self.assertIn("disgust", self.detector.emotion_patterns)

    def test_detect_emotions_joy(self):
        """Test joy emotion detection"""
        text = "I am very happy and excited about this product!"
        emotions = self.detector.detect_emotions(text)

        self.assertIn("joy", emotions)
        self.assertGreater(emotions["joy"], 0)
        self.assertLessEqual(emotions["joy"], 1.0)

    def test_detect_emotions_sadness(self):
        """Test sadness emotion detection"""
        text = "I feel sad and disappointed with the service."
        emotions = self.detector.detect_emotions(text)

        self.assertIn("sadness", emotions)
        self.assertGreater(emotions["sadness"], 0)
        self.assertLessEqual(emotions["sadness"], 1.0)

    def test_detect_emotions_anger(self):
        """Test anger emotion detection"""
        text = "I am absolutely furious and angry about this!"
        emotions = self.detector.detect_emotions(text)

        self.assertIn("anger", emotions)
        self.assertGreater(emotions["anger"], 0)
        self.assertLessEqual(emotions["anger"], 1.0)

    def test_detect_emotions_fear(self):
        """Test fear emotion detection"""
        text = "I am scared and terrified of what might happen."
        emotions = self.detector.detect_emotions(text)

        self.assertIn("fear", emotions)
        self.assertGreater(emotions["fear"], 0)
        self.assertLessEqual(emotions["fear"], 1.0)

    def test_detect_emotions_disgust(self):
        """Test disgust emotion detection"""
        text = "This is absolutely disgusting and revolting."
        emotions = self.detector.detect_emotions(text)

        self.assertIn("disgust", emotions)
        self.assertGreater(emotions["disgust"], 0)
        self.assertLessEqual(emotions["disgust"], 1.0)

    def test_intensity_modifiers(self):
        """Test intensity modifier detection"""
        text = "I am extremely happy and very excited!"
        emotions = self.detector.detect_emotions(text)

        # Should have higher scores due to intensity modifiers
        self.assertIn("joy", emotions)
        self.assertGreater(emotions["joy"], 0.3)  # Higher than base score

    def test_empty_text(self):
        """Test handling of empty text"""
        emotions = self.detector.detect_emotions("")
        self.assertEqual(emotions, {})

        emotions = self.detector.detect_emotions("   ")
        self.assertEqual(emotions, {})

        emotions = self.detector.detect_emotions(None)
        self.assertEqual(emotions, {})

    def test_no_emotions_detected(self):
        """Test text with no detectable emotions"""
        text = "The product arrived on time and was packaged well."
        emotions = self.detector.detect_emotions(text)
        self.assertEqual(emotions, {})

    def test_multiple_emotions(self):
        """Test text with multiple emotions"""
        text = "I am happy but also a bit worried about the future."
        emotions = self.detector.detect_emotions(text)

        self.assertIn("joy", emotions)
        self.assertIn("fear", emotions)
        self.assertGreater(len(emotions), 1)

    def test_get_primary_emotion(self):
        """Test primary emotion detection"""
        emotions = {"joy": 0.8, "sadness": 0.3, "anger": 0.1}
        primary, confidence = self.detector.get_primary_emotion(emotions)

        self.assertEqual(primary, "joy")
        self.assertEqual(confidence, 0.8)

    def test_get_primary_emotion_empty(self):
        """Test primary emotion with empty emotions dict"""
        primary, confidence = self.detector.get_primary_emotion({})
        self.assertEqual(primary, "neutral")
        self.assertEqual(confidence, 0.0)

    def test_analyze_feedback_success(self):
        """Test complete feedback analysis"""
        text = "I am very happy with this amazing product!"
        result = self.detector.analyze_feedback(text)

        self.assertTrue(result["success"])
        self.assertEqual(result["text"], text)
        self.assertIn("emotions", result)
        self.assertIn("primary_emotion", result)
        self.assertIn("confidence", result)
        self.assertIn("sentiment", result)
        self.assertEqual(result["sentiment"], "positive")

    def test_analyze_feedback_negative(self):
        """Test negative feedback analysis"""
        text = "I am extremely angry and disappointed with this terrible service!"
        result = self.detector.detect_emotions(text)

        self.assertIn("anger", result)
        self.assertGreater(result["anger"], 0)


class TestFlaskEndpoints(unittest.TestCase):
    """Test cases for Flask endpoints"""

    def setUp(self):
        """Set up test fixtures"""
        self.app = app.test_client()
        self.app.testing = True

    def test_index_route(self):
        """Test main page route"""
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"AI Emotion Detection", response.data)

    def test_health_check(self):
        """Test health check endpoint"""
        response = self.app.get("/health")
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["service"], "Emotion Detection API")
        self.assertEqual(data["version"], "1.0.0")

    def test_analyze_endpoint_success(self):
        """Test successful emotion analysis endpoint"""
        test_data = {"text": "I am very happy with this product!"}
        response = self.app.post(
            "/analyze", data=json.dumps(test_data), content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data["success"])
        self.assertIn("emotions", data)
        self.assertIn("primary_emotion", data)

    def test_analyze_endpoint_no_text(self):
        """Test analyze endpoint with no text"""
        test_data = {}
        response = self.app.post(
            "/analyze", data=json.dumps(test_data), content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data["success"])
        self.assertIn("error", data)

    def test_analyze_endpoint_empty_text(self):
        """Test analyze endpoint with empty text"""
        test_data = {"text": ""}
        response = self.app.post(
            "/analyze", data=json.dumps(test_data), content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data["success"])
        self.assertIn("error", data)

    def test_analyze_endpoint_invalid_json(self):
        """Test analyze endpoint with invalid JSON"""
        response = self.app.post(
            "/analyze", data="invalid json", content_type="application/json"
        )

        self.assertEqual(response.status_code, 500)
        data = json.loads(response.data)
        self.assertFalse(data["success"])
        self.assertIn("error", data)

    def test_analyze_endpoint_wrong_method(self):
        """Test analyze endpoint with wrong HTTP method"""
        response = self.app.get("/analyze")
        self.assertEqual(response.status_code, 405)  # Method not allowed


class TestErrorHandling(unittest.TestCase):
    """Test cases for error handling"""

    def setUp(self):
        """Set up test fixtures"""
        self.detector = EmotionDetector()

    def test_analyze_feedback_exception_handling(self):
        """Test exception handling in analyze_feedback"""
        # Mock the detect_emotions method to raise an exception
        with patch.object(
            self.detector, "detect_emotions", side_effect=Exception("Test error")
        ):
            result = self.detector.analyze_feedback("test text")

            self.assertFalse(result["success"])
            self.assertIn("error", result)
            self.assertEqual(result["error"], "Test error")

    def test_edge_cases(self):
        """Test various edge cases"""
        # Very long text
        long_text = "happy " * 1000
        emotions = self.detector.detect_emotions(long_text)
        self.assertIn("joy", emotions)
        self.assertLessEqual(emotions["joy"], 1.0)  # Should be capped

        # Text with special characters
        special_text = "I'm very happy!!! 😊 🎉"
        emotions = self.detector.detect_emotions(special_text)
        self.assertIn("joy", emotions)

        # Mixed case text
        mixed_text = "I am VERY HAPPY and extremely EXCITED!"
        emotions = self.detector.detect_emotions(mixed_text)
        self.assertIn("joy", emotions)


if __name__ == "__main__":
    # Create test suite
    test_suite = unittest.TestSuite()

    # Add test classes
    test_suite.addTest(unittest.makeSuite(TestEmotionDetector))
    test_suite.addTest(unittest.makeSuite(TestFlaskEndpoints))
    test_suite.addTest(unittest.makeSuite(TestErrorHandling))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    # Exit with appropriate code
    exit(0 if result.wasSuccessful() else 1)
