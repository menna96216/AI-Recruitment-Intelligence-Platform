from pymongo import MongoClient
from dotenv import load_dotenv
import os



# ==========================================
# Load Environment Variables
# ==========================================

load_dotenv()



MONGO_URI = os.getenv(
    "MONGO_URI"
)



if not MONGO_URI:

    raise ValueError(
        "MONGO_URI is missing in .env file"
    )



# ==========================================
# MongoDB Connection
# ==========================================

client = MongoClient(
    MONGO_URI
)



db = client[
    "AI_Recruitment_Platform"
]



# ==========================================
# Collections
# ==========================================


candidates_collection = db[
    "candidates"
]


jobs_collection = db[
    "jobs"
]


ats_collection = db[
    "ats_reports"
]


ranking_collection = db[
    "rankings"
]


interviews_collection = db[
    "interviews"
]


decisions_collection = db[
    "decisions"
]


career_collection = db[
    "career_plans"
]



# ==========================================
# Candidate Operations
# ==========================================


def insert_candidate(candidate_data):

    result = candidates_collection.insert_one(
        candidate_data
    )

    return str(
        result.inserted_id
    )



def get_all_candidates():

    candidates = list(

        candidates_collection.find(

            {},

            {
                "_id": 0
            }

        )
        .sort(

            "created_at",

            -1

        )

    )

    return candidates



def count_candidates():

    return candidates_collection.count_documents(
        {}
    )



def get_top_candidates(limit=10):

    candidates = list(

        candidates_collection.find(

            {},

            {
                "_id": 0
            }

        )
        .sort(

            "ats_score",

            -1

        )
        .limit(
            limit
        )

    )

    return candidates



def search_candidates(keyword):

    candidates = list(

        candidates_collection.find(

            {

                "$or": [

                    {
                        "candidate_profile.name":
                        {
                            "$regex": keyword,
                            "$options": "i"
                        }
                    },


                    {
                        "candidate_profile.skills":
                        {
                            "$regex": keyword,
                            "$options": "i"
                        }
                    }

                ]

            },

            {
                "_id":0
            }

        )

    )

    return candidates



def get_average_ats_score():

    pipeline = [

        {

            "$group":

            {

                "_id": None,

                "average":

                {

                    "$avg":
                    "$ats_score"

                }

            }

        }

    ]


    result = list(

        candidates_collection.aggregate(
            pipeline
        )

    )


    if result:

        return round(
            result[0]["average"],
            2
        )


    return 0



def delete_candidate(candidate_id):

    result = candidates_collection.delete_one(
        {
            "_id": candidate_id
        }
    )


    return result.deleted_count > 0



# ==========================================
# Job Operations
# ==========================================


def insert_job(job_data):

    result = jobs_collection.insert_one(
        job_data
    )

    return str(
        result.inserted_id
    )



def get_all_jobs():

    return list(

        jobs_collection.find(
            {},
            {
                "_id":0
            }
        )

    )



# ==========================================
# ATS Operations
# ==========================================


def insert_ats_report(ats_data):

    result = ats_collection.insert_one(
        ats_data
    )

    return str(
        result.inserted_id
    )



def get_all_ats_reports():

    return list(

        ats_collection.find(
            {},
            {
                "_id":0
            }
        )

    )



# ==========================================
# Ranking Operations
# ==========================================


def insert_ranking(ranking_data):

    result = ranking_collection.insert_one(
        ranking_data
    )

    return str(
        result.inserted_id
    )



# ==========================================
# Interview Operations
# ==========================================


def insert_interview(interview_data):

    result = interviews_collection.insert_one(
        interview_data
    )

    return str(
        result.inserted_id
    )



def get_all_interviews():

    return list(

        interviews_collection.find(
            {},
            {
                "_id":0
            }
        )

    )



# ==========================================
# Decision Operations
# ==========================================


def insert_decision(decision_data):

    result = decisions_collection.insert_one(
        decision_data
    )

    return str(
        result.inserted_id
    )



def get_all_decisions():

    return list(

        decisions_collection.find(
            {},
            {
                "_id":0
            }
        )

    )



# ==========================================
# Career Plan Operations
# ==========================================


def insert_career_plan(career_data):

    result = career_collection.insert_one(
        career_data
    )

    return str(
        result.inserted_id
    )



def get_all_career_plans():

    return list(

        career_collection.find(
            {},
            {
                "_id":0
            }
        )

    )



# ==========================================
# Recruitment Statistics
# ==========================================


def get_hiring_statistics():


    total = count_candidates()


    strong_candidates = candidates_collection.count_documents(

        {
            "ats_score":
            {
                "$gte":80
            }
        }

    )


    medium_candidates = candidates_collection.count_documents(

        {
            "ats_score":
            {
                "$gte":60,
                "$lt":80
            }
        }

    )


    weak_candidates = candidates_collection.count_documents(

        {
            "ats_score":
            {
                "$lt":60
            }
        }

    )


    return {


        "total_candidates": total,


        "strong_candidates": strong_candidates,


        "medium_candidates": medium_candidates,


        "weak_candidates": weak_candidates


    }



# ==========================================
# Connection Test
# ==========================================


try:

    client.admin.command(
        "ping"
    )


    print(
        "MongoDB Connected Successfully"
    )


except Exception as e:


    print(
        "MongoDB Connection Error:",
        e
    )