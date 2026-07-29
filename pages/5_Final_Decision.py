import streamlit as st
import json
import os

st.set_page_config(
    page_title="Final Recruitment Decision",
    page_icon="✅",
    layout="wide"
)

OUTPUT_FOLDER = "outputs"

DECISION_FILE = os.path.join(
    OUTPUT_FOLDER,
    "final_decision.json"
)

# ==========================================
# Validation
# ==========================================

if not os.path.exists(DECISION_FILE):

    st.error(
        "Final Decision has not been generated yet."
    )

    st.stop()

with open(
    DECISION_FILE,
    "r",
    encoding="utf-8"
) as f:

    decision = json.load(f)

# ==========================================
# Title
# ==========================================

st.title("✅ Final Recruitment Decision")

st.markdown("---")

# ==========================================
# Decision
# ==========================================

final_decision = decision.get(
    "final_decision",
    "Unknown"
)

if final_decision == "Strong Hire":

    st.success(
        f"🏆 {final_decision}"
    )

elif final_decision == "Hire":

    st.success(
        f"✅ {final_decision}"
    )

elif final_decision == "Consider":

    st.warning(
        f"⚠️ {final_decision}"
    )

else:

    st.error(
        f"❌ {final_decision}"
    )

# ==========================================
# Metrics
# ==========================================

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Overall Score",
        decision.get(
            "overall_score",
            0
        )
    )

with col2:

    st.metric(
        "Confidence",
        decision.get(
            "confidence_level",
            "-"
        )
    )

st.markdown("---")

# ==========================================
# Decision Reason
# ==========================================

st.subheader(
    "📝 Decision Reason"
)

st.write(
    decision.get(
        "decision_reason",
        "-"
    )
)

# ==========================================
# Candidate Strengths
# ==========================================

st.subheader(
    "✅ Candidate Strengths"
)

for item in decision.get(
    "candidate_strengths",
    []
):

    st.success(item)

# ==========================================
# Candidate Risks
# ==========================================

st.subheader(
    "⚠️ Candidate Risks"
)

for item in decision.get(
    "candidate_risks",
    []
):

    st.warning(item)

# ==========================================
# Skill Match
# ==========================================

st.subheader(
    "📊 Skill Match Summary"
)

st.write(
    decision.get(
        "skill_match_summary",
        "-"
    )
)

# ==========================================
# Recommendation
# ==========================================

st.subheader(
    "👨‍💼 Recommendation For HR"
)

st.info(
    decision.get(
        "recommendation_for_hr",
        "-"
    )
)

st.markdown("---")

# ==========================================
# Navigation
# ==========================================

col1, col2 = st.columns(2)

with col1:

    if st.button(
        "⬅ Back to HR Dashboard",
        use_container_width=True
    ):

        st.switch_page(
            "pages/1_HR_Dashboard.py"
        )

with col2:

    if st.button(
        "➡ Candidate Development Plan",
        use_container_width=True
    ):

        st.switch_page(
            "pages/6_Career_Plan.py"
        )