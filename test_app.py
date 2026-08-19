import json
import sys
from app import app, predict_performance, calculate_goal_plan

# Force UTF-8 on stdout if available
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

print("=== 1. Direct Function Testing ===")
result, error, warnings = predict_performance(hours=6.0, prev_cgpa=8.0, extra=1, sleep=7.5, papers=5)
print("Predict Result CGPA:", result["cgpa"])
print("Predict Result Tier:", result["tier"])
print("Error:", error)
print("Warnings:", warnings)

plan = calculate_goal_plan(target_cgpa=9.0, prev_cgpa=7.5, extra=1, current_sleep=7.5, current_hours=5.0, current_papers=4)
print("\nGoal Plan Recommended Hours:", plan["recommended_study_hours"])
print("Goal Plan Recommended Papers:", plan["recommended_practice_papers"])

print("\n=== 2. Flask Client Route Testing ===")
client = app.test_client()

# GET /
res_home = client.get('/')
print("GET / -> Status:", res_home.status_code)
assert res_home.status_code == 200, f"Expected 200, got {res_home.status_code}"

# POST / (HTML Form Submit)
res_form = client.post('/', data={
    'hours': '6',
    'prev': '8.0',
    'extra': '1',
    'sleep': '7',
    'papers': '4'
})
print("POST / (Form) -> Status:", res_form.status_code)
assert res_form.status_code == 200, f"Expected 200, got {res_form.status_code}"

# POST /api/predict (JSON)
res_api_pred = client.post('/api/predict', json={
    'hours': 7,
    'prev': 8.5,
    'extra': 1,
    'sleep': 8,
    'papers': 6
})
print("POST /api/predict -> Status:", res_api_pred.status_code)
assert res_api_pred.status_code == 200, f"Expected 200, got {res_api_pred.status_code}"
data = res_api_pred.get_json()["data"]
print(f"Predicted CGPA: {data['cgpa']}, Grade: {data['grade']}, Tier: {data['tier']}")

# POST /api/goal-planner (JSON)
res_api_goal = client.post('/api/goal-planner', json={
    'target_cgpa': 9.2,
    'prev_cgpa': 7.8,
    'extra': 1,
    'sleep': 7.5,
    'hours': 5,
    'papers': 3
})
print("POST /api/goal-planner -> Status:", res_api_goal.status_code)
assert res_api_goal.status_code == 200, f"Expected 200, got {res_api_goal.status_code}"
plan_data = res_api_goal.get_json()["plan"]
print(f"Target: {plan_data['target_cgpa']}, Recommended Study: {plan_data['recommended_study_hours']}h, Effort: {plan_data['difficulty']}")

# GET /api/model-info (JSON)
res_api_info = client.get('/api/model-info')
print("GET /api/model-info -> Status:", res_api_info.status_code)
assert res_api_info.status_code == 200, f"Expected 200, got {res_api_info.status_code}"

# Test Hard Validation (hours + sleep > 24)
res_invalid = client.post('/api/predict', json={
    'hours': 15,
    'prev': 8,
    'extra': 1,
    'sleep': 12,
    'papers': 3
})
print("POST /api/predict (Invalid 27h) -> Status:", res_invalid.status_code)
assert res_invalid.status_code == 400, f"Expected 400, got {res_invalid.status_code}"

print("\n🎉 ALL TESTS PASSED SUCCESSFULLY WITH ZERO ERRORS!")
