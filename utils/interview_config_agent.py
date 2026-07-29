import json

from utils.helper import generate_json
from utils.json_utils import extract_json


def generate_interview_config(
    candidate_profile,
    job_profile,
    ats_report,
    career_report
):

    interview_config_prompt = f"""
You are an Interview Configuration Agent
for an AI Recruitment Intelligence Platform.

Your task is to configure a realistic personalized interview
for any job role based on the actual job requirements.

Analyze ONLY:

1. Candidate Profile
2. Job Profile
3. ATS Report
4. Career Report

====================
OUTPUT RULES
====================

Return ONLY valid JSON.

Do not add markdown.

Do not add explanations.

Follow exactly this JSON structure.

Do not add extra keys.

Required JSON format:

{{
    "interview_type": "",
    "interview_goal": "",
    "difficulty": "",
    "number_of_questions": 0,
    "focus_areas": []
}}

====================
INTERVIEW TYPE RULES
====================

Select the most suitable interview type based on the Job Profile.

Available options:

- Technical Interview
- HR Interview
- Mixed Interview
- Project Discussion
- Domain Knowledge Interview

Rules:

Technical Interview:
Use when the role requires technical knowledge,
engineering skills,
programming,
tools,
frameworks,
or practical implementation.

HR Interview:
Use when communication,
behavior,
motivation,
or culture fit are the main focus.

Mixed Interview:
Use when both technical
and behavioral skills are important.

Project Discussion:
Use when projects are highly relevant.

Domain Knowledge Interview:
Use for specialized professions.

====================
INTERVIEW GOAL RULES
====================

Generate one short interview goal.

====================
DIFFICULTY RULES
====================

Junior:
Easy or Medium

Mid-Level:
Medium

Senior:
Medium or Hard

====================
NUMBER OF QUESTIONS
====================

Choose:

5
8
10

====================
FOCUS AREAS RULES
====================

Generate interview topics from:

- Required skills
- Preferred skills
- Job responsibilities

Generate between 5 and 10 focus areas.

====================
CANDIDATE PROFILE
====================

{json.dumps(candidate_profile, indent=4)}

====================
ATS REPORT
====================

{json.dumps(ats_report, indent=4)}

====================
CAREER REPORT
====================

{json.dumps(career_report, indent=4)}

====================
JOB PROFILE
====================

{json.dumps(job_profile, indent=4)}
"""

    response = generate_json(
        interview_config_prompt
    )

    interview_config = extract_json(
        response
    )

    return interview_config