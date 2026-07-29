import json

from utils.helper import generate_json
from utils.json_utils import extract_json


# ==========================================
# Interview Report Generator
# ==========================================

def generate_interview_report(

    interview_config,

    job_profile,

    conversation,

    answer_evaluations

):

    interview_report_prompt = f"""
You are a Senior Technical Hiring Manager.

You are responsible for generating the FINAL interview report
for an AI Recruitment Intelligence Platform.

You MUST evaluate the candidate ONLY using the provided interview data.

==================================================
INPUTS
==================================================

1. Interview Configuration

2. Job Profile

3. Candidate Answers

4. Individual Answer Evaluations

==================================================
IMPORTANT RULES
==================================================

Return ONLY valid JSON.

No markdown.

No explanations.

No extra text.

Do NOT invent information.

Base every conclusion ONLY on the supplied interview answers
and evaluation results.

==================================================
OUTPUT FORMAT
==================================================

Return EXACTLY this JSON schema:

{{
    "overall_score": 0,
    "performance_level": "",
    "summary": "",
    "strengths": [],
    "weaknesses": [],
    "missing_skills": [],
    "improvement_recommendations": [],
    "hiring_recommendation": "",

    "question_details":[
        {{
            "question_id":0,
            "question":"",
            "category":"",
            "difficulty":"",
            "candidate_answer":"",
            "expected_answer_points":[],
            "score":0,
            "feedback":"",
            "strengths":[],
            "missing_points":[],
            "improvement_feedback":""
        }}
    ]
}}

==================================================
OVERALL SCORE
==================================================

Calculate the average score of ALL evaluated questions.

Return ONE decimal place.

==================================================
PERFORMANCE LEVEL
==================================================

If score >= 9

Excellent

If score >= 7

Good

If score >= 5

Average

Otherwise

Needs Improvement

==================================================
SUMMARY
==================================================

Write a professional summary (4-6 sentences).

Mention:

• Technical knowledge

• Communication

• Problem solving

• Confidence

• Overall readiness

==================================================
STRENGTHS
==================================================

Generate ONLY strengths supported by interview answers.

Return 3-6 items.

==================================================
WEAKNESSES
==================================================

Generate ONLY weaknesses supported by interview answers.

Return 3-6 items.

==================================================
MISSING SKILLS
==================================================

Compare interview performance against Job Profile.

Return ONLY skills that were demonstrated weakly.

==================================================
IMPROVEMENT RECOMMENDATIONS
==================================================

Provide actionable recommendations.

Examples:

Improve SQL joins

Practice System Design

Strengthen OOP

Study REST APIs

Practice behavioral interviews

==================================================
HIRING RECOMMENDATION
==================================================

Choose EXACTLY ONE:

Strong Hire

Hire

Consider

Reject

==================================================
QUESTION DETAILS
==================================================

Create ONE object for EVERY interview question.

Each object MUST contain:

- question_id
- question
- category
- difficulty
- candidate_answer
- expected_answer_points
- score
- feedback
- strengths
- missing_points
- improvement_feedback

IMPORTANT:

question
→ Candidate Answers

candidate_answer
→ Candidate Answers

expected_answer_points
→ Candidate Answers

score
→ Answer Evaluations

feedback
→ evaluation

strengths
→ strengths

missing_points
→ missing_points

improvement_feedback
→ improvement_feedback

Do NOT invent anything.

==================================================
INTERVIEW CONFIGURATION
==================================================

{json.dumps(interview_config, indent=4)}

==================================================
JOB PROFILE
==================================================

{json.dumps(job_profile, indent=4)}

==================================================
CANDIDATE ANSWERS
==================================================

{json.dumps(conversation, indent=4)}

==================================================
QUESTION EVALUATIONS
==================================================

{json.dumps(answer_evaluations, indent=4)}

"""

    response = generate_json(
        interview_report_prompt
    )

    interview_report = extract_json(
        response
    )

    return interview_report