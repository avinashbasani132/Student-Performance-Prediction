import pandas as pd

# Load dataset
data = pd.read_csv("student_performance.csv")

print(data.head())
print(data.info())
