import os
import logging
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
import numpy as np

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Initialize the database
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default-dev-secret")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database to use PostgreSQL
DATABASE_URL = os.environ.get("DATABASE_URL")
# Fallback to SQLite for development if no DATABASE_URL is provided
if not DATABASE_URL:
    DATABASE_URL = "sqlite:///diabetes_predictor.db"
    logging.warning("DATABASE_URL not found, using SQLite as fallback")

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the app with the extension
db.init_app(app)

# Import the diabetes predictor after app initialization
from diabetes_predictor import DiabetesPredictor

# Initialize the predictor
predictor = DiabetesPredictor()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get form data
        pregnancies = float(request.form.get('pregnancies', 0))
        glucose = float(request.form.get('glucose', 0))
        blood_pressure = float(request.form.get('blood_pressure', 0))
        skin_thickness = float(request.form.get('skin_thickness', 0))
        insulin = float(request.form.get('insulin', 0))
        bmi = float(request.form.get('bmi', 0))
        dpf = float(request.form.get('dpf', 0))
        age = float(request.form.get('age', 0))
        
        # Prepare input for prediction
        input_data = np.array([[
            pregnancies, glucose, blood_pressure, skin_thickness, 
            insulin, bmi, dpf, age
        ]])
        
        # Get prediction
        prediction, probability = predictor.predict(input_data)
        
        # Get feature importance
        feature_importance = predictor.get_feature_importance()
        
        # Prepare data for visualization
        user_data = {
            'pregnancies': pregnancies,
            'glucose': glucose,
            'blood_pressure': blood_pressure,
            'skin_thickness': skin_thickness,
            'insulin': insulin,
            'bmi': bmi,
            'dpf': dpf,
            'age': age
        }
        
        # Generate AI health recommendations and insights
        from ai_health_advisor import AIHealthAdvisor
        advisor = AIHealthAdvisor()
        health_recommendations = advisor.generate_recommendations(user_data, prediction, probability)
        health_insight = advisor.generate_health_insight(user_data, prediction, probability)
        
        # Save prediction to database if user is logged in
        # TODO: Implement user authentication
        # if current_user.is_authenticated:
        #     prediction_record = Prediction(
        #         user_id=current_user.id,
        #         pregnancies=pregnancies,
        #         glucose=glucose,
        #         blood_pressure=blood_pressure,
        #         skin_thickness=skin_thickness,
        #         insulin=insulin,
        #         bmi=bmi,
        #         diabetes_pedigree_function=dpf,
        #         age=age,
        #         prediction=bool(prediction),
        #         probability=probability
        #     )
        #     db.session.add(prediction_record)
        #     db.session.commit()
        #     
        #     # Save AI recommendations to database
        #     advisor.save_recommendations(current_user, prediction_record, health_recommendations)
        
        return render_template(
            'result.html', 
            prediction=prediction, 
            probability=round(probability * 100, 2),
            user_data=user_data,
            feature_importance=feature_importance,
            recommendations=health_recommendations,
            health_insight=health_insight
        )
    except Exception as e:
        logging.error(f"Prediction error: {str(e)}")
        flash(f"An error occurred during prediction: {str(e)}", "danger")
        return redirect(url_for('index'))

@app.route('/about')
def about():
    return render_template('about.html')
    
@app.route('/pitch-deck')
def pitch_deck():
    return redirect('/static/pitch_deck/pitch.html')
    
@app.route('/pitch-deck-pdf')
def pitch_deck_pdf():
    return redirect('/static/pitch_deck/pitch.pdf.html')
    
@app.route('/download-pitch-deck')
def download_pitch_deck():
    return redirect('/static/pitch_deck/DiabetesPredict_Pitch_Deck.txt')

@app.route('/api/predict', methods=['POST'])
def api_predict():
    try:
        # Get JSON data
        data = request.get_json()
        
        # Prepare input for prediction
        input_data = np.array([[
            data.get('pregnancies', 0),
            data.get('glucose', 0),
            data.get('blood_pressure', 0),
            data.get('skin_thickness', 0),
            data.get('insulin', 0),
            data.get('bmi', 0),
            data.get('dpf', 0),
            data.get('age', 0)
        ]])
        
        # Get prediction
        prediction, probability = predictor.predict(input_data)
        
        return jsonify({
            'prediction': int(prediction),
            'probability': float(probability),
            'risk_level': 'High' if probability > 0.7 else 'Medium' if probability > 0.3 else 'Low'
        })
    except Exception as e:
        logging.error(f"API prediction error: {str(e)}")
        return jsonify({'error': str(e)}), 400

# Create database tables within the app context
with app.app_context():
    from models import User  # noqa: F401
    db.create_all()
