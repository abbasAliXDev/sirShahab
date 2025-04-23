import os
import logging
import openai
from datetime import datetime
from models import AIRecommendation

# Configure OpenAI API
openai.api_key = os.environ.get("OPENAI_API_KEY")
# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user
MODEL_NAME = "gpt-4o"

class AIHealthAdvisor:
    """
    Uses OpenAI to generate personalized health recommendations based on 
    diabetes risk assessment and health metrics.
    """
    
    def __init__(self):
        if not openai.api_key:
            logging.warning("OpenAI API key not found. AI recommendations will not be available.")
    
    def generate_recommendations(self, user_data, prediction, probability):
        """
        Generate personalized health recommendations based on user data and prediction.
        
        Args:
            user_data (dict): User health metrics
            prediction (int): 0 or 1 indicating diabetes prediction (1 = positive)
            probability (float): Probability of having diabetes (0-1)
            
        Returns:
            list: List of recommendation dictionaries with categories and content
        """
        if not openai.api_key:
            return self._get_fallback_recommendations(user_data, prediction, probability)
        
        try:
            # Format the user data for the prompt
            user_metrics = "\n".join([f"- {k.replace('_', ' ').title()}: {v}" for k, v in user_data.items()])
            risk_level = "High" if probability > 0.7 else "Medium" if probability > 0.3 else "Low"
            risk_percentage = f"{probability * 100:.1f}%"
            
            # Create the prompt for OpenAI
            prompt = f"""
            As a healthcare AI assistant, generate personalized health recommendations for a patient based on their diabetes risk assessment.
            
            PATIENT DATA:
            {user_metrics}
            
            DIABETES RISK ASSESSMENT:
            - Prediction: {"Positive" if prediction == 1 else "Negative"} for diabetes risk
            - Risk Level: {risk_level} ({risk_percentage})
            
            Please provide 3-5 specific, actionable health recommendations in the following categories:
            1. Diet
            2. Physical Activity
            3. Lifestyle Changes
            4. Monitoring and Medical Follow-up
            
            For each recommendation, include:
            - A clear, concise title
            - Detailed explanation with scientific rationale
            - Practical steps for implementation
            - Expected health benefits
            
            Format each recommendation as a JSON object with the following structure:
            {{
                "category": "diet|exercise|lifestyle|monitoring",
                "title": "Concise recommendation title",
                "content": "Detailed explanation and implementation steps",
                "priority": "high|medium|low"
            }}
            
            Prioritize recommendations based on the patient's specific risk factors. Set priority based on impact on diabetes risk.
            """
            
            try:
                # Call OpenAI API
                response = openai.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[
                        {"role": "system", "content": "You are a healthcare AI specializing in diabetes prevention and management."},
                        {"role": "user", "content": prompt}
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.5,
                    max_tokens=1500
                )
                
                # Parse the response
                recommendations_text = response.choices[0].message.content
                import json
                recommendations = json.loads(recommendations_text)
                
                # If the response has a 'recommendations' key, use that
                if 'recommendations' in recommendations:
                    return recommendations['recommendations']
                
                # Otherwise, assume the response is a list of recommendations
                return recommendations
            except Exception as api_error:
                logging.error(f"OpenAI API error: {str(api_error)}")
                # Fall back to pre-generated recommendations
                return self._get_fallback_recommendations(user_data, prediction, probability)
        
        except Exception as e:
            logging.error(f"Error generating AI recommendations: {str(e)}")
            return self._get_fallback_recommendations(user_data, prediction, probability)
    
    def _get_fallback_recommendations(self, user_data, prediction, probability):
        """
        Provide pre-generated recommendations when OpenAI API is unavailable.
        
        Args:
            user_data (dict): User health metrics
            prediction (int): 0 or 1 indicating diabetes prediction
            probability (float): Probability of having diabetes
            
        Returns:
            list: List of recommendation dictionaries
        """
        risk_level = "high" if probability > 0.7 else "medium" if probability > 0.3 else "low"
        has_high_glucose = user_data.get('glucose', 0) > 125
        has_high_bmi = user_data.get('bmi', 0) > 30
        has_high_bp = user_data.get('blood_pressure', 0) > 90
        is_older = user_data.get('age', 0) > 45
        
        recommendations = []
        
        # Diet recommendations
        diet_priority = "high" if has_high_glucose else "medium"
        diet_rec = {
            "category": "diet",
            "title": "Adopt a Balanced, Low-Glycemic Diet",
            "content": """
                <p>A balanced diet focused on low-glycemic foods can help maintain healthy blood glucose levels and reduce diabetes risk.</p>
                
                <h5>Key Components:</h5>
                <ul>
                    <li>Emphasize fiber-rich foods like vegetables, legumes, and whole grains</li>
                    <li>Choose lean proteins (fish, poultry, tofu) over processed meats</li>
                    <li>Include healthy fats from sources like olive oil, nuts, and avocados</li>
                    <li>Limit added sugars, refined carbohydrates, and processed foods</li>
                    <li>Practice portion control, especially with carbohydrate-rich foods</li>
                </ul>
                
                <h5>Benefits:</h5>
                <p>This eating pattern helps stabilize blood sugar, improve insulin sensitivity, maintain a healthy weight, and reduce inflammation.</p>
                
                <h5>Implementation:</h5>
                <p>Start by replacing one refined carbohydrate meal with a whole-food alternative each day, gradually increasing the proportion of whole foods in your diet.</p>
            """,
            "priority": diet_priority
        }
        recommendations.append(diet_rec)
        
        # Physical activity
        exercise_priority = "high" if has_high_bmi else "medium"
        exercise_rec = {
            "category": "exercise",
            "title": "Establish Regular Physical Activity Routine",
            "content": """
                <p>Regular physical activity is crucial for diabetes prevention as it helps improve insulin sensitivity and maintain healthy weight.</p>
                
                <h5>Key Components:</h5>
                <ul>
                    <li>Aim for at least 150 minutes of moderate-intensity aerobic activity weekly</li>
                    <li>Include strength training exercises 2-3 times per week</li>
                    <li>Incorporate daily movement (walking, taking stairs) into your routine</li>
                    <li>Include flexibility exercises like stretching or yoga</li>
                    <li>Break up sitting time with short activity breaks every 30 minutes</li>
                </ul>
                
                <h5>Benefits:</h5>
                <p>Exercise helps your cells become more sensitive to insulin, lowers blood glucose, reduces body fat, improves heart health, and enhances overall well-being.</p>
                
                <h5>Implementation:</h5>
                <p>Start with 10-minute walking sessions three times daily, gradually increasing duration and intensity as your fitness improves. Find activities you enjoy to make exercise sustainable.</p>
            """,
            "priority": exercise_priority
        }
        recommendations.append(exercise_rec)
        
        # Lifestyle changes
        lifestyle_priority = "medium"
        lifestyle_rec = {
            "category": "lifestyle",
            "title": "Prioritize Quality Sleep and Stress Management",
            "content": """
                <p>Poor sleep and chronic stress can negatively impact blood glucose levels and increase diabetes risk.</p>
                
                <h5>Key Components:</h5>
                <ul>
                    <li>Aim for 7-9 hours of quality sleep nightly</li>
                    <li>Establish a regular sleep schedule and bedtime routine</li>
                    <li>Practice stress-reduction techniques like meditation, deep breathing, or progressive muscle relaxation</li>
                    <li>Limit screen time before bed</li>
                    <li>Create a sleep-friendly environment (cool, dark, quiet)</li>
                </ul>
                
                <h5>Benefits:</h5>
                <p>Adequate sleep and stress management help regulate hormones that affect blood sugar, including cortisol and growth hormone. They also support healthy eating habits and exercise consistency.</p>
                
                <h5>Implementation:</h5>
                <p>Begin with a 10-minute daily relaxation practice and establish a consistent bedtime. Keep a sleep log to identify patterns and areas for improvement.</p>
            """,
            "priority": lifestyle_priority
        }
        recommendations.append(lifestyle_rec)
        
        # Monitoring recommendation
        monitoring_priority = "high" if prediction == 1 or probability > 0.5 else "medium"
        monitoring_rec = {
            "category": "monitoring",
            "title": "Regular Health Monitoring and Medical Check-ups",
            "content": """
                <p>Regular monitoring of health metrics and professional medical evaluation are essential for early detection and prevention of diabetes.</p>
                
                <h5>Key Components:</h5>
                <ul>
                    <li>Schedule annual physical exams including blood glucose screening</li>
                    <li>Monitor blood pressure regularly</li>
                    <li>Track weight changes and body measurements</li>
                    <li>Be aware of diabetes symptoms (increased thirst, frequent urination, unexplained weight loss)</li>
                    <li>Consider using a health tracking app to record metrics over time</li>
                </ul>
                
                <h5>Benefits:</h5>
                <p>Regular monitoring allows for early detection of pre-diabetes or diabetes, enabling prompt intervention. It also provides feedback on the effectiveness of lifestyle changes.</p>
                
                <h5>Implementation:</h5>
                <p>Schedule a comprehensive health check-up with your healthcare provider. Discuss your diabetes risk assessment and develop a personalized monitoring plan.</p>
            """,
            "priority": monitoring_priority
        }
        recommendations.append(monitoring_rec)
        
        return recommendations
    
    def save_recommendations(self, user, prediction_obj, recommendations):
        """
        Save generated recommendations to the database.
        
        Args:
            user: User model object
            prediction_obj: Prediction model object
            recommendations: List of recommendation dictionaries
            
        Returns:
            list: List of AIRecommendation model objects
        """
        saved_recommendations = []
        
        for rec in recommendations:
            recommendation = AIRecommendation(
                user_id=user.id,
                prediction_id=prediction_obj.id,
                category=rec.get('category', 'general'),
                title=rec.get('title', 'Health Recommendation'),
                content=rec.get('content', ''),
                priority=rec.get('priority', 'medium'),
                created_at=datetime.utcnow()
            )
            
            from app import db
            db.session.add(recommendation)
            saved_recommendations.append(recommendation)
        
        try:
            from app import db
            db.session.commit()
        except Exception as e:
            from app import db
            db.session.rollback()
            logging.error(f"Error saving recommendations: {str(e)}")
        
        return saved_recommendations

    def generate_health_insight(self, user_data, prediction, probability):
        """
        Generate a personalized health insight summary based on user data.
        
        Args:
            user_data (dict): User health metrics
            prediction (int): 0 or 1 indicating diabetes prediction
            probability (float): Probability of having diabetes (0-1)
            
        Returns:
            str: Personalized health insight text
        """
        if not openai.api_key:
            return self._get_fallback_health_insight(user_data, prediction, probability)
        
        try:
            # Format the user data for the prompt
            user_metrics = "\n".join([f"- {k.replace('_', ' ').title()}: {v}" for k, v in user_data.items()])
            risk_level = "High" if probability > 0.7 else "Medium" if probability > 0.3 else "Low"
            risk_percentage = f"{probability * 100:.1f}%"
            
            # Create the prompt for OpenAI
            prompt = f"""
            As a healthcare AI assistant, provide a brief, personalized health insight for a patient based on their diabetes risk assessment.
            
            PATIENT DATA:
            {user_metrics}
            
            DIABETES RISK ASSESSMENT:
            - Prediction: {"Positive" if prediction == 1 else "Negative"} for diabetes risk
            - Risk Level: {risk_level} ({risk_percentage})
            
            Provide a concise, personalized summary (200-300 words) that:
            1. Explains the patient's current risk level in understandable terms
            2. Highlights the 2-3 most significant factors affecting their risk
            3. Offers encouragement and a positive perspective
            4. Suggests their most important next steps
            
            Use a compassionate, informative tone. Avoid medical jargon and explain concepts clearly.
            """
            
            try:
                # Call OpenAI API
                response = openai.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[
                        {"role": "system", "content": "You are a healthcare AI specializing in diabetes prevention and management."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=600
                )
                
                # Return the response
                insight = response.choices[0].message.content
                return insight
            
            except Exception as api_error:
                logging.error(f"OpenAI API error in health insight: {str(api_error)}")
                return self._get_fallback_health_insight(user_data, prediction, probability)
            
        except Exception as e:
            logging.error(f"Error generating health insight: {str(e)}")
            return self._get_fallback_health_insight(user_data, prediction, probability)
    
    def _get_fallback_health_insight(self, user_data, prediction, probability):
        """
        Provide a pre-generated health insight when the OpenAI API is unavailable.
        
        Args:
            user_data (dict): User health metrics
            prediction (int): 0 or 1 indicating diabetes prediction
            probability (float): Probability of having diabetes (0-1)
            
        Returns:
            str: Fallback health insight text
        """
        # Determine risk level and key metrics
        risk_level = "high" if probability > 0.7 else "medium" if probability > 0.3 else "low"
        risk_percentage = round(probability * 100, 1)
        
        # Extract key health metrics
        glucose = user_data.get('glucose', 0)
        bmi = user_data.get('bmi', 0)
        blood_pressure = user_data.get('blood_pressure', 0)
        age = user_data.get('age', 0)
        
        # Identify concerning factors
        concerning_factors = []
        if glucose > 125:
            concerning_factors.append("elevated blood glucose")
        if bmi > 30:
            concerning_factors.append("BMI in the obese range")
        elif bmi > 25:
            concerning_factors.append("BMI in the overweight range")
        if blood_pressure > 90:
            concerning_factors.append("elevated blood pressure")
        if age > 45:
            concerning_factors.append("age above 45")
            
        # Generate insight text based on risk level and factors
        if prediction == 1 or risk_level == "high":
            insight = f"""
            <p>Based on your health assessment, your current diabetes risk is at a <strong>higher level ({risk_percentage}%)</strong>. This means that your combination of health factors suggests an increased likelihood of developing type 2 diabetes compared to the general population.</p>
            
            <p>The analysis identified several factors contributing to your risk profile:
            """
            
            if concerning_factors:
                insight += "<ul>"
                for factor in concerning_factors[:3]:
                    insight += f"<li>Your {factor} is a significant factor</li>"
                insight += "</ul>"
            else:
                insight += "<p>While no single factor stands out dramatically, the combination of your metrics suggests increased risk.</p>"
                
            insight += f"""
            <p>It's important to understand that having risk factors doesn't mean you'll definitely develop diabetes. Many people with similar profiles successfully reduce their risk through lifestyle modifications.</p>
            
            <p>Consider scheduling a consultation with a healthcare provider to discuss your results and develop a personalized prevention plan. Focus on areas where you can make meaningful changes, such as improving your diet with more whole foods, engaging in regular physical activity, and maintaining consistent health monitoring.</p>
            
            <p>Remember, small, sustainable changes often lead to the most significant long-term health improvements.</p>
            """
            
        elif risk_level == "medium":
            insight = f"""
            <p>Your health assessment indicates a <strong>moderate diabetes risk level ({risk_percentage}%)</strong>. This suggests that while you have some risk factors, you're not in the highest risk category.</p>
            
            <p>Key factors influencing your risk assessment:
            """
            
            if concerning_factors:
                insight += "<ul>"
                for factor in concerning_factors[:2]:
                    insight += f"<li>Your {factor} contributes to your risk profile</li>"
                insight += "</ul>"
            else:
                insight += "<p>Your overall health profile shows some areas that could be optimized.</p>"
                
            insight += f"""
            <p>The good news is that moderate risk means you have an excellent opportunity to prevent diabetes development through proactive lifestyle choices. Many people at this risk level successfully avoid diabetes entirely.</p>
            
            <p>Consider incorporating more regular physical activity into your routine and reviewing your dietary choices with a focus on reducing refined carbohydrates. Regular health check-ups can help track your progress and catch any changes early.</p>
            
            <p>With consistent attention to healthy habits, you can significantly reduce your diabetes risk over time.</p>
            """
            
        else:  # low risk
            insight = f"""
            <p>Your health assessment shows a <strong>lower diabetes risk level ({risk_percentage}%)</strong>, which is positive news about your current health status.</p>
            
            <p>While your overall risk is low, it's still beneficial to maintain awareness of the factors that contribute to metabolic health:
            """
            
            if concerning_factors:
                insight += "<ul>"
                for factor in concerning_factors[:1]:
                    insight += f"<li>Your {factor} is something to keep an eye on</li>"
                insight += "</ul>"
            else:
                insight += "<p>Your current health metrics are generally within healthy ranges.</p>"
                
            insight += f"""
            <p>Even with lower risk, maintaining healthy habits is important for long-term well-being. Continue with regular physical activity, a balanced diet rich in whole foods, and routine health check-ups.</p>
            
            <p>Your current health practices appear to be working well - keep up the good work! This is an excellent foundation for lifelong health.</p>
            """
            
        return insight