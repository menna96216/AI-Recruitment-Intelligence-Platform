import streamlit as st
import json
import os

st.set_page_config(
    page_title="Career Development Plan",
    page_icon="📚",
    layout="wide"
)

OUTPUT_FOLDER = "outputs"

CAREER_FILE = os.path.join(
    OUTPUT_FOLDER,
    "career_report.json"
)

# ==========================================
# Validation
# ==========================================

if not os.path.exists(CAREER_FILE):

    st.error(
        "Career Development Plan not found."
    )

    st.stop()

with open(
    CAREER_FILE,
    "r",
    encoding="utf-8"
) as f:

    report = json.load(f)

# ==========================================
# Title
# ==========================================

st.title("📚 Candidate Development Plan")

st.markdown("---")

# ==========================================
# Overview
# ==========================================

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Target Role",
        report["target_role"]
    )

with col2:

    st.metric(
        "Candidate Level",
        report["candidate_level"]
    )

st.markdown("---")

# ==========================================
# Strengths
# ==========================================

st.subheader("✅ Candidate Strengths")

for item in report["strengths"]:

    st.success(item)

# ==========================================
# Improvement Areas
# ==========================================

st.subheader("📌 Improvement Areas")

for item in report["improvement_areas"]:

    st.warning(item)

# ==========================================
# Learning Plan
# ==========================================

st.markdown("---")

st.header("📖 Personalized Learning Roadmap")

for i, skill in enumerate(report["learning_plan"], start=1):

    with st.expander(
        f"{i}. {skill['skill_name']}"
    ):

        st.write(
            f"**Priority:** {skill['priority']}"
        )

        st.write(
            f"**Reason:** {skill['reason']}"
        )

        if "estimated_duration" in skill:

            st.write(
                f"**Estimated Duration:** {skill['estimated_duration']}"
            )

        st.write("### Recommended Resources")

        for resource in skill["learning_resources"]:

            st.write(
                "-",
                resource
            )

# ==========================================
# Recommended Projects
# ==========================================

st.markdown("---")

st.header("💻 Recommended Projects")

for project in report["recommended_projects"]:

    with st.expander(
        project["project_name"]
    ):

        st.write(
            f"**Related Skill:** {project['related_skill']}"
        )

        if "difficulty" in project:

            st.write(
                f"**Difficulty:** {project['difficulty']}"
            )

        st.write(
            f"**Description:** {project['description']}"
        )

        st.write(
            f"**Expected Outcome:** {project['expected_outcome']}"
        )

# ==========================================
# Career Advice
# ==========================================

st.markdown("---")

st.subheader("🚀 Career Advice")

st.info(
    report["career_advice"]
)

# ==========================================
# Back
# ==========================================

st.markdown("---")

if st.button(
    "⬅ Back to HR Dashboard",
    use_container_width=True
):

    st.switch_page(
        "pages/1_HR_Dashboard.py"
    )