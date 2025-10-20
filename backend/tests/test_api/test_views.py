"""
Tests for API views.
"""

import os
from unittest.mock import MagicMock, patch

from api_app.views import (
    exercise_registry,
)
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TestAPIRootView(APITestCase):
    """Test APIRootView."""

    def test_api_root_get(self):
        """Test GET request to API root."""
        url = reverse("api:api-root")
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        data = response.data

        assert "name" in data
        assert "version" in data
        assert "description" in data
        assert "endpoints" in data
        assert "available_exercises" in data
        assert "documentation" in data

        assert data["name"] == "Open Ear Trainer API"
        assert data["version"] == "1.0.0"
        assert data["available_exercises"] == exercise_registry.get_exercise_count()


class TestExerciseListView(APITestCase):
    """Test ExerciseListView."""

    def test_exercise_list_get(self):
        """Test GET request to exercise list."""
        url = reverse("api:exercise-list")
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        data = response.data

        assert isinstance(data, list)
        assert len(data) > 0

        # Check structure of first exercise
        if data:
            exercise = data[0]
            assert "id" in exercise
            assert "name" in exercise
            assert "description" in exercise
            assert "difficulty" in exercise
            assert "category" in exercise

    def test_exercise_list_get_with_mock_registry(self):
        """Test exercise list with mocked registry."""
        with patch("api_app.views.exercise_registry") as mock_registry:
            mock_exercises = [
                {
                    "id": "test_exercise_1",
                    "name": "Test Exercise 1",
                    "description": "A test exercise",
                    "difficulty": 3,
                    "category": "interval_recognition",
                    "tags": ["intervals"],
                    "estimated_time": 30,
                    "prerequisites": [],
                    "learning_objectives": ["Learn intervals"],
                    "input_type": "multiple_choice",
                    "answer_format": "interval_name",
                    "requires_progression": False,
                    "requires_single_note": True,
                    "audio_duration": 2,
                    "config_options": {"key": "C", "octave": 4},
                }
            ]
            mock_registry.get_exercise_list.return_value = mock_exercises

            url = reverse("api:exercise-list")
            response = self.client.get(url)

            assert response.status_code == status.HTTP_200_OK
            assert response.data == mock_exercises

    def test_exercise_list_get_with_registry_error(self):
        """Test exercise list when registry raises an error."""
        with patch("api_app.views.exercise_registry") as mock_registry:
            mock_registry.get_exercise_list.side_effect = Exception("Registry error")

            url = reverse("api:exercise-list")
            response = self.client.get(url)

            assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
            data = response.data
            assert "error" in data
            assert "message" in data
            assert data["error"] == "internal_error"


class TestExerciseDetailView(APITestCase):
    """Test ExerciseDetailView."""

    def test_exercise_detail_get_existing(self):
        """Test GET request for existing exercise."""
        # Get a valid exercise ID from the registry
        exercises = exercise_registry.get_exercise_list()
        if exercises:
            exercise_id = exercises[0].id

            url = reverse("api:exercise-detail", kwargs={"exercise_id": exercise_id})
            response = self.client.get(url)

            assert response.status_code == status.HTTP_200_OK
            data = response.data

            assert "id" in data
            assert "name" in data
            assert "description" in data
            assert "difficulty" in data
            assert "category" in data
            assert data["id"] == exercise_id

    def test_exercise_detail_get_nonexistent(self):
        """Test GET request for nonexistent exercise."""
        url = reverse(
            "api:exercise-detail", kwargs={"exercise_id": "nonexistent_exercise"}
        )
        response = self.client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.data
        assert "error" in data
        assert "message" in data
        assert data["error"] == "not_found"

    def test_exercise_detail_get_with_mock_registry(self):
        """Test exercise detail with mocked registry."""
        with patch("api_app.views.exercise_registry") as mock_registry:
            mock_metadata = MagicMock()
            mock_metadata.id = "test_exercise"
            mock_metadata.name = "Test Exercise"
            mock_metadata.description = "A test exercise"
            mock_metadata.difficulty = 3
            mock_metadata.category = "interval_recognition"
            mock_metadata.tags = ["intervals"]
            mock_metadata.estimated_time = 30
            mock_metadata.prerequisites = []
            mock_metadata.learning_objectives = ["Learn intervals"]
            mock_metadata.input_type = "multiple_choice"
            mock_metadata.answer_format = "interval_name"
            mock_metadata.requires_progression = False
            mock_metadata.requires_single_note = True
            mock_metadata.audio_duration = 2
            mock_metadata.config_options = {}

            mock_registry.get_exercise_metadata.return_value = mock_metadata

            url = reverse(
                "api:exercise-detail", kwargs={"exercise_id": "test_exercise"}
            )
            response = self.client.get(url)

            assert response.status_code == status.HTTP_200_OK
            data = response.data
            assert data["id"] == "test_exercise"
            assert data["name"] == "Test Exercise"

    def test_exercise_detail_get_with_registry_error(self):
        """Test exercise detail when registry raises an error."""
        with patch("api_app.views.exercise_registry") as mock_registry:
            mock_registry.get_exercise_metadata.side_effect = Exception(
                "Registry error"
            )

            url = reverse(
                "api:exercise-detail", kwargs={"exercise_id": "test_exercise"}
            )
            response = self.client.get(url)

            assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
            data = response.data
            assert "error" in data
            assert data["error"] == "internal_error"


class TestExerciseGenerateView(APITestCase):
    """Test ExerciseGenerateView."""

    def test_exercise_generate_get_existing(self):
        """Test GET request for existing exercise generation."""
        # Get a valid exercise ID from the registry
        exercises = exercise_registry.get_exercise_list()
        if exercises:
            exercise_id = exercises[0].id

            url = reverse("api:exercise-generate", kwargs={"exercise_id": exercise_id})
            response = self.client.get(url)

            assert response.status_code == status.HTTP_200_OK
            data = response.data

            assert "key" in data
            assert "scale" in data
            assert "options" in data
            assert "correct_answer" in data
            assert "context" in data

    def test_exercise_generate_get_with_config(self):
        """Test GET request with configuration parameters."""
        exercises = exercise_registry.get_exercise_list()
        if exercises:
            exercise_id = exercises[0].id

            url = reverse("api:exercise-generate", kwargs={"exercise_id": exercise_id})
            response = self.client.get(url, {"key": "C", "octave": 4})

            assert response.status_code == status.HTTP_200_OK
            data = response.data
            # Exercise key should be descriptive and non-empty
            assert data["key"] is not None
            assert len(data["key"]) > 0

    def test_exercise_generate_get_nonexistent(self):
        """Test GET request for nonexistent exercise generation."""
        url = reverse(
            "api:exercise-generate", kwargs={"exercise_id": "nonexistent_exercise"}
        )
        response = self.client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.data
        assert "error" in data
        assert data["error"] == "not_found"

    def test_exercise_generate_get_with_mock_exercise(self):
        """Test exercise generation with mocked exercise."""
        with patch("api_app.views.exercise_registry") as mock_registry:
            mock_exercise = MagicMock()
            mock_exercise_data = MagicMock()
            mock_exercise_data.key = "C major"
            mock_exercise_data.scale = ["C", "D", "E", "F", "G", "A", "B"]
            mock_exercise_data.progression_audio = None
            mock_exercise_data.target_audio = "/api/audio/test.wav"
            mock_exercise_data.options = ["minor_third", "major_third", "octave"]
            mock_exercise_data.correct_answer = "major_third"
            mock_exercise_data.context = {"root_note": "C-4"}

            mock_exercise.generate.return_value = mock_exercise_data
            mock_registry.get_exercise.return_value = mock_exercise

            url = reverse(
                "api:exercise-generate", kwargs={"exercise_id": "test_exercise"}
            )
            response = self.client.get(url)

            assert response.status_code == status.HTTP_200_OK
            data = response.data
            assert data["key"] == "C major"
            assert data["correct_answer"] == "major_third"

    def test_exercise_generate_get_with_exercise_error(self):
        """Test exercise generation when exercise raises an error."""
        with patch("api_app.views.exercise_registry") as mock_registry:
            mock_exercise = MagicMock()
            mock_exercise.generate.side_effect = Exception("Exercise error")
            mock_registry.get_exercise.return_value = mock_exercise

            url = reverse(
                "api:exercise-generate", kwargs={"exercise_id": "test_exercise"}
            )
            response = self.client.get(url)

            assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
            data = response.data
            assert "error" in data
            assert data["error"] == "internal_error"


class TestExerciseCheckView(APITestCase):
    """Test ExerciseCheckView."""

    def test_exercise_check_post_valid(self):
        """Test POST request with valid answer data."""
        exercises = exercise_registry.get_exercise_list()
        if exercises:
            exercise_id = exercises[0].id

            url = reverse("api:exercise-check", kwargs={"exercise_id": exercise_id})
            data = {
                "answer": "Higher",
                "context": {
                    "correct_answer": "Higher",
                    "first_note": "C-4",
                    "second_note": "E-5",
                    "direction": "higher",
                },
            }
            response = self.client.post(url, data, format="json")

            if response.status_code != status.HTTP_200_OK:
                print(f"Response status: {response.status_code}")
                print(f"Response data: {response.data}")

            assert response.status_code == status.HTTP_200_OK
            response_data = response.data

            assert "is_correct" in response_data
            assert "user_answer" in response_data
            assert "correct_answer" in response_data
            assert "feedback" in response_data

    def test_exercise_check_post_invalid_data(self):
        """Test POST request with invalid data."""
        exercises = exercise_registry.get_exercise_list()
        if exercises:
            exercise_id = exercises[0].id

            url = reverse("api:exercise-check", kwargs={"exercise_id": exercise_id})
            data = {}  # Missing required answer field
            response = self.client.post(url, data, format="json")

            assert response.status_code == status.HTTP_400_BAD_REQUEST
            response_data = response.data
            assert "error" in response_data
            assert response_data["error"] == "validation_error"

    def test_exercise_check_post_nonexistent_exercise(self):
        """Test POST request for nonexistent exercise."""
        url = reverse(
            "api:exercise-check", kwargs={"exercise_id": "nonexistent_exercise"}
        )
        data = {"answer": "major_third"}
        response = self.client.post(url, data, format="json")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.data
        assert "error" in data
        assert data["error"] == "not_found"

    def test_exercise_check_post_with_mock_exercise(self):
        """Test answer checking with mocked exercise."""
        with patch("api_app.views.exercise_registry") as mock_registry:
            mock_exercise = MagicMock()
            mock_result = MagicMock()
            mock_result.is_correct = True
            mock_result.user_answer = "major_third"
            mock_result.correct_answer = "major_third"
            mock_result.feedback = "Correct!"
            mock_result.hints_used = []
            mock_result.time_taken = 5

            mock_exercise.check_answer.return_value = mock_result
            mock_registry.get_exercise.return_value = mock_exercise

            url = reverse("api:exercise-check", kwargs={"exercise_id": "test_exercise"})
            data = {"answer": "major_third"}
            response = self.client.post(url, data, format="json")

            assert response.status_code == status.HTTP_200_OK
            response_data = response.data
            assert response_data["is_correct"] is True
            assert response_data["user_answer"] == "major_third"

    def test_exercise_check_post_with_exercise_error(self):
        """Test answer checking when exercise raises an error."""
        with patch("api_app.views.exercise_registry") as mock_registry:
            mock_exercise = MagicMock()
            mock_exercise.check_answer.side_effect = Exception("Check error")
            mock_registry.get_exercise.return_value = mock_exercise

            url = reverse("api:exercise-check", kwargs={"exercise_id": "test_exercise"})
            data = {"answer": "major_third"}
            response = self.client.post(url, data, format="json")

            assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
            data = response.data
            assert "error" in data
            assert data["error"] == "internal_error"


class TestAudioFileView(APITestCase):
    """Test AudioFileView."""

    def test_audio_file_get_existing(self):
        """Test GET request for existing audio file."""
        # Create a test audio file

        from django.conf import settings

        # Create temporary audio file
        audio_dir = os.path.join(settings.MEDIA_ROOT, "audio")
        os.makedirs(audio_dir, exist_ok=True)

        test_audio_path = os.path.join(audio_dir, "test.wav")
        with open(test_audio_path, "w") as f:
            f.write("fake audio content")

        filename = "test.wav"
        url = reverse("api:audio-file", kwargs={"filename": filename})
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response["Content-Type"] in ["audio/wav", "audio/mpeg"]

    def test_audio_file_get_nonexistent(self):
        """Test GET request for nonexistent audio file."""
        url = reverse("api:audio-file", kwargs={"filename": "nonexistent.wav"})
        response = self.client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.data
        assert "error" in data
        assert data["error"] == "not_found"

    def test_audio_file_get_with_different_extensions(self):
        """Test GET request with different audio file extensions."""
        # Create a test audio file
        from django.conf import settings

        audio_dir = os.path.join(settings.MEDIA_ROOT, "audio")
        os.makedirs(audio_dir, exist_ok=True)

        test_audio_path = os.path.join(audio_dir, "test.wav")
        with open(test_audio_path, "w") as f:
            f.write("fake audio content")

        filename = "test.wav"
        url = reverse("api:audio-file", kwargs={"filename": filename})
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response["Content-Type"] == "audio/wav"

    def test_audio_file_get_with_mock_file(self):
        """Test audio file serving with mocked file."""
        # Create a test audio file
        from django.conf import settings

        audio_dir = os.path.join(settings.MEDIA_ROOT, "audio")
        os.makedirs(audio_dir, exist_ok=True)

        test_audio_path = os.path.join(audio_dir, "test.wav")
        with open(test_audio_path, "w") as f:
            f.write("fake audio content")

        filename = "test.wav"
        url = reverse("api:audio-file", kwargs={"filename": filename})
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response["Content-Type"] == "audio/wav"

    def test_audio_file_get_with_error(self):
        """Test audio file serving when an error occurs."""
        with patch("api_app.views.os.path.exists") as mock_exists:
            mock_exists.side_effect = Exception("File system error")

            url = reverse("api:audio-file", kwargs={"filename": "test.wav"})
            response = self.client.get(url)

            assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
            data = response.data
            assert "error" in data
            assert data["error"] == "internal_error"


class TestExerciseInstructionsView(APITestCase):
    """Test ExerciseInstructionsView."""

    def test_exercise_instructions_get_existing(self):
        """Test GET request for existing exercise instructions."""
        exercises = exercise_registry.get_exercise_list()
        if exercises:
            exercise_id = exercises[0].id

            url = reverse(
                "api:exercise-instructions", kwargs={"exercise_id": exercise_id}
            )
            response = self.client.get(url)

            assert response.status_code == status.HTTP_200_OK
            data = response.data

            assert "instructions" in data
            assert "hints" in data
            assert isinstance(data["instructions"], str)
            assert isinstance(data["hints"], list)

    def test_exercise_instructions_get_nonexistent(self):
        """Test GET request for nonexistent exercise instructions."""
        url = reverse(
            "api:exercise-instructions", kwargs={"exercise_id": "nonexistent_exercise"}
        )
        response = self.client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.data
        assert "error" in data
        assert data["error"] == "not_found"

    def test_exercise_instructions_get_with_mock_exercise(self):
        """Test instructions with mocked exercise."""
        with patch("api_app.views.exercise_registry") as mock_registry:
            mock_exercise = MagicMock()
            mock_exercise.get_instructions.return_value = "Test instructions"
            mock_exercise.get_hints.return_value = ["Hint 1", "Hint 2"]
            mock_registry.get_exercise.return_value = mock_exercise

            url = reverse(
                "api:exercise-instructions", kwargs={"exercise_id": "test_exercise"}
            )
            response = self.client.get(url)

            assert response.status_code == status.HTTP_200_OK
            data = response.data
            assert data["instructions"] == "Test instructions"
            assert data["hints"] == ["Hint 1", "Hint 2"]

    def test_exercise_instructions_get_with_exercise_error(self):
        """Test instructions when exercise raises an error."""
        with patch("api_app.views.exercise_registry") as mock_registry:
            mock_exercise = MagicMock()
            mock_exercise.get_instructions.side_effect = Exception("Instructions error")
            mock_registry.get_exercise.return_value = mock_exercise

            url = reverse(
                "api:exercise-instructions", kwargs={"exercise_id": "test_exercise"}
            )
            response = self.client.get(url)

            assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
            data = response.data
            assert "error" in data
            assert data["error"] == "internal_error"


class TestAPIViewIntegration(APITestCase):
    """Test API view integration and edge cases."""

    def test_all_endpoints_accessible(self):
        """Test that all API endpoints are accessible."""
        # Test API root
        url = reverse("api:api-root")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

        # Test exercise list
        url = reverse("api:exercise-list")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

        # Test exercise detail (with valid exercise)
        exercises = exercise_registry.get_exercise_list()
        if exercises:
            exercise_id = exercises[0].id
            url = reverse("api:exercise-detail", kwargs={"exercise_id": exercise_id})
            response = self.client.get(url)
            assert response.status_code == status.HTTP_200_OK

    def test_api_error_handling_consistency(self):
        """Test that API error handling is consistent across endpoints."""
        # Test 404 errors
        url = reverse("api:exercise-detail", kwargs={"exercise_id": "nonexistent"})
        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.data
        assert "error" in data
        assert "message" in data
        assert data["error"] == "not_found"

    def test_api_response_format_consistency(self):
        """Test that API responses have consistent format."""
        # Test successful response format
        url = reverse("api:exercise-list")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

        # Should return a list
        assert isinstance(response.data, list)

        # Each exercise should have required fields
        if response.data:
            exercise = response.data[0]
            required_fields = ["id", "name", "description", "difficulty", "category"]
            for field in required_fields:
                assert field in exercise
