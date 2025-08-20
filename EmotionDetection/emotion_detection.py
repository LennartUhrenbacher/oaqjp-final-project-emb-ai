import requests
import json

def emotion_detector(text_to_analyze):
    """
    Function to detect emotions using Watson NLP library
    
    Args:
        text_to_analyze (str): Text to be analyzed for emotions
        
    Returns:
        dict: Formatted output with emotion scores and dominant emotion, or None values for errors
    """
    # Check for blank entries
    if not text_to_analyze or text_to_analyze.strip() == '':
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }
    
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    input_json = {"raw_document": {"text": text_to_analyze}}
    
    try:
        response = requests.post(url, json=input_json, headers=headers)
        
        # Check status code for error handling
        if response.status_code == 400:
            return {
                'anger': None,
                'disgust': None,
                'fear': None,
                'joy': None,
                'sadness': None,
                'dominant_emotion': None
            }
        
        # Convert response text to dictionary
        response_dict = json.loads(response.text)
        
        # Extract emotion scores
        emotions = response_dict.get('emotions', [])
        
        # Initialize emotion scores
        anger_score = 0
        disgust_score = 0
        fear_score = 0
        joy_score = 0
        sadness_score = 0
        
        # Extract scores for each emotion
        for emotion in emotions:
            emotion_name = emotion.get('emotion', '').lower()
            score = emotion.get('score', 0)
            
            if emotion_name == 'anger':
                anger_score = score
            elif emotion_name == 'disgust':
                disgust_score = score
            elif emotion_name == 'fear':
                fear_score = score
            elif emotion_name == 'joy':
                joy_score = score
            elif emotion_name == 'sadness':
                sadness_score = score
        
        # Find dominant emotion
        emotion_scores = {
            'anger': anger_score,
            'disgust': disgust_score,
            'fear': fear_score,
            'joy': joy_score,
            'sadness': sadness_score
        }
        
        dominant_emotion = max(emotion_scores, key=emotion_scores.get)
        
        # Return formatted output
        return {
            'anger': anger_score,
            'disgust': disgust_score,
            'fear': fear_score,
            'joy': joy_score,
            'sadness': sadness_score,
            'dominant_emotion': dominant_emotion
        }
        
    except Exception as e:
        # Return None values for any errors
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }
