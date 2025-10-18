"""
URL configuration for the ear trainer API.
"""

from django.urls import path

from . import views

app_name = "api"

urlpatterns = [
    # API root
    path("", views.APIRootView.as_view(), name="api-root"),
    # Exercise endpoints
    path("exercises/", views.ExerciseListView.as_view(), name="exercise-list"),
    path(
        "exercises/<str:exercise_id>/",
        views.ExerciseDetailView.as_view(),
        name="exercise-detail",
    ),
    path(
        "exercises/<str:exercise_id>/generate/",
        views.ExerciseGenerateView.as_view(),
        name="exercise-generate",
    ),
    path(
        "exercises/<str:exercise_id>/check/",
        views.ExerciseCheckView.as_view(),
        name="exercise-check",
    ),
    path(
        "exercises/<str:exercise_id>/instructions/",
        views.ExerciseInstructionsView.as_view(),
        name="exercise-instructions",
    ),
    # Audio endpoints
    path("audio/<str:filename>/", views.AudioFileView.as_view(), name="audio-file"),
]
