from typing import List

from pydantic import BaseModel, Field


class QuestionRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=10000
    )


class TextRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=20000
    )


class QuizRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=10,
        max_length=20000
    )


class LearningPathRequest(BaseModel):
    topic: str = Field(
        ...,
        min_length=1,
        max_length=500
    )

    level: str = Field(
        default="Beginner",
        min_length=1,
        max_length=100
    )


class QuizQuestion(BaseModel):
    question: str
    options: List[str]
    correct_answer: str
    explanation: str


class QuizResponse(BaseModel):
    questions: List[QuizQuestion]