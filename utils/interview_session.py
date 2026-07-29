def initialize_interview(interview_questions):

    return {

        "current_question": 0,

        "questions": interview_questions["questions"],

        "answers": [],

        "completed": False

    }


def save_answer(session, answer):

    question = session["questions"][session["current_question"]]

    session["answers"].append(

        {

            "question_id": session["current_question"] + 1,

            "question": question["question"],

            "category": question["category"],

            "difficulty": question["difficulty"],

            "expected_answer_points": question["expected_answer_points"],

            "answer": answer

        }

    )

    session["current_question"] += 1

    if session["current_question"] >= len(session["questions"]):

        session["completed"] = True

    return session