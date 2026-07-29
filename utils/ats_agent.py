from utils.skills_utils import normalize_skill


skill_aliases = {

    "python programming": [
        "python",
        "python programming"
    ],

    "machine learning algorithms": [
        "machine learning",
        "ml",
        "supervised learning",
        "unsupervised learning",
        "scikit learn",
        "scikit-learn"
    ],

    "deep learning": [
        "deep learning",
        "ann",
        "cnn",
        "tensorflow",
        "pytorch"
    ],

    "computer vision": [
        "computer vision",
        "opencv",
        "yolo",
        "yolov8",
        "faster r cnn",
        "mediapipe",
        "object detection"
    ],

    "nlp": [
        "nlp",
        "natural language processing",
        "transformers",
        "tokenization",
        "embeddings",
        "text classification"
    ],

    "data preprocessing": [
        "data preprocessing",
        "preprocessing",
        "data cleaning",
        "data preparation"
    ],

    "deploying ml models using apis or streamlit": [
        "streamlit",
        "deployment",
        "model deployment"
    ],

    "mlops practices": [
        "mlops",
        "mlflow",
        "hugging face"
    ],

    "cloud platforms": [
        "cloud",
        "azure",
        "aws",
        "gcp"
    ]

}


def skill_match(job_skill, candidate_skills):

    job_skill = normalize_skill(job_skill)

    candidate_skills = [

        normalize_skill(skill)

        for skill in candidate_skills

    ]

    if job_skill in candidate_skills:

        return True

    if job_skill in skill_aliases:

        for alias in skill_aliases[job_skill]:

            alias = normalize_skill(alias)

            for skill in candidate_skills:

                if alias in skill:

                    return True

    return False


def calculate_ats_score(candidate_profile, job_profile):

    candidate_skills = candidate_profile.get(
        "skills_normalized",
        []
    )

    required_skills = job_profile.get(
        "required_skills",
        []
    )

    preferred_skills = job_profile.get(
        "preferred_skills",
        []
    )

    matched_required = []
    missing_required = []

    for skill in required_skills:

        if skill_match(skill, candidate_skills):

            matched_required.append(skill)

        else:

            missing_required.append(skill)

    matched_preferred = []
    missing_preferred = []

    for skill in preferred_skills:

        if skill_match(skill, candidate_skills):

            matched_preferred.append(skill)

        else:

            missing_preferred.append(skill)

    required_score = 0

    if required_skills:

        required_score = (
            len(matched_required)
            /
            len(required_skills)
        ) * 80

    preferred_score = 0

    if preferred_skills:

        preferred_score = (
            len(matched_preferred)
            /
            len(preferred_skills)
        ) * 20

    return {

        "ats_score": round(
            required_score + preferred_score,
            2
        ),

        "matched_required_skills": matched_required,

        "missing_required_skills": missing_required,

        "matched_preferred_skills": matched_preferred,

        "missing_preferred_skills": missing_preferred

    }
    
# ==========================================
# Wrapper Function
# ==========================================

def generate_ats_report(

    candidate_profile,

    job_profile

):

    return calculate_ats_score(

        candidate_profile,

        job_profile

    )