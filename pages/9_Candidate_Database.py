import streamlit as st

from utils.mongodb import (
    get_all_candidates,
    count_candidates,
    get_top_candidates
)

from collections import Counter



# ==========================================
# Page Config
# ==========================================

st.set_page_config(
    page_title="Candidate Database",
    page_icon="👥",
    layout="wide"
)



# ==========================================
# Header
# ==========================================

st.title(
    "👥 Candidate Database"
)


st.caption(
    "MongoDB Powered Candidate Management System"
)


st.divider()



# ==========================================
# Refresh
# ==========================================

if st.button(
    "🔄 Refresh Database"
):

    st.cache_data.clear()

    st.rerun()



# ==========================================
# Load Data
# ==========================================

@st.cache_data(ttl=10)
def load_candidates():

    return get_all_candidates()



try:

    candidates = load_candidates()


except Exception as e:

    st.error(
        f"MongoDB Error: {e}"
    )

    st.stop()



# ==========================================
# Statistics
# ==========================================

total_candidates = count_candidates()


scores = [

    c.get(
        "ats_score",
        0
    )

    for c in candidates

]


average_score = (

    sum(scores) / len(scores)

    if scores

    else 0

)



strong = len(

    [

        x for x in scores

        if x >= 80

    ]

)


medium = len(

    [

        x for x in scores

        if 60 <= x < 80

    ]

)


weak = len(

    [

        x for x in scores

        if x < 60

    ]

)



col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Total Candidates",
        total_candidates
    )


with col2:

    st.metric(
        "Average ATS",
        f"{average_score:.1f}%"
    )


with col3:

    st.metric(
        "Strong Candidates",
        strong
    )


with col4:

    st.metric(
        "Database",
        "Connected ✅"
    )



st.divider()



# ==========================================
# Distribution
# ==========================================

st.subheader(
    "📊 Candidate Distribution"
)


c1,c2,c3 = st.columns(3)


with c1:

    st.success(
        f"🟢 Strong\n\n{strong}"
    )


with c2:

    st.warning(
        f"🟡 Average\n\n{medium}"
    )


with c3:

    st.error(
        f"🔴 Weak\n\n{weak}"
    )



st.divider()



# ==========================================
# Ranking
# ==========================================

st.subheader(
    "🏆 Top Candidates"
)



top_candidates = get_top_candidates(
    5
)



ranking = []


for rank,candidate in enumerate(
    top_candidates,
    start=1
):

    profile = candidate.get(
        "candidate_profile",
        {}
    )


    ranking.append(
        {
            "Rank": rank,

            "Name":
            profile.get(
                "name",
                "Unknown"
            ),

            "ATS Score":
            f"{candidate.get('ats_score',0)}%"
        }
    )



if ranking:

    st.dataframe(
        ranking,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No candidates yet"
    )



st.divider()



# ==========================================
# ATS Analytics
# ==========================================

st.subheader(
    "📈 ATS Score Analytics"
)


if scores:

    st.line_chart(
        scores
    )

else:

    st.info(
        "No scores available"
    )



st.divider()



# ==========================================
# Skills Analytics
# ==========================================

st.subheader(
    "🔥 Most Common Skills"
)



all_skills=[]



for candidate in candidates:

    profile = candidate.get(
        "candidate_profile",
        {}
    )


    skills = profile.get(
        "skills",
        []
    )


    if isinstance(
        skills,
        list
    ):

        all_skills.extend(
            skills
        )


    elif isinstance(
        skills,
        str
    ):

        all_skills.extend(
            skills.split(",")
        )



if all_skills:

    skill_count = Counter(
        [

            s.strip()

            for s in all_skills

        ]
    )


    st.bar_chart(

        dict(
            skill_count.most_common(10)
        )

    )


else:

    st.info(
        "No skills data"
    )



st.divider()



# ==========================================
# Search
# ==========================================

st.subheader(
    "🔍 Search Candidates"
)


query = st.text_input(
    "Search by name or skill"
)



filtered = candidates



if query:

    query=query.lower()


    filtered=[]


    for candidate in candidates:


        profile=candidate.get(
            "candidate_profile",
            {}
        )


        name=str(
            profile.get(
                "name",
                ""
            )
        ).lower()


        skills=str(
            profile.get(
                "skills",
                ""
            )
        ).lower()


        if query in name or query in skills:

            filtered.append(
                candidate
            )



# ==========================================
# Cards
# ==========================================

st.subheader(
    f"📋 Candidates ({len(filtered)})"
)



for candidate in filtered:


    profile = candidate.get(
        "candidate_profile",
        {}
    )


    ats = candidate.get(
        "ats_report",
        {}
    )


    score = candidate.get(
        "ats_score",
        0
    )


    name = profile.get(
        "name",
        "Unknown"
    )


    email = profile.get(
        "email",
        "Not Available"
    )



    with st.container(
        border=True
    ):


        col1,col2,col3 = st.columns(
            [3,2,1]
        )


        with col1:

            st.subheader(
                f"👤 {name}"
            )

            st.write(
                f"📧 {email}"
            )


        with col2:

            st.metric(
                "ATS Score",
                f"{score}%"
            )


        with col3:

            if score >=80:

                st.success(
                    "Strong"
                )

            elif score>=60:

                st.warning(
                    "Average"
                )

            else:

                st.error(
                    "Weak"
                )



        with st.expander(
            "View Details"
        ):


            st.markdown(
                "### Candidate Profile"
            )


            st.json(
                profile
            )


            st.markdown(
                "### Matched Skills"
            )


            st.write(
                ats.get(
                    "matched_required_skills",
                    []
                )
            )


            st.markdown(
                "### Missing Skills"
            )


            st.write(
                ats.get(
                    "missing_required_skills",
                    []
                )
            )


            st.markdown(
                "### Full Record"
            )


            st.json(
                candidate
            )



st.divider()


st.caption(
    "AI Recruitment Intelligence Platform | MongoDB Candidate Database"
)