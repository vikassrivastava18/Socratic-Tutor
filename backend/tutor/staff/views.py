from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response

from app.models import SubTopic, Topic
from .utils import (
    create_coding_problems,
    create_quizzes,
    create_subtopics,
    create_topic_summary,
)
# Create your views here.


class CodingProblemCreateView(APIView):
    # permission_classes = (IsAdminUser,)

    def post(self, request, subtopic_id):
        subtopic = get_object_or_404(SubTopic, pk=subtopic_id)
        codes = create_coding_problems(subtopic.summary).model_dump()
        SubTopic.objects.filter(pk=subtopic.pk).update(codes=codes)
        return Response(codes)


class QuizCreateView(APIView):
    # permission_classes = (IsAdminUser,)

    def post(self, request, subtopic_id):
        subtopic = get_object_or_404(SubTopic, pk=subtopic_id)
        quizzes = create_quizzes(subtopic.summary)
        return Response(quizzes.model_dump())


class CreateSubTopicView(APIView):
    # permission_classes = (IsAdminUser,)

    def post(self, request, topic_id):
        topic = get_object_or_404(Topic, pk=topic_id)

        summary = create_topic_summary(topic.content)
        topic.summary = summary
        topic.save(update_fields=["summary"])

        generated_subtopics = create_subtopics(summary).model_dump()
        subtopics = generated_subtopics.get("subtopics", [])

        for item in subtopics:
            content = item["summary"]
            title = item["title"]
            item["codes"] = create_coding_problems(content).model_dump()
            item["quizzes"] = create_quizzes(content).model_dump()

            SubTopic.objects.create(
                topic=topic,
                title=title,
                summary=content,
                codes=item["codes"],
                quizzes=item["quizzes"],
            )

        return Response({
            "summary": summary,
            "subtopics": subtopics,
        })
