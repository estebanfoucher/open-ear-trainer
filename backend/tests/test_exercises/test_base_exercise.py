"""
Tests for base exercise classes and metadata.
"""

from exercises.base.exercise import BaseExercise
from exercises.base.metadata import ExerciseData, ExerciseMetadata, ExerciseResult


class TestExerciseMetadata:
    """Test ExerciseMetadata dataclass."""

    def test_metadata_creation(self):
        """Test basic metadata creation."""
        metadata = ExerciseMetadata(
            id="test_exercise",
            name="Test Exercise",
            description="A test exercise",
            difficulty=5,
            prerequisites=[],
            learning_objectives=["Learn to identify intervals"],
            estimated_time=30,
            category="interval_recognition",
            tags=["intervals", "melodic"],
            input_type="multiple_choice",
            answer_format="interval_name",
        )

        assert metadata.id == "test_exercise"
        assert metadata.difficulty == 5
        assert metadata.prerequisites == []
        assert metadata.config_options == {}

    def test_metadata_with_config_options(self):
        """Test metadata with custom config options."""
        config = {"key": "C", "octave": 4}
        metadata = ExerciseMetadata(
            id="test_exercise",
            name="Test Exercise",
            description="A test exercise",
            difficulty=5,
            prerequisites=[],
            learning_objectives=["Learn to identify intervals"],
            estimated_time=30,
            category="interval_recognition",
            tags=["intervals", "melodic"],
            input_type="multiple_choice",
            answer_format="interval_name",
            config_options=config,
        )

        assert metadata.config_options == config

    def test_metadata_defaults(self):
        """Test metadata default values."""
        metadata = ExerciseMetadata(
            id="test_exercise",
            name="Test Exercise",
            description="A test exercise",
            difficulty=5,
            prerequisites=[],
            learning_objectives=["Learn to identify intervals"],
            estimated_time=30,
            category="interval_recognition",
            tags=["intervals", "melodic"],
            input_type="multiple_choice",
            answer_format="interval_name",
        )

        assert metadata.requires_progression is False
        assert metadata.requires_single_note is True
        assert metadata.audio_duration == 2


class TestExerciseData:
    """Test ExerciseData dataclass."""

    def test_exercise_data_creation(self):
        """Test basic exercise data creation."""
        data = ExerciseData(
            key="C major",
            scale=["C", "D", "E", "F", "G", "A", "B"],
            correct_answer="major_third",
        )

        assert data.key == "C major"
        assert data.scale == ["C", "D", "E", "F", "G", "A", "B"]
        assert data.correct_answer == "major_third"
        assert data.options == []
        assert data.context == {}

    def test_exercise_data_with_audio(self):
        """Test exercise data with audio files."""
        data = ExerciseData(
            key="C major",
            scale=["C", "D", "E", "F", "G", "A", "B"],
            progression_audio="/api/audio/progression.wav",
            target_audio="/api/audio/target.wav",
            correct_answer="major_third",
        )

        assert data.progression_audio == "/api/audio/progression.wav"
        assert data.target_audio == "/api/audio/target.wav"

    def test_exercise_data_with_options(self):
        """Test exercise data with answer options."""
        options = ["minor_third", "major_third", "perfect_fourth"]
        data = ExerciseData(
            key="C major",
            scale=["C", "D", "E", "F", "G", "A", "B"],
            options=options,
            correct_answer="major_third",
        )

        assert data.options == options


class TestExerciseResult:
    """Test ExerciseResult dataclass."""

    def test_exercise_result_creation(self):
        """Test basic exercise result creation."""
        result = ExerciseResult(
            is_correct=True,
            user_answer="major_third",
            correct_answer="major_third",
            feedback="Correct! Well done!",
        )

        assert result.is_correct is True
        assert result.user_answer == "major_third"
        assert result.correct_answer == "major_third"
        assert result.feedback == "Correct! Well done!"
        assert result.hints_used == []
        assert result.time_taken is None

    def test_exercise_result_with_hints(self):
        """Test exercise result with hints used."""
        hints = ["interval_size", "harmonic_quality"]
        result = ExerciseResult(
            is_correct=False,
            user_answer="minor_third",
            correct_answer="major_third",
            feedback="Incorrect. The correct answer was major_third.",
            hints_used=hints,
            time_taken=15,
        )

        assert result.hints_used == hints
        assert result.time_taken == 15


class TestBaseExercise:
    """Test BaseExercise abstract class."""

    def test_base_exercise_abstract_methods(self):
        """Test that BaseExercise has abstract methods."""

        # Create a concrete implementation for testing
        class ConcreteExercise(BaseExercise):
            metadata = ExerciseMetadata(
                id="concrete_test",
                name="Concrete Test",
                description="A concrete test exercise",
                difficulty=1,
                prerequisites=[],
                learning_objectives=["Test"],
                estimated_time=10,
                category="test",
                tags=["test"],
                input_type="multiple_choice",
                answer_format="test",
            )

            def generate(self, **kwargs):
                return ExerciseData(
                    key="C major",
                    scale=["C", "D", "E", "F", "G", "A", "B"],
                    correct_answer="test",
                )

            def check_answer(self, answer, context):
                return ExerciseResult(
                    is_correct=True,
                    user_answer=answer,
                    correct_answer="test",
                    feedback="Test feedback",
                )

        exercise = ConcreteExercise()
        assert exercise.metadata.id == "concrete_test"

    def test_base_exercise_helper_methods(self):
        """Test BaseExercise helper methods."""

        # Create a concrete implementation for testing
        class ConcreteExercise(BaseExercise):
            metadata = ExerciseMetadata(
                id="concrete_test",
                name="Concrete Test",
                description="A concrete test exercise",
                difficulty=1,
                prerequisites=[],
                learning_objectives=["Test"],
                estimated_time=10,
                category="test",
                tags=["test"],
                input_type="multiple_choice",
                answer_format="test",
            )

            def generate(self, **kwargs):
                return ExerciseData(
                    key="C major",
                    scale=["C", "D", "E", "F", "G", "A", "B"],
                    correct_answer="test",
                )

            def check_answer(self, answer, context):
                return ExerciseResult(
                    is_correct=True,
                    user_answer=answer,
                    correct_answer="test",
                    feedback="Test feedback",
                )

        exercise = ConcreteExercise()

        # Test get_instructions
        instructions = exercise.get_instructions()
        assert instructions == "A concrete test exercise"

        # Test get_hints
        hints = exercise.get_hints()
        assert hints == []

        # Test get_feedback
        feedback_correct = exercise.get_feedback(True, "major_third", "major_third")
        assert "Correct" in feedback_correct

        feedback_incorrect = exercise.get_feedback(False, "minor_third", "major_third")
        assert "Incorrect" in feedback_incorrect
        assert "major_third" in feedback_incorrect

        # Test get_random_key
        key = exercise.get_random_key()
        assert key in [
            "C",
            "G",
            "D",
            "A",
            "E",
            "B",
            "F#",
            "C#",
            "F",
            "Bb",
            "Eb",
            "Ab",
            "Db",
            "Gb",
            "Cb",
        ]

        # Test get_random_minor_key
        minor_key = exercise.get_random_minor_key()
        assert minor_key in [
            "Am",
            "Em",
            "Bm",
            "F#m",
            "C#m",
            "G#m",
            "D#m",
            "A#m",
            "Dm",
            "Gm",
            "Cm",
            "Fm",
            "Bbm",
            "Ebm",
            "Abm",
        ]

        # Test get_scale_degrees
        scale_degrees = exercise.get_scale_degrees()
        assert scale_degrees == [1, 2, 3, 4, 5, 6, 7]

        # Test get_note_names
        note_names = exercise.get_note_names()
        assert note_names == ["C", "D", "E", "F", "G", "A", "B"]

        # Test get_chord_qualities
        chord_qualities = exercise.get_chord_qualities()
        assert chord_qualities == ["major", "minor", "diminished", "augmented"]

        # Test get_intervals
        intervals = exercise.get_intervals()
        expected_intervals = [
            "unison",
            "minor_second",
            "major_second",
            "minor_third",
            "major_third",
            "perfect_fourth",
            "tritone",
            "perfect_fifth",
            "minor_sixth",
            "major_sixth",
            "minor_seventh",
            "major_seventh",
            "octave",
        ]
        assert intervals == expected_intervals

    def test_validate_config(self):
        """Test config validation."""

        # Create a concrete implementation for testing
        class ConcreteExercise(BaseExercise):
            metadata = ExerciseMetadata(
                id="concrete_test",
                name="Concrete Test",
                description="A concrete test exercise",
                difficulty=1,
                prerequisites=[],
                learning_objectives=["Test"],
                estimated_time=10,
                category="test",
                tags=["test"],
                input_type="multiple_choice",
                answer_format="test",
            )

            def generate(self, **kwargs):
                return ExerciseData(
                    key="C major",
                    scale=["C", "D", "E", "F", "G", "A", "B"],
                    correct_answer="test",
                )

            def check_answer(self, answer, context):
                return ExerciseResult(
                    is_correct=True,
                    user_answer=answer,
                    correct_answer="test",
                    feedback="Test feedback",
                )

        exercise = ConcreteExercise()

        # Test valid config
        config = {"key": "C", "difficulty": 5}
        validated = exercise.validate_config(config)
        assert validated["key"] == "C"
        assert validated["difficulty"] == 5

        # Test invalid difficulty
        config = {"difficulty": 15}
        validated = exercise.validate_config(config)
        assert "difficulty" not in validated

        # Test invalid difficulty (too low)
        config = {"difficulty": 0}
        validated = exercise.validate_config(config)
        assert "difficulty" not in validated


class TestBaseIntervalExercise:
    """Test BaseIntervalExercise class."""

    def test_base_interval_exercise_initialization(self):
        """Test BaseIntervalExercise initialization."""
        # This will be tested with actual implementations
        # since BaseIntervalExercise is likely abstract
        pass

    def test_interval_exercise_metadata(self):
        """Test that interval exercises have proper metadata."""
        # This will be tested with actual implementations
        pass
