import streamlit as st
import pandas as pd
import joblib
import numpy as np
import os

# Set page config
st.set_page_config(page_title="Student Stress Predictor", layout="wide")

# ==========================================
# 1. Helper Functions & Model Loading
# ==========================================

@st.cache_resource
def load_models():
    if not os.path.exists("stress_model.pkl") or not os.path.exists("label_encoder.pkl"):
        st.error("Model files not found! Please ensure 'stress_model.pkl' and 'label_encoder.pkl' are in the same directory.")
        st.stop()
    
    model = joblib.load("stress_model.pkl")
    le = joblib.load("label_encoder.pkl")
    return model, le

def explain_stress_ui(sample):
    reasons = []
    # Academics
    if sample["study_hours"] > 7: reasons.append("High study workload (>7 hrs/day)")
    if sample["assignment_load"] > 3: reasons.append("Heavy assignment load")
    if sample["attendance"] < 75: reasons.append("Low attendance pressure (<75%)")
    
    # Lifestyle
    if sample["sleep_hours"] < 6: reasons.append("Insufficient sleep (<6 hrs/day)")
    if sample["screen_time"] > 6: reasons.append("Excessive screen time (>6 hrs/day)")
    if sample["physical_activity"] < 2: reasons.append("Low physical activity (<2 hrs/week)")
    if sample["social_interaction"] < 3: reasons.append("Low social interaction")
    
    # Relationships
    if sample["relationship_status"] == 1: reasons.append("Uncertain 'Situationship' status")
    elif sample["relationship_status"] == 3:
        if sample["relationship_satisfaction"] <= 2: reasons.append("Unsatisfying casual relationship")
    elif sample["relationship_status"] == 2:
        if sample["relationship_satisfaction"] <= 2: reasons.append("Low satisfaction in committed relationship")
        elif sample["relationship_satisfaction"] <= 4: reasons.append("Moderate relationship stress")
        
    # Substances
    substance_count = sample["alcohol_use"] + sample["smoking_use"] + sample["weed_use"]
    if substance_count > 0:
        if sample["substance_frequency"] == 2:
            reasons.append("Frequent substance use")
        if substance_count >= 2 and sample["substance_frequency"] == 2:
            reasons.append("High risk: Multiple frequent substances")
            
    return reasons

# ==========================================
# 2. Session State Management
# ==========================================
if 'page' not in st.session_state:
    st.session_state.page = "prediction"

# ==========================================
# 3. Page 1: Prediction Page
# ==========================================
if st.session_state.page == "prediction":
    
    # Centered Title and Subtitle
    st.markdown("<h1 style='text-align: center;'>Student Stress Predictor</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Adjust the sliders and options below to predict student stress levels.</p>", unsafe_allow_html=True)
    st.markdown("---") 
    
    # Main Layout: 3 Columns
    col1, col2, col3 = st.columns(3)

    # --- Column 1: Academics ---
    with col1:
        st.header("📚 Academics")
        study_hours = st.slider("Study Hours (Daily)", 0, 12, 5)
        attendance = st.slider("Attendance (%)", 0, 100, 80)
        assignment_load = st.slider("Assignment Load (1-5)", 1, 5, 3)

    # --- Column 2: Lifestyle ---
    with col2:
        st.header("🧘 Lifestyle")
        sleep_hours = st.slider("Sleep Hours", 0, 12, 7)
        screen_time = st.slider("Screen Time (Hours)", 0, 12, 4)
        physical_activity = st.slider("Physical Activity (Hrs/Week)", 0, 10, 2)
        social_interaction = st.slider("Social Interaction (1-5)", 1, 5, 3)

    # --- Column 3: Relationships & Substances ---
    with col3:
        st.header("❤️ Relationships")
        
        # Relationships Section
        rel_status_map = {0: "Single", 1: "Talking/Situationship", 2: "Committed", 3: "Casual/Hookup"}
        rel_status_input = st.selectbox("Relationship Status", options=list(rel_status_map.keys()), format_func=lambda x: rel_status_map[x])

        rel_satisfaction = 0
        if rel_status_input != 0:
            rel_satisfaction = st.slider("Relationship Satisfaction (0-5)", 0, 5, 3)

        st.markdown("---")
        st.subheader("🍺 Substance Usage")
        
        # --- NEW LAYOUT: Side-by-Side Checkboxes and Frequency ---
        sub_c1, sub_c2 = st.columns([1, 1]) # Create two sub-columns
        
        with sub_c1:
            alcohol = st.checkbox("Alcohol")
            smoking = st.checkbox("Smoking")
            weed = st.checkbox("Weed")
            
        substance_freq = 0
        with sub_c2:
            # Only show frequency options if a substance is selected
            if alcohol or smoking or weed:
                substance_freq = st.radio("Usage Frequency", options=[1, 2], format_func=lambda x: "Occasional" if x==1 else "Frequent")

    st.markdown("---")
    
    # Centered Predict Button
    b_col1, b_col2, b_col3 = st.columns([1, 2, 1])
    with b_col2:
        if st.button("Predict Stress Level", type="primary", use_container_width=True):
            st.session_state.input_data = {
                "study_hours": study_hours,
                "sleep_hours": sleep_hours,
                "screen_time": screen_time,
                "attendance": attendance,
                "assignment_load": assignment_load,
                "physical_activity": physical_activity,
                "social_interaction": social_interaction,
                "relationship_status": rel_status_input,
                "relationship_satisfaction": rel_satisfaction,
                "alcohol_use": int(alcohol),
                "smoking_use": int(smoking),
                "weed_use": int(weed),
                "substance_frequency": substance_freq
            }
            st.session_state.page = "result"
            st.rerun()

# ==========================================
# 4. Page 2: Result Page
# ==========================================
elif st.session_state.page == "result":
    st.markdown("<h1 style='text-align: center;'>Prediction Result</h1>", unsafe_allow_html=True)
    
    model, le = load_models()
    input_data = st.session_state.input_data
    sample_df = pd.DataFrame([input_data])
    
    prediction_idx = model.predict(sample_df)[0]
    prediction_label = le.inverse_transform([prediction_idx])[0]
    reasons = explain_stress_ui(input_data)
    
    color_map = {"Low": "green", "Medium": "orange", "High": "red"}
    
    st.markdown("---")
    st.markdown(f"<h2 style='text-align: center; color: {color_map[prediction_label]};'>Predicted Stress Level: {prediction_label}</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    if reasons:
        st.subheader("⚠️ Possible Contributing Factors:")
        for r in reasons:
            st.markdown(f"- {r}")
    else:
        st.success("Based on the inputs, there are no major stress factors detected.")

    # --- ADDED: Help Suggestion Section ---

    if prediction_label == "Low":
        st.write("💡 You seem to be managing stress well. Keep it up!")
    
    elif prediction_label == "Medium":
        st.info("💡 Small lifestyle adjustments (sleep, routine, balance) could help reduce stress.")

    else:
        st.warning("💡 Consider addressing the highlighted factors gradually. Support and balance matter.")
        
    st.divider()

    # Centered New Prediction Button
    b_col1, b_col2, b_col3 = st.columns([1, 2, 1])
    with b_col2:
        if st.button("New Prediction", type="secondary", use_container_width=True):
            st.session_state.page = "prediction"
            st.rerun()