"""
Tests for API serializers.
"""

from api_app.serializers import (
    AnswerCheckSerializer,
    AnswerResultSerializer,
    ErrorSerializer,
    ExerciseDataSerializer,
    ExerciseGenerateSerializer,
    ExerciseListSerializer,
)


class TestExerciseListSerializer:
    """Test ExerciseListSerializer."""

    def test_valid_exercise_list_serialization(self):
        """Test serialization of valid exercise data."""
        data = {
            "id": "test_exercise",
            "name": "Test Exercise",
            "description": "A test exercise",
            "difficulty": 5,
            "category": "interval_recognition",
            "tags": ["intervals", "melodic"],
            "estimated_time": 30,
            "prerequisites": ["basic_intervals"],
            "learning_objectives": ["Learn to identify intervals"],
            "input_type": "multiple_choice",
            "answer_format": "interval_name",
            "requires_progression": False,
            "requires_single_note": True,
            "audio_duration": 2,
            "config_options": {"key": "C", "octave": 4},
        }

        serializer = ExerciseListSerializer(data=data)
        assert serializer.is_valid()
        assert serializer.validated_data == data

    def test_exercise_list_serialization_missing_required_fields(self):
        """Test serialization with missing required fields."""
        data = {
            "id": "test_exercise",
            "name": "Test Exercise",
            # Missing required fields
        }

        serializer = ExerciseListSerializer(data=data)
        assert not serializer.is_valid()
        assert "description" in serializer.errors
        assert "difficulty" in serializer.errors
        assert "category" in serializer.errors

    def test_exercise_list_serialization_invalid_types(self):
        """Test serialization with invalid field types."""
        data = {
            "id": "test_exercise",
            "name": "Test Exercise",
            "description": "A test exercise",
            "difficulty": "invalid",  # Should be int
            "category": "interval_recognition",
            "tags": "not_a_list",  # Should be list
            "estimated_time": 30,
            "prerequisites": ["basic_intervals"],
            "learning_objectives": ["Learn to identify intervals"],
            "input_type": "multiple_choice",
            "answer_format": "interval_name",
            "requires_progression": False,
            "requires_single_note": True,
            "audio_duration": 2,
            "config_options": {"key": "C", "octave": 4},
        }

        serializer = ExerciseListSerializer(data=data)
        assert not serializer.is_valid()
        assert "difficulty" in serializer.errors
        assert "tags" in serializer.errors

    def test_exercise_list_serialization_with_optional_fields(self):
        """Test serialization with optional fields."""
        data = {
            "id": "test_exercise",
            "name": "Test Exercise",
            "description": "A test exercise",
            "difficulty": 5,
            "category": "interval_recognition",
            "tags": ["intervals", "melodic"],
            "estimated_time": 30,
            "prerequisites": ["basic_intervals"],
            "learning_objectives": ["Learn to identify intervals"],
            "input_type": "multiple_choice",
            "answer_format": "interval_name",
            "requires_progression": True,
            "requires_single_note": False,
            "audio_duration": 3,
            "config_options": {"key": "C", "octave": 4},
        }

        serializer = ExerciseListSerializer(data=data)
        assert serializer.is_valid()


class TestExerciseDataSerializer:
    """Test ExerciseDataSerializer."""

    def test_valid_exercise_data_serialization(self):
        """Test serialization of valid exercise data."""
        data = {
            "key": "C major",
            "scale": ["C", "D", "E", "F", "G", "A", "B"],
            "progression_audio": "/api/audio/progression.wav",
            "target_audio": "/api/audio/target.wav",
            "options": ["minor_third", "major_third", "octave"],
            "correct_answer": "major_third",
            "context": {"root_note": "C-4", "interval": "major_third"},
        }

        serializer = ExerciseDataSerializer(data=data)
        assert serializer.is_valid()
        assert serializer.validated_data == data

    def test_exercise_data_serialization_with_none_audio(self):
        """Test serialization with None audio files."""
        data = {
            "key": "C major",
            "scale": ["C", "D", "E", "F", "G", "A", "B"],
            "progression_audio": None,
            "target_audio": None,
            "options": ["minor_third", "major_third", "octave"],
            "correct_answer": "major_third",
            "context": {},
        }

        serializer = ExerciseDataSerializer(data=data)
        assert serializer.is_valid()

    def test_exercise_data_serialization_missing_required_fields(self):
        """Test serialization with missing required fields."""
        data = {
            "key": "C major",
            # Missing required fields
        }

        serializer = ExerciseDataSerializer(data=data)
        assert not serializer.is_valid()
        assert "scale" in serializer.errors
        assert "options" in serializer.errors
        assert "correct_answer" in serializer.errors

    def test_exercise_data_serialization_invalid_types(self):
        """Test serialization with invalid field types."""
        data = {
            "key": "C major",
            "scale": "not_a_list",  # Should be list
            "progression_audio": "/api/audio/progression.wav",
            "target_audio": "/api/audio/target.wav",
            "options": "not_a_list",  # Should be list
            "correct_answer": "major_third",
            "context": "not_a_dict",  # Should be dict
        }

        serializer = ExerciseDataSerializer(data=data)
        assert not serializer.is_valid()
        assert "scale" in serializer.errors
        assert "options" in serializer.errors
        assert "context" in serializer.errors


class TestAnswerCheckSerializer:
    """Test AnswerCheckSerializer."""

    def test_valid_answer_check_serialization(self):
        """Test serialization of valid answer check data."""
        data = {
            "answer": "major_third",
        }

        serializer = AnswerCheckSerializer(data=data)
        assert serializer.is_valid()
        assert serializer.validated_data == data

    def test_answer_check_serialization_missing_answer(self):
        """Test serialization with missing answer."""
        data = {}

        serializer = AnswerCheckSerializer(data=data)
        assert not serializer.is_valid()
        assert "answer" in serializer.errors

    def test_answer_check_serialization_empty_answer(self):
        """Test serialization with empty answer."""
        data = {
            "answer": "",
        }

        serializer = AnswerCheckSerializer(data=data)
        # Empty string should be valid (let the exercise handle validation)
        assert serializer.is_valid()

    def test_answer_check_serialization_with_extra_fields(self):
        """Test serialization with extra fields (should be ignored)."""
        data = {
            "answer": "major_third",
            "extra_field": "should_be_ignored",
        }

        serializer = AnswerCheckSerializer(data=data)
        assert serializer.is_valid()
        # Extra field should not be in validated_data
        assert "extra_field" not in serializer.validated_data


class TestAnswerResultSerializer:
    """Test AnswerResultSerializer."""

    def test_valid_answer_result_serialization(self):
        """Test serialization of valid answer result data."""
        data = {
            "is_correct": True,
            "user_answer": "major_third",
            "correct_answer": "major_third",
            "feedback": "Correct! Well done!",
            "hints_used": ["interval_size"],
            "time_taken": 15,
        }

        serializer = AnswerResultSerializer(data=data)
        assert serializer.is_valid()
        assert serializer.validated_data == data

    def test_answer_result_serialization_without_optional_fields(self):
        """Test serialization without optional fields."""
        data = {
            "is_correct": False,
            "user_answer": "minor_third",
            "correct_answer": "major_third",
            "feedback": "Incorrect. The correct answer was major_third.",
        }

        serializer = AnswerResultSerializer(data=data)
        assert serializer.is_valid()

    def test_answer_result_serialization_missing_required_fields(self):
        """Test serialization with missing required fields."""
        data = {
            "is_correct": True,
            # Missing required fields
        }

        serializer = AnswerResultSerializer(data=data)
        assert not serializer.is_valid()
        assert "user_answer" in serializer.errors
        assert "correct_answer" in serializer.errors
        assert "feedback" in serializer.errors

    def test_answer_result_serialization_invalid_types(self):
        """Test serialization with invalid field types."""
        data = {
            "is_correct": "not_a_boolean",  # Should be boolean
            "user_answer": "major_third",
            "correct_answer": "major_third",
            "feedback": "Correct!",
            "hints_used": "not_a_list",  # Should be list
            "time_taken": "not_a_number",  # Should be int
        }

        serializer = AnswerResultSerializer(data=data)
        assert not serializer.is_valid()
        assert "is_correct" in serializer.errors
        assert "hints_used" in serializer.errors
        assert "time_taken" in serializer.errors


class TestExerciseGenerateSerializer:
    """Test ExerciseGenerateSerializer."""

    def test_valid_exercise_generate_serialization(self):
        """Test serialization of valid exercise generation data."""
        data = {
            "key": "C",
            "difficulty": 5,
            "progression_type": "major",
            "octave": 4,
        }

        serializer = ExerciseGenerateSerializer(data=data)
        assert serializer.is_valid()
        assert serializer.validated_data == data

    def test_exercise_generate_serialization_without_optional_fields(self):
        """Test serialization without optional fields."""
        data = {}

        serializer = ExerciseGenerateSerializer(data=data)
        assert serializer.is_valid()
        assert serializer.validated_data == {}

    def test_exercise_generate_serialization_invalid_difficulty(self):
        """Test serialization with invalid difficulty values."""
        # Test difficulty too low
        data = {"difficulty": 0}
        serializer = ExerciseGenerateSerializer(data=data)
        assert not serializer.is_valid()
        assert "difficulty" in serializer.errors

        # Test difficulty too high
        data = {"difficulty": 11}
        serializer = ExerciseGenerateSerializer(data=data)
        assert not serializer.is_valid()
        assert "difficulty" in serializer.errors

    def test_exercise_generate_serialization_invalid_octave(self):
        """Test serialization with invalid octave values."""
        # Test octave too low
        data = {"octave": 0}
        serializer = ExerciseGenerateSerializer(data=data)
        assert not serializer.is_valid()
        assert "octave" in serializer.errors

        # Test octave too high
        data = {"octave": 9}
        serializer = ExerciseGenerateSerializer(data=data)
        assert not serializer.is_valid()
        assert "octave" in serializer.errors

    def test_exercise_generate_serialization_valid_boundary_values(self):
        """Test serialization with valid boundary values."""
        # Test minimum valid values
        data = {"difficulty": 1, "octave": 1}
        serializer = ExerciseGenerateSerializer(data=data)
        assert serializer.is_valid()

        # Test maximum valid values
        data = {"difficulty": 10, "octave": 8}
        serializer = ExerciseGenerateSerializer(data=data)
        assert serializer.is_valid()


class TestErrorSerializer:
    """Test ErrorSerializer."""

    def test_valid_error_serialization(self):
        """Test serialization of valid error data."""
        data = {
            "error": "not_found",
            "message": "Exercise not found",
            "details": {"exercise_id": "invalid_exercise"},
        }

        serializer = ErrorSerializer(data=data)
        assert serializer.is_valid()
        assert serializer.validated_data == data

    def test_error_serialization_without_details(self):
        """Test serialization without optional details field."""
        data = {
            "error": "validation_error",
            "message": "Invalid input data",
        }

        serializer = ErrorSerializer(data=data)
        assert serializer.is_valid()

    def test_error_serialization_missing_required_fields(self):
        """Test serialization with missing required fields."""
        data = {
            "error": "not_found",
            # Missing message
        }

        serializer = ErrorSerializer(data=data)
        assert not serializer.is_valid()
        assert "message" in serializer.errors

    def test_error_serialization_invalid_types(self):
        """Test serialization with invalid field types."""
        data = {
            "error": None,  # Should be string
            "message": "Error message",
            "details": "not_a_dict",  # Should be dict
        }

        serializer = ErrorSerializer(data=data)
        assert not serializer.is_valid()
        assert "error" in serializer.errors
        assert "details" in serializer.errors


class TestSerializerIntegration:
    """Test serializer integration and edge cases."""

    def test_serializer_round_trip(self):
        """Test serialization and deserialization round trip."""
        original_data = {
            "id": "test_exercise",
            "name": "Test Exercise",
            "description": "A test exercise",
            "difficulty": 5,
            "category": "interval_recognition",
            "tags": ["intervals", "melodic"],
            "estimated_time": 30,
            "prerequisites": ["basic_intervals"],
            "learning_objectives": ["Learn to identify intervals"],
            "input_type": "multiple_choice",
            "answer_format": "interval_name",
            "requires_progression": False,
            "requires_single_note": True,
            "audio_duration": 2,
            "config_options": {"key": "C", "octave": 4},
        }

        # Serialize
        serializer = ExerciseListSerializer(data=original_data)
        assert serializer.is_valid()
        validated_data = serializer.validated_data

        # Deserialize (create new serializer with validated data)
        serializer2 = ExerciseListSerializer(data=validated_data)
        assert serializer2.is_valid()

        # Should be the same
        assert serializer2.validated_data == original_data

    def test_serializer_with_unicode_data(self):
        """Test serializers with unicode data."""
        data = {
            "id": "test_exercise_émojis",
            "name": "Test Exercise with émojis 🎵",
            "description": "A test exercise with unicode: émojis 🎵 and accents",
            "difficulty": 5,
            "category": "interval_recognition",
            "tags": ["intervals", "melodic", "émojis"],
            "estimated_time": 30,
            "prerequisites": ["basic_intervals"],
            "learning_objectives": ["Learn to identify intervals"],
            "input_type": "multiple_choice",
            "answer_format": "interval_name",
            "requires_progression": False,
            "requires_single_note": True,
            "audio_duration": 2,
            "config_options": {"key": "C", "octave": 4},
        }

        serializer = ExerciseListSerializer(data=data)
        assert serializer.is_valid()

    def test_serializer_with_large_data(self):
        """Test serializers with large data structures."""
        # Large list of tags
        large_tags = [f"tag_{i}" for i in range(100)]
        large_prerequisites = [f"prereq_{i}" for i in range(50)]
        large_objectives = [f"objective_{i}" for i in range(50)]

        data = {
            "id": "test_exercise",
            "name": "Test Exercise",
            "description": "A test exercise",
            "difficulty": 5,
            "category": "interval_recognition",
            "tags": large_tags,
            "estimated_time": 30,
            "prerequisites": large_prerequisites,
            "learning_objectives": large_objectives,
            "input_type": "multiple_choice",
            "answer_format": "interval_name",
            "requires_progression": False,
            "requires_single_note": True,
            "audio_duration": 2,
            "config_options": {"key": "C", "octave": 4},
        }

        serializer = ExerciseListSerializer(data=data)
        assert serializer.is_valid()

    def test_serializer_error_handling(self):
        """Test serializer error handling with malformed data."""
        # Test with completely invalid data
        invalid_data = {
            "id": None,
            "name": 123,
            "description": [],
            "difficulty": "invalid",
            "category": None,
            "tags": "not_a_list",
            "estimated_time": -1,
            "prerequisites": "not_a_list",
            "learning_objectives": "not_a_list",
            "input_type": None,
            "answer_format": None,
        }

        serializer = ExerciseListSerializer(data=invalid_data)
        assert not serializer.is_valid()

        # Should have errors for all fields
        assert len(serializer.errors) > 0
