import streamlit as st
import os
import json

st.set_page_config(
    page_title="Admin Dashboard",
    page_icon="🛠️",
    layout="wide"
)

OUTPUT_FOLDER = "outputs"

st.title("🛠️ Admin Dashboard")

st.markdown(
    """
Administrative dashboard for monitoring
the Recruitment Intelligence Platform.
"""
)

st.markdown("---")

# ==========================================
# Helper
# ==========================================

def file_exists(filename):

    return os.path.exists(
        os.path.join(
            OUTPUT_FOLDER,
            filename
        )
    )

# ==========================================
# Workflow Status
# ==========================================

st.header("📊 Workflow Status")

workflow = [

    ("Candidate Profile", "candidate_profile.json"),

    ("Job Profile", "job_profile.json"),

    ("ATS Report", "ats_report.json"),

    ("Interview Config", "interview_config.json"),

    ("Interview Questions", "interview_questions.json"),

    ("Candidate Answers", "candidate_answers.json"),

    ("Answer Evaluations", "answer_evaluations.json"),

    ("Interview Report", "interview_report.json"),

    ("Final Decision", "final_decision.json"),

    ("Career Report", "career_report.json")

]

for title, filename in workflow:

    col1, col2 = st.columns([4,1])

    with col1:

        st.write(title)

    with col2:

        if file_exists(filename):

            st.success("Ready")

        else:

            st.error("Missing")

st.markdown("---")

# ==========================================
# Statistics
# ==========================================

st.header("📈 Generated Files")

generated_files = []

if os.path.exists(OUTPUT_FOLDER):

    generated_files = os.listdir(
        OUTPUT_FOLDER
    )

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Generated Files",
        len(generated_files)
    )

with col2:

    completed_steps = sum(

        1

        for _, file in workflow

        if file_exists(file)

    )

    st.metric(
        "Completed Steps",
        f"{completed_steps}/{len(workflow)}"
    )

st.markdown("---")

# ==========================================
# Quick Navigation
# ==========================================

st.header("🚀 Quick Navigation")

col1, col2 = st.columns(2)

with col1:

    if st.button(
        "👨‍💼 HR Dashboard",
        use_container_width=True
    ):

        st.switch_page(
            "pages/1_HR_Dashboard.py"
        )

    if st.button(
        "🎤 Interview",
        use_container_width=True
    ):

        st.switch_page(
            "pages/3_Interview.py"
        )

    if st.button(
        "📑 Interview Report",
        use_container_width=True
    ):

        if file_exists(
            "interview_report.json"
        ):

            st.switch_page(
                "pages/4_Interview_Report.py"
            )

        else:

            st.warning(
                "Interview Report not generated."
            )

with col2:

    if st.button(
        "✅ Final Decision",
        use_container_width=True
    ):

        if file_exists(
            "final_decision.json"
        ):

            st.switch_page(
                "pages/5_Final_Decision.py"
            )

        else:

            st.warning(
                "Final Decision not generated."
            )

    if st.button(
        "📚 Career Plan",
        use_container_width=True
    ):

        if file_exists(
            "career_report.json"
        ):

            st.switch_page(
                "pages/6_Career_Plan.py"
            )

        else:

            st.warning(
                "Career Plan not generated."
            )

st.markdown("---")

# ==========================================
# Download Reports
# ==========================================

st.header("📥 Download Reports")

if generated_files:

    selected = st.selectbox(

        "Choose Report",

        generated_files

    )

    with open(

        os.path.join(
            OUTPUT_FOLDER,
            selected
        ),

        "rb"

    ) as f:

        st.download_button(

            "⬇ Download",

            f,

            file_name=selected,

            mime="application/json",

            use_container_width=True

        )

else:

    st.info(
        "No generated reports."
    )

st.markdown("---")

# ==========================================
# Preview JSON
# ==========================================

st.header("🔍 Preview Report")

if generated_files:

    preview = st.selectbox(

        "Preview JSON",

        generated_files,

        key="preview"

    )

    with open(

        os.path.join(
            OUTPUT_FOLDER,
            preview
        ),

        "r",
        encoding="utf-8"

    ) as f:

        data = json.load(f)

    st.json(data)

st.markdown("---")

# ==========================================
# System Information
# ==========================================

with st.expander("⚙️ System Information"):

    st.write(
        "Output Folder:"
    )

    st.code(
        OUTPUT_FOLDER
    )

    st.write(
        "Current Files:"
    )

    st.write(
        generated_files
    )