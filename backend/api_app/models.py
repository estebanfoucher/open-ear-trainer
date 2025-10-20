"""
Django models for curriculum structure: Chapters, Lessons, and Exercises.
"""

from django.db import models


class Chapter(models.Model):
    """
    A chapter represents a major learning module in the curriculum.
    Example: "Direction & Contour", "Intervals", "Triads & Chord Qualities"
    """

    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.IntegerField(default=0, help_text="Display order in curriculum")
    difficulty_level = models.IntegerField(
        default=1, help_text="Overall difficulty (1-10)"
    )
    is_published = models.BooleanField(
        default=False, help_text="Whether chapter is visible to users"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Chapter"
        verbose_name_plural = "Chapters"

    def __str__(self):
        return f"{self.order}. {self.title}"


class Lesson(models.Model):
    """
    A lesson is a focused learning unit within a chapter.
    Example: "Rise or Fall?", "Find Do", "Interval ID"
    """

    chapter = models.ForeignKey(
        Chapter, on_delete=models.CASCADE, related_name="lessons"
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.IntegerField(default=0, help_text="Display order within chapter")
    learning_objectives = models.TextField(
        blank=True, help_text="What the user will learn"
    )
    estimated_minutes = models.IntegerField(
        default=10, help_text="Estimated time to complete in minutes"
    )
    is_published = models.BooleanField(
        default=False, help_text="Whether lesson is visible to users"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["chapter", "order"]
        verbose_name = "Lesson"
        verbose_name_plural = "Lessons"
        unique_together = ["chapter", "order"]

    def __str__(self):
        return f"{self.chapter.title} - {self.order}. {self.title}"


class Exercise(models.Model):
    """
    An exercise links a lesson to an actual exercise implementation.
    The exercise_type corresponds to the exercise ID in the exercise registry.
    """

    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name="exercises"
    )
    exercise_type = models.CharField(
        max_length=100,
        help_text="Exercise ID from registry (e.g., 'minor_third_major_third_octave_melodic')",
    )
    title = models.CharField(
        max_length=200, help_text="Display title (can override exercise name)"
    )
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0, help_text="Display order within lesson")
    difficulty_level = models.IntegerField(
        default=1, help_text="Difficulty level (1-10)"
    )
    config = models.JSONField(
        default=dict,
        blank=True,
        help_text="Exercise-specific configuration (e.g., intervals, timing)",
    )
    is_published = models.BooleanField(
        default=False, help_text="Whether exercise is visible to users"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["lesson", "order"]
        verbose_name = "Exercise"
        verbose_name_plural = "Exercises"
        unique_together = ["lesson", "order"]

    def __str__(self):
        return f"{self.lesson.title} - {self.order}. {self.title}"
