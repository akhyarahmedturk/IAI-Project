import streamlit as st
from main import initialize_knowledge_base, apply_rules

# ----------------------------------
# PAGE CONFIG
# ----------------------------------
st.set_page_config(
    page_title="Clinic Expert System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ----------------------------------
# CUSTOM CSS (Refined Alignment + Style)
# ----------------------------------
st.markdown("""
<style>
/* App Background */
.stApp {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
}

/* Centered Title and Subtitle */
.main-title {
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 3rem;
    font-weight: 800;
    color: white;
    text-shadow: 0 0 40px rgba(0, 255, 255, 1), 0 0 20px rgba(0, 255, 255, 0.8);
    margin-top: 1rem;
    margin-bottom: 0.2rem;
}
.subtitle {
    text-align: center;
    color: #ffffff !important;
    font-size: 1.4rem;
    margin-bottom: 2rem;
    font-weight: 500;
    text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
}

/* Headings */
h2, h3 {
    color: #ffffff !important;
    text-shadow: 0 0 15px rgba(0, 255, 255, 0.7);
}
h2 {
    border-bottom: 4px solid #00ffff;
    padding-bottom: 0.8rem;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #00ffff 0%, #0099ff 100%);
    color: #1a1a2e;
    font-size: 1.3rem;
    font-weight: bold;
    padding: 0.85rem 2rem;
    border-radius: 12px;
    border: 2px solid #00ffff;
    box-shadow: 0 4px 20px rgba(0, 255, 255, 0.5);
    transition: all 0.3s ease;
    width: 100%;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 30px rgba(0, 255, 255, 0.8);
}

/* Results Section */
.assessment-section {
    margin-top: 2rem;
    text-align: center;
}
.result-container {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 2rem;
    margin-top: 2rem;
}
.result-card {
    background: linear-gradient(135deg, #1e1e2e, #2b2b3c);
    border: 2px solid #444;
    border-radius: 20px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.4);
    padding: 1.5rem 2rem;
    min-width: 260px;
    text-align: center;
    color: #EEE;
    transition: transform 0.2s ease;
}
.result-card:hover {
    transform: translateY(-5px);
}
.result-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: #B5B5B5;
    margin-bottom: 0.3rem;
}
.result-value {
    font-size: 1.6rem;
    font-weight: 700;
    color: #79b8ff;
}

/* Recommendation & Patient Info */
.info-box {
    background: #202030;
    border: 2px solid #3a3a4a;
    border-radius: 16px;
    padding: 1.5rem 2rem;
    margin-top: 1rem;
    color: #D8D8D8;
    box-shadow: 0 4px 14px rgba(0,0,0,0.4);
}
.info-label {
    font-weight: 600;
    color: #9E9E9E;
    margin-bottom: 0.4rem;
}

/* Urgency Badge */
.urgency-badge {
    color: #1a1a2e;
    font-weight: bold;
    padding: 0.5rem 2rem;
    border-radius: 25px;
    display: inline-block;
    margin-top: 1rem;
    font-size: 1.2rem;
}


/* --- */
div[data-testid="stCheckbox"] div[data-testid="stMarkdownContainer"],
div[data-testid="stCheckbox"] label p,
div[data-testid="stCheckbox"] label span {
    color: #ffffff !important;
    opacity: 1 !important;
    font-weight: 600 !important;
    text-shadow: none !important;
}

/* Optional: brighter emojis and icons */
div[data-testid="stCheckbox"] span[role="img"] {
    filter: brightness(1.5);
}

/* Optional: cyan accent for checkmarks */
div[data-testid="stCheckbox"] input[type="checkbox"] {
    accent-color: #00e5ff;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------------
# HEADER
# ----------------------------------
st.markdown("<div class='main-title'>🏥 <span>Clinic Expert System</span></div>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>AI-Powered Patient Assessment & Referral System</p>", unsafe_allow_html=True)

# ----------------------------------
# PATIENT DEMOGRAPHICS
# ----------------------------------
st.markdown("## 👤 Patient Demographics")
col1, col2 = st.columns(2)

with col1:
    gender = st.selectbox(
        "Gender",
        ["Male", "Female", "Other"],
        key="gender"
    )

with col2:
    age_group = st.selectbox(
        "Age Group",
        ["0-12 (Child)", "13-17 (Adolescent)", "18-39 (Young Adult)",
         "40-64 (Middle-aged Adult)", "65+ (Senior)"],
        key="age_group"
    )

st.markdown("---")

# ----------------------------------
# SYMPTOM ASSESSMENT
# ----------------------------------
st.markdown("## 🩺 Symptom Assessment")
st.markdown("<p style='color: #ffffff; margin-bottom: 1.5rem;'>Please select all symptoms that apply to the patient:</p>", unsafe_allow_html=True)

symptoms = initialize_knowledge_base()
patient_data = {}

# Temperature & General Symptoms
st.markdown("### 🌡️ Temperature & General Symptoms")
col1, col2, col3 = st.columns(3)
with col1:
    patient_data['fever'] = st.checkbox("Fever (>100.4°F)")
    patient_data['high_fever'] = st.checkbox("High Fever (>103°F)")
with col2:
    patient_data['fatigue'] = st.checkbox("Fatigue/Weakness")
    patient_data['body_aches'] = st.checkbox("Body Aches")
with col3:
    patient_data['headache'] = st.checkbox("Headache")
    patient_data['nausea'] = st.checkbox("Nausea/Vomiting")

# Respiratory
st.markdown("### 🫁 Respiratory Symptoms")
col1, col2, col3 = st.columns(3)
with col1:
    patient_data['cough'] = st.checkbox("Cough")
    patient_data['severe_cough'] = st.checkbox("Severe/Persistent Cough")
with col2:
    patient_data['sore_throat'] = st.checkbox("Sore Throat")
    patient_data['difficulty_breathing'] = st.checkbox("⚠️ Difficulty Breathing")
with col3:
    patient_data['chest_pain'] = st.checkbox("⚠️ Chest Pain")

# Nasal & Eye
st.markdown("### 👃 Nasal & Eye Symptoms")
col1, col2, col3 = st.columns(3)
with col1:
    patient_data['runny_nose'] = st.checkbox("Runny/Stuffy Nose")
with col2:
    patient_data['sneezing'] = st.checkbox("Sneezing")
with col3:
    patient_data['itchy_eyes'] = st.checkbox("Itchy/Watery Eyes")

# Duration
st.markdown("### ⏱️ Duration")
patient_data['duration_long'] = st.checkbox("Symptoms lasting more than 10 days")

st.markdown("---")

# ----------------------------------
# ANALYZE BUTTON
# ----------------------------------
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    analyze_button = st.button("🔍 Analyze Symptoms & Get Recommendation")

# ----------------------------------
# RESULTS
# ----------------------------------
if analyze_button:
    diagnosis, recommendation, urgency, explanation = apply_rules(patient_data)

    st.markdown("<div class='assessment-section'>", unsafe_allow_html=True)
    st.markdown("## 📋 Assessment Results")

    # Urgency color mapping
    urgency_colors = {
        "URGENT": "#ff4757",
        "HIGH": "#ffa502",
        "MODERATE": "#f0e68c",
        "LOW": "#2ed573"
    }
    urgency_color = urgency_colors.get(urgency, "#2ed573")

    # Result cards
    st.markdown(f"""
    <div class='result-container'>
        <div class='result-card'>
            <div class='result-title'>Condition</div>
            <div class='result-value'>{diagnosis}</div>
        </div>
        <div class='result-card'>
            <div class='result-title'>Urgency</div>
            <div class='result-value' style='color:{urgency_color};'>{urgency}</div>
        </div>
        <div class='result-card'>
            <div class='result-title'>Explanation</div>
            <div class='result-value' style='font-size:1rem;'>{explanation}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Recommendation
    st.markdown("<h3 style='text-align:center; margin-top:2rem;'>Recommendation</h3>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class='info-box'>
        <div class='info-label'>Suggested Action:</div>
        {recommendation}
    </div>
    """, unsafe_allow_html=True)

    # Patient Info
    st.markdown("<h3 style='text-align:center; margin-top:2rem;'>Patient Information</h3>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class='info-box'>
        <div class='info-label'>Gender:</div> {gender}<br>
        <div class='info-label'>Age Group:</div> {age_group}
    </div>
    """, unsafe_allow_html=True)

    # Urgency alert box
    if urgency == "URGENT":
        st.markdown(f"""
        <div style='background:linear-gradient(135deg,#ff4757,#ff6b81);border-radius:15px;padding:1.5rem;margin:1.5rem 0;
        border:2px solid #ff4757;box-shadow:0 5px 20px rgba(255,71,87,0.4);color:white;text-align:center;font-weight:bold;'>
        🚨 URGENT: Patient should see a doctor IMMEDIATELY or visit emergency room.
        </div>
        """, unsafe_allow_html=True)
    elif urgency == "HIGH":
        st.markdown(f"""
        <div style='background:linear-gradient(135deg,#ffa502,#ffb833);border-radius:15px;padding:1.5rem;margin:1.5rem 0;
        border:2px solid #ffa502;box-shadow:0 5px 20px rgba(255,165,2,0.4);color:white;text-align:center;font-weight:bold;'>
        ⚠️ HIGH PRIORITY: Schedule doctor appointment as soon as possible.
        </div>
        """, unsafe_allow_html=True)
    elif urgency == "MODERATE":
        st.markdown(f"""
        <div style='background:linear-gradient(135deg,#f0e68c,#ffd93d);border-radius:15px;padding:1.5rem;margin:1.5rem 0;
        border:2px solid #f0e68c;box-shadow:0 5px 20px rgba(240,230,140,0.4);color:#1a1a2e;text-align:center;font-weight:bold;'>
        ℹ️ MODERATE: Schedule doctor appointment within 1–2 days.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style='background:linear-gradient(135deg,#2ed573,#7bed9f);border-radius:15px;padding:1.5rem;margin:1.5rem 0;
        border:2px solid #2ed573;box-shadow:0 5px 20px rgba(46,213,115,0.4);color:white;text-align:center;font-weight:bold;'>
        ✅ LOW PRIORITY: Home care recommended. See doctor if symptoms persist.
        </div>
        """, unsafe_allow_html=True)

# ----------------------------------
# FOOTER
# ----------------------------------
st.markdown("---")
st.markdown("""
<div style='text-align:center;color:#a0a0ff;padding:2rem 0;'>
<p><strong>Disclaimer:</strong> This system provides decision support only and should not replace professional medical judgment.</p>
<p>Always consult with qualified healthcare professionals for accurate diagnosis and treatment.</p>
</div>
""", unsafe_allow_html=True)
