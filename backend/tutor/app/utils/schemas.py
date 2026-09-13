from pydantic import BaseModel


class MCQ(BaseModel):
    question: str
    options: list[str]
    answer: str
    explanation: str
    hint: str

class TrueFalse(BaseModel):
    question: str
    answer: bool
    explanation: str
    hint: str

class FillBlank(BaseModel):
    quiz: str
    answer: str
    hint: str

class QuizSchema(BaseModel):
    mcq: list[MCQ]
    true_false: list[TrueFalse]

class CodeSchema(BaseModel):
    problem: str
    code: str
    answer: str
    hint: str

class CodeListSchema(BaseModel):
    codes: list[CodeSchema]


class SubTopicSchema(BaseModel):
    title: str
    summary: str

class SubTopicsSchema(BaseModel):
    subtopics: list[SubTopicSchema]