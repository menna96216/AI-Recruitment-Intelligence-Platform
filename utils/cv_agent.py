import json

from utils.helper import generate_json
from utils.json_utils import extract_json


CV_PARSER_PROMPT = """
You are a CV Information Extraction Agent.

Extract structured candidate information from the CV text.

Return ONLY valid JSON.

Required format:

{
    "name": "",
    "contact": {
        "email": "",
        "phone": "",
        "location": ""
    },
    "summary": "",
    "skills": [],
    "experience": [],
    "projects": [],
    "education": [],
    "certificates": []
}

Rules:

- Do not invent information.
- Use only the CV.
- Return JSON only.
"""


def parse_cv(cv_text):

    prompt = f"""

{CV_PARSER_PROMPT}

CV Text:

{cv_text}

"""

    response = generate_json(prompt)

    candidate_profile = extract_json(response)

    return candidate_profile