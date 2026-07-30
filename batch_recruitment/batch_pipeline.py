from utils.pdf_parser import extract_pdf_text
from utils.cv_agent import parse_cv
from utils.job_agent import analyze_job
from utils.ats_agent import generate_ats_report
from utils.skills_utils import prepare_candidate_skills



def process_candidate(
    pdf_path,
    job_description
):

    cv_text = extract_pdf_text(
        pdf_path
    )


    candidate_profile = parse_cv(
        cv_text
    )


    candidate_profile = prepare_candidate_skills(
        candidate_profile
    )


    job_profile = analyze_job(
        job_description
    )


    ats_report = generate_ats_report(
        candidate_profile,
        job_profile
    )


    return {

        "candidate_profile": candidate_profile,

        "job_profile": job_profile,

        "ats_report": ats_report

    }



def process_multiple_candidates(
    pdf_files,
    job_description
):

    results = []


    for pdf in pdf_files:

        result = process_candidate(
            pdf,
            job_description
        )

        results.append(
            result
        )


    return results