from flask import Flask, render_template, request
import pandas as pd
import joblib

# Initialize Flask app
app = Flask(__name__)

# Load trained ML model
model = joblib.load("student_model.pkl")


@app.route("/", methods=["GET", "POST"])
def home():

    cgpa = None
    error = None
    warnings = []

    if request.method == "POST":
        try:
            # Get form values
            hours = float(request.form["hours"])
            prev_cgpa = float(request.form["prev"])
            extra = int(request.form["extra"])
            sleep = float(request.form["sleep"])
            papers = int(request.form["papers"])

            # Convert CGPA to marks (because model trained on marks)
            prev_marks = prev_cgpa * 10

            # ❌ Hard Validation: Impossible case
            if hours + sleep > 24:
                error = "In a day, there are only 24 hours."

            else:
                # ⚠️ Soft Warning: Study >= 20
                if hours > 20:
                    warnings.append(
                        "If you study more than 20 hours, it may affect your health."
                    )

                # ⚠️ Soft Warning: Sleep >= 20
                if sleep > 20:
                    warnings.append(
                        "If you sleep more than 20 hours, it may affect your health."
                    )

                # Prepare input data for prediction
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

                # Predict
                prediction = model.predict(input_data)[0]

                # Keep prediction within safe range
                prediction = max(0, min(100, prediction))

                # Convert marks to CGPA
                cgpa = round(prediction / 10, 2)

        except Exception as e:
            print("Error:", e)
            error = "Invalid input. Please enter correct values."

    return render_template(
        "index.html",
        cgpa=cgpa,
        error=error,
        warnings=warnings
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)