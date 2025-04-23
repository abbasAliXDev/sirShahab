from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    predictions = db.relationship('Prediction', backref='user', lazy='dynamic')
    health_metrics = db.relationship('HealthMetric', backref='user', lazy='dynamic')
    health_goals = db.relationship('HealthGoal', backref='user', lazy='dynamic')
    recommendations = db.relationship('AIRecommendation', backref='user', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_recent_metrics(self, limit=5):
        """Get the user's most recent health metrics"""
        return self.health_metrics.order_by(HealthMetric.date.desc()).limit(limit).all()
        
    def get_predictions_over_time(self):
        """Get the user's prediction history to show trends"""
        return self.predictions.order_by(Prediction.timestamp.desc()).all()

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    pregnancies = db.Column(db.Float)
    glucose = db.Column(db.Float)
    blood_pressure = db.Column(db.Float)
    skin_thickness = db.Column(db.Float)
    insulin = db.Column(db.Float)
    bmi = db.Column(db.Float)
    diabetes_pedigree_function = db.Column(db.Float)
    age = db.Column(db.Float)
    prediction = db.Column(db.Boolean)
    probability = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)
    
    # Health factors/recommendations associated with this prediction
    recommendations = db.relationship('AIRecommendation', backref='prediction', lazy='dynamic')

class HealthMetric(db.Model):
    """Track user health metrics over time"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.Date, default=datetime.utcnow().date)
    
    # Basic health metrics
    weight = db.Column(db.Float)  # in kg
    height = db.Column(db.Float)  # in cm
    bmi = db.Column(db.Float)
    glucose = db.Column(db.Float)  # mg/dL
    blood_pressure_systolic = db.Column(db.Float)
    blood_pressure_diastolic = db.Column(db.Float)
    heart_rate = db.Column(db.Integer)  # beats per minute
    cholesterol_hdl = db.Column(db.Float)  # mg/dL
    cholesterol_ldl = db.Column(db.Float)  # mg/dL
    triglycerides = db.Column(db.Float)  # mg/dL
    
    # Physical activity
    steps = db.Column(db.Integer)
    physical_activity_minutes = db.Column(db.Integer)
    
    # Diet information
    calories_consumed = db.Column(db.Integer)
    carbs_grams = db.Column(db.Float)
    protein_grams = db.Column(db.Float)
    fat_grams = db.Column(db.Float)
    sugar_grams = db.Column(db.Float)
    fiber_grams = db.Column(db.Float)
    
    # Sleep and stress
    sleep_hours = db.Column(db.Float)
    stress_level = db.Column(db.Integer)  # Scale 1-10
    
    # Other
    notes = db.Column(db.Text)
    
    def __repr__(self):
        return f'<HealthMetric {self.date}>'

class HealthGoal(db.Model):
    """Store user health goals"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    target_date = db.Column(db.Date)
    
    # Goal metrics
    metric_type = db.Column(db.String(64))  # e.g., 'weight', 'glucose', 'bmi'
    current_value = db.Column(db.Float)
    target_value = db.Column(db.Float)
    
    # Status
    completed = db.Column(db.Boolean, default=False)
    completed_date = db.Column(db.Date)
    
    # Description
    description = db.Column(db.Text)
    notes = db.Column(db.Text)
    
    def __repr__(self):
        return f'<HealthGoal {self.metric_type}: {self.current_value} → {self.target_value}>'

class AIRecommendation(db.Model):
    """Store AI-generated health recommendations"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    prediction_id = db.Column(db.Integer, db.ForeignKey('prediction.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Recommendation content
    category = db.Column(db.String(64))  # e.g., 'diet', 'exercise', 'lifestyle'
    title = db.Column(db.String(128))
    content = db.Column(db.Text)
    priority = db.Column(db.String(20))  # 'high', 'medium', 'low'
    
    # User interaction
    viewed = db.Column(db.Boolean, default=False)
    viewed_at = db.Column(db.DateTime)
    user_rating = db.Column(db.Integer)  # Scale 1-5
    user_feedback = db.Column(db.Text)
    
    # Tracking
    implemented = db.Column(db.Boolean, default=False)
    implemented_at = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<AIRecommendation {self.title}>'
