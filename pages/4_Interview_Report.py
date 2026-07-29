import streamlit as st
import json
import os

st.set_page_config(
    page_title="Interview Report",
    page_icon="📑",
    layout="wide"
)

OUTPUT_FOLDER = "outputs"

REPORT_FILE = os.path.join(
    OUTPUT_FOLDER,
    "interview_report.json"
)

# ==========================================
# Validation
# ==========================================

if not os.path.exists(REPORT_FILE):

    st.error(
        "Interview Report not found."
    )

    st.stop()

with open(
    REPORT_FILE,
    "r",
    encoding="utf-8"
) as f:

    report = json.load(f)

# ==========================================
# Title
# ==========================================

st.title("📑 AI Interview Report")

st.markdown("---")

# ==========================================
# Overall Results
# ==========================================

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Overall Score",
        report.get(
            "overall_score",
            0
        )
    )

with col2:

    st.metric(
        "Performance Level",
        report.get(
            "performance_level",
            "N/A"
        )
    )

st.markdown("---")

# ==========================================
# Summary
# ==========================================

st.subheader("📝 Interview Summary")

st.write(
    report.get(
        "summary",
        ""
    )
)

# ==========================================
# Strengths
# ==========================================

st.subheader("✅ Strengths")

for item in report.get(
    "strengths",
    []
):

    st.success(item)

# ==========================================
# Weaknesses
# ==========================================

st.subheader("❌ Weaknesses")

for item in report.get(
    "weaknesses",
    []
):

    st.error(item)

# ==========================================
# Missing Skills
# ==========================================

st.subheader("📌 Missing Skills")

for item in report.get(
    "missing_skills",
    []
):

    st.warning(item)

# ==========================================
# Recommendations
# ==========================================

st.subheader("💡 Improvement Recommendations")

for item in report.get(
    "improvement_recommendations",
    []
):

    st.info(item)

# ==========================================
# Hiring Recommendation
# ==========================================

st.subheader("🏆 Hiring Recommendation")

decision = report.get(
    "hiring_recommendation",
    "N/A"
)

if decision == "Strong Hire":

    st.success("🌟 Strong Hire")

elif decision == "Hire":

    st.success("✅ Hire")

elif decision == "Consider":

    st.warning("⚠️ Consider")

else:

    st.error("❌ Reject")

st.markdown("---")

# ==========================================
# Question Details
# ==========================================

st.header("📋 Question Evaluation")

question_details = report.get(
    "question_details",
    []
)

if len(question_details) == 0:

    st.info(
        "No question details available."
    )

else:

    for item in question_details:

        with st.expander(

            f"Question {item['question_id']}"

        ):

            st.markdown("### ❓ Question")

            st.write(
                item["question"]
            )

            col1, col2 = st.columns(2)

            with col1:

                st.write(
                    f"**Category:** {item['category']}"
                )

            with col2:

                st.write(
                    f"**Difficulty:** {item['difficulty']}"
                )

            st.markdown("### 💬 Candidate Answer")

            st.write(
                item["candidate_answer"]
            )

            st.metric(
                "Score",
                f"{item['score']} / 10"
            )

            st.markdown("### 📝 Feedback")

            st.write(
                item["feedback"]
            )

            st.markdown("### ✅ Good Points")

            strengths = item.get(
                "strengths",
                []
            )

            if strengths:

                for point in strengths:

                    st.success(point)

            else:

                st.info(
                    "No strengths detected."
                )

            st.markdown("### ❌ Missing Points")

            missing = item.get(
                "missing_points",
                []
            )

            if missing:

                for point in missing:

                    st.error(point)

            else:

                st.success(
                    "No missing points."
                )

            st.markdown("### 🚀 Improvement Feedback")

            st.info(
                item.get(
                    "improvement_feedback",
                    ""
                )
            )

            st.markdown("### 🎯 Expected Answer Points")

            expected = item.get(
                "expected_answer_points",
                []
            )

            if expected:

                for point in expected:

                    st.write(
                        "•",
                        point
                    )

st.markdown("---")

# ==========================================
# Back
# ==========================================

if st.button(
    "⬅ Back to HR Dashboard",
    use_container_width=True
):

    st.switch_page(
        "pages/1_HR_Dashboard.py"
    )