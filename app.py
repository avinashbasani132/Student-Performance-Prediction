from flask import Flask, render_template, request
import pandas as pd
import joblib

app = Flask(__name__)

model = joblib.load("student_model.pkl")

@app.route("/", methods=["GET", "POST"])
def home():

    cgpa = None
    error = None

    if request.method == "POST":

        try:
            hours = float(request.form["hours"])
            prev_cgpa = float(request.form["prev"])
            prev = prev_cgpa * 10
            extra = int(request.form["extra"])
            sleep = float(request.form["sleep"])
            papers = int(request.form["papers"])

            # ✅ Validation
            if not (1 <= hours <= 24):
                error = "Hours studied must be between 1 and 24."

            elif not (0 <= prev_cgpa <= 10):
                error = "CGPA must be between 0 and 10."

            elif not (0 <= sleep <= 24):
                error = "Sleep hours must be between 0 and 24."

            elif not (0 <= papers <= 10):
                error = "Subjects must be between 0 and 10."

            else:
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

                prediction = model.predict(input_data)[0]
                prediction = max(0, min(100, prediction))
                cgpa = round(prediction / 10, 2)

        except:
            error = "Invalid input. Please enter correct values."

    return render_template("index.html", cgpa=cgpa, error=error)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
