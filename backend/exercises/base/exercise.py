"""
Base exercise class for the ear trainer.
"""

import random
from abc import ABC, abstractmethod
from typing import Any

from .metadata import ExerciseData, ExerciseMetadata, ExerciseResult


class BaseExercise(ABC):
    """
    Abstract base class for all ear training exercises.

    Each exercise must implement the core methods and define its metadata.
    The framework handles exercise discovery, registration, and API integration.
    """

    # Each exercise must define its metadata
    metadata: ExerciseMetadata

    def __init__(self):
        """Initialize the exercise."""
        if not hasattr(self, "metadata"):
            raise NotImplementedError(
                f"Exercise {self.__class__.__name__} must define metadata"
            )

    @abstractmethod
    def generate(self, **kwargs) -> ExerciseData:
        """
        Generate exercise data including audio and answer options.

        Args:
            **kwargs: Exercise-specific parameters (e.g., key, difficulty)

        Returns:
            ExerciseData: Complete exercise data for the frontend
        """
        pass

    @abstractmethod
    def check_answer(self, answer: Any, context: dict[str, Any]) -> ExerciseResult:
        """
        Validate user answer and provide feedback.

        Args:
            answer: User's answer
            context: Exercise context from generate()

        Returns:
            ExerciseResult: Validation result with feedback
        """
        pass

    def get_instructions(self) -> str:
        """
        Get exercise instructions for the user.

        Returns:
            str: Human-readable instructions
        """
        return self.metadata.description

    def get_hints(self) -> list[str]:
        """
        Get hints for the exercise.

        Returns:
            List[str]: List of hints (can be empty)
        """
        return []

    def get_feedback(self, is_correct: bool, answer: Any, correct_answer: Any) -> str:
        """
        Generate feedback message for the user.

        Args:
            is_correct: Whether the answer was correct
            answer: User's answer
            correct_answer: The correct answer

        Returns:
            str: Feedback message
        """
        if is_correct:
            return "Correct! Well done!"
        else:
            return f"Incorrect. The correct answer was {correct_answer}. Try again!"

    def get_random_key(self) -> str:
        """
        Get a random major key for the exercise.

        Returns:
            str: Random major key (e.g., "C", "G", "F")
        """
        major_keys = [
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
        return random.choice(major_keys)

    def get_random_minor_key(self) -> str:
        """
        Get a random minor key for the exercise.

        Returns:
            str: Random minor key (e.g., "Am", "Em", "Bm")
        """
        minor_keys = [
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
        return random.choice(minor_keys)

    def get_scale_degrees(self) -> list[int]:
        """
        Get list of scale degrees (1-7).

        Returns:
            List[int]: Scale degrees [1, 2, 3, 4, 5, 6, 7]
        """
        return [1, 2, 3, 4, 5, 6, 7]

    def get_note_names(self) -> list[str]:
        """
        Get list of note names.

        Returns:
            List[str]: Note names ["C", "D", "E", "F", "G", "A", "B"]
        """
        return ["C", "D", "E", "F", "G", "A", "B"]

    def get_chord_qualities(self) -> list[str]:
        """
        Get list of basic chord qualities.

        Returns:
            List[str]: Chord qualities ["major", "minor", "diminished", "augmented"]
        """
        return ["major", "minor", "diminished", "augmented"]

    def get_intervals(self) -> list[str]:
        """
        Get list of common intervals.

        Returns:
            List[str]: Interval names
        """
        return [
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

    def validate_config(self, config: dict[str, Any]) -> dict[str, Any]:
        """
        Validate and sanitize exercise configuration.

        Args:
            config: Raw configuration from request

        Returns:
            Dict[str, Any]: Validated configuration
        """
        # Default validation - exercises can override for specific validation
        validated = {}

        # Common validations
        if "key" in config:
            validated["key"] = str(config["key"])

        if "difficulty" in config:
            difficulty = int(config["difficulty"])
            if 1 <= difficulty <= 10:
                validated["difficulty"] = difficulty

        return validated

    @staticmethod
    def weighted_choice(weights: dict[str, float]) -> str:
        """
        Choose an item based on weighted probabilities.

        This utility method can be used by any exercise to implement custom
        probability distributions for answer choices, chord types, intervals, etc.

        Args:
            weights: Dictionary mapping choices to their probabilities

        Returns:
            str: Selected choice based on weighted probabilities

        Examples:
            # Equal probabilities (25% each)
            chord_type = self.weighted_choice({"major": 0.25, "minor": 0.25, "dim": 0.25, "aug": 0.25})

            # Custom probabilities (favor major/minor)
            chord_type = self.weighted_choice({"major": 0.4, "minor": 0.4, "dim": 0.1, "aug": 0.1})

            # Direction probabilities (favor higher)
            direction = self.weighted_choice({"higher": 0.7, "lower": 0.3})

        Usage in exercise generate() method:
            # 1. Add config option to metadata
            config_options={
                "choice_probabilities": {
                    "type": "dict",
                    "default": {"A": 0.5, "B": 0.5},
                    "description": "Custom probabilities for choices"
                }
            }

            # 2. Use in generate() method
            probabilities = kwargs.get("choice_probabilities", {"A": 0.5, "B": 0.5})
            choice = self.weighted_choice(probabilities)
        """
        # Normalize weights to ensure they sum to 1.0
        total_weight = sum(weights.values())
        if total_weight == 0:
            # If all weights are 0, return equal probability
            return random.choice(list(weights.keys()))

        normalized_weights = {k: v / total_weight for k, v in weights.items()}

        # Generate random number and select based on cumulative probability
        rand = random.random()
        cumulative = 0.0

        for choice, weight in normalized_weights.items():
            cumulative += weight
            if rand <= cumulative:
                return choice

        # Fallback (should never reach here)
        return list(weights.keys())[0]
