# AI-Based Emotion Detection Web Application

## Project Overview

This project implements an AI-based web application that performs analytics on customer feedback by detecting emotions using advanced Natural Language Processing (NLP) techniques. The application extends beyond simple sentiment analysis to identify specific emotions like joy, sadness, anger, fear, and disgust.

## Features

- **Advanced Emotion Detection**: Identifies 5 primary emotions with confidence scoring
- **Real-time Analysis**: Instant feedback analysis with modern web interface
- **Confidence Scoring**: Provides percentage-based confidence for each detected emotion
- **Sentiment Classification**: Overall positive/negative/neutral sentiment determination
- **Modern UI/UX**: Beautiful, responsive web interface with Bootstrap 5
- **Error Handling**: Comprehensive error handling and user feedback
- **API Endpoints**: RESTful API for integration with other systems
- **Unit Testing**: Comprehensive test suite for reliability

## Technology Stack

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Styling**: Bootstrap 5, Font Awesome
- **Testing**: Python unittest framework
- **Code Quality**: flake8, pylint, black

## Installation and Setup

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd oaqjp-final-project-emb-ai
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Run the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Project Structure

```
oaqjp-final-project-emb-ai/
├── app.py                 # Main Flask application
├── config.py             # Configuration management
├── test_app.py           # Unit tests
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Main web interface
├── static/
│   └── mywebscript.js    # Frontend JavaScript
├── PROJECT_GUIDE.md      # Project implementation guide
└── README.md             # This file
```

## Usage

### Web Interface

1. Open your browser and navigate to `http://localhost:5000`
2. Enter customer feedback text in the textarea
3. Click "Analyze Emotions" to process the text
4. View detailed emotion analysis results

### API Usage

The application provides RESTful API endpoints:

#### Analyze Emotions
```bash
POST /analyze
Content-Type: application/json

{
    "text": "I am very happy with this amazing product!"
}
```

#### Health Check
```bash
GET /health
```

### Example API Response

```json
{
    "success": true,
    "text": "I am very happy with this amazing product!",
    "emotions": {
        "joy": 0.675
    },
    "primary_emotion": "joy",
    "confidence": 0.675,
    "sentiment": "positive",
    "analysis_timestamp": null
}
```

## Testing

### Run Unit Tests

```bash
python test_app.py
```

### Run with Coverage

```bash
pytest --cov=app test_app.py
```

## Code Quality Analysis

### Linting with flake8
```bash
flake8 app.py config.py test_app.py
```

### Code Formatting with black
```bash
black app.py config.py test_app.py
```

### Static Analysis with pylint
```bash
pylint app.py config.py test_app.py
```

## Emotion Detection Algorithm

The application uses a rule-based approach with regex patterns to identify emotions:

- **Joy**: happy, excited, thrilled, love, enjoy, fantastic
- **Sadness**: sad, disappointed, depressed, sorrow, grief
- **Anger**: angry, furious, enraged, hate, rage, wrath
- **Fear**: afraid, scared, terrified, anxious, worried
- **Disgust**: disgust, repulsed, revolted, gross, nasty

### Intensity Modifiers

The system recognizes intensity modifiers to adjust confidence scores:
- **High Intensity**: extremely (1.8x), incredibly (1.7x), absolutely (1.6x)
- **Medium Intensity**: very (1.5x), really (1.4x)
- **Low Intensity**: slightly (0.7x), somewhat (0.8x), kind of (0.6x)

## Error Handling

The application implements comprehensive error handling:

- **Input Validation**: Checks for empty or invalid input
- **API Error Handling**: Graceful handling of API failures
- **User Feedback**: Clear error messages and loading states
- **Logging**: Comprehensive logging for debugging

## Deployment

### Development
```bash
export FLASK_ENV=development
python app.py
```

### Production
```bash
export FLASK_ENV=production
export SECRET_KEY=your-secret-key-here
python app.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Screenshot Requirements

For peer grading, save screenshots with the following nomenclature:

- **Task Completion**: `task1_completion.png`, `task2_completion.png`, etc.
- **Application Running**: `app_running.png`
- **Test Results**: `test_results.png`
- **Error Handling**: `error_handling.png`
- **Code Analysis**: `code_analysis.png`

## Support

For questions or issues, please refer to the project documentation or create an issue in the repository.

---

**Note**: This platform is not persistent. It is recommended to keep a copy of your code on your local machine and save changes regularly.
