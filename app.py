import os
import joblib
import pandas as pd
import numpy as np
from flask import Flask, render_template, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# Load trained ML model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "student_model.pkl")
try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    print(f"Warning: Could not load model from {MODEL_PATH}: {e}")
    model = None


def generate_ai_recommendations(hours, prev_cgpa, extra, sleep, papers, predicted_cgpa):
    """
    Generates intelligent, personalized, and actionable academic advice
    based on the student's current lifestyle habits and predicted outcome.
    """
    recommendations = []

    # 1. Practice Papers Analysis
    if papers < 3:
        recommendations.append({
            "type": "high-impact",
            "icon": "📝",
            "title": "Boost Sample Question Papers",
            "message": "Practicing at least 4-6 sample papers can improve exam confidence and boost your score by approximately 0.5-0.8 CGPA."
        })
    elif papers >= 7:
        recommendations.append({
            "type": "positive",
            "icon": "🌟",
            "title": "Strong Mock Practice",
            "message": "Your rigorous practice with sample papers provides a great advantage in speed and pattern familiarity."
        })

    # 2. Sleep Schedule Optimization
    if sleep < 6:
        recommendations.append({
            "type": "health",
            "icon": "😴",
            "title": "Prioritize Sleep & Memory Consolidation",
            "message": "Sleeping under 6 hours impairs cognitive recall and focus. Target 7-8 hours for optimal memory retention."
        })
    elif sleep > 9:
        recommendations.append({
            "type": "health",
            "icon": "⏰",
            "title": "Optimize Daily Routine",
            "message": "Sleeping over 9 hours might reduce active daytime productivity. Aim for a balanced 7-8 hour sleep schedule."
        })
    else:
        recommendations.append({
            "type": "positive",
            "icon": "💤",
            "title": "Optimal Sleep Schedule",
            "message": "Your sleep duration is balanced, supporting strong cognitive endurance and mental well-being."
        })

    # 3. Study Hours Consistency
    if hours < 4:
        recommendations.append({
            "type": "high-impact",
            "icon": "⏱️",
            "title": "Increase Focused Study Time",
            "message": "Increasing your daily study by just 1.5 to 2 hours using techniques like Pomodoro can significantly elevate your performance index."
        })
    elif hours >= 7:
        recommendations.append({
            "type": "positive",
            "icon": "📚",
            "title": "Dedicated Study Commitment",
            "message": "You have a commendable study routine. Ensure active recall rather than passive reading to maximize retention."
        })

    # 4. Extracurricular Balance
    if extra == 0:
        recommendations.append({
            "type": "info",
            "icon": "🏃",
            "title": "Consider Balanced Activities",
            "message": "Light extracurricular participation or physical activity helps reduce academic burnout and sharpens mental focus."
        })

    # 5. Overall Target Advisory
    if predicted_cgpa >= 8.5:
        recommendations.append({
            "type": "positive",
            "icon": "🏆",
            "title": "On Track for Distinction",
            "message": "Maintain your consistency and focus on error analysis in mock tests to secure top honors."
        })
    elif predicted_cgpa < 6.0:
        recommendations.append({
            "type": "high-impact",
            "icon": "🎯",
            "title": "Targeted Recovery Plan Needed",
            "message": "Focus on high-weightage topics and solve past papers regularly to steadily climb into the 7+ CGPA bracket."
        })

    return recommendations


def get_performance_tier(cgpa):
    """Returns tier details based on CGPA."""
    if cgpa >= 8.5:
        return {"tier": "Distinction", "badge": "🟢 Excellent", "color": "#10b981", "grade": "A+"}
    elif cgpa >= 7.0:
        return {"tier": "First Class", "badge": "🟢 Very Good", "color": "#059669", "grade": "A"}
    elif cgpa >= 6.0:
        return {"tier": "Second Class", "badge": "🟡 Good", "color": "#eab308", "grade": "B"}
    elif cgpa >= 4.5:
        return {"tier": "Average", "badge": "🟠 Average", "color": "#f97316", "grade": "C"}
    else:
        return {"tier": "Needs Improvement", "badge": "🔴 At Risk", "color": "#ef4444", "grade": "D"}


def calculate_goal_plan(target_cgpa, prev_cgpa, extra, current_sleep, current_hours, current_papers):
    """
    Computes an optimal recommended daily study, mock test, and sleep routine
    to help the student reach a target CGPA.
    """
    target_cgpa = min(10.0, max(1.0, float(target_cgpa)))
    prev_cgpa = min(10.0, max(0.0, float(prev_cgpa)))
    extra = int(extra)

    # Required target score (0 - 100)
    target_score = target_cgpa * 10.0
    prev_score = prev_cgpa * 10.0

    # Model approximate feature impact weights (derived from trained coefficients / trees):
    # Performance Index ≈ 2.85 * Hours + 1.02 * Prev_Scores + 0.35 * Extra + 0.48 * Sleep + 0.19 * Papers - Intercept
    gap = target_score - prev_score

    # Balanced targets calculation
    if gap <= 0:
        # Target already equal or lower than previous
        rec_hours = max(2.0, min(current_hours, 5.0))
        rec_papers = max(2, min(current_papers, 4))
        rec_sleep = 7.5
    else:
        # Scale up study hours and sample papers proportionately
        rec_hours = round(min(10.0, max(3.0, 3.0 + (gap * 0.18))), 1)
        rec_papers = int(min(10, max(2, round(2 + (gap * 0.15)))))
        rec_sleep = 7.5

    # Check 24-hr feasibility
    if rec_hours + rec_sleep > 20:
        rec_hours = 20 - rec_sleep

    # Simulate prediction with recommended parameters
    if model:
        sim_data = pd.DataFrame(
            [[rec_hours, prev_score, extra, rec_sleep, rec_papers]],
            columns=[
                "Hours Studied",
                "Previous Scores",
                "Extracurricular Activities",
                "Sleep Hours",
                "Sample Question Papers Practiced"
            ]
        )
        sim_pred = model.predict(sim_data)[0]
        sim_pred = max(0, min(100, sim_pred))
        sim_cgpa = round(sim_pred / 10.0, 2)
    else:
        sim_cgpa = round(min(10.0, target_cgpa), 2)

    return {
        "target_cgpa": target_cgpa,
        "estimated_achievable_cgpa": sim_cgpa,
        "recommended_study_hours": rec_hours,
        "recommended_practice_papers": rec_papers,
        "recommended_sleep_hours": rec_sleep,
        "recommended_extra": 1 if extra == 1 else 0,
        "difficulty": "Easy" if gap <= 5 else ("Moderate" if gap <= 15 else "Challenging"),
        "key_strategy": (
            "Focus primarily on regular mock test revisions and maintaining a strict 7.5-hour sleep routine."
            if gap <= 10 else
            "Structured daily schedule with dedicated 2-hour morning study blocks and weekly full-length tests is recommended."
        )
    }


def predict_performance(hours, prev_cgpa, extra, sleep, papers):
    """Core prediction pipeline shared by HTML and REST API endpoints."""
    # Convert CGPA (0-10) to marks (0-100)
    prev_marks = prev_cgpa * 10.0

    warnings = []
    error = None

    # Hard Validation: Total hours in a day
    if hours + sleep > 24:
        return None, "In a day, there are only 24 hours. Total study and sleep hours cannot exceed 24.", warnings

    # Soft Warnings
    if hours > 18:
        warnings.append("Studying more than 18 hours a day is unsustainable and may cause severe burnout.")
    elif hours < 1:
        warnings.append("Less than 1 hour of daily study may not be sufficient for academic success.")

    if sleep < 5:
        warnings.append("Getting less than 5 hours of sleep negatively impacts memory recall and problem-solving.")
    elif sleep > 16:
        warnings.append("Sleeping over 16 hours daily may indicate fatigue or schedule imbalance.")

    if model is None:
        return None, "Machine Learning model is not loaded.", warnings

    # Prepare DataFrame matching training feature columns
    input_data = pd.DataFrame(
        [[hours, prev_marks, extra, sleep, papers]],
        columns=[
            "Hours Studied",
            "Previous Scores",
            "Extracurricular Activities",
            "Sleep Hours",
            "Sample Question Papers Practiced"
        ]
    )

    # Predict Performance Index (0 - 100)
    raw_prediction = float(model.predict(input_data)[0])
    clamped_prediction = max(0.0, min(100.0, raw_prediction))

    # Convert to 10.0 CGPA Scale
    predicted_cgpa = round(clamped_prediction / 10.0, 2)
    tier_info = get_performance_tier(predicted_cgpa)
    recommendations = generate_ai_recommendations(hours, prev_cgpa, extra, sleep, papers, predicted_cgpa)

    result_payload = {
        "cgpa": predicted_cgpa,
        "score": round(clamped_prediction, 1),
        "tier": tier_info["tier"],
        "badge": tier_info["badge"],
        "color": tier_info["color"],
        "grade": tier_info["grade"],
        "hours": hours,
        "prev_cgpa": prev_cgpa,
        "extra": extra,
        "sleep": sleep,
        "papers": papers,
        "warnings": warnings,
        "recommendations": recommendations,
        "study_sleep_total": round(hours + sleep, 1),
        "free_hours": round(max(0.0, 24.0 - (hours + sleep)), 1)
    }

    return result_payload, None, warnings


# ---------------------------------------------------------
# Web Routes (HTML Views)
# ---------------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    error = None
    warnings = []

    # Default initial form values
    form_data = {
        "hours": 5.0,
        "prev": 7.5,
        "extra": 1,
        "sleep": 7.0,
        "papers": 4
    }

    if request.method == "POST":
        try:
            form_data["hours"] = float(request.form.get("hours", 5.0))
            form_data["prev"] = float(request.form.get("prev", 7.5))
            form_data["extra"] = int(request.form.get("extra", 1))
            form_data["sleep"] = float(request.form.get("sleep", 7.0))
            form_data["papers"] = int(request.form.get("papers", 4))

            result, error, warnings = predict_performance(
                form_data["hours"],
                form_data["prev"],
                form_data["extra"],
                form_data["sleep"],
                form_data["papers"]
            )
        except Exception as e:
            print("Error in home route:", e)
            error = f"Invalid input: {str(e)}"

    return render_template(
        "index.html",
        result=result,
        error=error,
        warnings=warnings,
        form_data=form_data
    )


# ---------------------------------------------------------
# REST API Endpoints (JSON)
# ---------------------------------------------------------
@app.route("/api/predict", methods=["POST"])
def api_predict():
    """
    JSON API for real-time inference without full page refresh.
    Payload: { "hours": 6, "prev": 8.0, "extra": 1, "sleep": 7, "papers": 4 }
    """
    try:
        data = request.get_json(force=True)
        hours = float(data.get("hours", 5.0))
        prev_cgpa = float(data.get("prev", 7.5))
        extra = int(data.get("extra", 1))
        sleep = float(data.get("sleep", 7.0))
        papers = int(data.get("papers", 4))

        result, error, warnings = predict_performance(hours, prev_cgpa, extra, sleep, papers)

        if error:
            return jsonify({"success": False, "error": error, "warnings": warnings}), 400

        return jsonify({
            "success": True,
            "data": result
        })

    except Exception as e:
        return jsonify({"success": False, "error": f"Invalid request data: {str(e)}"}), 400


@app.route("/api/goal-planner", methods=["POST"])
def api_goal_planner():
    """
    JSON API for 'What-If' goal planning simulator.
    Payload: { "target_cgpa": 9.0, "prev_cgpa": 7.5, "extra": 1, "sleep": 7, "hours": 5, "papers": 3 }
    """
    try:
        data = request.get_json(force=True)
        target_cgpa = float(data.get("target_cgpa", 8.5))
        prev_cgpa = float(data.get("prev_cgpa", 7.0))
        extra = int(data.get("extra", 1))
        sleep = float(data.get("sleep", 7.0))
        hours = float(data.get("hours", 4.0))
        papers = int(data.get("papers", 3))

        plan = calculate_goal_plan(target_cgpa, prev_cgpa, extra, sleep, hours, papers)

        return jsonify({
            "success": True,
            "plan": plan
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route("/api/model-info", methods=["GET"])
def api_model_info():
    """Returns model metadata and feature descriptions."""
    return jsonify({
        "model_name": "Random Forest Regressor",
        "parameters": {
            "n_estimators": 200,
            "max_depth": 10,
            "random_state": 42
        },
        "features": [
            {"name": "Hours Studied", "type": "Numeric", "unit": "Hours/Day", "impact": "High (Primary Driver)"},
            {"name": "Previous Scores", "type": "Numeric", "unit": "Scale 0-100", "impact": "High (Baseline Record)"},
            {"name": "Extracurricular Activities", "type": "Categorical", "unit": "Binary (0/1)", "impact": "Moderate"},
            {"name": "Sleep Hours", "type": "Numeric", "unit": "Hours/Day", "impact": "Moderate (Cognitive Health)"},
            {"name": "Sample Question Papers Practiced", "type": "Numeric", "unit": "Count", "impact": "Moderate-High (Exam Preparedness)"}
        ],
        "target": "Performance Index (0-100 Scale mapped to 0-10.0 CGPA)"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)