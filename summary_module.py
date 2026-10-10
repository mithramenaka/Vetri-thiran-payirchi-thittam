from gemini_client import gemini_service


def summarize_text(text: str) -> str:
    """
    Summarize educational text.
    """

    prompt = f"""
You are EduGenie, an educational summarization assistant.

Summarize the following educational text.

Requirements:

- Keep all important ideas.
- Remove repetition.
- Use simple English.
- Make it useful for revision.
- Use headings and bullet points where appropriate.
- Do not add facts that are not present in the original text.
- Preserve important definitions, facts, and examples.

Text:

{text}

Summary:
"""

    return gemini_service.generate(
        prompt=prompt,
        temperature=0.2,
        max_output_tokens=3000
    )