"""
Integration tests for complete exercise workflows.
"""

from api_app.views import exercise_registry
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TestExerciseWorkflowIntegration(APITestCase):
    """Test complete exercise workflows from generation to completion."""

    def test_complete_exercise_workflow(self):
        """Test complete workflow: list → generate → check answer."""
        # Step 1: Get exercise list
        url = reverse("api:exercise-list")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

        exercises = response.data
        assert len(exercises) > 0

        # Get first exercise
        exercise_id = exercises[0]["id"]

        # Step 2: Get exercise details
        url = reverse("api:exercise-detail", kwargs={"exercise_id": exercise_id})
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

        exercise_detail = response.data
        assert exercise_detail["id"] == exercise_id

        # Step 3: Generate exercise with fixed configuration
        url = reverse("api:exercise-generate", kwargs={"exercise_id": exercise_id})
        # Use fixed parameters to ensure deterministic results
        response = self.client.get(
            url, {"interval": "major_third", "reference_note": "C"}
        )
        assert response.status_code == status.HTTP_200_OK

        exercise_data = response.data
        assert "key" in exercise_data
        assert "scale" in exercise_data
        assert "options" in exercise_data
        assert "correct_answer" in exercise_data
        assert "context" in exercise_data

        # Step 4: Check correct answer
        url = reverse("api:exercise-check", kwargs={"exercise_id": exercise_id})
        context = exercise_data["context"].copy()
        context["correct_answer"] = exercise_data["correct_answer"]
        data = {"answer": exercise_data["correct_answer"], "context": context}
        response = self.client.post(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK

        result = response.data
        assert result["is_correct"] is True
        assert result["user_answer"] == exercise_data["correct_answer"]
        assert result["correct_answer"] == exercise_data["correct_answer"]

        # Step 5: Check incorrect answer
        # Find an incorrect answer
        incorrect_answer = None
        for option in exercise_data["options"]:
            if option != exercise_data["correct_answer"]:
                incorrect_answer = option
                break

        if incorrect_answer:
            data = {"answer": incorrect_answer, "context": exercise_data["context"]}
            response = self.client.post(url, data, format="json")
            assert response.status_code == status.HTTP_200_OK

            result = response.data
            assert result["is_correct"] is False
            assert result["user_answer"] == incorrect_answer
            assert result["correct_answer"] == exercise_data["correct_answer"]

    def test_multiple_question_session(self):
        """Test multiple question session workflow."""
        # Get exercise list
        url = reverse("api:exercise-list")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

        exercises = response.data
        exercise_id = exercises[0]["id"]

        # Generate multiple questions
        questions = []
        for i in range(5):
            url = reverse("api:exercise-generate", kwargs={"exercise_id": exercise_id})
            response = self.client.get(url, {"question_number": i + 1})
            assert response.status_code == status.HTTP_200_OK

            exercise_data = response.data
            questions.append(exercise_data)

            # Each question should have different content (due to randomization)
            assert "key" in exercise_data
            assert "correct_answer" in exercise_data

        # Check that we got different questions
        correct_answers = [q["correct_answer"] for q in questions]
        # At least some should be different (due to randomization)
        assert len(set(correct_answers)) > 1 or len(questions) == 1

    def test_exercise_with_audio_generation(self):
        """Test exercise workflow with audio generation."""
        # Get exercise list
        url = reverse("api:exercise-list")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

        exercises = response.data
        exercise_id = exercises[0]["id"]

        # Generate exercise
        url = reverse("api:exercise-generate", kwargs={"exercise_id": exercise_id})
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

        exercise_data = response.data

        # Check if audio files are generated
        if exercise_data.get("target_audio"):
            audio_url = exercise_data["target_audio"]
            # Test audio file access
            if audio_url.startswith("/api/audio/"):
                filename = audio_url.split("/")[-1]
                if filename:  # Only test if filename is not empty
                    url = reverse("api:audio-file", kwargs={"filename": filename})
                    response = self.client.get(url)
                    # Should either return the file or 404 (if file doesn't exist yet)
                    assert response.status_code in [
                        status.HTTP_200_OK,
                        status.HTTP_404_NOT_FOUND,
                    ]

    def test_exercise_instructions_workflow(self):
        """Test exercise instructions workflow."""
        # Get exercise list
        url = reverse("api:exercise-list")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

        exercises = response.data
        exercise_id = exercises[0]["id"]

        # Get instructions
        url = reverse("api:exercise-instructions", kwargs={"exercise_id": exercise_id})
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

        instructions_data = response.data
        assert "instructions" in instructions_data
        assert "hints" in instructions_data
        assert isinstance(instructions_data["instructions"], str)
        assert isinstance(instructions_data["hints"], list)

    def test_exercise_workflow_with_configuration(self):
        """Test exercise workflow with different configurations."""
        # Get exercise list
        url = reverse("api:exercise-list")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

        exercises = response.data
        exercise_id = exercises[0]["id"]

        # Test with different configurations
        configs = [
            {"key": "C"},
            {"key": "G"},
            {"octave": 4},
            {"octave": 5},
            {"key": "F", "octave": 4},
        ]

        for config in configs:
            url = reverse("api:exercise-generate", kwargs={"exercise_id": exercise_id})
            response = self.client.get(url, config)
            assert response.status_code == status.HTTP_200_OK

            exercise_data = response.data
            assert "key" in exercise_data
            assert "correct_answer" in exercise_data

            # For interval exercises, key is formatted as "Question X/Y"
            # If key was specified, it should be reflected in the response
            if "key" in config:
                # For interval exercises, the key format is different
                assert (
                    "Question" in exercise_data["key"]
                    or exercise_data["key"] == config["key"]
                )

    def test_exercise_workflow_error_handling(self):
        """Test exercise workflow error handling."""
        # Test with invalid exercise ID
        url = reverse("api:exercise-detail", kwargs={"exercise_id": "invalid_exercise"})
        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

        # Test exercise generation with invalid ID
        url = reverse(
            "api:exercise-generate", kwargs={"exercise_id": "invalid_exercise"}
        )
        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

        # Test answer checking with invalid ID
        url = reverse("api:exercise-check", kwargs={"exercise_id": "invalid_exercise"})
        data = {"answer": "major_third"}
        response = self.client.post(url, data, format="json")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_exercise_registry_integration(self):
        """Test integration with exercise registry."""
        # Test that registry is properly integrated
        exercises = exercise_registry.get_exercise_list()
        assert len(exercises) > 0

        # Test that all exercises in registry are accessible via API
        for exercise in exercises:
            exercise_id = exercise.id

            # Test detail endpoint
            url = reverse("api:exercise-detail", kwargs={"exercise_id": exercise_id})
            response = self.client.get(url)
            assert response.status_code == status.HTTP_200_OK

            # Test generation endpoint
            url = reverse("api:exercise-generate", kwargs={"exercise_id": exercise_id})
            response = self.client.get(url)
            assert response.status_code == status.HTTP_200_OK

    def test_exercise_workflow_performance(self):
        """Test exercise workflow performance."""
        import time

        # Get exercise list
        url = reverse("api:exercise-list")
        start_time = time.time()
        response = self.client.get(url)
        end_time = time.time()

        assert response.status_code == status.HTTP_200_OK
        assert (end_time - start_time) < 1.0  # Should complete in less than 1 second

        exercises = response.data
        exercise_id = exercises[0]["id"]

        # Test exercise generation performance
        url = reverse("api:exercise-generate", kwargs={"exercise_id": exercise_id})
        start_time = time.time()
        response = self.client.get(url)
        end_time = time.time()

        assert response.status_code == status.HTTP_200_OK
        assert (end_time - start_time) < 5.0  # Should complete in less than 5 seconds

    def test_exercise_workflow_with_mocked_audio(self):
        """Test exercise workflow with mocked audio generation."""
        # Get exercise list
        url = reverse("api:exercise-list")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

        exercises = response.data
        exercise_id = exercises[0]["id"]

        # Generate exercise (should use mocked audio)
        url = reverse("api:exercise-generate", kwargs={"exercise_id": exercise_id})
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

        exercise_data = response.data
        assert "target_audio" in exercise_data

        # If audio is generated, test the audio endpoint
        if exercise_data.get("target_audio"):
            audio_url = exercise_data["target_audio"]
            if audio_url.startswith("/api/audio/"):
                filename = audio_url.split("/")[-1]
                if filename:  # Only test if filename is not empty
                    url = reverse("api:audio-file", kwargs={"filename": filename})
                    response = self.client.get(url)
                    # Should return 200 with mocked audio
                    assert response.status_code == status.HTTP_200_OK

    def test_exercise_workflow_data_consistency(self):
        """Test that exercise data is consistent across workflow."""
        # Get exercise list
        url = reverse("api:exercise-list")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

        exercises = response.data
        exercise_id = exercises[0]["id"]

        # Generate exercise multiple times
        exercise_data_list = []
        for _ in range(3):
            url = reverse("api:exercise-generate", kwargs={"exercise_id": exercise_id})
            response = self.client.get(url)
            assert response.status_code == status.HTTP_200_OK

            exercise_data = response.data
            exercise_data_list.append(exercise_data)

        # Check that all exercises have consistent structure
        for exercise_data in exercise_data_list:
            assert "key" in exercise_data
            assert "scale" in exercise_data
            assert "options" in exercise_data
            assert "correct_answer" in exercise_data
            assert "context" in exercise_data

            # Check that correct answer is in options
            assert exercise_data["correct_answer"] in exercise_data["options"]

            # Check that options are valid
            assert len(exercise_data["options"]) > 0
            for option in exercise_data["options"]:
                assert isinstance(option, str)
                assert len(option) > 0

    def test_exercise_workflow_with_different_exercises(self):
        """Test workflow with different exercise types."""
        # Get all exercises
        url = reverse("api:exercise-list")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

        exercises = response.data

        # Test workflow with each exercise type
        for exercise in exercises:
            exercise_id = exercise["id"]

            # Generate exercise
            url = reverse("api:exercise-generate", kwargs={"exercise_id": exercise_id})
            response = self.client.get(url)
            assert response.status_code == status.HTTP_200_OK

            exercise_data = response.data

            # Check answer
            url = reverse("api:exercise-check", kwargs={"exercise_id": exercise_id})
            context = exercise_data["context"].copy()
            context["correct_answer"] = exercise_data["correct_answer"]
            data = {"answer": exercise_data["correct_answer"], "context": context}
            response = self.client.post(url, data, format="json")
            assert response.status_code == status.HTTP_200_OK

            result = response.data
            assert result["is_correct"] is True
