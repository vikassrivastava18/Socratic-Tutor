from typing import cast

from app.utils.schemas import CodeListSchema, QuizSchema, SubTopicsSchema
from app.utils.open_ai import llm


def create_topic_summary(content: str):
    prompt = f"""
    You are given a CS topic for creating a summary. Keep it short and engaging

    content: {content}
    
    sample output: Regex, short for **Regular Expression**, is a way to search, match, and manipulate text using a special pattern. It is useful when we need to find specific types of information in a large amount of text. For example, regex can find email addresses, phone numbers, dates, or words that follow a certain pattern.

    <p>Short History of Regex</p>

    - **1951–1956:** Mathematician **Stephen Kleene** developed the mathematical foundations of regular expressions and regular languages. His work was later published in 1956.\
    [Read more: Stanford CS103 Timeline](<https://web.stanford.edu/class/archive/cs/cs103/cs103.1262/timeline_of_results>)
    - **1968:** **Ken Thompson** implemented regular expressions in the **QED text editor**. He also published his famous paper, _Regular Expression Search Algorithm_.\
    [Read more: Bell Labs – History of QED](<https://www.nokia.com/bell-labs/about/dennis-m-ritchie/qed.html>)
    - **1970s:** Regex became widely used in **Unix** tools such as `ed`, `grep`, `sed`, and `awk`, making text searching and processing much easier.\
    [Read more: GNU sed – Regular Expressions](<https://www.gnu.org/software/sed/manual/html_node/Regular-Expressions.html>)
    - **Today:** Regular expressions are supported by many programming languages, including **Python, Java, JavaScript, Perl, and PHP**. They are commonly used for searching, validating, extracting, and replacing text.

    This session will help you learn Regex from scratch in Python through **dialogues, quizzes and coding** assignments.
    """

    messages = [{"role": "system", "content": prompt}]
    summary = llm.invoke(messages)
    return summary.content


def create_subtopics(summary: str):
    prompt = f"""
        Break a topics summary into subtopics (maximum 4). Return title and summary for the subtopics. The summary should be in 
        markdown syntax.

        summary {summary}
        """
    structures_llm = llm.with_structured_output(SubTopicsSchema)
    messages = [{"role": "system", "content": prompt}]

    response = structures_llm.invoke(messages)
    return cast(SubTopicsSchema, response)


def create_coding_problems(content: str) -> CodeListSchema:
    prompt = f"""
        You are a code chef. Use the content to create 5 coding problems. 
        Keep the problem level to be easy for first 3 and medium for remaining two.
        Use the content provided only.

        Content: {content}

        Sample (follow strictly!): 
        Question: Create a class called `Student` that has attributes `name` and `house`. Implement a method `get_info` that returns a string in the format 'Name: <name>, House: <house>'.

        class Student:
            def __init__(self, name, house):
                self.name = name
                self.house = house

            def get_info(self):
                raise NotImplementedError

        student = Student('John', 'Gryffindor')
        print(student.get_info())

        Answer: Name: John, House: Gryffindor
    """
    structured_llm = llm.with_structured_output(CodeListSchema)
    messages = [{"role": "system", "content": prompt}]

    response = structured_llm.invoke(messages)
    return cast(CodeListSchema, response)


def create_quizzes(content: str) -> QuizSchema:
    prompt = f"""
    You are a quiz master. Use the content of a chapter to create quizzes that help students in their study.
    For MCQ, only one option should be correct. Create at least 5 MCQ and 5 True/False quizzes.
    Return the response in the format specified.    

    Content: {content}
    """
    structured_llm = llm.with_structured_output(QuizSchema)
    messages = [{"role": "system", "content": prompt}]

    response = structured_llm.invoke(messages)
    return cast(QuizSchema, response)




