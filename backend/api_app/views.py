"""
API views for the ear trainer.
"""

import logging
import os
from pathlib import Path

from django.conf import settings

from exercises.level1.combined_intervals_melodic import (
    CombinedIntervalsMelodicExercise,
)

# Simple exercise registry - we'll import exercises directly
from exercises.level1.interval_recognition import (
    MinorThirdMajorThirdOctaveMelodicExercise,
)
from exercises.level1.perfect_intervals_harmonic import (
    PerfectFourthPerfectFifthOctaveHarmonicExercise,
)
from exercises.level1.perfect_intervals_melodic import (
    PerfectFourthPerfectFifthOctaveMelodicExercise,
)
from exercises.level1.thirds_octave_harmonic import (
    MinorThirdMajorThirdOctaveHarmonicExercise,
)


# Simple exercise registry replacement
class SimpleExerciseRegistry:
    def __init__(self):
        self.exercises = {
            # New exercises
            "minor_third_major_third_octave_melodic": MinorThirdMajorThirdOctaveMelodicExercise(),
            "perfect_fourth_fifth_octave_melodic": PerfectFourthPerfectFifthOctaveMelodicExercise(),
            "minor_third_major_third_octave_harmonic": MinorThirdMajorThirdOctaveHarmonicExercise(),
            "perfect_fourth_fifth_octave_harmonic": PerfectFourthPerfectFifthOctaveHarmonicExercise(),
            "combined_intervals_melodic": CombinedIntervalsMelodicExercise(),
        }

    def get_exercise_count(self):
        return len(self.exercises)

    def get_exercise_list(self):
        return [exercise.metadata for exercise in self.exercises.values()]

    def get_exercise_metadata(self, exercise_id):
        if exercise_id in self.exercises:
            return self.exercises[exercise_id].metadata
        return None

    def get_exercise(self, exercise_id):
        return self.exercises.get(exercise_id)


exercise_registry = SimpleExerciseRegistry()
from django.http import FileResponse
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    AnswerCheckSerializer,
    AnswerResultSerializer,
    ExerciseDataSerializer,
    ExerciseListSerializer,
)

logger = logging.getLogger(__name__)


class APIRootView(APIView):
    """API root with documentation."""

    def get(self, request):
        """Get API documentation and available endpoints."""
        return Response(
            {
                "name": "Open Ear Trainer API",
                "version": "1.0.0",
                "description": "A scalable ear training web application for musicians",
                "endpoints": {
                    "exercises": {
                        "list": "/api/exercises/",
                        "detail": "/api/exercises/{id}/",
                        "generate": "/api/exercises/{id}/generate/",
                        "check": "/api/exercises/{id}/check/",
                        "instructions": "/api/exercises/{id}/instructions/",
                    },
                    "audio": {"file": "/api/audio/{filename}/"},
                },
                "available_exercises": exercise_registry.get_exercise_count(),
                "documentation": "https://github.com/estebanfoucher/open-ear-trainer",
            }
        )


class ExerciseListView(APIView):
    """List all available exercises."""

    def get(self, request):
        """Get list of all exercises."""
        try:
            exercises = exercise_registry.get_exercise_list()
            serializer = ExerciseListSerializer(exercises, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error getting exercise list: {e}")
            return Response(
                {"error": "internal_error", "message": "Failed to get exercise list"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ExerciseDetailView(APIView):
    """Get details of a specific exercise."""

    def get(self, request, exercise_id):
        """Get exercise details by ID."""
        try:
            metadata = exercise_registry.get_exercise_metadata(exercise_id)
            if not metadata:
                return Response(
                    {
                        "error": "not_found",
                        "message": f"Exercise {exercise_id} not found",
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Convert metadata to dict for serialization
            exercise_data = {
                "id": metadata.id,
                "name": metadata.name,
                "description": metadata.description,
                "difficulty": metadata.difficulty,
                "category": metadata.category,
                "tags": metadata.tags,
                "estimated_time": metadata.estimated_time,
                "prerequisites": metadata.prerequisites,
                "learning_objectives": metadata.learning_objectives,
                "input_type": metadata.input_type,
                "answer_format": metadata.answer_format,
                "requires_progression": metadata.requires_progression,
                "requires_single_note": metadata.requires_single_note,
                "audio_duration": metadata.audio_duration,
                "config_options": metadata.config_options,
            }

            serializer = ExerciseListSerializer(exercise_data)
            return Response(serializer.data)

        except Exception as e:
            logger.error(f"Error getting exercise details for {exercise_id}: {e}")
            return Response(
                {
                    "error": "internal_error",
                    "message": "Failed to get exercise details",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ExerciseGenerateView(APIView):
    """Generate a new exercise instance."""

    parser_classes = [JSONParser]

    def get(self, request, exercise_id):
        """Generate a new exercise instance."""
        try:
            # Get the exercise class
            exercise_class = exercise_registry.get_exercise(exercise_id)
            if not exercise_class:
                return Response(
                    {
                        "error": "not_found",
                        "message": f"Exercise {exercise_id} not found",
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Parse query parameters for configuration
            config = {}
            # Handle both DRF Request and Django WSGIRequest
            if hasattr(request, "query_params"):
                query_params = request.query_params
            else:
                query_params = request.GET

            for key, value in query_params.items():
                config[key] = value

            # Get exercise instance and generate data
            exercise = exercise_class
            exercise_data = exercise.generate(**config)

            # Convert to dict for serialization
            data_dict = {
                "key": exercise_data.key,
                "scale": exercise_data.scale,
                "progression_audio": exercise_data.progression_audio,
                "target_audio": exercise_data.target_audio,
                "options": exercise_data.options,
                "correct_answer": exercise_data.correct_answer,
                "context": exercise_data.context,
            }

            serializer = ExerciseDataSerializer(data=data_dict)
            if serializer.is_valid():
                return Response(serializer.data)
            else:
                return Response(
                    {
                        "error": "validation_error",
                        "message": "Invalid exercise data",
                        "details": serializer.errors,
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        except Exception as e:
            logger.error(f"Error generating exercise {exercise_id}: {e}")
            return Response(
                {"error": "internal_error", "message": "Failed to generate exercise"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ExerciseCheckView(APIView):
    """Check an answer for an exercise."""

    parser_classes = [JSONParser]

    def post(self, request, exercise_id):
        """Check if the user's answer is correct."""
        try:
            # Get the exercise class
            exercise_class = exercise_registry.get_exercise(exercise_id)
            if not exercise_class:
                return Response(
                    {
                        "error": "not_found",
                        "message": f"Exercise {exercise_id} not found",
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Validate request data
            serializer = AnswerCheckSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {
                        "error": "validation_error",
                        "message": "Invalid request data",
                        "details": serializer.errors,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Get exercise context from session or request
            # For now, we'll need to pass context somehow
            # This is a simplified version - in a real app, you'd store context in session/DB
            context = request.data.get("context", {})

            # Add correct_answer to context if not present
            if "correct_answer" not in context:
                # Generate a temporary exercise to get the correct answer
                # Use the same parameters from the context if available
                temp_exercise = exercise_class
                temp_config = {}
                if "interval" in context:
                    temp_config["interval"] = context["interval"]
                if "reference_note" in context:
                    temp_config["reference_note"] = context["reference_note"]
                temp_data = temp_exercise.generate(**temp_config)
                context["correct_answer"] = temp_data.correct_answer

            # Create exercise instance and check answer
            exercise = exercise_class
            result = exercise.check_answer(serializer.validated_data["answer"], context)

            # Convert result to dict for serialization
            result_dict = {
                "is_correct": result.is_correct,
                "user_answer": result.user_answer,
                "correct_answer": result.correct_answer,
                "feedback": result.feedback,
                "hints_used": result.hints_used,
                "time_taken": result.time_taken,
            }

            result_serializer = AnswerResultSerializer(data=result_dict)
            if result_serializer.is_valid():
                return Response(result_serializer.data)
            else:
                return Response(
                    {
                        "error": "validation_error",
                        "message": "Invalid result data",
                        "details": result_serializer.errors,
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        except Exception as e:
            logger.error(f"Error checking answer for exercise {exercise_id}: {e}")
            return Response(
                {"error": "internal_error", "message": "Failed to check answer"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class AudioFileView(APIView):
    """Serve generated audio files."""

    def get(self, request, filename):
        """Serve an audio file."""
        try:
            # Construct file path (supports cached files)
            primary_path = os.path.join(settings.MEDIA_ROOT, "audio", filename)
            cache_path = os.path.join(settings.MEDIA_ROOT, "audio", "cache", filename)
            file_path = primary_path if os.path.exists(primary_path) else cache_path

            # Check if file exists in either location
            if not os.path.exists(file_path):
                return Response(
                    {
                        "error": "not_found",
                        "message": f"Audio file {filename} not found",
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Determine content type based on file extension
            if filename.endswith(".wav"):
                content_type = "audio/wav"
            elif filename.endswith(".mp3"):
                content_type = "audio/mpeg"
            else:
                content_type = "audio/wav"  # Default

            # Serve the file
            file_handle = open(file_path, "rb")  # noqa: SIM115
            response = FileResponse(
                file_handle, content_type=content_type, filename=filename
            )
            response["Content-Length"] = Path(file_path).stat().st_size
            return response

        except Exception as e:
            logger.error(f"Error serving audio file {filename}: {e}")
            return Response(
                {"error": "internal_error", "message": "Failed to serve audio file"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ExerciseInstructionsView(APIView):
    """Get exercise instructions."""

    def get(self, request, exercise_id):
        """Get instructions for an exercise."""
        try:
            exercise_class = exercise_registry.get_exercise(exercise_id)
            if not exercise_class:
                return Response(
                    {
                        "error": "not_found",
                        "message": f"Exercise {exercise_id} not found",
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )

            exercise = exercise_class
            instructions = exercise.get_instructions()
            hints = exercise.get_hints()

            return Response({"instructions": instructions, "hints": hints})

        except Exception as e:
            logger.error(f"Error getting instructions for exercise {exercise_id}: {e}")
            return Response(
                {"error": "internal_error", "message": "Failed to get instructions"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
