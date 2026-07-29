import streamlit as st
import json
import os

st.set_page_config(
    page_title="AI Interview",
    page_icon="🎤",
    layout="wide"
)

OUTPUT_FOLDER = "outputs"

QUESTIONS_FILE = os.path.join(
    OUTPUT_FOLDER,
    "interview_questions.json"
)

ANSWERS_FILE = os.path.join(
    OUTPUT_FOLDER,
    "candidate_answers.json"
)

CANDIDATE_FILE = os.path.join(
    OUTPUT_FOLDER,
    "candidate_profile.json"
)

JOB_FILE = os.path.join(
    OUTPUT_FOLDER,
    "job_profile.json"
)

st.title("🎤 AI Interview")

st.markdown("---")

# ==========================================
# Validation
# ==========================================

if not os.path.exists(CANDIDATE_FILE):

    st.error(
        "No candidate has been selected."
    )

    st.stop()

if not os.path.exists(JOB_FILE):

    st.error(
        "No Job Description found."
    )

    st.stop()

if not os.path.exists(QUESTIONS_FILE):

    st.warning(
        "Interview has not been generated yet."
    )

    st.stop()

with open(
    QUESTIONS_FILE,
    "r",
    encoding="utf-8"
) as f:

    interview_questions = json.load(f)

questions = interview_questions["questions"]

# ==========================================
# Session State
# ==========================================

if "started" not in st.session_state:
    st.session_state.started = False

if "current_question" not in st.session_state:
    st.session_state.current_question = 0

if "answers" not in st.session_state:
    st.session_state.answers = []

if "interview_finished" not in st.session_state:
    st.session_state.interview_finished = False

if "next_clicked" not in st.session_state:
    st.session_state.next_clicked = False

# ==========================================
# Welcome Screen
# ==========================================

if not st.session_state.started:

    st.header("Welcome")

    st.write("""
You are about to start your AI Interview.

• Read each question carefully.

• Answer honestly.

• Click Next to continue.

Good Luck!
""")

    if st.button(
        "Start Interview",
        use_container_width=True
    ):

        st.session_state.started = True
        st.rerun()

    st.stop()

# ==========================================
# Finished Screen
# ==========================================

if st.session_state.interview_finished:

    st.success(
        "🎉 Interview Completed Successfully!"
    )

    st.info(
        "Your answers have been submitted successfully."
    )

    st.write(
        "Thank you for completing the interview."
    )

    if st.button(
        "Submit Interview",
        use_container_width=True
    ):

        if os.path.exists(
            QUESTIONS_FILE
        ):
            os.remove(
                QUESTIONS_FILE
            )

        st.session_state.interview_completed = True

        st.session_state.started = False
        st.session_state.current_question = 0
        st.session_state.answers = []
        st.session_state.interview_finished = False
        st.session_state.next_clicked = False

        for i in range(len(questions)):

            key = f"answer_{i}"

            if key in st.session_state:

                del st.session_state[key]

        st.switch_page(
            "pages/1_HR_Dashboard.py"
        )

    st.stop()

# ==========================================
# Current Question
# ==========================================

current = st.session_state.current_question

progress = (current + 1) / len(questions)

st.progress(progress)

question = questions[current]

st.subheader(
    f"Question {current + 1} / {len(questions)}"
)

col1, col2 = st.columns(2)

with col1:

    st.caption(
        f"Category: {question['category']}"
    )

with col2:

    st.caption(
        f"Difficulty: {question['difficulty']}"
    )

st.write(
    question["question"]
)

answer = st.text_area(
    "Your Answer",
    height=220,
    key=f"answer_{current}"
)

# ==========================================
# Next Question
# ==========================================

if st.button(
    "Next",
    disabled=st.session_state.next_clicked,
    use_container_width=True
):

    st.session_state.next_clicked = True

    if not answer.strip():

        st.session_state.next_clicked = False

        st.warning(
            "Please answer the question before continuing."
        )

        st.stop()

    st.session_state.answers.append({

        "question_id": current + 1,

        "question": question["question"],

        "category": question["category"],

        "difficulty": question["difficulty"],

        "expected_answer_points":
            question["expected_answer_points"],

        "answer": answer

    })

    with open(
        ANSWERS_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            st.session_state.answers,
            f,
            indent=4,
            ensure_ascii=False
        )

    # ==========================================
    # Next Question
    # ==========================================

    st.session_state.current_question += 1

    st.session_state.next_clicked = False

    if st.session_state.current_question >= len(questions):

        st.session_state.interview_finished = True

    st.rerun()