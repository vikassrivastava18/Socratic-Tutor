
from dotenv import load_dotenv
from typing import cast
from rest_framework import  status
from rest_framework.response import Response

from .open_ai import llm

load_dotenv(override=True)

		
def answers_match(submitted_answer, expected_answer):
    if isinstance(expected_answer, bool):
        return submitted_answer is expected_answer
    if not isinstance(submitted_answer, str) or not isinstance(expected_answer, str):
        return submitted_answer == expected_answer
    return submitted_answer.strip().casefold() == expected_answer.strip().casefold()


def evaulate_response(subtopic, answers):
        quizzes = subtopic.quizzes or {}
        results = {}
        score = 0
        total = 0
    
        for category in quizzes.keys():
            category_quizzes = quizzes.get(category, [])
            category_answers = answers.get(category, [])
            if not isinstance(category_answers, list):
                return Response(
                    {category: 'Answers must be an array.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            category_results = []
            for index, quiz in enumerate(category_quizzes):
                submitted_answer = (
                    category_answers[index] if index < len(category_answers) else None
                )
                expected_answer = quiz.get('answer')
                is_correct = answers_match(
                    submitted_answer,
                    expected_answer,
                )
                score += int(is_correct)
                total += 1
                category_results.append({
                    'question': quiz.get('question', quiz.get('quiz')),
                    'submitted_answer': submitted_answer,
                    'correct': is_correct,
                    'expected_answer': expected_answer,
                    'explanation': quiz.get('explanation'),
                })

            results[category] = category_results
        return results, score, total

