"""
Django admin configuration for curriculum models.
"""

from django.contrib import admin

from .models import Chapter, Exercise, Lesson


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    """Admin interface for Chapter model."""

    list_display = ["order", "title", "difficulty_level", "is_published", "created_at"]
    list_filter = ["is_published", "difficulty_level"]
    search_fields = ["title", "description"]
    ordering = ["order"]
    list_editable = ["is_published"]


class LessonInline(admin.TabularInline):
    """Inline admin for lessons within a chapter."""

    model = Lesson
    extra = 1
    fields = ["order", "title", "estimated_minutes", "is_published"]


class ExerciseInline(admin.TabularInline):
    """Inline admin for exercises within a lesson."""

    model = Exercise
    extra = 1
    fields = ["order", "title", "exercise_type", "difficulty_level", "is_published"]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """Admin interface for Lesson model."""

    list_display = [
        "chapter",
        "order",
        "title",
        "estimated_minutes",
        "is_published",
        "created_at",
    ]
    list_filter = ["is_published", "chapter"]
    search_fields = ["title", "description", "learning_objectives"]
    ordering = ["chapter", "order"]
    list_editable = ["is_published"]
    inlines = [ExerciseInline]


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    """Admin interface for Exercise model."""

    list_display = [
        "lesson",
        "order",
        "title",
        "exercise_type",
        "difficulty_level",
        "is_published",
        "created_at",
    ]
    list_filter = ["is_published", "difficulty_level", "lesson__chapter"]
    search_fields = ["title", "description", "exercise_type"]
    ordering = ["lesson", "order"]
    list_editable = ["is_published"]
