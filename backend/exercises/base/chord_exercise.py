"""
Base class for chord recognition exercises.

This provides common functionality for all chord recognition exercises,
including different chord types, inversions, and audio generation.
"""

import random
from typing import Any

from audio_app.synthesizer import AudioSynthesizer
from music_app.chords import get_chord_display_name, get_chord_notes_with_octaves

from .exercise import BaseExercise
from .metadata import ExerciseData, ExerciseMetadata, ExerciseResult


class BaseChordExercise(BaseExercise):
    """
    Base class for chord recognition exercises.

    Provides common functionality for generating chord exercises with
    different chord types, inversions, and audio generation.
    """

    def __init__(
        self, chord_types: list[str], exercise_type: str, description: str | None = None
    ):
        """
        Initialize the chord exercise.

        Args:
            chord_types: List of chord type names (e.g., ["major", "minor", "diminished", "augmented"])
            exercise_type: Type of exercise (e.g., "triad_types", "suspended_chords")
            description: Custom description for the exercise
        """
        self.chord_types = chord_types
        self.exercise_type = exercise_type
        self.description = description or f"Identify {', '.join(chord_types)} chords"

        # Set up metadata
        self.metadata = self._create_metadata()

    def _create_metadata(self) -> ExerciseMetadata:
        """Create metadata based on the exercise configuration."""
        chord_names = [
            self._get_chord_display_name(chord_type) for chord_type in self.chord_types
        ]
        chord_list = ", ".join(chord_names[:-1]) + f" and {chord_names[-1]}"

        return ExerciseMetadata(
            id=self.exercise_type,
            name=f"{chord_list.title()} Recognition",
            description=self.description,
            difficulty=3,
            category="chords",
            tags=["chords"]
            + [chord_type.replace("_", "") for chord_type in self.chord_types],
            estimated_time=900,
            prerequisites=["major_vs_minor_chords"],
            learning_objectives=[
                f"Recognize {chord_name} chords" for chord_name in chord_names
            ]
            + ["Develop chord recognition skills"],
            input_type="multiple_choice",
            answer_format="chord_type",
            requires_progression=False,
            requires_single_note=False,
            audio_duration=4,
            config_options={
                "available_chord_types": self.chord_types,
                "root_notes": ["C", "D", "E", "F", "G", "A", "B"],
                "octave": 4,
                "chord_probabilities": {
                    "type": "dict",
                    "default": {
                        chord_type: 1.0 / len(self.chord_types)
                        for chord_type in self.chord_types
                    },
                    "description": "Custom probabilities for chord type selection (must sum to 1.0)",
                },
            },
        )

    def _get_chord_display_name(self, chord_type: str) -> str:
        """Get display name for chord type."""
        return get_chord_display_name(chord_type)

    def generate(self, **kwargs) -> ExerciseData:
        """
        Generate a chord recognition exercise.

        Args:
            **kwargs: Configuration options
                - root_note: Specific root note to use (optional)
                - chord_type: Specific chord type to use (optional)
                - octave: Octave for the chord (default: 4)

        Returns:
            ExerciseData: Complete exercise data
        """
        # Get configuration
        config = self.validate_config(kwargs)

        # Select root note randomly
        available_notes = self.metadata.config_options.get(
            "root_notes", ["C", "D", "E", "F", "G", "A", "B"]
        )
        root_note = config.get("root_note", random.choice(available_notes))
        octave = config.get("octave", 4)

        # Custom probabilities for chord type selection
        chord_probabilities = config.get(
            "chord_probabilities",
            {
                chord_type: 1.0 / len(self.chord_types)
                for chord_type in self.chord_types
            },
        )

        # Select chord type with weighted choice
        chord_type = config.get("chord_type", self.weighted_choice(chord_probabilities))

        # Generate chord notes based on type using centralized chord functions
        chord_notes = get_chord_notes_with_octaves(root_note, chord_type, octave)

        # Generate audio using AudioSynthesizer
        audio_synthesizer = AudioSynthesizer()
        audio_path = audio_synthesizer.synthesize_chord(chord_notes, duration=2.0)
        target_audio_url = audio_synthesizer.get_audio_url(audio_path)

        # Create options and correct answer
        options = [self._get_chord_display_name(ct) for ct in self.chord_types]
        correct_answer = self._get_chord_display_name(chord_type)

        context = {
            "root_note": root_note,
            "octave": octave,
            "chord_type": chord_type,
            "chord_notes": chord_notes,
        }

        return ExerciseData(
            key=f"{root_note} {correct_answer}",
            scale=[],
            progression_audio=None,
            target_audio=target_audio_url,
            options=options,
            correct_answer=correct_answer,
            context=context,
        )

    def check_answer(self, answer: Any, context: dict[str, Any]) -> ExerciseResult:
        """
        Check the user's answer against the correct chord type.

        Args:
            answer: User's answer
            context: Exercise context from generate()

        Returns:
            ExerciseResult: Result with feedback
        """
        correct_chord_type = context.get("chord_type", "")
        correct_answer = self._get_chord_display_name(correct_chord_type)
        is_correct = str(answer) == correct_answer

        feedback = self.get_feedback(is_correct, answer, correct_answer)
        if is_correct:
            feedback = f"Correct! This is a {correct_answer} chord."
        else:
            feedback = f"Incorrect. This is a {correct_answer} chord."

        return ExerciseResult(
            is_correct=is_correct,
            user_answer=str(answer),
            correct_answer=correct_answer,
            feedback=feedback,
            hints_used=[],
        )

    def validate_config(self, config: dict[str, Any]) -> dict[str, Any]:
        """
        Validate and normalize configuration options.

        Args:
            config: Raw configuration dictionary

        Returns:
            Dict[str, Any]: Validated configuration
        """
        validated = {}

        # Common validations
        if "root_note" in config:
            validated["root_note"] = str(config["root_note"])

        if "octave" in config:
            octave = int(config["octave"])
            if 1 <= octave <= 7:
                validated["octave"] = octave

        if "chord_type" in config and config["chord_type"] in self.chord_types:
            validated["chord_type"] = config["chord_type"]

        if "chord_probabilities" in config:
            probabilities = config["chord_probabilities"]
            if isinstance(probabilities, dict):
                # Validate that all chord types are present and probabilities sum to 1.0
                total = sum(probabilities.values())
                if abs(total - 1.0) < 0.001:  # Allow small floating point errors
                    validated["chord_probabilities"] = probabilities

        return validated
