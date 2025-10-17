"""
Exercise: Interval Recognition

This exercise plays two notes with staggered timing (root note starts first,
then second note begins 400ms later) and asks the student to identify the interval:
octave (8ve), minor third (m3), or major third (M3).
The exercise consists of 20 questions with random intervals and root notes.
"""

import random
from typing import Any

from music_app.notes import transpose_note

from exercises.base.exercise import BaseExercise
from exercises.base.metadata import ExerciseData, ExerciseMetadata, ExerciseResult


class IntervalRecognitionExercise(BaseExercise):
    """
    Exercise for recognizing basic intervals.

    The exercise:
    1. Plays a reference note
    2. Plays an interval (two notes simultaneously)
    3. Student identifies the interval type
    """

    metadata = ExerciseMetadata(
        id="interval_recognition",
        name="Interval Recognition",
        description="Identify the interval: octave, minor third, or major third. 20 questions with melodic intervals.",
        difficulty=1,
        prerequisites=[],
        learning_objectives=[
            "Recognize octave intervals",
            "Distinguish between minor and major thirds",
            "Develop melodic interval recognition skills",
        ],
        estimated_time=300,  # 5 minutes for 20 questions
        category="interval_recognition",
        tags=["intervals", "octave", "thirds", "melodic"],
        input_type="multiple_choice",
        answer_format="interval_name",
        requires_progression=False,
        requires_single_note=False,
        audio_duration=3,  # Longer for two notes
        config_options={
            "available_intervals": ["octave", "minor_third", "major_third"],
            "reference_notes": ["C", "D", "E", "F", "G", "A", "B"],
            "octave": 4,
            "total_questions": 20,
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

        # Select interval randomly
        available_intervals = self.metadata.config_options.get(
            "available_intervals", ["octave", "minor_third", "major_third"]
        )
        interval = config.get("interval", random.choice(available_intervals))

        # Calculate the second note based on the interval
        second_note = self._get_interval_note(reference_note_with_octave, interval)

        # Generate audio files using the audio synthesizer
        from audio_app.synthesizer import AudioSynthesizer

        synthesizer = AudioSynthesizer()

        # Generate harmonic interval audio with staggered timing
        # Root note starts 400ms before the second note, both last 1.5 seconds
        interval_audio_path = synthesizer.synthesize_staggered_interval(
            reference_note_with_octave,
            second_note,
            root_duration=1.5,
            second_duration=1.5,
            delay_ms=400,
        )
        interval_audio = synthesizer.get_audio_url(interval_audio_path)

        # Get current question number
        question_number = config.get("question_number", 1)
        total_questions = self.metadata.config_options.get("total_questions", 20)

        # Create exercise data
        exercise_data = ExerciseData(
            key=f"Question {question_number}/{total_questions}",  # Context key
            scale=[],  # Not needed for interval exercise
            progression_audio=None,  # Not needed
            target_audio=interval_audio,
            options=["octave", "minor_third", "major_third"],
            correct_answer=interval,
            context={
                "reference_note": reference_note_with_octave,
                "second_note": second_note,
                "interval": interval,
                "interval_semitones": self._get_interval_semitones(interval),
                "question_number": question_number,
                "total_questions": total_questions,
            },
        )

        return exercise_data

    def check_answer(self, answer: Any, context: dict[str, Any]) -> ExerciseResult:
        """
        Check if the user's answer is correct.

        Args:
            answer: User's answer (interval name)
            context: Exercise context from generate()

        Returns:
            ExerciseResult: Validation result with feedback
        """
        correct_answer = context.get("interval")
        reference_note = context.get("reference_note")
        second_note = context.get("second_note")
        interval_semitones = context.get("interval_semitones")

        # Check if answer is correct
        is_correct = answer == correct_answer

        # Generate feedback
        if is_correct:
            feedback = f"Correct! The interval from {reference_note} to {second_note} is a {self._get_interval_display_name(correct_answer)}."
        else:
            feedback = f"Incorrect. The interval from {reference_note} to {second_note} is a {self._get_interval_display_name(correct_answer)} ({interval_semitones} semitones)."

        return ExerciseResult(
            is_correct=is_correct,
            user_answer=answer,
            correct_answer=correct_answer,
            feedback=feedback,
        )

    def get_instructions(self) -> str:
        """Get exercise instructions."""
        return (
            "Listen to the two notes played with staggered timing. "
            "The root note starts first, then the second note begins 400ms later. "
            "Identify whether the interval is an octave, minor third, or major third. "
            "An octave spans 12 semitones, a minor third spans 3 semitones, and a major third spans 4 semitones. "
            "You will have 20 questions total. Click your answer to move to the next question."
        )

    def get_hints(self) -> list[str]:
        """Get hints for the exercise."""
        return [
            "An octave sounds very consonant and 'complete' - like the same note at different pitches",
            "A minor third sounds sadder and more dissonant than a major third",
            "A major third sounds brighter and more consonant than a minor third",
            "Count the semitones: octave = 12, minor third = 3, major third = 4",
        ]

    def _get_interval_note(self, reference_note: str, interval: str) -> str:
        """
        Get the second note of an interval from a reference note.

        Args:
            reference_note: Reference note (e.g., "C-4")
            interval: Interval type ("octave", "minor_third", "major_third")

        Returns:
            str: Second note of the interval
        """
        semitones = self._get_interval_semitones(interval)
        return transpose_note(reference_note, semitones)

    def _get_interval_semitones(self, interval: str) -> int:
        """
        Get the number of semitones for an interval.

        Args:
            interval: Interval type

        Returns:
            int: Number of semitones
        """
        interval_semitones = {
            # Perfect intervals
            "unison": 0,
            "perfect_fourth": 5,
            "perfect_fifth": 7,
            "octave": 12,
            # Minor intervals
            "minor_second": 1,
            "minor_third": 3,
            "minor_sixth": 8,
            "minor_seventh": 10,
            # Major intervals
            "major_second": 2,
            "major_third": 4,
            "major_sixth": 9,
            "major_seventh": 11,
            # Augmented intervals
            "augmented_fourth": 6,  # Tritone
            "augmented_fifth": 8,
            # Diminished intervals
            "diminished_fifth": 6,  # Tritone (same as augmented fourth)
            "diminished_seventh": 9,
        }
        return interval_semitones.get(interval, 0)

    def _get_interval_display_name(self, interval: str) -> str:
        """
        Get the display name for an interval.

        Args:
            interval: Interval type

        Returns:
            str: Display name
        """
        display_names = {
            # Perfect intervals
            "unison": "perfect unison",
            "perfect_fourth": "perfect fourth",
            "perfect_fifth": "perfect fifth",
            "octave": "perfect octave",
            # Minor intervals
            "minor_second": "minor second",
            "minor_third": "minor third",
            "minor_sixth": "minor sixth",
            "minor_seventh": "minor seventh",
            # Major intervals
            "major_second": "major second",
            "major_third": "major third",
            "major_sixth": "major sixth",
            "major_seventh": "major seventh",
            # Augmented intervals
            "augmented_fourth": "augmented fourth (tritone)",
            "augmented_fifth": "augmented fifth",
            # Diminished intervals
            "diminished_fifth": "diminished fifth (tritone)",
            "diminished_seventh": "diminished seventh",
        }
        return display_names.get(interval, interval.replace("_", " "))

    def validate_config(self, config: dict[str, Any]) -> dict[str, Any]:
        """Validate exercise configuration."""
        validated = super().validate_config(config)

        # Validate reference note
        if "reference_note" in config:
            note = str(config["reference_note"]).upper()
            available_notes = self.metadata.config_options.get("reference_notes", [])
            if available_notes and note not in available_notes:
                validated["reference_note"] = random.choice(available_notes)
            else:
                validated["reference_note"] = note

        # Validate interval
        if "interval" in config:
            interval = str(config["interval"])
            available_intervals = self.metadata.config_options.get(
                "available_intervals", []
            )
            if interval in available_intervals:
                validated["interval"] = interval

        # Validate octave
        if "octave" in config:
            octave = int(config["octave"])
            if 1 <= octave <= 8:
                validated["octave"] = octave

        return validated
