import json

from utils.helper import generate_json
from utils.json_utils import extract_json


# ==========================================
# Evaluate Single Answer
# ==========================================

def evaluate_answer(interview_item):

    evaluation_prompt = f"""
You are an Answer Evaluation Agent
for an AI Recruitment Intelligence Platform.

Evaluate ONE interview answer.

Return ONLY valid JSON.

Do NOT write markdown.
Do NOT write explanations.
Do NOT write extra text.

Required JSON format:

{{
    "question_id": {interview_item["question_id"]},
    "score": 0,
    "feedback": "",
    "strengths": [],
    "missing_points": [],
    "improvement_feedback": ""
}}

====================
SCORING RULES
====================

Score from 0 to 10.

0-3
Poor answer.

4-6
Partially correct.

7-8
Good answer.

9-10
Excellent answer.

====================
Evaluate Based On
====================

- Technical correctness
- Completeness
- Relevance
- Clarity
- Practical understanding

====================
Interview Question
====================

{interview_item["question"]}

====================
Question Category
====================

{interview_item["category"]}

====================
Candidate Answer
====================

{interview_item["answer"]}

====================
Expected Answer Points
====================

{json.dumps(interview_item["expected_answer_points"], indent=4)}

"""

    response = generate_json(
        evaluation_prompt
    )
    print("=" * 80)
    print("LLM Response:")
    print(response)
    print("=" * 80)

    evaluation = extract_json(
        response
    )

    return evaluation


# ==========================================
# Evaluate Whole Interview
# ==========================================

def evaluate_interview(interview_answers):

    evaluations = []

    total_score = 0

    for item in interview_answers:

        evaluation = evaluate_answer(item)

        evaluations.append(
            evaluation
        )

        total_score += evaluation.get(
            "score",
            0
        )

    return evaluations