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

    answer = serializers.CharField()


class AnswerResultSerializer(serializers.Serializer):
    """Serializer for answer check responses."""

    is_correct = serializers.BooleanField()
    user_answer = serializers.CharField()
    correct_answer = serializers.CharField()
    feedback = serializers.CharField()
    hints_used = serializers.ListField(child=serializers.CharField(), required=False)
    time_taken = serializers.IntegerField(required=False)


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
