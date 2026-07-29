import re


def flatten_skills(skills):

    extracted_skills = []

    for skill in skills:

        if ":" in skill:

            _, items = skill.split(":", 1)

            for item in items.split(","):

                extracted_skills.append(
                    item.strip()
                )

        else:

            extracted_skills.append(
                skill.strip()
            )

    return extracted_skills



def normalize_skill(skill):

    skill = skill.lower()

    skill = re.sub(
        r"\s+",
        " ",
        skill
    )

    skill = skill.replace("-", " ")

    skill = skill.replace("_", " ")

    skill = skill.replace("&", "and")

    return skill.strip()



def prepare_candidate_skills(candidate_profile):

    raw_skills = candidate_profile.get(
        "skills",
        []
    )

    skills = flatten_skills(
        raw_skills
    )

    normalized = list(

        set(

            normalize_skill(skill)

            for skill in skills

        )

    )

    candidate_profile["skills_original"] = skills

    candidate_profile["skills_normalized"] = normalized

    return candidate_profile