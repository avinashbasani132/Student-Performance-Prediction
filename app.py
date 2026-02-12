from flask import Flask, render_template, request
import pandas as pd
import joblib

app = Flask(__name__)

# Load trained ML model
model = joblib.load("student_model.pkl")

@app.route("/", methods=["GET", "POST"])
def home():

    cgpa = None

    if request.method == "POST":

        try:
            # Get inputs
            hours = float(request.form["hours"])

            # USER ENTERS CGPA → convert to marks
            prev_cgpa = float(request.form["prev"])
            prev = prev_cgpa * 10

            extra = int(request.form["extra"])
            sleep = float(request.form["sleep"])
            papers = int(request.form["papers"])

            print("Converted inputs:", hours, prev, extra, sleep, papers)

            # Create dataframe
            input_data = pd.DataFrame(
                [[hours, prev, extra, sleep, papers]],
                columns=[
                    "Hours Studied",
                    "Previous Scores",
                    "Extracurricular Activities",
                    "Sleep Hours",
                    "Sample Question Papers Practiced"
                ]
            )

            # Predict marks
            prediction = model.predict(input_data)[0]

            print("Raw prediction:", prediction)

            # Keep within range
            prediction = max(0, min(100, prediction))

            # Convert marks → CGPA
            cgpa = round(prediction / 10, 2)

            print("Final CGPA:", cgpa)

        except Exception as e:
            print("Error:", e)
            cgpa = "Error"

    return render_template("index.html", cgpa=cgpa)


if __name__ == "__main__":
 app.run(host="0.0.0.0", port=5000, debug=True)

