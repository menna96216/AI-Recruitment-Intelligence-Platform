import streamlit as st



# ==========================================
# Page Config
# ==========================================

st.set_page_config(
    page_title="AI Recruitment Intelligence Platform",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)



# ==========================================
# Authentication State
# ==========================================

if "authenticated" not in st.session_state:

    st.session_state.authenticated = False



# ==========================================
# Hide Sidebar & Pages Before Login
# ==========================================

if not st.session_state.authenticated:

    st.markdown(
        """
        <style>

        [data-testid="stSidebar"] {
            display: none;
        }


        [data-testid="stSidebarNav"] {
            display: none;
        }

        </style>
        """,
        unsafe_allow_html=True
    )



# ==========================================
# Custom Styling
# ==========================================

st.markdown(
    """
    <style>

    .login-card {

        background-color: #ffffff;

        padding: 40px;

        border-radius: 20px;

        box-shadow: 0px 8px 30px rgba(0,0,0,0.08);

        text-align: center;

    }


    .login-title {

        font-size: 32px;

        font-weight: 700;

        text-align:center;

    }


    .login-subtitle {

        color: gray;

        text-align:center;

        font-size:18px;

    }


    .main-title {

        font-size: 40px;

        font-weight:700;

    }


    </style>
    """,
    unsafe_allow_html=True
)



# ==========================================
# Password
# ==========================================

PASSWORD = "admin123"



# ==========================================
# Login Page
# ==========================================

if not st.session_state.authenticated:


    st.markdown(
        "<br><br><br>",
        unsafe_allow_html=True
    )


    col1, col2, col3 = st.columns(
        [1,2,1]
    )


    with col2:


        st.markdown(
            '<div class="login-card">',
            unsafe_allow_html=True
        )


        st.markdown(
            """
            <div class="login-title">
            🤖 AI Recruitment Intelligence Platform
            </div>
            """,
            unsafe_allow_html=True
        )


        st.markdown(
            """
            <div class="login-subtitle">
            Enterprise AI-Powered Recruitment & Talent Intelligence System
            </div>
            """,
            unsafe_allow_html=True
        )


        st.write("")


        password = st.text_input(
            "🔐 Enter Access Password",
            type="password"
        )


        if st.button(
            "Login",
            use_container_width=True
        ):


            if password == PASSWORD:


                st.session_state.authenticated = True


                st.success(
                    "Login Successful"
                )


                st.rerun()


            else:


                st.error(
                    "Incorrect Password"
                )


        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


    st.stop()



# ==========================================
# Sidebar After Login
# ==========================================

with st.sidebar:


    st.title(
        "🤖 AI Recruitment"
    )


    st.caption(
        "Intelligence Platform"
    )


    st.divider()



    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):


        st.session_state.authenticated = False


        st.rerun()



# ==========================================
# Home Header
# ==========================================


st.markdown(

    """
    <div class="main-title">
    🤖 AI Recruitment Intelligence Platform
    </div>
    """,

    unsafe_allow_html=True

)



st.caption(
    "Enterprise AI-Powered Recruitment & Talent Intelligence System"
)



st.divider()



# ==========================================
# Hero Section
# ==========================================

st.markdown(
"""
## Transforming Recruitment with Artificial Intelligence


The **AI Recruitment Intelligence Platform** is an end-to-end intelligent hiring
solution designed to automate and optimize recruitment using
multiple AI agents.


From CV screening to interview evaluation,
hiring decisions, candidate ranking,
and personalized career development,
the platform helps HR teams recruit faster,
smarter, and with greater consistency.
"""
)



st.divider()



# ==========================================
# Platform Overview
# ==========================================

st.header(
    "🚀 Platform Overview"
)



st.write(
"""
The platform combines **Large Language Models (LLMs)**,
AI Agents, and intelligent decision pipelines to create
a fully automated recruitment workflow.


It evaluates technical and soft skills,
generates AI interviews,
analyzes candidate performance,
and provides data-driven hiring recommendations.
"""
)



# ==========================================
# Metrics
# ==========================================

st.subheader(
    "📊 Platform Statistics"
)



col1, col2, col3, col4 = st.columns(4)



with col1:

    st.metric(
        "AI Agents",
        "8+"
    )


with col2:

    st.metric(
        "Workflow Steps",
        "8"
    )


with col3:

    st.metric(
        "Generated Reports",
        "6"
    )


with col4:

    st.metric(
        "System Status",
        "Ready"
    )



st.divider()



# ==========================================
# Features
# ==========================================

st.header(
    "✨ Core Features"
)



left, right = st.columns(2)



with left:


    st.markdown(
"""
### 📄 Intelligent Screening


✅ AI CV Parsing

✅ Job Description Analysis

✅ ATS Scoring

✅ Skills Matching

✅ Skill Gap Detection

✅ Candidate Ranking
"""
)



with right:


    st.markdown(
"""
### 🎯 Intelligent Hiring


✅ AI Interview Generation

✅ Answer Evaluation

✅ Interview Report

✅ Hiring Recommendation

✅ Career Development Plan

✅ Recruitment Analytics
"""
)



st.divider()



# ==========================================
# Workflow
# ==========================================

st.header(
    "🔄 Recruitment Workflow"
)



st.markdown(
"""
1. 📄 Upload Job Description

2. 👤 Upload Candidate CV

3. 📊 ATS Analysis

4. 🎤 AI Interview Simulation

5. 📑 Interview Performance Report

6. ✅ Final Hiring Decision

7. 📚 Personalized Career Development Plan

8. 📈 Recruitment Analytics & Administration
"""
)



st.divider()



# ==========================================
# Technology Stack
# ==========================================

st.header(
    "🛠️ Technology Stack"
)



st.markdown(
"""
- **Large Language Models (LLMs)**

- **LangGraph Multi-Agent Architecture**

- **Streamlit**

- **Python**

- **MongoDB**

- **SQLite**

- **JSON Pipelines**

- **Prompt Engineering**

- **AI Interview Evaluation**

- **Recruitment Intelligence**
"""
)



st.divider()



# ==========================================
# Footer
# ==========================================

st.info(
"""
This platform demonstrates how Artificial Intelligence can support HR professionals
by reducing hiring time, improving candidate evaluation,
and delivering consistent recruitment decisions.
"""
)