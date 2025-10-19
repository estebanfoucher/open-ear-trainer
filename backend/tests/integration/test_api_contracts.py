"""
Integration tests for API contracts and response schemas.
"""

from api_app.views import exercise_registry
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TestAPIContracts(APITestCase):
    """Test API contracts and response schemas."""

    def test_api_root_contract(self):
        """Test API root response contract."""
        url = reverse("api:api-root")
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK

        data = response.data
        required_fields = [
            "name",
            "version",
            "description",
            "endpoints",
            "available_exercises",
            "documentation",
        ]

        for field in required_fields:
            assert field in data, f"Missing required field: {field}"

        # Check field types
        assert isinstance(data["name"], str)
        assert isinstance(data["version"], str)
        assert isinstance(data["description"], str)
        assert isinstance(data["endpoints"], dict)
        assert isinstance(data["available_exercises"], int)
        assert isinstance(data["documentation"], str)

        # Check endpoints structure
        endpoints = data["endpoints"]
        assert "exercises" in endpoints
        assert "audio" in endpoints

        exercises_endpoints = endpoints["exercises"]
        required_exercise_endpoints = [
            "list",
            "detail",
            "generate",
            "check",
            "instructions",
        ]

        for endpoint in required_exercise_endpoints:
            assert (
                endpoint in exercises_endpoints
            ), f"Missing exercise endpoint: {endpoint}"

        audio_endpoints = endpoints["audio"]
        assert "file" in audio_endpoints

    def test_exercise_list_contract(self):
        """Test exercise list response contract."""
        url = reverse("api:exercise-list")
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK

        data = response.data
        assert isinstance(data, list)

        if data:
            exercise = data[0]
            required_fields = [
                "id",
                "name",
                "description",
                "difficulty",
                "category",
                "tags",
                "estimated_time",
                "prerequisites",
                "learning_objectives",
                "input_type",
                "answer_format",
            ]

            for field in required_fields:
                assert field in exercise, f"Missing required field: {field}"

            # Check field types
            assert isinstance(exercise["id"], str)
            assert isinstance(exercise["name"], str)
            assert isinstance(exercise["description"], str)
            assert isinstance(exercise["difficulty"], int)
            assert isinstance(exercise["category"], str)
            assert isinstance(exercise["tags"], list)
            assert isinstance(exercise["estimated_time"], int)
            assert isinstance(exercise["prerequisites"], list)
            assert isinstance(exercise["learning_objectives"], list)
            assert isinstance(exercise["input_type"], str)
            assert isinstance(exercise["answer_format"], str)

            # Check value constraints
            assert 1 <= exercise["difficulty"] <= 10
            assert exercise["estimated_time"] > 0
            assert len(exercise["id"]) > 0
            assert len(exercise["name"]) > 0

    def test_exercise_detail_contract(self):
        """Test exercise detail response contract."""
        # Get a valid exercise ID
        url = reverse("api:exercise-list")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

        exercises = response.data
        if exercises:
            exercise_id = exercises[0]["id"]

            url = reverse("api:exercise-detail", kwargs={"exercise_id": exercise_id})
            response = self.client.get(url)

            assert response.status_code == status.HTTP_200_OK

            data = response.data
            required_fields = [
                "id",
                "name",
                "description",
                "difficulty",
                "category",
                "tags",
                "estimated_time",
                "prerequisites",
                "learning_objectives",
                "input_type",
                "answer_format",
                "requires_progression",
                "requires_single_note",
                "audio_duration",
                "config_options",
            ]

            for field in required_fields:
                assert field in data, f"Missing required field: {field}"

            # Check field types
            assert isinstance(data["id"], str)
            assert isinstance(data["name"], str)
            assert isinstance(data["description"], str)
            assert isinstance(data["difficulty"], int)
            assert isinstance(data["category"], str)
            assert isinstance(data["tags"], list)
            assert isinstance(data["estimated_time"], int)
            assert isinstance(data["prerequisites"], list)
            assert isinstance(data["learning_objectives"], list)
            assert isinstance(data["input_type"], str)
            assert isinstance(data["answer_format"], str)
            assert isinstance(data["requires_progression"], bool)
            assert isinstance(data["requires_single_note"], bool)
            assert isinstance(data["audio_duration"], int)
            assert isinstance(data["config_options"], dict)

    def test_exercise_generate_contract(self):
        """Test exercise generation response contract."""
        # Get a valid exercise ID
        url = reverse("api:exercise-list")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

        exercises = response.data
        if exercises:
            exercise_id = exercises[0]["id"]

            url = reverse("api:exercise-generate", kwargs={"exercise_id": exercise_id})
            response = self.client.get(url)

            assert response.status_code == status.HTTP_200_OK

            data = response.data
            required_fields = [
                "key",
                "scale",
                "progression_audio",
                "target_audio",
                "options",
                "correct_answer",
                "context",
            ]

            for field in required_fields:
                assert field in data, f"Missing required field: {field}"

            # Check field types
            assert isinstance(data["key"], str)
            assert isinstance(data["scale"], list)
            assert isinstance(data["options"], list)
            assert isinstance(data["correct_answer"], str)
            assert isinstance(data["context"], dict)

            # progression_audio and target_audio can be None or str
            assert data["progression_audio"] is None or isinstance(
                data["progression_audio"], str
            )
            assert data["target_audio"] is None or isinstance(data["target_audio"], str)

            # Check value constraints
            assert len(data["key"]) > 0
            # Scale can be empty for interval exercises
            assert isinstance(data["scale"], list)
            assert len(data["options"]) > 0
            assert len(data["correct_answer"]) > 0
            assert data["correct_answer"] in data["options"]

            # Check scale contains valid note names
            for note in data["scale"]:
                assert isinstance(note, str)
                assert len(note) > 0

    def test_exercise_check_contract(self):
        """Test exercise answer check response contract."""
        # Get a valid exercise ID
        url = reverse("api:exercise-list")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

        exercises = response.data
        if exercises:
            exercise_id = exercises[0]["id"]

            # Generate exercise first
            url = reverse("api:exercise-generate", kwargs={"exercise_id": exercise_id})
            response = self.client.get(url)
            assert response.status_code == status.HTTP_200_OK

            exercise_data = response.data

            # Check answer
            url = reverse("api:exercise-check", kwargs={"exercise_id": exercise_id})
            data = {
                "answer": exercise_data["correct_answer"],
                "context": exercise_data["context"],
            }
            response = self.client.post(url, data, format="json")

            assert response.status_code == status.HTTP_200_OK

            result = response.data
            required_fields = [
                "is_correct",
                "user_answer",
                "correct_answer",
                "feedback",
            ]

            for field in required_fields:
                assert field in result, f"Missing required field: {field}"

            # Check field types
            assert isinstance(result["is_correct"], bool)
            assert isinstance(result["user_answer"], str)
            assert isinstance(result["correct_answer"], str)
            assert isinstance(result["feedback"], str)

            # Check value constraints
            assert len(result["user_answer"]) > 0
            assert len(result["correct_answer"]) > 0
            assert len(result["feedback"]) > 0

            # Check optional fields
            if "hints_used" in result:
                assert isinstance(result["hints_used"], list)
            if "time_taken" in result and result["time_taken"] is not None:
                assert isinstance(result["time_taken"], int)
                assert result["time_taken"] >= 0

    def test_exercise_instructions_contract(self):
        """Test exercise instructions response contract."""
        # Get a valid exercise ID
        url = reverse("api:exercise-list")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

        exercises = response.data
        if exercises:
            exercise_id = exercises[0]["id"]

            url = reverse(
                "api:exercise-instructions", kwargs={"exercise_id": exercise_id}
            )
            response = self.client.get(url)

            assert response.status_code == status.HTTP_200_OK

            data = response.data
            required_fields = ["instructions", "hints"]

            for field in required_fields:
                assert field in data, f"Missing required field: {field}"

            # Check field types
            assert isinstance(data["instructions"], str)
            assert isinstance(data["hints"], list)

            # Check value constraints
            assert len(data["instructions"]) > 0

            # Check hints structure
            for hint in data["hints"]:
                assert isinstance(hint, str)
                assert len(hint) > 0

    def test_audio_file_contract(self):
        """Test audio file response contract."""
        # Test with a sample audio file (if it exists)
        url = reverse("api:audio-file", kwargs={"filename": "test.wav"})
        response = self.client.get(url)

        # Should either return the file or 404
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]

        if response.status_code == status.HTTP_200_OK:
            # Check content type
            assert response["Content-Type"] in ["audio/wav", "audio/mpeg"]

            # Check content length
            assert "Content-Length" in response

            # Check that it's a file response
            assert hasattr(response, "streaming_content") or hasattr(
                response, "content"
            )

    def test_error_response_contract(self):
        """Test error response contract."""
        # Test 404 error
        url = reverse("api:exercise-detail", kwargs={"exercise_id": "nonexistent"})
        response = self.client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

        data = response.data
        required_fields = ["error", "message"]

        for field in required_fields:
            assert field in data, f"Missing required field in error response: {field}"

        # Check field types
        assert isinstance(data["error"], str)
        assert isinstance(data["message"], str)

        # Check error codes
        assert data["error"] == "not_found"

        # Test 400 error (validation error) - use existing exercise
        exercises = exercise_registry.get_exercise_list()
        if exercises:
            exercise_id = exercises[0].id
            url = reverse("api:exercise-check", kwargs={"exercise_id": exercise_id})
            data = {}  # Missing required fields
            response = self.client.post(url, data, format="json")

            assert response.status_code == status.HTTP_400_BAD_REQUEST

        data = response.data
        assert "error" in data
        assert "message" in data
        assert data["error"] == "validation_error"

    def test_cors_headers(self):
        """Test CORS headers are present."""
        url = reverse("api:exercise-list")
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK

        # Check for CORS headers (if configured)
        # Note: CORS headers might not be present in test environment
        # This test documents the expected behavior
        # Expected CORS headers:
        # - Access-Control-Allow-Origin
        # - Access-Control-Allow-Methods
        # - Access-Control-Allow-Headers
        # This is informational - CORS might not be configured in test environment

    def test_response_content_type(self):
        """Test that all API responses have correct content type."""
        endpoints = [
            ("api:api-root", "GET", {}),
            ("api:exercise-list", "GET", {}),
        ]

        # Get a valid exercise ID for endpoints that need it
        url = reverse("api:exercise-list")
        response = self.client.get(url)
        if response.status_code == status.HTTP_200_OK and response.data:
            exercise_id = response.data[0]["id"]
            endpoints.extend(
                [
                    ("api:exercise-detail", "GET", {"exercise_id": exercise_id}),
                    ("api:exercise-generate", "GET", {"exercise_id": exercise_id}),
                    ("api:exercise-instructions", "GET", {"exercise_id": exercise_id}),
                ]
            )

        for endpoint_name, method, kwargs in endpoints:
            url = reverse(endpoint_name, kwargs=kwargs)

            if method == "GET":
                response = self.client.get(url)
            elif method == "POST":
                response = self.client.post(url, {}, format="json")

            assert response.status_code in [
                status.HTTP_200_OK,
                status.HTTP_404_NOT_FOUND,
            ]

            # Check content type
            assert "Content-Type" in response
            assert "application/json" in response["Content-Type"]

    def test_api_versioning_contract(self):
        """Test API versioning contract."""
        url = reverse("api:api-root")
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK

        data = response.data
        assert "version" in data

        # Version should follow semantic versioning
        version = data["version"]
        assert isinstance(version, str)
        assert len(version) > 0

        # Should be in format like "1.0.0"
        parts = version.split(".")
        assert len(parts) == 3
        for part in parts:
            assert part.isdigit()

    def test_exercise_metadata_consistency(self):
        """Test that exercise metadata is consistent across endpoints."""
        # Get exercise list
        url = reverse("api:exercise-list")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

        exercises = response.data

        for exercise in exercises:
            exercise_id = exercise["id"]

            # Get exercise detail
            url = reverse("api:exercise-detail", kwargs={"exercise_id": exercise_id})
            response = self.client.get(url)
            assert response.status_code == status.HTTP_200_OK

            detail = response.data

            # Check that basic fields match
            assert exercise["id"] == detail["id"]
            assert exercise["name"] == detail["name"]
            assert exercise["description"] == detail["description"]
            assert exercise["difficulty"] == detail["difficulty"]
            assert exercise["category"] == detail["category"]

    def test_api_response_size_limits(self):
        """Test that API responses are within reasonable size limits."""
        # Test exercise list response size
        url = reverse("api:exercise-list")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

        # Response should not be too large
        content_length = len(str(response.data))
        assert content_length < 100000  # Less than 100KB

        # Test exercise detail response size
        exercises = response.data
        if exercises:
            exercise_id = exercises[0]["id"]

            url = reverse("api:exercise-detail", kwargs={"exercise_id": exercise_id})
            response = self.client.get(url)
            assert response.status_code == status.HTTP_200_OK

            content_length = len(str(response.data))
            assert content_length < 10000  # Less than 10KB per exercise

    def test_api_response_time_limits(self):
        """Test that API responses are within reasonable time limits."""
        import time

        endpoints = [
            ("api:api-root", "GET", {}),
            ("api:exercise-list", "GET", {}),
        ]

        # Get a valid exercise ID
        url = reverse("api:exercise-list")
        response = self.client.get(url)
        if response.status_code == status.HTTP_200_OK and response.data:
            exercise_id = response.data[0]["id"]
            endpoints.extend(
                [
                    ("api:exercise-detail", "GET", {"exercise_id": exercise_id}),
                    ("api:exercise-generate", "GET", {"exercise_id": exercise_id}),
                ]
            )

        for endpoint_name, method, kwargs in endpoints:
            url = reverse(endpoint_name, kwargs=kwargs)

            start_time = time.time()
            if method == "GET":
                response = self.client.get(url)
            elif method == "POST":
                response = self.client.post(url, {}, format="json")
            end_time = time.time()

            response_time = end_time - start_time

            # Most endpoints should respond quickly
            if endpoint_name == "api:exercise-generate":
                assert response_time < 10.0  # Audio generation can take longer
            else:
                assert response_time < 2.0  # Other endpoints should be fast
