import streamlit as st
from main import initialize_knowledge_base, apply_rules


# -----------------------------
# Theme management & config
# -----------------------------
# Check if dark mode is enabled (default to light)
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# Function to toggle theme
def toggle_theme():
    st.session_state.dark_mode = not st.session_state.dark_mode
    

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="Clinic Expert System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)


# -----------------------------
# Custom lightweight CSS - modern, light theme
# -----------------------------
st.markdown(
    """
    <style>
    /* Light mode (default) */
    :root {
        --bg-color: #f7f9fc;
        --text-color: #0f1724;
        --card-bg: white;
        --card-shadow: 0 6px 20px rgba(16, 24, 40, 0.06);
        --card-border: 1px solid rgba(16,24,40,0.04);
        --brand-title: #0b2536;
        --brand-sub: #3b556b;
        --muted: #51667a;
        --result-value: #07203b;
        --urgent-bg: linear-gradient(90deg,#ffeded,#fff5f5);
        --high-bg: linear-gradient(90deg,#fff7e6,#fffdf0);
        --moderate-bg: linear-gradient(90deg,#f7f7ff,#fcfbff);
        --low-bg: linear-gradient(90deg,#effff6,#fbfff9);
        --hr-color: rgba(0,0,0,0.1);
    }

    /* Dark mode overrides */
    [data-theme="dark"] {
        --bg-color: #0f1724;
        --text-color: #e6edf3;
        --card-bg: #1a2634;
        --card-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
        --card-border: 1px solid rgba(255,255,255,0.05);
        --brand-title: #e6edf3;
        --brand-sub: #8b949e;
        --muted: #8b949e;
        --result-value: #e6edf3;
        --urgent-bg: linear-gradient(90deg,#3d1f1f,#2d1717);
        --high-bg: linear-gradient(90deg,#3d2f1f,#2d2417);
        --moderate-bg: linear-gradient(90deg,#1f1f3d,#17172d);
        --low-bg: linear-gradient(90deg,#1f3d2f,#172d24);
        --hr-color: rgba(255,255,255,0.1);
    }

    /* App background and font */
    .stApp {
        background: var(--bg-color);
        color: var(--text-color);
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial;
    }

    /* Header */
    .header {
        display: flex;
        align-items: center;
        gap: 16px;
        padding: 10px 0 20px 0;
    }
    .brand-title {
        font-size: 28px;
        font-weight: 700;
        color: var(--brand-title);
    }
    .brand-sub {
        color: var(--brand-sub);
        font-size: 14px;
        margin-top: -4px;
    }

    /* Cards */
    .card {
        background: var(--card-bg);
        border-radius: 12px;
        padding: 18px;
        box-shadow: var(--card-shadow);
        border: var(--card-border);
    }

    .result-value {
        font-size: 20px;
        font-weight: 700;
        color: var(--result-value);
    }

    .muted {
        color: var(--muted);
        font-size: 13px;
    }

    hr {
        border-color: var(--hr-color);
    }

    /* Theme toggle button */
    .theme-toggle {
        position: fixed;
        top: 1rem;
        right: 1rem;
        padding: 8px 12px;
        border-radius: 8px;
        background: var(--card-bg);
        border: var(--card-border);
        color: var(--text-color);
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 14px;
        z-index: 1000;
    }

    /* Urgency indicators with theme support */
    .urgent {
        background: var(--urgent-bg);
        border-left: 4px solid #ff4d4f;
        padding: 12px;
        border-radius: 8px;
        color: var(--text-color);
    }

    .high {
        background: var(--high-bg);
        border-left: 4px solid #ff9500;
        padding: 12px;
        border-radius: 8px;
        color: var(--text-color);
    }

    .moderate {
        background: var(--moderate-bg);
        border-left: 4px solid #7a7aff;
        padding: 12px;
        border-radius: 8px;
        color: var(--text-color);
    }

    .low {
        background: var(--low-bg);
        border-left: 4px solid #16a34a;
        padding: 12px;
        border-radius: 8px;
        color: var(--text-color);
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# -----------------------------
# Layout: sidebar for demographics & controls
# -----------------------------

# Add data-theme attribute based on dark mode state
st.markdown(f"""
    <script>
        document.querySelector('.stApp').setAttribute('data-theme', {'dark' if st.session_state.dark_mode else 'light'});
    </script>
    <button onclick="document.querySelector('.stApp').setAttribute('data-theme', document.querySelector('.stApp').getAttribute('data-theme') === 'dark' ? 'light' : 'dark')" class="theme-toggle">
        {" 🌙 Dark" if not st.session_state.dark_mode else " ☀️ Light"}
    </button>
""", unsafe_allow_html=True)

st.markdown("<div class='header'><div><span style='font-size:34px'>🏥</span></div><div><div class='brand-title'>Clinic Expert System</div><div class='brand-sub'>AI-assisted patient assessment</div></div></div>", unsafe_allow_html=True)

symptoms = initialize_knowledge_base()

# Sidebar inputs (demographics + quick controls)
with st.sidebar:
    st.markdown("## Patient Info")
    gender = st.selectbox("Gender", ["Male", "Female", "Other"], key="gender")
    age_group = st.selectbox(
        "Age Group",
        ["0-12 (Child)", "13-17 (Adolescent)", "18-39 (Young Adult)", "40-64 (Middle-aged Adult)", "65+ (Senior)"],
        key="age_group",
    )

    st.markdown("---")
    st.markdown("## Symptom Duration")
    duration_long = st.checkbox("Symptoms lasting more than 10 days", key="duration_long")

    st.markdown("---")
    st.caption("Tip: Select symptoms in the main area, then click Analyze.")
    st.markdown("\n")
    analyze_button_sidebar = st.button("Analyze (Sidebar)", key="analyze_sidebar")


# -----------------------------
# Main symptom selection area
# -----------------------------
st.markdown("## Symptom Assessment")
st.markdown("Select all symptoms that apply:")

patient_data = {}

st.markdown("### General")
col1, col2, col3 = st.columns(3)
with col1:
    patient_data['fever'] = st.checkbox("Fever (>100.4°F)", key="fever")
    patient_data['high_fever'] = st.checkbox("High Fever (>103°F)", key="high_fever")
with col2:
    patient_data['fatigue'] = st.checkbox("Fatigue/Weakness", key="fatigue")
    patient_data['body_aches'] = st.checkbox("Body Aches", key="body_aches")
with col3:
    patient_data['headache'] = st.checkbox("Headache", key="headache")
    patient_data['nausea'] = st.checkbox("Nausea/Vomiting", key="nausea")

st.markdown("### Respiratory")
col1, col2, col3 = st.columns(3)
with col1:
    patient_data['cough'] = st.checkbox("Cough", key="cough")
    patient_data['severe_cough'] = st.checkbox("Severe/Persistent Cough", key="severe_cough")
with col2:
    patient_data['sore_throat'] = st.checkbox("Sore Throat", key="sore_throat")
    patient_data['difficulty_breathing'] = st.checkbox("Difficulty Breathing", key="difficulty_breathing")
with col3:
    patient_data['chest_pain'] = st.checkbox("Chest Pain", key="chest_pain")

st.markdown("### Nasal / Eyes")
col1, col2, col3 = st.columns(3)
with col1:
    patient_data['runny_nose'] = st.checkbox("Runny / Stuffy Nose", key="runny_nose")
with col2:
    patient_data['sneezing'] = st.checkbox("Sneezing", key="sneezing")
with col3:
    patient_data['itchy_eyes'] = st.checkbox("Itchy / Watery Eyes", key="itchy_eyes")

# Ensure duration from sidebar is included in patient_data
patient_data['duration_long'] = duration_long

# Centered analyze button in main area (keeps both sidebar and main triggers)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    analyze_button = st.button("🔍 Analyze Symptoms & Get Recommendation", key="analyze_main")

# If either analyze button is clicked, run the logic
if analyze_button or analyze_button_sidebar:
    diagnosis, recommendation, urgency, explanation = apply_rules(patient_data)

    # Map urgency to styles
    urgency_map = {
        "URGENT": ("urgent", "URGENT"),
        "HIGH": ("high", "HIGH"),
        "MODERATE": ("moderate", "MODERATE"),
        "LOW": ("low", "LOW"),
        "NULL": ("-", "NULL","null")
    }
    
    urgency_class, urgency_label = urgency_map.get(urgency, ("low", urgency))

    # Results layout
    st.markdown("---")
    st.markdown("## Assessment Results")

    left, right = st.columns([2, 1])

    with left:
        st.markdown(f"<div class='card'> <div style='display:flex;justify-content:space-between;align-items:center;'><div><div class='muted'>Condition</div><div class='result-value'>{diagnosis}</div></div><div style='text-align:right'><div class='muted'>Urgency</div><div class='{urgency_class}' style='display:inline-block;margin-top:6px;padding:6px 12px;border-radius:8px;font-weight:600'>{urgency_label}</div></div></div><hr style='margin:12px 0'> <div class='muted'>Explanation</div><div style='margin-top:8px'>{explanation}</div></div>", unsafe_allow_html=True)

        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

        st.markdown("<div class='card'><div class='muted'>Recommendation</div><div style='margin-top:8px;font-weight:700'>" + recommendation + "</div></div>", unsafe_allow_html=True)

    with right:
        st.markdown("<div class='card'><div class='muted'>Patient Information</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='margin-top:10px'><strong>Gender:</strong> {gender}<br><strong>Age group:</strong> {age_group}<br><strong>Duration &gt;10d:</strong> {'Yes' if patient_data['duration_long'] else 'No'}</div></div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<div class='muted'>Disclaimer: This system provides decision support only and should not replace professional medical judgment.</div>", unsafe_allow_html=True)

