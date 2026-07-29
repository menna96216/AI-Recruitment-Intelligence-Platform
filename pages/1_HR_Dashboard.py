import streamlit as st
import tempfile
import os
import json
from datetime import datetime, timezone

from utils.pdf_parser import extract_pdf_text
from utils.cv_agent import parse_cv
from utils.skills_utils import prepare_candidate_skills
from utils.job_agent import analyze_job
from utils.ats_agent import calculate_ats_score

from utils.mongodb import (
    insert_candidate,
    jobs_collection
)

# Interview Pipeline
from utils.interview_pipeline import (
    run_interview_pipeline,
    generate_report_pipeline,
    final_decision_pipeline,
    career_pipeline
)


# ==========================================
# Page Config
# ==========================================

st.set_page_config(
    page_title="HR Dashboard",
    page_icon="👨‍💼",
    layout="wide"
)


# ==========================================
# Output Folder
# ==========================================

OUTPUT_FOLDER = "outputs"

os.makedirs(
    OUTPUT_FOLDER,
    exist_ok=True
)


# ==========================================
# Save JSON
# ==========================================

def save_json(data, filename):

    path = os.path.join(
        OUTPUT_FOLDER,
        filename
    )

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )


# ==========================================
# MongoDB Safe Insert
# ==========================================

def safe_insert(collection, data):

    try:

        result = collection.insert_one(
            data
        )

        return str(
            result.inserted_id
        )

    except Exception as e:

        st.warning(
            f"MongoDB Warning: {e}"
        )

        return None



# ==========================================
# Session State
# ==========================================

if "job_path" not in st.session_state:
    st.session_state.job_path = None


if "cv_path" not in st.session_state:
    st.session_state.cv_path = None


if "cv_name" not in st.session_state:
    st.session_state.cv_name = None


if "candidate_id" not in st.session_state:
    st.session_state.candidate_id = None


if "job_id" not in st.session_state:
    st.session_state.job_id = None



# ==========================================
# Workflow State
# ==========================================

if "ats_completed" not in st.session_state:

    st.session_state.ats_completed = False


if "interview_completed" not in st.session_state:

    st.session_state.interview_completed = False



# ==========================================
# Title
# ==========================================

st.title(
    "👨‍💼 HR Dashboard"
)


st.markdown(
"""
Manage the complete recruitment workflow
from candidate screening
to final hiring decision.
"""
)


st.markdown("---")



# ==========================================
# Step 1
# ==========================================

with st.container(border=True):

    st.subheader(
        "📄 Step 1: Upload Job Description"
    )


    job_file = st.file_uploader(

        "Upload Job Description (TXT)",

        type=["txt"],

        key="job_description"

    )


    if job_file is not None:


        with tempfile.NamedTemporaryFile(

            delete=False,

            suffix=".txt"

        ) as tmp:


            tmp.write(
                job_file.read()
            )


            st.session_state.job_path = tmp.name



        st.success(
            "✅ Job Description uploaded successfully."
        )



# ==========================================
# Step 2
# ==========================================

with st.container(border=True):

    st.subheader(
        "📄 Step 2: Upload Candidate CV"
    )


    cv_file = st.file_uploader(

        "Upload Candidate CV (PDF)",

        type=["pdf"],

        key="candidate_cv"

    )


    if cv_file is not None:


        with tempfile.NamedTemporaryFile(

            delete=False,

            suffix=".pdf"

        ) as tmp:


            tmp.write(
                cv_file.read()
            )


            st.session_state.cv_path = tmp.name


            st.session_state.cv_name = cv_file.name



        st.success(
            "✅ Candidate CV uploaded successfully."
        )


# ==========================================
# Step 3
# ==========================================

with st.container(border=True):

    st.subheader(
        "📊 Step 3: ATS Analysis"
    )


    if st.button(
        "Run ATS Analysis",
        use_container_width=True
    ):


        if st.session_state.job_path is None:


            st.error(
                "Please upload the Job Description first."
            )


        elif st.session_state.cv_path is None:


            st.error(
                "Please upload the Candidate CV first."
            )


        else:


            progress = st.empty()


            with st.spinner(
                "Running ATS Analysis..."
            ):



                # ==============================
                # Extract CV Text
                # ==============================

                progress.info(
                    "📄 Reading Candidate CV..."
                )


                cv_text = extract_pdf_text(
                    st.session_state.cv_path
                )


                progress.success(
                    "✅ CV Text Extracted"
                )



                # ==============================
                # Parse CV
                # ==============================

                progress.info(
                    "🤖 Parsing Candidate Profile..."
                )


                candidate_profile = parse_cv(
                    cv_text
                )


                progress.success(
                    "✅ Candidate Profile Parsed"
                )



                # ==============================
                # Normalize Skills
                # ==============================

                candidate_profile = prepare_candidate_skills(
                    candidate_profile
                )


                progress.success(
                    "✅ Skills Normalized"
                )



                # ==============================
                # Read Job Description
                # ==============================

                progress.info(
                    "📄 Reading Job Description..."
                )


                with open(

                    st.session_state.job_path,

                    "r",

                    encoding="utf-8"

                ) as f:


                    job_text = f.read()



                progress.success(
                    "✅ Job Description Loaded"
                )



                # ==============================
                # Analyze Job
                # ==============================

                progress.info(
                    "🤖 Analyzing Job Description..."
                )


                job_profile = analyze_job(
                    job_text
                )


                progress.success(
                    "✅ Job Profile Created"
                )



                # ==============================
                # Calculate ATS
                # ==============================

                progress.info(
                    "📊 Calculating ATS Score..."
                )


                ats_report = calculate_ats_score(

                    candidate_profile,

                    job_profile

                )


                progress.success(
                    "✅ ATS Report Generated"
                )



                # ==============================
                # Save Local Outputs
                # ==============================


                progress.info(
                    "💾 Saving Outputs..."
                )


                save_json(

                    candidate_profile,

                    "candidate_profile.json"

                )


                save_json(

                    job_profile,

                    "job_profile.json"

                )


                save_json(

                    ats_report,

                    "ats_report.json"

                )



                progress.success(
                    "✅ Files Saved Successfully"
                )



                # ==================================
                # Save Job To MongoDB
                # ==================================


                job_data = {


                    "job_profile": job_profile,


                    "job_description": job_text,


                    "created_at": datetime.now(
                        timezone.utc
                    )

                }



                try:


                    job_id = safe_insert(

                        jobs_collection,

                        job_data

                    )


                    st.session_state.job_id = job_id



                except Exception as e:


                    st.warning(
                        f"Job MongoDB Error: {e}"
                    )



                # ==================================
                # Save Candidate To MongoDB
                # ==================================


                mongo_candidate = {


                    "candidate_name": candidate_profile.get(

                        "name",

                        st.session_state.cv_name

                    ),


                    "cv_filename": st.session_state.cv_name,


                    "candidate_profile": candidate_profile,


                    "job_id": st.session_state.job_id,


                    "ats_report": ats_report,


                    "ats_score": ats_report.get(

                        "ats_score",

                        0

                    ),


                    "created_at": datetime.now(
                        timezone.utc
                    )

                }



                candidate_id = safe_insert(

                    __import__(
                        "utils.mongodb",
                        fromlist=["candidates_collection"]
                    ).candidates_collection,

                    mongo_candidate

                )



                st.session_state.candidate_id = candidate_id



                if candidate_id:


                    progress.success(

                        f"✅ Candidate Stored in MongoDB ID: {candidate_id}"

                    )

                else:


                    progress.warning(

                        "⚠️ Candidate saved locally only."

                    )



            # ==============================
            # Finish ATS
            # ==============================


            st.session_state.ats_completed = True


            st.success(
                "✅ ATS Analysis Completed Successfully!"
            )



            st.metric(

                "ATS Score",

                f"{ats_report['ats_score']}%"

            )



            col1, col2 = st.columns(2)



            with col1:


                st.subheader(
                    "✅ Matched Required Skills"
                )


                st.write(
                    ats_report[
                        "matched_required_skills"
                    ]
                )



            with col2:


                st.subheader(
                    "❌ Missing Required Skills"
                )


                st.write(
                    ats_report[
                        "missing_required_skills"
                    ]
                )
                
                
# ==========================================
# Step 4
# ==========================================

with st.container(border=True):

    st.subheader(
        "🎤 Step 4: Interview Simulation"
    )


    if st.session_state.interview_completed:


        st.success(
            "✅ Interview Completed"
        )


        if st.button(
            "View Interview Report",
            use_container_width=True
        ):


            st.switch_page(
                "pages/4_Interview_Report.py"
            )


    else:


        st.write(
"""
Generate interview configuration and interview questions,
then redirect the candidate to the Interview page.
"""
        )



        if st.button(
            "Start Interview",
            disabled=not st.session_state.ats_completed,
            use_container_width=True
        ):


            if not os.path.exists(

                os.path.join(
                    OUTPUT_FOLDER,
                    "candidate_profile.json"
                )

            ):


                st.error(
                    "Please run ATS Analysis first."
                )


            else:


                with st.spinner(
                    "Preparing Interview..."
                ):


                    run_interview_pipeline()



                st.success(
                    "✅ Interview Questions Generated Successfully."
                )



                st.switch_page(
                    "pages/3_Interview.py"
                )




# ==========================================
# Step 5
# ==========================================

with st.container(border=True):


    st.subheader(
        "📑 Step 5: Interview Report"
    )


    st.write(
"""
Evaluate all candidate answers and generate
the complete interview report.
"""
    )



    if st.button(

        "Generate Interview Report",

        disabled=not os.path.exists(

            os.path.join(
                OUTPUT_FOLDER,
                "candidate_answers.json"
            )

        ),

        use_container_width=True

    ):



        with st.spinner(
            "Generating Interview Report..."
        ):


            generate_report_pipeline()



            # ==============================
            # Save Interview Report MongoDB
            # ==============================

            try:

                from utils.mongodb import interviews_collection


                with open(

                    os.path.join(
                        OUTPUT_FOLDER,
                        "interview_report.json"
                    ),

                    "r",

                    encoding="utf-8"

                ) as f:


                    interview_report = json.load(f)



                interview_data = {


                    "candidate_id":
                        st.session_state.candidate_id,


                    "interview_report":
                        interview_report,


                    "created_at":
                        datetime.now(
                            timezone.utc
                        )

                }


                safe_insert(

                    interviews_collection,

                    interview_data

                )


            except Exception as e:


                st.warning(
                    f"Interview MongoDB Error: {e}"
                )




        st.success(
            "✅ Interview Report Generated Successfully."
        )


        st.switch_page(
            "pages/4_Interview_Report.py"
        )




# ==========================================
# Step 6
# ==========================================

with st.container(border=True):


    st.subheader(
        "✅ Step 6: Final Recruitment Decision"
    )



    st.write(
"""
Generate the final hiring recommendation
based on ATS and Interview performance.
"""
    )



    if st.button(

        "Generate Final Decision",

        disabled=not os.path.exists(

            os.path.join(
                OUTPUT_FOLDER,
                "interview_report.json"
            )

        ),

        use_container_width=True

    ):



        with st.spinner(
            "Generating Final Decision..."
        ):



            final_decision_pipeline()



            # ==============================
            # Save Decision MongoDB
            # ==============================

            try:


                from utils.mongodb import decisions_collection



                with open(

                    os.path.join(
                        OUTPUT_FOLDER,
                        "final_decision.json"
                    ),

                    "r",

                    encoding="utf-8"

                ) as f:


                    decision = json.load(f)



                decision_data = {


                    "candidate_id":

                        st.session_state.candidate_id,


                    "decision":

                        decision,


                    "created_at":

                        datetime.now(
                            timezone.utc
                        )

                }



                safe_insert(

                    decisions_collection,

                    decision_data

                )



            except Exception as e:


                st.warning(
                    f"Decision MongoDB Error: {e}"
                )



        st.success(
            "✅ Final Recruitment Decision Generated Successfully."
        )


        st.switch_page(
            "pages/5_Final_Decision.py"
        )





# ==========================================
# Step 7
# ==========================================

with st.container(border=True):


    st.subheader(
        "📚 Step 7: Candidate Development Plan"
    )



    st.write(
"""
Generate a personalized learning roadmap
to improve the candidate's missing skills.
"""
    )



    if st.button(

        "Generate Development Plan",

        disabled=not os.path.exists(

            os.path.join(
                OUTPUT_FOLDER,
                "final_decision.json"
            )

        ),

        use_container_width=True

    ):



        with st.spinner(
            "Generating Development Plan..."
        ):



            career_pipeline()



            # ==============================
            # Save Career Plan MongoDB
            # ==============================

            try:


                from utils.mongodb import career_collection



                with open(

                    os.path.join(
                        OUTPUT_FOLDER,
                        "career_report.json"
                    ),

                    "r",

                    encoding="utf-8"

                ) as f:


                    career_report = json.load(f)



                career_data = {


                    "candidate_id":

                        st.session_state.candidate_id,


                    "career_plan":

                        career_report,


                    "created_at":

                        datetime.now(
                            timezone.utc
                        )

                }



                safe_insert(

                    career_collection,

                    career_data

                )


            except Exception as e:


                st.warning(
                    f"Career MongoDB Error: {e}"
                )



        st.success(
            "✅ Development Plan Generated Successfully."
        )



        st.switch_page(
            "pages/6_Career_Plan.py"
        )




# ==========================================
# Step 8
# ==========================================

with st.container(border=True):


    st.subheader(
        "📥 Step 8: Download Reports"
    )


    report_files = [

        "candidate_profile.json",

        "job_profile.json",

        "ats_report.json",

        "interview_config.json",

        "interview_questions.json",

        "candidate_answers.json",

        "answer_evaluations.json",

        "interview_report.json",

        "final_decision.json",

        "career_report.json"

    ]



    available_reports = [

        file

        for file in report_files

        if os.path.exists(

            os.path.join(
                OUTPUT_FOLDER,
                file
            )

        )

    ]



    if available_reports:


        selected_report = st.selectbox(

            "Choose Report",

            available_reports

        )



        with open(

            os.path.join(
                OUTPUT_FOLDER,
                selected_report
            ),

            "rb"

        ) as f:



            st.download_button(

                label="⬇ Download Selected Report",

                data=f,

                file_name=selected_report,

                mime="application/json",

                use_container_width=True

            )


    else:


        st.info(
            "No reports generated yet."
        )




# ==========================================
# Debug
# ==========================================

st.markdown("---")



with st.expander(
    "Debug Information"
):


    st.write(
        "Job File Path:"
    )

    st.write(
        st.session_state.job_path
    )


    st.write(
        "Candidate CV Path:"
    )

    st.write(
        st.session_state.cv_path
    )


    st.write(
        "Candidate MongoDB ID:"
    )

    st.write(
        st.session_state.candidate_id
    )


    st.write(
        "Job MongoDB ID:"
    )

    st.write(
        st.session_state.job_id
    )


    st.write(
        "Output Folder:"
    )

    st.write(
        OUTPUT_FOLDER
    )


    st.write(
        "Generated Files:"
    )


    generated_files = os.listdir(
        OUTPUT_FOLDER
    )


    if generated_files:

        st.write(
            generated_files
        )

    else:

        st.write(
            "No generated files."
        )