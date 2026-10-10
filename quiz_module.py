import json

from gemini_client import gemini_service


def generate_quiz(text: str) -> dict:
    """
    Generate exactly three MCQs.
    """

    prompt = f"""
You are EduGenie, an educational quiz generator.

Create exactly THREE multiple-choice questions
from the educational text below.

Each question must contain:

- question
- exactly four options
- correct_answer
- explanation

The correct_answer MUST exactly match one
of the four options.

Return ONLY JSON.

Required JSON structure:

{{
    "questions": [
        {{
            "question": "Question text",
            "options": [
                "Option A",
                "Option B",
                "Option C",
                "Option D"
            ],
            "correct_answer": "Option A",
            "explanation": "Explanation"
        }}
    ]
}}

Educational text:

{text}
"""

    raw_response = gemini_service.generate_json(
        prompt=prompt,
        temperature=0.4,
        max_output_tokens=3500
    )

    try:
        data = json.loads(raw_response)

    except json.JSONDecodeError as exc:
        raise RuntimeError(
            "Gemini returned invalid JSON for the quiz."
        ) from exc

    if not isinstance(data, dict):
        raise RuntimeError(
            "Quiz response must be a JSON object."
        )

    questions = data.get("questions")

    if not isinstance(questions, list):
        raise RuntimeError(
            "Quiz response does not contain questions."
        )

    if len(questions) != 3:
        raise RuntimeError(
            "The quiz must contain exactly 3 questions."
        )

    validated = []

    for number, item in enumerate(
        questions,
        start=1
    ):

        if not isinstance(item, dict):
            raise RuntimeError(
                f"Question {number} is invalid."
            )

        question = item.get(
            "question"
        )

        options = item.get(
            "options"
        )

        correct_answer = item.get(
            "correct_answer"
        )

        explanation = item.get(
            "explanation",
            ""
        )

        if not isinstance(
            question,
            str
        ):
            raise RuntimeError(
                f"Question {number} has no valid question."
            )

        if (
            not isinstance(options, list)
            or len(options) != 4
        ):
            raise RuntimeError(
                f"Question {number} must contain 4 options."
            )

        if not all(
            isinstance(option, str)
            for option in options
        ):
            raise RuntimeError(
                f"Question {number} has invalid options."
            )

        if correct_answer not in options:
            raise RuntimeError(
                f"Question {number} has an invalid correct answer."
            )

        validated.append(
            {
                "question": question,
                "options": options,
                "correct_answer": correct_answer,
                "explanation": str(
                    explanation
                )
            }
        )

    return {
        "questions": validated
    }