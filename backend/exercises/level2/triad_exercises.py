"""
Triad and chord quality exercises for Chapter 4: Triads and Chord Qualities.

This module contains chord recognition exercises that inherit from BaseChordExercise,
providing a clean, reusable interface for chord-based exercises.
"""

import random
from typing import Any

from music_app.chords import get_fifth_quality_chord

from ..base.chord_exercise import BaseChordExercise
from ..base.exercise import BaseExercise
from ..base.metadata import ExerciseData, ExerciseMetadata, ExerciseResult


# Chord exercises using BaseChordExercise
class MajorMinorTriadExercise(BaseChordExercise):
    """Exercise: Major vs Minor Triads using BaseChordExercise."""

    def __init__(self):
        super().__init__(
            chord_types=["major", "minor"],
            exercise_type="major_minor_triads",
            description="Listen to a triad and identify if it sounds happy (major) or sad (minor).",
        )


class AllTriadTypesExercise(BaseChordExercise):
    """Exercise: All Triad Types using BaseChordExercise."""

    def __init__(self):
        super().__init__(
            chord_types=["major", "minor", "diminished", "augmented"],
            exercise_type="all_triad_types",
            description="Listen to a triad and identify its quality: major, minor, diminished, or augmented.",
        )


class SuspendedChordsExercise(BaseChordExercise):
    """Exercise: Suspended Chords using BaseChordExercise."""

    def __init__(self):
        super().__init__(
            chord_types=["sus2", "sus4", "3m", "3M"],
            exercise_type="suspended_chords",
            description="Listen to a chord and identify its type: suspended 2nd, suspended 4th, minor third, or major third.",
        )

    def _get_chord_display_name(self, chord_type: str) -> str:
        """Override to use the specific notation for suspended chords."""
        display_names = {"sus2": "sus2", "sus4": "sus4", "3m": "3m", "3M": "3M"}
        return display_names.get(chord_type, chord_type)


# Specialized exercises that need custom logic
class FifthQualityExercise(BaseExercise):
    """Exercise: Fifth Quality - Identify 5dim vs 5J vs 5aug (major third fixed)."""

    metadata = ExerciseMetadata(
        id="triad_fifth_quality",
        name="Fifth Quality (5dim / 5J / 5aug)",
        description="Listen to a major triad (major third fixed) and identify the fifth quality: diminished (5dim), perfect (5J), or augmented (5aug).",
        difficulty=3,
        category="chords",
        tags=["triads", "fifth", "diminished", "augmented", "perfect"],
        estimated_time=900,
        prerequisites=["major_minor_triads"],
        learning_objectives=["Differentiate fifth qualities with a fixed major third"],
        input_type="multiple_choice",
        answer_format="fifth_quality",
        requires_progression=False,
        requires_single_note=False,
        audio_duration=4,
        config_options={
            "root_notes": {
                "type": "list",
                "default": ["C", "D", "E", "F", "G", "A", "B"],
            },
            "octave": {"type": "int", "default": 4, "min": 3, "max": 5},
            "fifth_probabilities": {
                "type": "dict",
                "default": {"5dim": 0.333, "5J": 0.333, "5aug": 0.333},
                "description": "Custom probabilities for fifth quality selection (must sum to 1.0)",
            },
        },
    )

    def generate(self, **kwargs) -> ExerciseData:
        """Generate a major triad with varying fifth quality (5dim, 5J, 5aug)."""
        root_notes = kwargs.get("root_notes", ["C", "D", "E", "F", "G", "A", "B"])
        octave = kwargs.get("octave", 4)

        # Custom probabilities for fifth quality selection
        fifth_probabilities = kwargs.get(
            "fifth_probabilities", {"5dim": 0.333, "5J": 0.333, "5aug": 0.333}
        )

        # Choose root note and fifth quality. Third is always major (+4 semitones)
        root = random.choice(root_notes)
        fifth_quality = self.weighted_choice(fifth_probabilities)

        # Generate triad notes using centralized chord function
        triad_notes = get_fifth_quality_chord(root, fifth_quality, octave)

        options = ["5dim", "5J", "5aug"]
        correct_answer = fifth_quality

        # Generate audio using AudioSynthesizer
        from audio_app.synthesizer import AudioSynthesizer

        audio_synthesizer = AudioSynthesizer()

        # Generate chord audio (three notes played simultaneously)
        audio_path = audio_synthesizer.synthesize_chord(triad_notes, duration=2.0)
        target_audio_url = audio_synthesizer.get_audio_url(audio_path)

        context = {
            "root": root,
            "octave": octave,
            "third_quality": "major",
            "fifth_quality": fifth_quality,
            "triad_notes": triad_notes,
        }

        return ExerciseData(
            key=f"{root} Major Triad ({fifth_quality})",
            scale=[],
            progression_audio=None,
            target_audio=target_audio_url,
            options=options,
            correct_answer=correct_answer,
            context=context,
        )

    def check_answer(self, answer: Any, context: dict[str, Any]) -> ExerciseResult:
        """Check if the fifth quality answer is correct (5dim/5J/5aug)."""
        correct_fifth = context.get("fifth_quality", "")
        is_correct = str(answer) == correct_fifth

        feedback = self.get_feedback(is_correct, answer, correct_fifth)
        if is_correct:
            desc = {
                "5dim": "Correct! Diminished fifth adds strong tension.",
                "5J": "Correct! Perfect fifth sounds stable and consonant.",
                "5aug": "Correct! Augmented fifth adds bright tension.",
            }.get(correct_fifth, "Correct!")
            feedback = desc
        else:
            feedback = f"Incorrect. The fifth quality is {correct_fifth}."

        return ExerciseResult(
            is_correct=is_correct,
            user_answer=str(answer),
            correct_answer=correct_fifth,
            feedback=feedback,
            hints_used=[],
        )


# Backward compatibility aliases
MajorVsMinorChordsExercise = MajorMinorTriadExercise
SuspendedChordExercise = SuspendedChordsExercise
