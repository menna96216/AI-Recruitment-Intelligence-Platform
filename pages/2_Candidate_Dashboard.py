import streamlit as st
import json
import os

st.set_page_config(
    page_title="Candidate Dashboard",
    page_icon="👤",
    layout="wide"
)

OUTPUT_FOLDER = "outputs"

CANDIDATE_FILE = os.path.join(
    OUTPUT_FOLDER,
    "candidate_profile.json"
)

ATS_FILE = os.path.join(
    OUTPUT_FOLDER,
    "ats_report.json"
)

CAREER_FILE = os.path.join(
    OUTPUT_FOLDER,
    "career_report.json"
)

FINAL_FILE = os.path.join(
    OUTPUT_FOLDER,
    "final_decision.json"
)

st.title("👤 Candidate Dashboard")

st.markdown("---")

# ==========================================
# Candidate Profile
# ==========================================

if os.path.exists(CANDIDATE_FILE):

    with open(
        CANDIDATE_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        candidate = json.load(f)

    st.header("📄 Candidate Profile")

    col1, col2 = st.columns(2)

    with col1:

        contact = candidate.get("contact", {})

        st.write(
            "**Name:**",
            candidate.get("name", "N/A")
        )

        st.write(
            "**Email:**",
            contact.get("email", "N/A")
        )

        st.write(
            "**Phone:**",
            contact.get("phone", "N/A")
        )

        st.write(
            "**Location:**",
            contact.get("location", "N/A")
        )

    education = candidate.get("education", [])

    if education:

        edu = education[0]

        st.write(
            "**University:**",
            edu.get("institution", "N/A")
        )

        st.write(
            "**Degree:**",
            edu.get("degree", "N/A")
        )

        st.write(
            "**Study Period:**",
            f"{edu.get('start_year')} - {edu.get('end_year')}"
        )

        st.write(
            "**GPA:**",
            edu.get("gpa", "N/A")
        )

    else:

        st.write("Education: N/A")
        

        st.write(
            "**Experience:**",
            len(candidate.get("experience", [])),
            "Experience(s)"
        )

    st.subheader("🛠 Skills")

    skills = candidate.get("skills", [])

    if skills:

        st.write(", ".join(skills))

    else:

        st.info("No skills available.")

st.markdown("---")

# ==========================================
# ATS Report
# ==========================================

if os.path.exists(ATS_FILE):

    with open(
        ATS_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        ats = json.load(f)

    st.header("📊 ATS Result")

    st.metric(
        "ATS Score",
        f"{ats.get('ats_score',0)}%"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.subheader(
            "✅ Matched Skills"
        )

        for skill in ats.get(
            "matched_required_skills",
            []
        ):

            st.success(skill)

    with col2:

        st.subheader(
            "❌ Missing Skills"
        )

        for skill in ats.get(
            "missing_required_skills",
            []
        ):

            st.error(skill)

st.markdown("---")

# ==========================================
# Career Plan
# ==========================================

if os.path.exists(CAREER_FILE):

    with open(
        CAREER_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        career = json.load(f)

    st.header("📚 Development Plan")

    learning_plan = career.get(
        "learning_plan",
        []
    )

    for item in learning_plan:

        with st.expander(
            item["skill_name"]
        ):

            st.write(
                "**Priority:**",
                item["priority"]
            )

            st.write(
                "**Reason:**",
                item["reason"]
            )

            st.write(
                "**Resources:**"
            )

            for resource in item.get(
                "learning_resources",
                []
            ):

                st.write(
                    "•",
                    resource
                )

st.markdown("---")

# ==========================================
# Final Decision
# ==========================================

if os.path.exists(FINAL_FILE):

    with open(
        FINAL_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        decision = json.load(f)

    st.header("🏆 Recruitment Decision")

    st.success(
        decision.get(
            "final_decision",
            "N/A"
        )
    )

else:

    st.info(
        "Final recruitment decision has not been generated yet."
    )