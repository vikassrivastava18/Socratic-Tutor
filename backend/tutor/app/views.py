from uuid import uuid4

from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import SubTopic, Topic
from .serializers import (
	SubTopicSerializer,
	TopicDetailSerializer,
	TopicSerializer,
)
from .utils.chat import TutorGraph
from .utils.quiz import evaulate_response
from .utils.open_ai import llm


def _call_llm(prompt):
	return llm.invoke(prompt)


class TopicListView(generics.ListAPIView):
	queryset = Topic.objects.all()
	serializer_class = TopicSerializer


class TopicDetailView(generics.RetrieveAPIView):
	queryset = Topic.objects.all()
	serializer_class = TopicDetailSerializer

	def retrieve(self, request, *args, **kwargs):
		instance = self.get_object()
		data = self.get_serializer(instance).data
		first_subtopic = (
			SubTopic.objects
			.filter(topic=instance)
			.order_by('pk')
			.first()
		)
		data['first_subtopic_id'] = first_subtopic.pk if first_subtopic else None
		return Response(data)


class SubTopicDetailView(generics.RetrieveAPIView):
	queryset = SubTopic.objects.all()
	serializer_class = SubTopicSerializer


class ChatQueryView(APIView):
	def post(self, request, subtopic_id):
		query = request.data.get('query')
		if not isinstance(query, str) or not query.strip():
			return Response(
				{'query': 'This field is required.'},
				status=status.HTTP_400_BAD_REQUEST,
			)

		subtopic = get_object_or_404(SubTopic, pk=subtopic_id)
		thread_id = request.data.get('thread_id') or str(uuid4())
		topic_graph = TutorGraph(subtopic.title)
		result = topic_graph.invoke(
			query=query,
			context=subtopic.summary,
			thread_id=thread_id,
		)

		return Response({
			'answer': result['answer'],
			'thread_id': thread_id,
		})


class CodingProblemListView(APIView):

	def get(self, request, subtopic_id):
		subtopic = get_object_or_404(SubTopic, pk=subtopic_id)
		next_subtopic = (
			SubTopic.objects
			.filter(topic=subtopic.topic, pk__gt=subtopic.pk)
			.order_by('pk')
			.first()
		)
		return Response({
			'codes': subtopic.codes or {},
			'next_id': next_subtopic.pk if next_subtopic else None,
		})


class QuizListView(APIView):
	def get(self, request, subtopic_id):
		subtopic = get_object_or_404(SubTopic, pk=subtopic_id)
		return Response(subtopic.quizzes or {})
	

class QuizEvaluationView(APIView):
    def post(self, request, subtopic_id):
        subtopic = get_object_or_404(SubTopic, pk=subtopic_id)
        answers = request.data.get('answers')

        if not isinstance(answers, dict):
            return Response(
                {'answers': 'This field must be an object.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        results, score, total = evaulate_response(subtopic, answers)
        percentage = round(score / total * 100, 2) if total else 0
        response = {
            'score': score,
            'total': total,
            'percentage': percentage,
            'results': results,
        }

        if percentage < 70:			
            response["proceed"] = False
        else:
            response["proceed"] = True

        return Response(response)