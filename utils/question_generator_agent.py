import json

from utils.helper import generate_json
from utils.json_utils import extract_json


def generate_interview_questions(
    candidate_profile,
    job_profile,
    ats_report,
    interview_config
):

    # ==========================================
    # Reduce Prompt Size
    # ==========================================

    candidate_summary = {

        "skills": candidate_profile.get(
            "skills",
            []
        ),

        "projects": candidate_profile.get(
            "projects",
            []
        ),

        "experience": candidate_profile.get(
            "experience",
            []
        )

    }

    job_summary = {

        "job_title": job_profile.get(
            "job_title",
            ""
        ),

        "required_skills": job_profile.get(
            "required_skills",
            []
        ),

        "preferred_skills": job_profile.get(
            "preferred_skills",
            []
        )

    }

    ats_summary = {

        "ats_score": ats_report.get(
            "ats_score",
            0
        ),

        "missing_required_skills": ats_report.get(
            "missing_required_skills",
            []
        ),

        "missing_preferred_skills": ats_report.get(
            "missing_preferred_skills",
            []
        )

    }

    config_summary = {

        "interview_type": interview_config.get(
            "interview_type",
            ""
        ),

        "difficulty": interview_config.get(
            "difficulty",
            ""
        ),

        "number_of_questions": interview_config.get(
            "number_of_questions",
            5
        ),

        "focus_areas": interview_config.get(
            "focus_areas",
            []
        )

    }

    # ==========================================
    # Prompt
    # ==========================================

    prompt = f"""
You are an AI Technical Interview Question Generator.

Generate realistic interview questions.

Return ONLY valid JSON.

No markdown.

No explanations.

Required format:

{{
    "questions":[
        {{
            "question":"",
            "category":"",
            "difficulty":"",
            "expected_answer_points":[]
        }}
    ]
}}

Generate exactly
{config_summary["number_of_questions"]}
questions.

Use:

Interview Type:
{config_summary["interview_type"]}

Difficulty:
{config_summary["difficulty"]}

Focus Areas:
{json.dumps(config_summary["focus_areas"], indent=4)}

Candidate Summary:
{json.dumps(candidate_summary, indent=4)}

Job Summary:
{json.dumps(job_summary, indent=4)}

ATS Summary:
{json.dumps(ats_summary, indent=4)}
"""

    response = generate_json(prompt)

    questions = extract_json(response)

    return questions