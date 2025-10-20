"""
Direction and contour exercises for Chapter 1: Sound Awareness & Direction.
"""

import random
from typing import Any

from audio_app.synthesizer import AudioSynthesizer

from ..base.exercise import BaseExercise
from ..base.metadata import ExerciseData, ExerciseMetadata, ExerciseResult


class HighOrLowDirectionExercise(BaseExercise):
    """Exercise: High or Low? - Two tones, user selects if 2nd note is higher or lower."""

    metadata = ExerciseMetadata(
        id="high_or_low_direction",
        name="High or Low?",
        description="Listen to two tones and identify if the second note is higher or lower than the first.",
        difficulty=1,
        category="direction",
        tags=["pitch", "direction", "basic"],
        estimated_time=600,
        prerequisites=[],
        learning_objectives=[
            "Recognize pitch direction",
            "Build basic auditory discrimination",
        ],
        input_type="multiple_choice",
        answer_format="direction",
        requires_progression=False,
        requires_single_note=False,
        audio_duration=3,
        config_options={
            "octave_range": {"type": "int", "default": 2, "min": 1, "max": 3},
            "note_duration": {"type": "float", "default": 1.0, "min": 0.5, "max": 2.0},
            "direction_probabilities": {
                "type": "dict",
                "default": {"higher": 0.5, "lower": 0.5},
                "description": "Custom probabilities for direction (must sum to 1.0)",
            },
        },
    )

    def generate(self, **kwargs) -> ExerciseData:
        """Generate two tones with clear direction."""
        octave_range = kwargs.get("octave_range", 2)
        note_duration = kwargs.get("note_duration", 1.0)

        # Custom probabilities for direction
        direction_probabilities = kwargs.get(
            "direction_probabilities",
            {
                "higher": 0.5,  # 50% chance
                "lower": 0.5,  # 50% chance
            },
        )

        # Choose a base note and octave
        base_note = random.choice(["C", "D", "E", "F", "G", "A", "B"])
        base_octave = random.randint(4, 5)

        # Generate second note with weighted direction choice
        direction = self.weighted_choice(direction_probabilities)

        if direction == "higher":
            # Second note is higher
            second_octave = base_octave + random.randint(1, octave_range)
            second_note = random.choice(["C", "D", "E", "F", "G", "A", "B"])
        else:
            # Second note is lower
            second_octave = base_octave - random.randint(1, octave_range)
            second_note = random.choice(["C", "D", "E", "F", "G", "A", "B"])

        # Create audio sequence
        first_note = f"{base_note}-{base_octave}"
        second_note_full = f"{second_note}-{second_octave}"

        # Generate audio using AudioSynthesizer
        audio_synthesizer = AudioSynthesizer()

        # Generate melodic interval audio (two notes played one after the other)
        audio_path = audio_synthesizer.synthesize_melodic_interval(
            first_note,
            second_note_full,
            note_duration=note_duration,
            gap_duration=0.5,
        )
        target_audio_url = audio_synthesizer.get_audio_url(audio_path)

        # Create options
        options = ["Higher", "Lower"]
        correct_answer = direction.title()

        context = {
            "first_note": first_note,
            "second_note": second_note_full,
            "direction": direction,
            "audio_sequence": [first_note, second_note_full],
            "note_duration": note_duration,
        }

        return ExerciseData(
            key=f"Direction: {first_note} → {second_note_full}",
            scale=[],
            progression_audio=None,
            target_audio=target_audio_url,
            options=options,
            correct_answer=correct_answer,
            context=context,
        )

    def check_answer(self, answer: Any, context: dict[str, Any]) -> ExerciseResult:
        """Check if the direction answer is correct."""
        correct_direction = context.get("direction", "").title()
        is_correct = str(answer).title() == correct_direction

        feedback = self.get_feedback(is_correct, answer, correct_direction)

        return ExerciseResult(
            is_correct=is_correct,
            user_answer=str(answer),
            correct_answer=correct_direction,
            feedback=feedback,
            hints_used=[],
        )


class StepVsLeapExercise(BaseExercise):
    """Exercise: Step vs. Leap Challenge - Identify if interval is a step or leap."""

    metadata = ExerciseMetadata(
        id="step_vs_leap",
        name="Step vs. Leap Challenge",
        description="Listen to two notes and identify if the interval is a step (2nd) or leap (3rd or larger).",
        difficulty=1,
        category="direction",
        tags=["intervals", "steps", "leaps", "basic"],
        estimated_time=600,
        prerequisites=[],
        learning_objectives=[
            "Distinguish steps from leaps",
            "Recognize interval size qualitatively",
        ],
        input_type="multiple_choice",
        answer_format="interval_type",
        requires_progression=False,
        requires_single_note=False,
        audio_duration=3,
        config_options={
            "step_intervals": {"type": "list", "default": ["2m", "2M"]},
            "leap_intervals": {
                "type": "list",
                "default": ["3m", "3M", "4J", "5J", "6m", "6M", "7m", "7M", "8J"],
            },
            "interval_type_probabilities": {
                "type": "dict",
                "default": {"step": 0.5, "leap": 0.5},
                "description": "Custom probabilities for step vs leap (must sum to 1.0)",
            },
        },
    )

    def generate(self, **kwargs) -> ExerciseData:
        """Generate step or leap interval."""
        step_intervals = kwargs.get("step_intervals", ["2m", "2M"])
        leap_intervals = kwargs.get(
            "leap_intervals", ["3m", "3M", "4J", "5J", "6m", "6M", "7m", "7M", "8J"]
        )

        # Custom probabilities for interval type
        interval_type_probabilities = kwargs.get(
            "interval_type_probabilities",
            {
                "step": 0.5,  # 50% chance
                "leap": 0.5,  # 50% chance
            },
        )

        # Choose whether to generate step or leap with weighted choice
        interval_type = self.weighted_choice(interval_type_probabilities)

        if interval_type == "step":
            interval = random.choice(step_intervals)
        else:
            interval = random.choice(leap_intervals)

        # Generate notes for the interval
        base_note = random.choice(["C", "D", "E", "F", "G", "A", "B"])
        base_octave = random.randint(4, 5)

        # Calculate second note based on interval
        second_note, second_octave = self._calculate_second_note(
            base_note, base_octave, interval
        )

        first_note = f"{base_note}-{base_octave}"
        second_note_full = f"{second_note}-{second_octave}"

        # Generate audio using AudioSynthesizer
        audio_synthesizer = AudioSynthesizer()

        # Generate melodic interval audio (two notes played one after the other)
        audio_path = audio_synthesizer.synthesize_melodic_interval(
            first_note,
            second_note_full,
            note_duration=1.0,
            gap_duration=0.5,
        )
        target_audio_url = audio_synthesizer.get_audio_url(audio_path)

        options = ["Step", "Leap"]
        correct_answer = interval_type.title()

        context = {
            "first_note": first_note,
            "second_note": second_note_full,
            "interval": interval,
            "interval_type": interval_type,
            "audio_sequence": [first_note, second_note_full],
        }

        return ExerciseData(
            key=f"Interval: {first_note} → {second_note_full}",
            scale=[],
            progression_audio=None,
            target_audio=target_audio_url,
            options=options,
            correct_answer=correct_answer,
            context=context,
        )

    def check_answer(self, answer: Any, context: dict[str, Any]) -> ExerciseResult:
        """Check if the step/leap answer is correct."""
        correct_type = context.get("interval_type", "").title()
        is_correct = str(answer).title() == correct_type

        feedback = self.get_feedback(is_correct, answer, correct_type)

        return ExerciseResult(
            is_correct=is_correct,
            user_answer=str(answer),
            correct_answer=correct_type,
            feedback=feedback,
            hints_used=[],
        )

    def _calculate_second_note(
        self, base_note: str, base_octave: int, interval: str
    ) -> tuple[str, int]:
        """Calculate the second note based on interval."""
        note_order = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

        # Get base note index
        base_index = note_order.index(base_note)

        # Map intervals to semitones
        interval_semitones = {
            "2m": 1,
            "2M": 2,
            "3m": 3,
            "3M": 4,
            "4J": 5,
            "5J": 7,
            "6m": 8,
            "6M": 9,
            "7m": 10,
            "7M": 11,
            "8J": 12,
        }

        semitones = interval_semitones.get(interval, 2)
        second_index = (base_index + semitones) % 12
        second_octave = base_octave + (base_index + semitones) // 12

        return note_order[second_index], second_octave


class MelodicShapesExercise(BaseExercise):
    """Exercise: Melodic Shapes - Identify melodic contour patterns."""

    metadata = ExerciseMetadata(
        id="melodic_shapes",
        name="Melodic Shapes",
        description="Listen to a short melodic phrase and identify its shape (arch, zigzag, ascending, descending).",
        difficulty=2,
        category="direction",
        tags=["melody", "contour", "patterns"],
        estimated_time=900,
        prerequisites=["high_or_low_direction"],
        learning_objectives=["Recognize melodic patterns", "Build pattern recognition"],
        input_type="multiple_choice",
        answer_format="shape",
        requires_progression=False,
        requires_single_note=False,
        audio_duration=5,
        config_options={
            "phrase_length": {"type": "int", "default": 4, "min": 3, "max": 6},
            "shapes": {
                "type": "list",
                "default": ["arch", "zigzag", "ascending", "descending"],
            },
            "shape_probabilities": {
                "type": "dict",
                "default": {
                    "arch": 0.25,
                    "zigzag": 0.25,
                    "ascending": 0.25,
                    "descending": 0.25,
                },
                "description": "Custom probabilities for melodic shapes (must sum to 1.0)",
            },
        },
    )

    def generate(self, **kwargs) -> ExerciseData:
        """Generate melodic phrase with specific shape."""
        phrase_length = kwargs.get("phrase_length", 4)

        # Custom probabilities for shapes
        shape_probabilities = kwargs.get(
            "shape_probabilities",
            {
                "arch": 0.25,  # 25% chance
                "zigzag": 0.25,  # 25% chance
                "ascending": 0.25,  # 25% chance
                "descending": 0.25,  # 25% chance
            },
        )

        # Choose shape with weighted choice
        shape = self.weighted_choice(shape_probabilities)

        # Generate notes based on shape
        base_note = random.choice(["C", "D", "E", "F", "G", "A", "B"])
        base_octave = random.randint(4, 5)

        notes = self._generate_shape_notes(base_note, base_octave, shape, phrase_length)

        # Generate audio using AudioSynthesizer
        audio_synthesizer = AudioSynthesizer()

        # Generate melodic sequence audio (multiple notes played one after the other)
        note_strings = [f"{note}-{octave}" for note, octave in notes]
        audio_path = audio_synthesizer.synthesize_notes(note_strings, duration=0.8)
        target_audio_url = audio_synthesizer.get_audio_url(audio_path)

        options = ["Arch", "Zigzag", "Ascending", "Descending"]
        correct_answer = shape.title()

        context = {
            "shape": shape,
            "notes": notes,
            "audio_sequence": note_strings,
            "phrase_length": phrase_length,
        }

        return ExerciseData(
            key=f"Shape: {shape.title()}",
            scale=[],
            progression_audio=None,
            target_audio=target_audio_url,
            options=options,
            correct_answer=correct_answer,
            context=context,
        )

    def check_answer(self, answer: Any, context: dict[str, Any]) -> ExerciseResult:
        """Check if the shape answer is correct."""
        correct_shape = context.get("shape", "").title()
        is_correct = str(answer).title() == correct_shape

        feedback = self.get_feedback(is_correct, answer, correct_shape)

        return ExerciseResult(
            is_correct=is_correct,
            user_answer=str(answer),
            correct_answer=correct_shape,
            feedback=feedback,
            hints_used=[],
        )

    def _generate_shape_notes(
        self, base_note: str, base_octave: int, shape: str, length: int
    ) -> list[tuple[str, int]]:
        """Generate notes that form the specified melodic shape."""
        note_order = ["C", "D", "E", "F", "G", "A", "B"]
        base_index = note_order.index(base_note)

        notes = []

        if shape == "ascending":
            for i in range(length):
                note_index = (base_index + i) % 7
                octave = base_octave + (base_index + i) // 7
                notes.append((note_order[note_index], octave))

        elif shape == "descending":
            for i in range(length):
                note_index = (base_index - i) % 7
                octave = base_octave - (base_index - i) // 7
                notes.append((note_order[note_index], octave))

        elif shape == "arch":
            # Go up then down
            for i in range(length // 2 + 1):
                note_index = (base_index + i) % 7
                octave = base_octave + (base_index + i) // 7
                notes.append((note_order[note_index], octave))
            for i in range(1, length - length // 2):
                note_index = (base_index + length // 2 - i) % 7
                octave = base_octave + (base_index + length // 2 - i) // 7
                notes.append((note_order[note_index], octave))

        elif shape == "zigzag":
            # Alternate up and down
            for i in range(length):
                if i % 2 == 0:
                    note_index = (base_index + i // 2) % 7
                    octave = base_octave + (base_index + i // 2) // 7
                else:
                    note_index = (base_index - i // 2) % 7
                    octave = base_octave - (base_index - i // 2) // 7
                notes.append((note_order[note_index], octave))

        return notes[:length]
