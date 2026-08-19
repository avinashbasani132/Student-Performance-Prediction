# 🎓 AI Student Performance & CGPA Predictor & Advisor

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.9+" />
  <img src="https://img.shields.io/badge/Flask-2.x-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask" />
  <img src="https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="scikit-learn" />
  <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas" />
  <img src="https://img.shields.io/badge/Gunicorn-499848?style=for-the-badge&logo=gunicorn&logoColor=white" alt="Gunicorn" />
  <img src="https://img.shields.io/badge/Status-Active%20%2F%20Production%20Ready-brightgreen?style=for-the-badge" alt="Status" />
</p>

<p align="center">
  <strong>A full-stack, AI-powered academic performance platform featuring a modern glassmorphic dashboard, real-time CGPA estimation, personalized AI study action plans, a "What-If" goal planner, and RESTful API endpoints.</strong>
</p>

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [Dataset & Feature Description](#-dataset--feature-description)
- [Machine Learning Model](#-machine-learning-model)
- [REST API Documentation](#-rest-api-documentation)
- [Project Directory Structure](#-project-directory-structure)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation & Setup](#installation--setup)
  - [Running the Application](#running-the-application)
- [Model Training & Pipeline](#-model-training--pipeline)
- [Deployment](#-deployment)
- [Validation & Edge-Case Handling](#-validation--edge-case-handling)
- [Future Enhancements](#-future-enhancements)
- [Author & Acknowledgments](#-author--acknowledgments)

---

## 📖 Overview

The **AI Student Performance Predictor & Advisor** is an end-to-end intelligent web application designed for students, educators, and academic advisors. By analyzing behavioral and academic parameters, it accurately forecasts expected CGPA and generates personalized, actionable recommendations to improve study efficiency, sleep balance, and mock exam readiness.

---

## ✨ Key Features

- **🔮 Smart Real-Time CGPA Predictor:** Instant prediction of academic outcomes with dynamic SVG circular radial gauges, grading tiers (A+, A, B, C, D), and score index conversions.
- **💡 Personalized AI Action Plan:** Rule-based AI advisory engine generating customized recommendations based on sleep balance, study habits, and question paper practice.
- **🎯 "What-If" Target Goal Planner:** Reverse-simulation tool that computes the exact daily study routine, sample papers, and sleep schedule required to achieve any desired target CGPA.
- **⚡ Persona Quick-Presets:** One-click autofill profiles (*Topper / Achiever*, *Balanced Routine*, *Night Owl Crammer*, *Recovery Mode*).
- **⏱️ 24-Hour Daily Time Budget Meter:** Real-time visual tracking of study, sleep, and free hours with automated burnout and schedule conflict alerts.
- **🌓 Dark & Light Glassmorphism UI:** Ultra-modern frosted-glass cards, animated multi-tone gradient backgrounds, and responsive mobile-first grid.
- **🖨️ Export / Print Summary:** One-click formatted report generation for student progress records.
- **🔌 Full REST API Suite:** Async JSON endpoints (`/api/predict`, `/api/goal-planner`, `/api/model-info`) for seamless third-party integrations.

---

## 🏗️ System Architecture

```mermaid
flowchart TD
    subgraph Frontend - Modern Glassmorphic Dashboard
        A1[Theme Switcher: Dark / Light]
        A2[Tab Navigation: Predictor | Goal Planner | Model Insights]
        A3[Dual Controls: Sliders + Numeric Inputs + Presets]
        A4[24-Hour Daily Budget Bar]
        A5[Animated Radial SVG Gauge]
        A6[AI Action Plan Cards]
    end

    subgraph Backend - Flask Application app.py
        B1[Web Controller: GET / POST /]
        B2[REST API: POST /api/predict]
        B3[REST API: POST /api/goal-planner]
        B4[REST API: GET /api/model-info]
        B5[AI Advisory Engine: generate_ai_recommendations]
        B6[Goal Optimization Engine: calculate_goal_plan]
    end

    subgraph Machine Learning Layer
        C1[student_model.pkl: RandomForestRegressor]
    end

    A3 -->|Live Fetch| B2
    A3 -->|Form Post| B1
    A2 -->|Goal Request| B3
    B1 --> C1
    B2 --> C1
    B3 --> C1
    B2 --> B5
    B3 --> B6
    B5 --> A6
    B6 --> A2
```

---

## 📊 Dataset & Feature Description

The model is trained on a 10,000-record student benchmark dataset:

| Feature Name | Type | Scale / Range | Impact Weight | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Hours Studied** | Numeric | $1 - 24\text{ hrs}$ | **Very High** | Daily self-study and revision hours |
| **Previous Scores** | Numeric | $0 - 100\text{ marks}$ ($0 - 10\text{ CGPA}$) | **Very High** | Historical academic baseline |
| **Sample Question Papers** | Numeric | $0 - 10\text{ papers}$ | **High** | Mock tests and practice papers solved |
| **Sleep Hours** | Numeric | $0 - 24\text{ hrs}$ | **Moderate** | Daily sleep duration for cognitive retention |
| **Extracurricular Activities**| Categorical | `Yes` ($1$) / `No` ($0$) | **Moderate** | Involvement in arts, sports, or clubs |
| **Performance Index (Target)**| Numeric | $10.0 - 100.0$ | **Target** | Target score mapped to 10.0 CGPA |

---

## 🔌 REST API Documentation

### 1. Predict Performance (`POST /api/predict`)

**Request Payload:**
```json
{
  "hours": 6.0,
  "prev": 8.0,
  "extra": 1,
  "sleep": 7.5,
  "papers": 5
}
```

**Response Payload:**
```json
{
  "success": true,
  "data": {
    "cgpa": 8.75,
    "score": 87.5,
    "tier": "Distinction",
    "badge": "🟢 Excellent",
    "grade": "A+",
    "free_hours": 10.5,
    "recommendations": [
      {
        "icon": "🌟",
        "title": "Strong Mock Practice",
        "message": "Your rigorous practice with sample papers provides a great advantage in speed and pattern familiarity.",
        "type": "positive"
      }
    ]
  }
}
```

### 2. "What-If" Goal Planner (`POST /api/goal-planner`)

**Request Payload:**
```json
{
  "target_cgpa": 9.0,
  "prev_cgpa": 7.2,
  "extra": 1,
  "sleep": 7.5,
  "hours": 5.0,
  "papers": 4
}
```

---

## 📂 Project Directory Structure

```text
Student-Performance-Prediction/
│
├── static/
│   ├── style.css                 # Glassmorphic CSS design system, dark/light theme, radial gauge styles
│   └── script.js                 # Real-time slider sync, 24-hr budget tracker, async API integration
├── templates/
│   └── index.html                # Multi-view dashboard template (Predictor, Goal Planner, Insights)
├── Student_Performance.csv       # 10,000-record student benchmark dataset
├── Student_Performance.xls       # Excel formatted raw dataset
├── student data.ipynb            # Exploratory Data Analysis (EDA) & baseline experimentation
├── train_model.py                # Model training & serialization pipeline
├── student_model.pkl             # Serialized Scikit-Learn Random Forest Regressor
├── app.py                        # Flask server with web views, REST APIs & AI advisory engines
├── requirements.txt              # Production Python dependencies
├── Procfile                      # Cloud deployment configuration
└── README.md                     # Comprehensive project documentation
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.9+** installed on your machine.
- `git` installed.

### Installation & Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/avinashbasani132/Student-Performance-Prediction.git
   cd Student-Performance-Prediction
   ```

2. **Create and Activate a Virtual Environment:**
   - **Windows (PowerShell):**
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
   - **Linux / macOS:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install Required Packages:**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. **Launch the Flask Server:**
   ```bash
   python app.py
   ```

2. **Access the Web Interface:**
   Open your browser and navigate to:
   ```text
   http://127.0.0.1:5000/
   ```

---

## ☁️ Deployment

The project is pre-configured with a `Procfile` for one-click deployment on **Render**, **Railway**, or **Heroku**:

- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app:app`

---

## 👨‍💻 Author & Acknowledgments

- **Developed by:** [Avinash Basani](https://github.com/avinashbasani132)
- **Dataset:** Student Performance Dataset ([Kaggle](https://www.kaggle.com/))
- **Libraries:** Flask, Scikit-Learn, Pandas, Joblib, Gunicorn

---

<p align="center">
  <sub>⭐ If you find this repository helpful, please consider starring the project on GitHub!</sub>
</p>
