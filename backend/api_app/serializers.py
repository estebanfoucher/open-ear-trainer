"""
Serializers for the ear trainer API.
"""

from rest_framework import serializers


class ExerciseListSerializer(serializers.Serializer):
    """Serializer for exercise list responses."""

    id = serializers.CharField()
    name = serializers.CharField()
    description = serializers.CharField()
    difficulty = serializers.IntegerField()
    category = serializers.CharField()
    tags = serializers.ListField(child=serializers.CharField())
    estimated_time = serializers.IntegerField()
    prerequisites = serializers.ListField(child=serializers.CharField())
    learning_objectives = serializers.ListField(child=serializers.CharField())
    input_type = serializers.CharField()
    answer_format = serializers.CharField()
    requires_progression = serializers.BooleanField()
    requires_single_note = serializers.BooleanField()
    audio_duration = serializers.IntegerField()
    config_options = serializers.DictField()


class ExerciseDataSerializer(serializers.Serializer):
    """Serializer for exercise data responses."""

    key = serializers.CharField()
    scale = serializers.ListField(child=serializers.CharField())
    progression_audio = serializers.CharField(allow_null=True)
    target_audio = serializers.CharField(allow_null=True)
    options = serializers.ListField()
    correct_answer = serializers.CharField()
    context = serializers.DictField()


class AnswerCheckSerializer(serializers.Serializer):
    """Serializer for answer check requests."""

    answer = serializers.CharField(allow_blank=True)


class AnswerResultSerializer(serializers.Serializer):
    """Serializer for answer check responses."""

    is_correct = serializers.BooleanField()
    user_answer = serializers.CharField()
    correct_answer = serializers.CharField()
    feedback = serializers.CharField()
    hints_used = serializers.ListField(child=serializers.CharField(), required=False)
    time_taken = serializers.IntegerField(required=False, allow_null=True)


class ExerciseGenerateSerializer(serializers.Serializer):
    """Serializer for exercise generation requests."""

    key = serializers.CharField(required=False)
    difficulty = serializers.IntegerField(required=False, min_value=1, max_value=10)
    progression_type = serializers.CharField(required=False)
    octave = serializers.IntegerField(required=False, min_value=1, max_value=8)


class ErrorSerializer(serializers.Serializer):
    """Serializer for error responses."""

    error = serializers.CharField()
    message = serializers.CharField()
    details = serializers.DictField(required=False)


# Curriculum Structure Serializers


class ExerciseSerializer(serializers.ModelSerializer):
    """Serializer for Exercise model."""

    class Meta:
        from .models import Exercise

        model = Exercise
        fields = [
            "id",
            "title",
            "description",
            "exercise_type",
            "order",
            "difficulty_level",
            "config",
            "is_published",
        ]


class LessonListSerializer(serializers.ModelSerializer):
    """Serializer for Lesson list in chapter detail."""

    exercise_count = serializers.SerializerMethodField()

    class Meta:
        from .models import Lesson

        model = Lesson
        fields = [
            "id",
            "title",
            "description",
            "order",
            "estimated_minutes",
            "exercise_count",
        ]

    def get_exercise_count(self, obj):
        """Get count of published exercises in this lesson."""
        return obj.exercises.filter(is_published=True).count()


class LessonDetailSerializer(serializers.ModelSerializer):
    """Serializer for Lesson detail with exercises."""

    exercises = ExerciseSerializer(many=True, read_only=True)
    chapter_id = serializers.IntegerField(source="chapter.id", read_only=True)
    chapter_title = serializers.CharField(source="chapter.title", read_only=True)

    class Meta:
        from .models import Lesson

        model = Lesson
        fields = [
            "id",
            "title",
            "description",
            "order",
            "learning_objectives",
            "estimated_minutes",
            "chapter_id",
            "chapter_title",
            "exercises",
        ]


class ChapterListSerializer(serializers.ModelSerializer):
    """Serializer for Chapter list."""

    lesson_count = serializers.SerializerMethodField()
    exercise_count = serializers.SerializerMethodField()

    class Meta:
        from .models import Chapter

        model = Chapter
        fields = [
            "id",
            "title",
            "description",
            "order",
            "difficulty_level",
            "lesson_count",
            "exercise_count",
        ]

    def get_lesson_count(self, obj):
        """Get count of published lessons in this chapter."""
        return obj.lessons.filter(is_published=True).count()

    def get_exercise_count(self, obj):
        """Get total count of published exercises in this chapter."""
        from .models import Exercise

        return Exercise.objects.filter(lesson__chapter=obj, is_published=True).count()


class ChapterDetailSerializer(serializers.ModelSerializer):
    """Serializer for Chapter detail with lessons."""

    lessons = LessonListSerializer(many=True, read_only=True)

    class Meta:
        from .models import Chapter

        model = Chapter
        fields = [
            "id",
            "title",
            "description",
            "order",
            "difficulty_level",
            "lessons",
        ]
