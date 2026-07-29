from utils.helper import generate_json
from utils.json_utils import extract_json


# ==========================================
# Career Development Agent
# ==========================================

def generate_career_report(

    candidate_profile,

    job_profile,

    ats_report,

    skill_gap_report

):

    career_prompt = f"""
You are the Career Development Agent
for an AI Recruitment Intelligence Platform.

Your task is to generate a realistic,
personalized Career Development Plan.

Use ONLY the provided information.

==================================================
INPUTS
==================================================

1. Candidate Profile

2. ATS Report

3. Skill Gap Report

4. Job Profile

==================================================
OUTPUT RULES
==================================================

Return ONLY valid JSON.

No markdown.

No explanations.

No additional text.

Required JSON format:

{{
    "target_role":"",
    "candidate_level":"",
    "strengths":[],
    "improvement_areas":[],
    "learning_plan":[
        {{
            "skill_name":"",
            "priority":"",
            "reason":"",
            "estimated_duration":"",
            "learning_resources":[]
        }}
    ],
    "recommended_projects":[
        {{
            "project_name":"",
            "related_skill":"",
            "difficulty":"",
            "description":"",
            "expected_outcome":""
        }}
    ],
    "career_advice":""
}}

==================================================
TARGET ROLE
==================================================

Extract the exact target job title
from the Job Profile.

==================================================
CANDIDATE LEVEL
==================================================

Choose ONLY ONE:

Intern

Junior

Mid-Level

Senior

Determine the level using ONLY:

• Education

• Experience

• Internship experience

• Projects

• Certifications

==================================================
STRENGTHS
==================================================

Generate strengths ONLY from
Candidate Profile and ATS Report.

Do NOT invent information.

==================================================
IMPROVEMENT AREAS
==================================================

Generate ONLY from Skill Gap Report.

Do NOT invent missing skills.

==================================================
LEARNING PLAN
==================================================

Create ONE learning plan item
for EACH missing skill.

Priority Rules:

High
→ Missing required skills

Medium
→ Missing preferred skills

Low
→ Optional improvements

For every skill include:

• skill_name

• priority

• reason

• estimated_duration
(Example:
2 weeks,
1 month,
2 months,
3 months)

• learning_resources

Learning resources should be realistic.

Examples:

Official Documentation

Coursera

Udemy

YouTube

freeCodeCamp

Kaggle

Hugging Face Course

Microsoft Learn

DeepLearning.AI

==================================================
RECOMMENDED PROJECTS
==================================================

Generate practical portfolio projects.

Each project must contain:

project_name

related_skill

difficulty
(Beginner / Intermediate / Advanced)

description

expected_outcome

Projects should help the candidate
become stronger for the target role.

==================================================
CAREER ADVICE
==================================================

Write a professional career recommendation.

Mention:

• Current readiness

• Main strengths

• Biggest weaknesses

• What to focus on next

Maximum 5 sentences.

==================================================
CANDIDATE PROFILE
==================================================

{candidate_profile}

==================================================
ATS REPORT
==================================================

{ats_report}

==================================================
SKILL GAP REPORT
==================================================

{skill_gap_report}

==================================================
JOB PROFILE
==================================================

{job_profile}

"""

    response = generate_json(
        career_prompt
    )

    career_report = extract_json(
        response
    )

    return career_report