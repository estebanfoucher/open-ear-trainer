"""
Tests for interval exercise implementations.
"""

from exercises.level1.combined_intervals_melodic import CombinedIntervalsMelodicExercise
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


class TestMinorThirdMajorThirdOctaveMelodicExercise:
    """Test MinorThirdMajorThirdOctaveMelodicExercise."""

    def test_exercise_initialization(self):
        """Test exercise initialization."""
        exercise = MinorThirdMajorThirdOctaveMelodicExercise()
        assert exercise.metadata.id == "minor_third_major_third_octave_melodic"
        assert exercise.metadata.name == "Minor Third, Major Third and Octave (Melodic)"
        assert exercise.metadata.difficulty == 1
        assert exercise.metadata.category == "interval_recognition"

    def test_exercise_generation(self):
        """Test exercise generation."""
        exercise = MinorThirdMajorThirdOctaveMelodicExercise()
        data = exercise.generate()

        # Check basic structure
        assert data.key is not None
        assert data.scale is not None
        assert data.target_audio is not None
        assert data.options is not None
        assert data.correct_answer is not None
        assert data.context is not None

        # Check that correct answer is in options
        assert data.correct_answer in data.options

        # Check that options contain expected intervals
        expected_intervals = ["3m", "3M", "8J"]  # minor_third, major_third, octave
        for option in data.options:
            assert option in expected_intervals

    def test_exercise_generation_with_config(self):
        """Test exercise generation with configuration."""
        exercise = MinorThirdMajorThirdOctaveMelodicExercise()
        data = exercise.generate(key="C", octave=4)

        assert data.key is not None
        assert len(data.key) > 0
        assert data.context.get("octave") == 4

    def test_answer_checking_correct(self):
        """Test correct answer checking."""
        exercise = MinorThirdMajorThirdOctaveMelodicExercise()
        data = exercise.generate()

        # Add correct_answer to context
        context = data.context.copy()
        context["correct_answer"] = data.correct_answer

        result = exercise.check_answer(data.correct_answer, context)
        assert result.is_correct is True
        assert result.user_answer == data.correct_answer
        assert result.correct_answer == data.correct_answer
        assert "Correct" in result.feedback

    def test_answer_checking_incorrect(self):
        """Test incorrect answer checking."""
        exercise = MinorThirdMajorThirdOctaveMelodicExercise()
        data = exercise.generate()

        # Find an incorrect answer
        incorrect_answer = None
        for option in data.options:
            if option != data.correct_answer:
                incorrect_answer = option
                break

        assert incorrect_answer is not None

        # Add correct_answer to context
        context = data.context.copy()
        context["correct_answer"] = data.correct_answer

        result = exercise.check_answer(incorrect_answer, context)
        assert result.is_correct is False
        assert result.user_answer == incorrect_answer
        assert result.correct_answer == data.correct_answer
        assert "Incorrect" in result.feedback

    def test_multiple_generations_different(self):
        """Test that multiple generations produce different results."""
        exercise = MinorThirdMajorThirdOctaveMelodicExercise()

        # Generate multiple exercises
        results = []
        for _ in range(10):
            data = exercise.generate()
            results.append((data.correct_answer, data.context.get("root_note")))

        # At least some should be different (due to randomization)
        unique_results = set(results)
        assert len(unique_results) > 1

    def test_instructions_and_hints(self):
        """Test exercise instructions and hints."""
        exercise = MinorThirdMajorThirdOctaveMelodicExercise()

        instructions = exercise.get_instructions()
        assert isinstance(instructions, str)
        assert len(instructions) > 0

        hints = exercise.get_hints()
        assert isinstance(hints, list)


class TestPerfectFourthPerfectFifthOctaveMelodicExercise:
    """Test PerfectFourthPerfectFifthOctaveMelodicExercise."""

    def test_exercise_initialization(self):
        """Test exercise initialization."""
        exercise = PerfectFourthPerfectFifthOctaveMelodicExercise()
        assert exercise.metadata.id == "perfect_fourth_fifth_octave_melodic"
        assert (
            exercise.metadata.name
            == "Perfect Fourth, Perfect Fifth and Octave (Melodic)"
        )
        assert exercise.metadata.difficulty == 1
        assert exercise.metadata.category == "interval_recognition"

    def test_exercise_generation(self):
        """Test exercise generation."""
        exercise = PerfectFourthPerfectFifthOctaveMelodicExercise()
        data = exercise.generate()

        # Check basic structure
        assert data.key is not None
        assert data.scale is not None
        assert data.target_audio is not None
        assert data.options is not None
        assert data.correct_answer is not None

        # Check that correct answer is in options
        assert data.correct_answer in data.options

        # Check that options contain expected intervals
        expected_intervals = ["4J", "5J", "8J"]  # perfect_fourth, perfect_fifth, octave
        for option in data.options:
            assert option in expected_intervals

    def test_answer_checking(self):
        """Test answer checking."""
        exercise = PerfectFourthPerfectFifthOctaveMelodicExercise()
        data = exercise.generate()

        # Test correct answer
        context = data.context.copy()
        context["correct_answer"] = data.correct_answer
        result = exercise.check_answer(data.correct_answer, context)
        assert result.is_correct is True

        # Test incorrect answer
        incorrect_answer = None
        for option in data.options:
            if option != data.correct_answer:
                incorrect_answer = option
                break

        if incorrect_answer:
            context = data.context.copy()
            context["correct_answer"] = data.correct_answer
            result = exercise.check_answer(incorrect_answer, context)
            assert result.is_correct is False


class TestMinorThirdMajorThirdOctaveHarmonicExercise:
    """Test MinorThirdMajorThirdOctaveHarmonicExercise."""

    def test_exercise_initialization(self):
        """Test exercise initialization."""
        exercise = MinorThirdMajorThirdOctaveHarmonicExercise()
        assert exercise.metadata.id == "minor_third_major_third_octave_harmonic"
        assert (
            exercise.metadata.name == "Minor Third, Major Third and Octave (Harmonic)"
        )
        assert exercise.metadata.difficulty == 1
        assert exercise.metadata.category == "interval_recognition"

    def test_exercise_generation(self):
        """Test exercise generation."""
        exercise = MinorThirdMajorThirdOctaveHarmonicExercise()
        data = exercise.generate()

        # Check basic structure
        assert data.key is not None
        assert data.scale is not None
        assert data.target_audio is not None
        assert data.options is not None
        assert data.correct_answer is not None

        # Check that correct answer is in options
        assert data.correct_answer in data.options

        # Check that options contain expected intervals
        expected_intervals = ["3m", "3M", "8J"]  # minor_third, major_third, octave
        for option in data.options:
            assert option in expected_intervals

    def test_answer_checking(self):
        """Test answer checking."""
        exercise = MinorThirdMajorThirdOctaveHarmonicExercise()
        data = exercise.generate()

        # Test correct answer
        context = data.context.copy()
        context["correct_answer"] = data.correct_answer
        result = exercise.check_answer(data.correct_answer, context)
        assert result.is_correct is True

        # Test incorrect answer
        incorrect_answer = None
        for option in data.options:
            if option != data.correct_answer:
                incorrect_answer = option
                break

        if incorrect_answer:
            context = data.context.copy()
            context["correct_answer"] = data.correct_answer
            result = exercise.check_answer(incorrect_answer, context)
            assert result.is_correct is False


class TestPerfectFourthPerfectFifthOctaveHarmonicExercise:
    """Test PerfectFourthPerfectFifthOctaveHarmonicExercise."""

    def test_exercise_initialization(self):
        """Test exercise initialization."""
        exercise = PerfectFourthPerfectFifthOctaveHarmonicExercise()
        assert exercise.metadata.id == "perfect_fourth_fifth_octave_harmonic"
        assert (
            exercise.metadata.name
            == "Perfect Fourth, Perfect Fifth and Octave (Harmonic)"
        )
        assert exercise.metadata.difficulty == 1
        assert exercise.metadata.category == "interval_recognition"

    def test_exercise_generation(self):
        """Test exercise generation."""
        exercise = PerfectFourthPerfectFifthOctaveHarmonicExercise()
        data = exercise.generate()

        # Check basic structure
        assert data.key is not None
        assert data.scale is not None
        assert data.target_audio is not None
        assert data.options is not None
        assert data.correct_answer is not None

        # Check that correct answer is in options
        assert data.correct_answer in data.options

        # Check that options contain expected intervals
        expected_intervals = ["4J", "5J", "8J"]  # perfect_fourth, perfect_fifth, octave
        for option in data.options:
            assert option in expected_intervals

    def test_answer_checking(self):
        """Test answer checking."""
        exercise = PerfectFourthPerfectFifthOctaveHarmonicExercise()
        data = exercise.generate()

        # Test correct answer
        context = data.context.copy()
        context["correct_answer"] = data.correct_answer
        result = exercise.check_answer(data.correct_answer, context)
        assert result.is_correct is True

        # Test incorrect answer
        incorrect_answer = None
        for option in data.options:
            if option != data.correct_answer:
                incorrect_answer = option
                break

        if incorrect_answer:
            context = data.context.copy()
            context["correct_answer"] = data.correct_answer
            result = exercise.check_answer(incorrect_answer, context)
            assert result.is_correct is False


class TestCombinedIntervalsMelodicExercise:
    """Test CombinedIntervalsMelodicExercise."""

    def test_exercise_initialization(self):
        """Test exercise initialization."""
        exercise = CombinedIntervalsMelodicExercise()
        assert exercise.metadata.id == "combined_intervals_melodic"
        assert (
            exercise.metadata.name
            == "Minor Third, Major Third, Perfect Fourth, Perfect Fifth and Octave (Melodic)"
        )
        assert exercise.metadata.difficulty == 1
        assert exercise.metadata.category == "interval_recognition"

    def test_exercise_generation(self):
        """Test exercise generation."""
        exercise = CombinedIntervalsMelodicExercise()
        data = exercise.generate()

        # Check basic structure
        assert data.key is not None
        assert data.scale is not None
        assert data.target_audio is not None
        assert data.options is not None
        assert data.correct_answer is not None

        # Check that correct answer is in options
        assert data.correct_answer in data.options

        # Check that options contain expected intervals (using notation)
        expected_intervals = [
            "2m",
            "2M",
            "3m",
            "3M",  # minor_second, major_second, minor_third, major_third
            "4J",
            "5J",
            "6m",
            "6M",  # perfect_fourth, perfect_fifth, minor_sixth, major_sixth
            "7m",
            "7M",
            "8J",  # minor_seventh, major_seventh, octave
        ]
        for option in data.options:
            assert option in expected_intervals

    def test_answer_checking(self):
        """Test answer checking."""
        exercise = CombinedIntervalsMelodicExercise()
        data = exercise.generate()

        # Test correct answer
        context = data.context.copy()
        context["correct_answer"] = data.correct_answer
        result = exercise.check_answer(data.correct_answer, context)
        assert result.is_correct is True

        # Test incorrect answer
        incorrect_answer = None
        for option in data.options:
            if option != data.correct_answer:
                incorrect_answer = option
                break

        if incorrect_answer:
            context = data.context.copy()
            context["correct_answer"] = data.correct_answer
            result = exercise.check_answer(incorrect_answer, context)
            assert result.is_correct is False


class TestExerciseEdgeCases:
    """Test edge cases across all exercises."""

    def test_all_exercises_have_metadata(self):
        """Test that all exercises have proper metadata."""
        exercises = [
            MinorThirdMajorThirdOctaveMelodicExercise(),
            PerfectFourthPerfectFifthOctaveMelodicExercise(),
            MinorThirdMajorThirdOctaveHarmonicExercise(),
            PerfectFourthPerfectFifthOctaveHarmonicExercise(),
            CombinedIntervalsMelodicExercise(),
        ]

        for exercise in exercises:
            assert hasattr(exercise, "metadata")
            assert exercise.metadata.id is not None
            assert exercise.metadata.name is not None
            assert exercise.metadata.description is not None
            assert 1 <= exercise.metadata.difficulty <= 10
            assert exercise.metadata.category is not None
            assert exercise.metadata.input_type is not None
            assert exercise.metadata.answer_format is not None

    def test_all_exercises_generate_valid_data(self):
        """Test that all exercises generate valid data."""
        exercises = [
            MinorThirdMajorThirdOctaveMelodicExercise(),
            PerfectFourthPerfectFifthOctaveMelodicExercise(),
            MinorThirdMajorThirdOctaveHarmonicExercise(),
            PerfectFourthPerfectFifthOctaveHarmonicExercise(),
            CombinedIntervalsMelodicExercise(),
        ]

        for exercise in exercises:
            data = exercise.generate()

            # Check required fields
            assert data.key is not None
            assert data.scale is not None
            assert data.correct_answer is not None
            assert data.options is not None
            assert len(data.options) > 0

            # Check that correct answer is in options
            assert data.correct_answer in data.options

            # Check that all options are valid
            for option in data.options:
                assert isinstance(option, str)
                assert len(option) > 0

    def test_all_exercises_check_answers_correctly(self):
        """Test that all exercises check answers correctly."""
        exercises = [
            MinorThirdMajorThirdOctaveMelodicExercise(),
            PerfectFourthPerfectFifthOctaveMelodicExercise(),
            MinorThirdMajorThirdOctaveHarmonicExercise(),
            PerfectFourthPerfectFifthOctaveHarmonicExercise(),
            CombinedIntervalsMelodicExercise(),
        ]

        for exercise in exercises:
            data = exercise.generate()

            # Test correct answer
            context = data.context.copy()
            context["correct_answer"] = data.correct_answer
            result = exercise.check_answer(data.correct_answer, context)
            assert result.is_correct is True
            assert result.user_answer == data.correct_answer
            assert result.correct_answer == data.correct_answer
            assert isinstance(result.feedback, str)
            assert len(result.feedback) > 0

            # Test incorrect answer
            incorrect_answer = None
            for option in data.options:
                if option != data.correct_answer:
                    incorrect_answer = option
                    break

            if incorrect_answer:
                context = data.context.copy()
                context["correct_answer"] = data.correct_answer
                result = exercise.check_answer(incorrect_answer, context)
                assert result.is_correct is False
                assert result.user_answer == incorrect_answer
                assert result.correct_answer == data.correct_answer
                assert isinstance(result.feedback, str)
                assert len(result.feedback) > 0

    def test_exercise_randomization(self):
        """Test that exercises produce different results over multiple runs."""
        exercise = MinorThirdMajorThirdOctaveMelodicExercise()

        # Generate multiple exercises and collect results
        results = []
        for _ in range(20):
            data = exercise.generate()
            results.append((data.correct_answer, data.context.get("root_note")))

        # Should have some variation due to randomization
        unique_results = set(results)
        assert len(unique_results) > 1, "Exercise should produce varied results"
