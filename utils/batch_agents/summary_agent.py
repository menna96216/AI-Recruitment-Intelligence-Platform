import json

from utils.helper import generate_json
from utils.json_utils import extract_json


# ==========================================
# Batch Recruitment Summary Agent
# ==========================================

def generate_batch_summary(

    ranking_result

):

    summary_prompt = f"""
You are an HR Recruitment Manager.

Generate a concise executive summary
for a batch recruitment process.

==================================================
INPUT
==================================================

Ranked Candidates

==================================================
OUTPUT
==================================================

Return ONLY valid JSON.

No markdown.

No explanations.

Required format:

{{
    "total_candidates":0,

    "excellent_matches":0,

    "strong_matches":0,

    "good_matches":0,

    "average_matches":0,

    "weak_matches":0,

    "best_candidate":"",

    "best_candidate_score":0,

    "overall_summary":""
}}

==================================================
RULES
==================================================

excellent_matches

Count recommendation == Excellent Match

--------------------------------------

strong_matches

Count recommendation == Strong Match

--------------------------------------

good_matches

Count recommendation == Good Match

--------------------------------------

average_matches

Count recommendation == Average Match

--------------------------------------

weak_matches

Count recommendation == Weak Match

--------------------------------------

best_candidate

Rank 1 candidate

--------------------------------------

overall_summary

Write 3-5 professional sentences.

Mention:

• total candidates

• quality of candidates

• strongest overall observations

• hiring recommendation

==================================================
RANKING
==================================================

{json.dumps(ranking_result, indent=4)}

"""

    response = generate_json(

        summary_prompt

    )

    summary = extract_json(

        response

    )

    return summary