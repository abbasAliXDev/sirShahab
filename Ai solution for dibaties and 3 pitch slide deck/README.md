
# DiabetesPredict: AI-Powered Diabetes Risk Assessment Tool

## Overview
DiabetesPredict is a web application that uses machine learning to assess diabetes risk based on health metrics. It provides personalized recommendations and insights using advanced AI capabilities.

## Technical Stack

### Backend
- **Flask**: Web framework for handling HTTP requests and routing
- **SQLite**: Database for storing user data and predictions
- **scikit-learn**: Machine learning library for the diabetes prediction model
- **OpenAI API**: Generates personalized health recommendations
- **Gunicorn**: Production WSGI server

### Frontend
- **Bootstrap**: Responsive design framework
- **Chart.js**: Data visualization
- **Font Awesome**: Icons and visual elements

## Core Components

### 1. Diabetes Predictor (`diabetes_predictor.py`)
- Implements Random Forest classifier
- Trains on Pima Indians Diabetes Dataset
- Features: pregnancies, glucose, blood pressure, skin thickness, insulin, BMI, diabetes pedigree function, age
- Model accuracy: ~73.4%

### 2. AI Health Advisor (`ai_health_advisor.py`)
- Integrates with OpenAI's GPT-4 model
- Generates personalized health recommendations
- Provides health insights based on risk assessment
- Includes fallback recommendation system

### 3. Application Routes (`app.py`)
- `/`: Home page with risk assessment form
- `/predict`: Processes health metrics and returns predictions
- `/about`: Information about the application
- `/api/predict`: REST API endpoint for predictions
- `/pitch-deck`: Interactive presentation slides

## Database Schema
- Users table: Basic user information
- Predictions table: Risk assessment records
- AIRecommendations table: Generated health recommendations

## Setup and Execution

1. **Environment Setup**
   ```bash
   # Install dependencies
   pip install -r requirements.txt
   npm install
   ```

2. **Configuration**
   - Set OpenAI API key in environment variables
   - Database URL configuration (defaults to SQLite)
   - Configure port settings (default: 5000)

3. **Running the Application**
   ```bash
   # Development mode
   python main.py
   
   # Production mode
   gunicorn --bind 0.0.0.0:5000 main:app
   ```

4. **API Usage**
   ```python
   # Example API request
   POST /api/predict
   {
     "pregnancies": 0,
     "glucose": 85,
     "blood_pressure": 66,
     "skin_thickness": 29,
     "insulin": 0,
     "bmi": 26.6,
     "dpf": 0.351,
     "age": 31
   }
   ```

## Key Features

1. **Risk Assessment**
   - Real-time diabetes risk prediction
   - Probability calculation
   - Feature importance analysis

2. **AI Recommendations**
   - Personalized diet suggestions
   - Exercise recommendations
   - Lifestyle modifications
   - Health monitoring advice

3. **Data Visualization**
   - Interactive charts
   - Risk factor analysis
   - Trend visualization

4. **Pitch Deck**
   - Problem overview
   - Solution demonstration
   - Market analysis
   - Business model

## Security Features
- Input validation and sanitization
- Error handling and logging
- Secure API endpoints
- Database connection pooling

## Limitations
- Model trained on specific demographic
- Requires accurate self-reported data
- Not a diagnostic tool
- Educational purpose only

## Future Enhancements
1. User authentication system
2. Additional health metrics
3. Integration with health devices
4. Enhanced visualization options
5. Multi-language support

## Disclaimer
This tool is for educational purposes only and should not replace professional medical advice.
