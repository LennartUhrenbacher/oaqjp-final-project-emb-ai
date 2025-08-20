"""
Unit tests for emotion detection application
Tests the emotion_detector function for various statements and dominant emotions
"""

from EmotionDetection import emotion_detector

def test_emotion_detection():
    """
    Test function to validate emotion detection for various statements
    """
    print("Running unit tests for emotion detection...")
    print("=" * 50)
    
    # Test cases with expected dominant emotions
    test_cases = [
        ("I am glad this happened", "joy"),
        ("I am really mad about this", "anger"),
        ("I feel disgusted just hearing about this", "disgust"),
        ("I am so sad about this", "sadness"),
        ("I am really afraid that this will happen", "fear")
    ]
    
    passed_tests = 0
    total_tests = len(test_cases)
    
    for statement, expected_emotion in test_cases:
        print(f"\nTesting statement: '{statement}'")
        print(f"Expected dominant emotion: {expected_emotion}")
        
        try:
            result = emotion_detector(statement)
            print(f"Result: {result}")
            
            if result and 'dominant_emotion' in result:
                actual_emotion = result['dominant_emotion']
                print(f"Actual dominant emotion: {actual_emotion}")
                
                if actual_emotion == expected_emotion:
                    print("✅ PASSED")
                    passed_tests += 1
                else:
                    print(f"❌ FAILED - Expected {expected_emotion}, got {actual_emotion}")
            else:
                print("❌ FAILED - No result or missing dominant_emotion")
                
        except Exception as e:
            print(f"❌ ERROR - {str(e)}")
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed successfully!")
    else:
        print("⚠️  Some tests failed. Please check the implementation.")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    test_emotion_detection()
