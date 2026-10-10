import os

from gemini_client import gemini_service


def explain_topic(topic: str) -> str:
    """
    Explain a topic in simple language.
    """

    provider = os.getenv(
        "EXPLANATION_PROVIDER",
        "gemini"
    ).lower().strip()

    if provider == "local":
        return local_explanation(topic)

    prompt = f"""
You are EduGenie, a friendly teacher.

Explain the following topic to a student
who is learning it for the first time.

Topic:
{topic}

Use this structure:

1. Simple Definition
2. Easy Explanation
3. Important Points
4. Example
5. Short Recap

Requirements:
- Use simple English.
- Keep the explanation educational.
- Avoid unnecessary technical language.
- Make the explanation suitable for students.
"""

    return gemini_service.generate(
        prompt=prompt,
        temperature=0.4,
        max_output_tokens=3000
    )


def local_explanation(topic: str) -> str:
    """
    Lightweight fallback when the local provider is selected.

    This does not require downloading a large model.
    """

    return f"""
Simple Explanation: {topic}

{topic} can be understood by breaking the concept
into smaller and easier ideas.

Start with:
1. Its definition
2. Its main characteristics
3. How it works
4. A practical example
5. A short revision

For full AI-generated explanations, change:

EXPLANATION_PROVIDER=gemini

in your .env file.
"""