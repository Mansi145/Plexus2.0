from rest_framework import viewsets
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from registration.models import society
from .models import Event, Question, Score, Rule
from .serializers import EventSerializer, QuestionSerializer, RuleSerializer, ScoreSerializer
from rest_framework.permissions import IsAuthenticated
from utils.permissions import IsPlayer, IsSociety
from datetime import timedelta
from django.utils import timezone


class EventViewSet(viewsets.ModelViewSet):
    permission_classes = [IsSociety & IsAuthenticated]
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def perform_create(self, serializer):
        new_society = society.objects.get(user=self.request.user)
        serializer.save(society=new_society)

    def get_questions(self, obj):
        query = obj.Question.all().order_by('order')
        return QuestionSerializer(query, many=True, read_only=True).data


class QuestionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsSociety & IsAuthenticated]
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get_queryset(self):
        return Question.objects.all()


class RuleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsSociety & IsAuthenticated]
    queryset = Rule.objects.all()
    serializer_class = RuleSerializer


class ScoreViewSet(viewsets.ModelViewSet):
    permission_classes = [IsPlayer & IsAuthenticated]
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer

    def get_queryset(self):
        return Score.objects.all()


class StartEvent(APIView):
    permission_classes = [IsPlayer & IsAuthenticated]

    def get(self, request):
        event = Event.objects.all()
        serializer = EventSerializer(event, many=True)
        return Response(serializer.data)


class EventDetails(APIView):
    permission_classes = [IsPlayer & IsAuthenticated]

    def get(self, request, pk, format=None):
        event = get_object_or_404(Event, pk=pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)


class QuestionsPlay(APIView):
    permission_classes = [IsPlayer & IsAuthenticated]

    def get(self, request, *args, **kwargs):
        event_url = self.kwargs["pk"]
        player_id = self.request.user.player
        score_play, created = Score.objects.get_or_create(
            player=player_id, event=Event.objects.get(pk=event_url))
        level = score_play.level
        question = Question.objects.get(event=event_url, level=level)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        event_url = self.kwargs["pk"]
        score_play = Score.objects.get(
            player=self.request.user.player, event=event_url)
        level = score_play.level
        answer = request.data["answer"]
        question = Question.objects.get(event=event_url, level=level)
        if answer == question.answer:
            score_play.level += 1
            score_play.score += question.correct_score
            score_play.save()
            return Response({"answer": "Correct"})
        else:
            score_play.score += question.incorrect_score
            score_play.save()
            return Response({"answer": "Inorrect"})


class Leaderboard(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        event_url = self.kwargs["pk"]
        queryset = Score.objects.order_by(
            "-score",
            "level").filter(
            event=event_url)
        serializer = ScoreSerializer(queryset, many=True)
        return Response(serializer.data)


class PastEventsView(APIView):
    permission_classes = [IsPlayer & IsAuthenticated]

    def get(self, request):
        past = timezone.now() - timedelta(days=1)
        queryset = Event.objects.filter(end_time__range=["2011-01-01", past])
        serializer = EventSerializer(queryset, many=True)
        return Response(serializer.data)


class PresentEventsView(APIView):
    permission_classes = [IsPlayer & IsAuthenticated]

    def get(self, request):
        queryset = Event.objects.filter(
            start_time__range=[
                timezone.now().date(),
                timezone.now()])
        serializer = EventSerializer(queryset, many=True)
        return Response(serializer.data)


class FutureEventsView(APIView):
    permission_classes = [IsPlayer & IsAuthenticated]

    def get(self, request):
        future = timezone.now() + timedelta(days=1)
        queryset = Event.objects.filter(
            start_time__range=[future, "2050-01-01"])
        serializer = EventSerializer(queryset, many=True)
        return Response(serializer.data)
