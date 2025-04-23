import os
import pandas as pd
import numpy as np
import pickle
import logging
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report

class DiabetesPredictor:
    def __init__(self, model_path=None):
        """
        Initialize the diabetes predictor.
        
        Args:
            model_path: Path to a pre-trained model. If None, a new model will be trained.
        """
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = [
            'Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 
            'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age'
        ]
        
        # Try to load a pre-trained model if provided
        if model_path and os.path.exists(model_path):
            try:
                with open(model_path, 'rb') as f:
                    model_data = pickle.load(f)
                    self.model = model_data['model']
                    self.scaler = model_data['scaler']
                logging.info("Pre-trained model loaded successfully")
            except Exception as e:
                logging.error(f"Error loading model: {str(e)}")
                self.train_model()
        else:
            # Train a new model
            self.train_model()
    
    def train_model(self):
        """Train a new diabetes prediction model using the Pima Indians Diabetes Dataset."""
        try:
            # Load the dataset
            data_path = os.path.join(os.path.dirname(__file__), 'static/data/diabetes.csv')
            df = pd.read_csv(data_path)
            
            # Replace zeros with NaN for specific columns where zero doesn't make sense
            zero_not_valid = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
            for column in zero_not_valid:
                df[column] = df[column].replace(0, np.nan)
            
            # Fill NaN values with the median of the column
            for column in zero_not_valid:
                df[column] = df[column].fillna(df[column].median())
            
            # Separate features and target
            X = df.drop('Outcome', axis=1)
            y = df['Outcome']
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Scale features
            self.scaler.fit(X_train)
            X_train_scaled = self.scaler.transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            # Train the model
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)
            self.model.fit(X_train_scaled, y_train)
            
            # Evaluate the model
            y_pred = self.model.predict(X_test_scaled)
            accuracy = accuracy_score(y_test, y_pred)
            report = classification_report(y_test, y_pred)
            
            logging.info(f"Model training completed with accuracy: {accuracy:.4f}")
            logging.debug(f"Classification report:\n{report}")
            
            # Save the model
            model_data = {
                'model': self.model,
                'scaler': self.scaler
            }
            with open('diabetes_model.pkl', 'wb') as f:
                pickle.dump(model_data, f)
            
        except Exception as e:
            logging.error(f"Error training model: {str(e)}")
            raise
    
    def predict(self, input_data):
        """
        Make a prediction based on input health metrics.
        
        Args:
            input_data: Numpy array or list of health metrics in the order:
                        [Pregnancies, Glucose, BloodPressure, SkinThickness,
                         Insulin, BMI, DiabetesPedigreeFunction, Age]
        
        Returns:
            tuple: (prediction, probability)
        """
        if self.model is None:
            raise ValueError("Model not initialized. Please train or load a model first.")
        
        try:
            # Scale the input data
            input_scaled = self.scaler.transform(input_data)
            
            # Make prediction
            prediction = self.model.predict(input_scaled)[0]
            
            # Get probability
            probabilities = self.model.predict_proba(input_scaled)[0]
            probability = probabilities[1]  # Probability of having diabetes (class 1)
            
            return prediction, probability
        
        except Exception as e:
            logging.error(f"Prediction error: {str(e)}")
            raise
    
    def get_feature_importance(self):
        """
        Get the importance of each feature in the prediction.
        
        Returns:
            dict: Feature names and their importance scores
        """
        if self.model is None:
            raise ValueError("Model not initialized. Please train or load a model first.")
        
        feature_importance = {}
        importance_scores = self.model.feature_importances_
        
        for i, feature in enumerate(self.feature_names):
            feature_importance[feature] = float(importance_scores[i])
        
        # Sort by importance
        sorted_importance = {k: v for k, v in sorted(
            feature_importance.items(), 
            key=lambda item: item[1], 
            reverse=True
        )}
        
        return sorted_importance
