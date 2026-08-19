import warnings
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import joblib

warnings.filterwarnings("ignore")

# Load Dataset
print("Loading Student_Performance.csv...")
data = pd.read_csv("Student_Performance.csv")

# Preprocessing: Map Extracurricular Activities
data["Extracurricular Activities"] = data["Extracurricular Activities"].map({
    "Yes": 1,
    "No": 0
})

# Split Features & Target
X = data.drop("Performance Index", axis=1)
y = data["Performance Index"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train Model
print("Training Random Forest Regressor...")
model = RandomForestRegressor(
    n_estimators=200,
    max_depth=10,
    random_state=42
)
model.fit(X_train, y_train)

# Evaluate Model
y_pred = model.predict(X_test)
r2 = r2_score(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)

print(f"Model Trained Successfully!")
print(f"R² Score: {r2:.4f}")
print(f"Mean Squared Error (MSE): {mse:.4f}")

# Save Model
joblib.dump(model, "student_model.pkl")
print("Model saved to student_model.pkl successfully!")
