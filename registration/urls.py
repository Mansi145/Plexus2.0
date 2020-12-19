from django.urls import path
from registration import views

app_name = "registration"


urlpatterns = [
    path(
        'player-register/',
        views.player_registration_view.as_view(),
        name="playerRegister"),
    path(
        'society-register/',
        views.society_registration_view.as_view(),
        name="societyRegister"),
    path(
        'login/',
        views.user_login.as_view(),
        name="loginView"),
]
