from utils.helper import generate_json
from utils.json_utils import extract_json

import json


# ==========================================
# Multi Candidate Ranking Agent
# ==========================================

def rank_candidates(

    candidates,

    job_description

):

    ranking_prompt = f"""
You are a Senior Technical Recruiter.

Your task is to rank multiple candidates for ONE job position.

You MUST compare ALL candidates.

==================================================
INPUT
==================================================

You receive:

1. Job Description

2. Candidate Profiles

3. ATS Reports

==================================================
RULES
==================================================

Return ONLY valid JSON.

No markdown.

No explanations.

No extra text.

==================================================
OUTPUT FORMAT
==================================================

{{
    "ranking":[
        {{
            "rank":1,
            "candidate_name":"",
            "ats_score":0,
            "overall_score":0,
            "recommendation":"",
            "reason":""
        }}
    ]
}}

==================================================
SCORING
==================================================

Rank candidates using:

1. ATS Score

2. Skill Match

3. Missing Required Skills

4. Experience

5. Projects

6. Education

If candidate background is completely unrelated to the job field,
reduce the ranking significantly and mention career mismatch.

==================================================
RECOMMENDATION
==================================================

Choose ONLY ONE

Excellent Match

Strong Match

Good Match

Average Match

Weak Match

==================================================
REASON
==================================================

Explain in 2-4 sentences WHY this candidate received this rank.

Mention:

• strongest skills

• missing skills

• ATS score

==================================================
JOB DESCRIPTION
==================================================

{job_description}

==================================================
CANDIDATES
==================================================

{json.dumps(candidates, indent=4)}

"""

    response = generate_json(

        ranking_prompt

    )

    ranking = extract_json(

        response

    )

    return ranking