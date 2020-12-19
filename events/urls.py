from rest_framework import routers as rest_routers
from django.conf.urls import url, include
from django.urls import path
from rest_framework_nested import routers as nested_routers
from .api import (
    EventViewSet, QuestionViewSet, RuleViewSet, StartEvent,
    EventDetails, QuestionsPlay, Leaderboard, PastEventsView,
    PresentEventsView, FutureEventsView, SocietyDasboard
    )


router = rest_routers.SimpleRouter()

router.register(
    r'events',
    EventViewSet)

event_router = nested_routers.NestedSimpleRouter(
    router,
    r'events',
    lookup='event')

event_router.register(
    r'questions',
    QuestionViewSet,
    basename='event-questions')
event_router.register(
    r'rules',
    RuleViewSet,
    basename='event-rules')

urlpatterns = [
    url(
        r'^',
        include(router.urls)),
    url(
        r'^',
        include(event_router.urls)),
    path(
        'society-dashboard/',
        SocietyDasboard.as_view(),
        name="societyDashbaord"),
    path(
        'past-events/',
        PastEventsView.as_view(),
        name="pastEvents"),
    path(
        'present-events/',
        PresentEventsView.as_view(),
        name="presentEvents"),
    path(
        'future-events/',
        FutureEventsView.as_view(),
        name="futureEvents"),
    path(
        'leaderboard/<int:pk>',
        Leaderboard.as_view(),
        name="leaderboard"),
    path(
        'player-dashboard/',
        StartEvent.as_view(),
        name="eventList"),
    path(
        'player-dashboard/<int:pk>',
        EventDetails.as_view(),
        name="eventDetails"),
    path(
        'player-dashboard/<int:pk>/play',
        QuestionsPlay.as_view(),
        name="questions"),
]
