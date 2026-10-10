from gemini_client import gemini_service


def answer_question(question: str) -> str:
    """
    Answer a student's question.
    """

    prompt = f"""
You are EduGenie, an AI educational assistant.

Answer the student's question accurately and clearly.

Rules:
- Use simple English.
- Give a direct answer first.
- Explain difficult terms.
- Use an example when useful.
- Avoid unnecessary information.
- Do not invent facts.
- If the question is unclear, state the assumption.

Student question:

{question}

Answer:
"""

    return gemini_service.generate(
        prompt=prompt,
        temperature=0.3,
        max_output_tokens=2500
    )