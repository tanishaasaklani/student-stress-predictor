#  Student Stress Predictor (Explainable ML)

---

An end-to-end Machine Learning application that predicts **student stress levels** and explains **why** a prediction was made — built with a real-world, product-first mindset.

This project goes beyond accuracy to focus on **explainability**, **human behavior**, and **deployment-ready ML systems**.

## Solution Overview
A **Random Forest–based stress prediction system** that:
- Analyzes **13 behavioral & lifestyle features**
- Predicts stress levels: **Low / Medium / High**
- Provides **human-readable explanations** for each prediction
- Is deployed as an interactive **Streamlit web app**

## Features Used
- Study hours & assignment load  
- Sleep, screen time & physical activity  
- Attendance & social interaction  
- Relationship status & satisfaction  
- Substance usage (alcohol, smoking, weed) with frequency  

## Tech Stack
- **Python**
- **Scikit-learn**
- **Pandas & NumPy**
- **Matplotlib & Seaborn**
- **Streamlit**
- **Joblib**

## Model Details
- Algorithm: **Random Forest Classifier**
- Explainability: **Feature Importance + Rule-based Reasoning**
- Focus: Interpretability over black-box predictions

## Web App (Streamlit)
The app allows users to:
- Adjust lifestyle & behavioral inputs
- Get real-time stress predictions
- See *why* the model made that prediction
- Reset and test different scenarios interactively

## Key Learnings
- Model explainability is critical for real-world ML products
- Accuracy alone doesn’t make a system usable
- Feature design matters as much as algorithm choice
- ML systems should communicate with humans, not just output labels

---
##  Run Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/tanishaasaklani/student-stress-predictor.git
   cd student-stress-predictor
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
3. Run the app:
   ```bash
   streamlit run st_app.py

## 📬 Contact
Created by **Tanisha Saklani** - MCA AI & DS Student.
Open to feedback!
