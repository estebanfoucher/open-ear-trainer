"""
Base class for interval recognition exercises.

This provides common functionality for all interval recognition exercises,
including melodic (staggered) and harmonic (simultaneous) versions.
"""

import random
from typing import Any

from music_app.notes import transpose_note

from exercises.base.exercise import BaseExercise
from exercises.base.metadata import ExerciseData, ExerciseMetadata, ExerciseResult


class BaseIntervalExercise(BaseExercise):
    """
    Base class for interval recognition exercises.

    Provides common functionality for generating interval exercises with
    different interval sets and timing (melodic vs harmonic).
    """

    def __init__(self, intervals: list[str], exercise_type: str, timing: str):
        """
        Initialize the interval exercise.

        Args:
            intervals: List of interval names (e.g., ["octave", "minor_third"])
            exercise_type: Type of exercise (e.g., "thirds_and_octave", "perfect_intervals")
            timing: "melodic" for staggered timing, "harmonic" for simultaneous
        """
        self.intervals = intervals
        self.exercise_type = exercise_type
        self.timing = timing
        self.is_melodic = timing == "melodic"

        # Set up metadata
        self.metadata = self._create_metadata()

    def _create_metadata(self) -> ExerciseMetadata:
        """Create metadata based on the exercise configuration."""
        interval_names = [
            self._get_interval_display_name(interval) for interval in self.intervals
        ]
        interval_list = ", ".join(interval_names[:-1]) + f" and {interval_names[-1]}"

        timing_desc = "melodic" if self.is_melodic else "harmonic"
        timing_desc_full = (
            "staggered timing" if self.is_melodic else "simultaneous notes"
        )

        return ExerciseMetadata(
            id=f"{self.exercise_type}_{timing_desc}",
            name=f"{interval_list} ({timing_desc.title()})",
            description=f"Identify the interval: {interval_list}. 20 questions with {timing_desc_full}.",
            difficulty=1,
            prerequisites=[],
            learning_objectives=[
                f"Recognize {interval_name} intervals"
                for interval_name in interval_names
            ]
            + [f"Develop {timing_desc} interval recognition skills"],
            estimated_time=300,  # 5 minutes for 20 questions
            category="interval_recognition",
            tags=["intervals"]
            + [interval.replace("_", "") for interval in self.intervals]
            + [timing_desc],
            input_type="multiple_choice",
            answer_format="interval_name",
            requires_progression=False,
            requires_single_note=False,
            audio_duration=3,  # Longer for two notes
            config_options={
                "available_intervals": self.intervals,
                "reference_notes": ["C", "D", "E", "F", "G", "A", "B"],
                "octave": 4,
                "total_questions": 20,
                "timing": self.timing,
                "interval_probabilities": {
                    "type": "dict",
                    "default": {
                        interval: 1.0 / len(self.intervals)
                        for interval in self.intervals
                    },
                    "description": "Custom probabilities for interval selection (must sum to 1.0)",
                },
            },
        )

    def generate(self, **kwargs) -> ExerciseData:
        """
        Generate an interval recognition exercise.

        Args:
            **kwargs: Configuration options
                - reference_note: Specific reference note to use (optional)
                - interval: Specific interval to use (optional)
                - question_number: Current question number (1-20)

        Returns:
            ExerciseData: Complete exercise data
        """
        # Get configuration
        config = self.validate_config(kwargs)

        # Select reference note randomly
        available_notes = self.metadata.config_options.get(
            "reference_notes", ["C", "D", "E", "F", "G", "A", "B"]
        )
        reference_note = config.get("reference_note", random.choice(available_notes))
        octave = config.get("octave", 4)
        reference_note_with_octave = f"{reference_note}-{octave}"

        # Custom probabilities for interval selection
        interval_probabilities = config.get(
            "interval_probabilities",
            {interval: 1.0 / len(self.intervals) for interval in self.intervals},
        )

        # Select interval with weighted choice
        interval = config.get("interval", self.weighted_choice(interval_probabilities))

        # Calculate the second note based on the interval
        second_note = self._get_interval_note(reference_note_with_octave, interval)

        # Generate audio files using the audio synthesizer
        from audio_app.synthesizer import AudioSynthesizer

        synthesizer = AudioSynthesizer()

        # Generate interval audio based on timing type
        if self.is_melodic:
            # Generate harmonic interval audio with staggered timing
            # Root note starts 400ms before the second note, both last 1.5 seconds
            interval_audio_path = synthesizer.synthesize_staggered_interval(
                reference_note_with_octave,
                second_note,
                root_duration=1.5,
                second_duration=1.5,
                delay_ms=400,
            )
        else:
            # Generate harmonic interval audio with simultaneous timing
            interval_audio_path = synthesizer.synthesize_harmonic_interval(
                reference_note_with_octave,
                second_note,
                duration=1.5,
            )

        # Get question number
        question_number = config.get("question_number", 1)
        total_questions = self.metadata.config_options.get("total_questions", 20)

        # Create options (all available intervals for this exercise)
        options = [self._get_interval_notation(interval) for interval in self.intervals]

        # Create context with exercise information
        context = {
            "reference_note": reference_note_with_octave,
            "second_note": second_note,
            "interval": interval,
            "interval_semitones": self._get_interval_semitones(interval),
            "question_number": question_number,
            "total_questions": total_questions,
            "timing": self.timing,
            "octave": octave,
        }

        # Convert file path to URL
        interval_audio_url = synthesizer.get_audio_url(interval_audio_path)

        return ExerciseData(
            key=f"Question {question_number}/{total_questions}",
            scale=[],
            progression_audio=None,
            target_audio=interval_audio_url,
            options=options,
            correct_answer=self._get_interval_notation(interval),
            context=context,
        )

    def check_answer(self, answer: Any, context: dict[str, Any]) -> ExerciseResult:
        """
        Check if the answer is correct.

        Args:
            answer: The student's answer
            context: Exercise context containing the correct answer

        Returns:
            ExerciseResult: Result of the answer check
        """
        correct_answer = context.get("correct_answer")
        is_correct = answer == correct_answer

        if is_correct:
            feedback = "Correct! Well done!"
        else:
            feedback = f"Incorrect. The correct answer was {correct_answer}."

        return ExerciseResult(
            is_correct=is_correct,
            feedback=feedback,
            correct_answer=correct_answer,
            user_answer=answer,
        )

    def get_instructions(self) -> str:
        """Get exercise instructions."""
        timing_desc = "staggered timing" if self.is_melodic else "simultaneous notes"
        return f"Listen to the two notes played with {timing_desc} and identify the interval."

    def get_hints(self) -> list[str]:
        """Get exercise hints."""
        return [
            "Listen carefully to the distance between the two notes",
            "Count the semitones if you're unsure",
            "Practice with a piano to develop your ear",
        ]

    def _get_interval_note(self, reference_note: str, interval: str) -> str:
        """
        Get the second note of an interval from a reference note.

        Args:
            reference_note: The reference note (e.g., "C-4")
            interval: The interval name (e.g., "octave", "minor_third")

        Returns:
            str: The second note (e.g., "C-5")
        """
        semitones = self._get_interval_semitones(interval)
        return transpose_note(reference_note, semitones)

    def _get_interval_semitones(self, interval: str) -> int:
        """
        Get the number of semitones for an interval.

        Args:
            interval: The interval name

        Returns:
            int: Number of semitones
        """
        interval_map = {
            "unison": 0,
            "minor_second": 1,
            "major_second": 2,
            "minor_third": 3,
            "major_third": 4,
            "perfect_fourth": 5,
            "augmented_fourth": 6,
            "diminished_fifth": 6,
            "perfect_fifth": 7,
            "minor_sixth": 8,
            "major_sixth": 9,
            "minor_seventh": 10,
            "major_seventh": 11,
            "octave": 12,
        }
        return interval_map.get(interval, 0)

    def _get_interval_display_name(self, interval: str) -> str:
        """
        Get the display name for an interval.

        Args:
            interval: The interval name

        Returns:
            str: Display name for the interval
        """
        display_names = {
            "unison": "Unison",
            "minor_second": "Minor Second",
            "major_second": "Major Second",
            "minor_third": "Minor Third",
            "major_third": "Major Third",
            "perfect_fourth": "Perfect Fourth",
            "augmented_fourth": "Augmented Fourth",
            "diminished_fifth": "Diminished Fifth",
            "perfect_fifth": "Perfect Fifth",
            "minor_sixth": "Minor Sixth",
            "major_sixth": "Major Sixth",
            "minor_seventh": "Minor Seventh",
            "major_seventh": "Major Seventh",
            "octave": "Octave",
        }
        return display_names.get(interval, interval.replace("_", " ").title())

    def _get_interval_notation(self, interval: str) -> str:
        """
        Get the interval notation for an interval.

        Args:
            interval: The interval name

        Returns:
            str: Interval notation (e.g., "3m", "3M", "4J", "5J", "8J")
        """
        notation_map = {
            "unison": "1J",
            "minor_second": "2m",
            "major_second": "2M",
            "minor_third": "3m",
            "major_third": "3M",
            "perfect_fourth": "4J",
            "augmented_fourth": "4+",
            "diminished_fifth": "5°",
            "perfect_fifth": "5J",
            "minor_sixth": "6m",
            "major_sixth": "6M",
            "minor_seventh": "7m",
            "major_seventh": "7M",
            "octave": "8J",
        }
        return notation_map.get(interval, interval.replace("_", " ").title())

    def validate_config(self, config: dict[str, Any]) -> dict[str, Any]:
        """
        Validate and set default configuration values.

        Args:
            config: Configuration dictionary

        Returns:
            dict: Validated configuration
        """
        validated = config.copy()

        # Set defaults
        validated.setdefault("question_number", 1)
        validated.setdefault("octave", 4)

        # Convert question_number to int if it's a string
        if "question_number" in validated:
            try:
                validated["question_number"] = int(validated["question_number"])
            except (ValueError, TypeError):
                validated["question_number"] = 1

        # Validate question number
        total_questions = self.metadata.config_options.get("total_questions", 20)
        if not (1 <= validated["question_number"] <= total_questions):
            validated["question_number"] = 1

        # Validate reference note
        available_notes = self.metadata.config_options.get(
            "reference_notes", ["C", "D", "E", "F", "G", "A", "B"]
        )
        if (
            "reference_note" in validated
            and validated["reference_note"] not in available_notes
        ):
            del validated["reference_note"]

        # Validate interval
        if "interval" in validated and validated["interval"] not in self.intervals:
            del validated["interval"]

        return validated
