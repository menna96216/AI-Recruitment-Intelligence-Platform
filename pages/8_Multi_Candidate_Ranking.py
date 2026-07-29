import streamlit as st
import json
import tempfile
import traceback
import os


from batch_recruitment.batch_pipeline import (
    process_multiple_candidates
)


from utils.batch_agents.ranking_agent import (
    rank_candidates
)


from utils.batch_agents.summary_agent import (
    generate_batch_summary
)


# ==========================================
# Page Config
# ==========================================

st.set_page_config(
    page_title="Multi Candidate Ranking",
    page_icon="🏆",
    layout="wide"
)


# ==========================================
# Title
# ==========================================

st.title(
    "🏆 Multi-Candidate Recruitment Ranking"
)

st.markdown("---")


st.write(
"""
Upload a Job Description together with multiple CVs.

The platform will automatically:

• Parse every CV

• Generate Candidate Profiles

• Run ATS Analysis

• Compare all candidates

• Rank them from best to worst

using AI.
"""
)


st.markdown("---")


# ==========================================
# Upload Section
# ==========================================

st.header(
    "📂 Upload Files"
)


job_description = st.text_area(

    "Paste Job Description",

    height=220

)



uploaded_cvs = st.file_uploader(

    "Upload Candidate CVs",

    type=["pdf"],

    accept_multiple_files=True

)



# ==========================================
# Run Analysis
# ==========================================

if st.button(

    "🚀 Analyze Candidates",

    use_container_width=True

):


    try:


        # ==============================
        # Validation
        # ==============================

        if not job_description.strip():

            st.error(
                "Please enter a Job Description."
            )

            st.stop()



        if not uploaded_cvs:


            st.error(
                "Please upload at least one CV."
            )

            st.stop()



        pdf_paths = []



        # ==============================
        # Save Temporary PDFs
        # ==============================

        with st.spinner(

            "Analyzing candidates..."

        ):


            for uploaded_file in uploaded_cvs:


                with tempfile.NamedTemporaryFile(

                    delete=False,

                    suffix=".pdf"

                ) as tmp:


                    tmp.write(

                        uploaded_file.read()

                    )


                    pdf_paths.append(

                        tmp.name

                    )



            # ==============================
            # CV Processing Pipeline
            # ==============================

            candidates = process_multiple_candidates(

                pdf_paths,

                job_description

            )



            # ==============================
            # Ranking Agent
            # ==============================

            ranking = rank_candidates(

                candidates,

                job_description

            )



            # ==============================
            # Summary Agent
            # ==============================

            summary = generate_batch_summary(

                ranking

            )



        st.success(

            "✅ Analysis Completed Successfully!"

        )



        st.markdown("---")



        # ==========================================
        # Executive Summary
        # ==========================================

        st.header(

            "📊 Executive Summary"

        )


        col1, col2, col3, col4 = st.columns(4)



        with col1:


            st.metric(

                "Candidates",

                summary.get(

                    "total_candidates",

                    0

                )

            )



        with col2:


            st.metric(

                "Best Candidate",

                summary.get(

                    "best_candidate",

                    "N/A"

                )

            )



        with col3:


            st.metric(

                "Best Score",

                summary.get(

                    "best_candidate_score",

                    0

                )

            )



        with col4:


            st.metric(

                "Excellent",

                summary.get(

                    "excellent_matches",

                    0

                )

            )



        st.info(

            summary.get(

                "overall_summary",

                ""

            )

        )



        st.markdown("---")



        # ==========================================
        # Ranking Results
        # ==========================================

        st.header(

            "🏆 Candidate Ranking"

        )


        ranking_list = ranking.get(

            "ranking",

            []

        )



        for candidate in ranking_list:



            with st.expander(


                f"#{candidate.get('rank')} - {candidate.get('candidate_name')}"


            ):



                col1, col2 = st.columns(2)



                with col1:


                    st.metric(

                        "ATS Score",

                        candidate.get(

                            "ats_score",

                            0

                        )

                    )



                with col2:


                    st.metric(

                        "Overall Score",

                        candidate.get(

                            "overall_score",

                            0

                        )

                    )



                st.write(

                    "**Recommendation:**",

                    candidate.get(

                        "recommendation",

                        ""

                    )

                )



                st.write(

                    "**Reason:**"

                )



                st.write(

                    candidate.get(

                        "reason",

                        ""

                    )

                )



        st.markdown("---")



        # ==========================================
        # Download
        # ==========================================


        st.download_button(


            label="⬇ Download Ranking JSON",


            data=json.dumps(

                ranking,

                indent=4,

                ensure_ascii=False

            ),


            file_name="candidate_ranking.json",


            mime="application/json",


            use_container_width=True

        )



        # Cleanup temp files

        for file in pdf_paths:

            if os.path.exists(file):

                os.remove(file)



    except Exception as e:


        st.error(

            "❌ Error occurred while processing."

        )


        st.write(

            str(e)

        )


        st.code(

            traceback.format_exc()

        )