import json


def extract_json(text):

    text = text.replace("```json", "")
    text = text.replace("```", "")
    text = text.strip()

    start = text.find("{")

    if start == -1:
        raise ValueError("No JSON object found.")

    count = 0
    end = None

    for i in range(start, len(text)):

        if text[i] == "{":
            count += 1

        elif text[i] == "}":
            count -= 1

        if count == 0:
            end = i + 1
            break

    if end is None:
        raise ValueError("Incomplete JSON object.")

    json_text = text[start:end]

    try:
        return json.loads(json_text)

    except json.JSONDecodeError as e:

        print("\n" + "=" * 80)
        print("INVALID JSON RECEIVED")
        print("=" * 80)
        print(json_text)
        print("=" * 80)
        print(e)
        print("=" * 80 + "\n")

        raise ValueError(
            f"Invalid JSON returned by model:\n{json_text}"
        ) from e