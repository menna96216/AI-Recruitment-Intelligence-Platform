import os
import json

from utils.interview_config_agent import generate_interview_config
from utils.question_generator_agent import generate_interview_questions

from utils.answer_evaluation_agent import evaluate_interview
from utils.interview_report_agent import generate_interview_report

from utils.final_decision_agent import generate_final_decision
from utils.career_agent import generate_career_report


# ==========================================
# Output Folder
# ==========================================

OUTPUT_FOLDER = "outputs"

os.makedirs(
    OUTPUT_FOLDER,
    exist_ok=True
)


# ==========================================
# Load JSON
# ==========================================

def load_json(filename):

    path = os.path.join(
        OUTPUT_FOLDER,
        filename
    )

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


# ==========================================
# Save JSON
# ==========================================

def save_json(data, filename):

    path = os.path.join(
        OUTPUT_FOLDER,
        filename
    )

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )


# ==========================================
# Pipeline 1
# Generate Interview
# ==========================================

def run_interview_pipeline():

    candidate_profile = load_json(
        "candidate_profile.json"
    )

    job_profile = load_json(
        "job_profile.json"
    )

    ats_report = load_json(
        "ats_report.json"
    )

    # مؤقتاً لحد ما نعمل Career بعد الـ Interview
    career_report = {

        "strengths": [],

        "improvement_areas": [],

        "learning_plan": [],

        "recommended_projects": []

    }

    interview_config = generate_interview_config(

        candidate_profile,

        job_profile,

        ats_report,

        career_report

    )

    save_json(

        interview_config,

        "interview_config.json"

    )

    interview_questions = generate_interview_questions(

        candidate_profile,

        job_profile,

        ats_report,

        interview_config

    )

    save_json(

        interview_questions,

        "interview_questions.json"

    )

    return interview_questions


# ==========================================
# Pipeline 2
# Generate Interview Report
# ==========================================

def generate_report_pipeline():

    # ===============================
    # Load Required Files
    # ===============================

    interview_config = load_json(
        "interview_config.json"
    )

    job_profile = load_json(
        "job_profile.json"
    )

    candidate_answers = load_json(
        "candidate_answers.json"
    )

    # ===============================
    # Evaluate Answers
    # ===============================

    answer_evaluations = evaluate_interview(
        candidate_answers
    )

    save_json(
        answer_evaluations,
        "answer_evaluations.json"
    )

    # ===============================
    # Generate Interview Report
    # ===============================

    interview_report = generate_interview_report(

        interview_config,

        job_profile,

        candidate_answers,

        answer_evaluations

    )

    # ==========================================
    # Add Question Details
    # ==========================================

    question_details = []

    for answer, evaluation in zip(

        candidate_answers,

        answer_evaluations

    ):

        question_details.append({

            "question_id":
                answer["question_id"],

            "question":
                answer["question"],

            "category":
                answer["category"],

            "difficulty":
                answer["difficulty"],

            "candidate_answer":
                answer["answer"],

            "expected_answer_points":
                answer["expected_answer_points"],

            "score":
                evaluation.get(
                    "score",
                    0
                ),

            "feedback":
                evaluation.get(
                    "feedback",
                    ""
                ),

            "strengths":
                evaluation.get(
                    "strengths",
                    []
                ),

            "missing_points":
                evaluation.get(
                    "missing_points",
                    []
                ),

            "improvement_feedback":
                evaluation.get(
                    "improvement_feedback",
                    ""
                )

        })

    interview_report["question_details"] = question_details

    save_json(

        interview_report,

        "interview_report.json"

    )

    return interview_report


# ==========================================
# Pipeline 3
# Final Recruitment Decision
# ==========================================

def final_decision_pipeline():

    candidate_profile = load_json(
        "candidate_profile.json"
    )

    job_profile = load_json(
        "job_profile.json"
    )

    ats_report = load_json(
        "ats_report.json"
    )

    interview_report = load_json(
        "interview_report.json"
    )

    final_decision = generate_final_decision(

        candidate_profile,

        job_profile,

        ats_report,

        interview_report

    )

    save_json(

        final_decision,

        "final_decision.json"

    )

    return final_decision


# ==========================================
# Pipeline 4
# Career Development Plan
# ==========================================

def career_pipeline():

    candidate_profile = load_json(
        "candidate_profile.json"
    )

    job_profile = load_json(
        "job_profile.json"
    )

    ats_report = load_json(
        "ats_report.json"
    )

    skill_gap_report = {

        "missing_required_skills":

            ats_report.get(
                "missing_required_skills",
                []
            ),

        "missing_preferred_skills":

            ats_report.get(
                "missing_preferred_skills",
                []
            )

    }

    career_report = generate_career_report(

        candidate_profile,

        job_profile,

        ats_report,

        skill_gap_report

    )

    save_json(

        career_report,

        "career_report.json"

    )

    return career_report