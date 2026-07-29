from utils.helper import generate_json
from utils.json_utils import extract_json


JOB_ANALYSIS_PROMPT = """
You are a recruitment job analysis assistant.

Extract structured information from the job description.

Return ONLY valid JSON.

Required format:

{
    "job_title":"",
    "required_skills":[],
    "preferred_skills":[],
    "experience_requirements":[],
    "education_requirements":[]
}

Rules:

- Extract only information mentioned in the job description.
- Keep every skill as a separate item.
- Do not invent information.
- Return JSON only.
"""


def analyze_job(job_text):

    prompt = f"""

{JOB_ANALYSIS_PROMPT}

Job Description:

{job_text}

"""

    response = generate_json(prompt)

    job_profile = extract_json(response)

    return job_profile