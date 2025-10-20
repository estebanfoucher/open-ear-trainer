"""
Tonal center and scale sense exercises for Chapter 2: Establishing Tonal Center (Do) and Scale Sense.
"""

import random
from typing import Any

from audio_app.synthesizer import AudioSynthesizer

from ..base.exercise import BaseExercise
from ..base.metadata import ExerciseData, ExerciseMetadata, ExerciseResult


class FindHomeNoteExercise(BaseExercise):
    """Exercise: Find Home Note - Identify the tonic in a melody."""

    metadata = ExerciseMetadata(
        id="find_home_note",
        name="Find Home Note",
        description="Listen to a melody and identify which note feels like 'home' (the tonic).",
        difficulty=2,
        category="tonal_center",
        tags=["tonic", "home", "resolution"],
        estimated_time=900,
        prerequisites=["melodic_shapes"],
        learning_objectives=["Recognize tonic stability", "Identify resolution"],
        input_type="multiple_choice",
        answer_format="note",
        requires_progression=False,
        requires_single_note=False,
        audio_duration=8,
        config_options={
            "melody_length": {"type": "int", "default": 6, "min": 4, "max": 8},
            "key": {
                "type": "str",
                "default": "random",
                "options": ["C", "G", "D", "A", "F", "Bb", "Eb", "random"],
            },
            "key_probabilities": {
                "type": "dict",
                "default": {
                    "C": 0.143,
                    "G": 0.143,
                    "D": 0.143,
                    "A": 0.143,
                    "F": 0.143,
                    "Bb": 0.143,
                    "Eb": 0.143,
                },
                "description": "Custom probabilities for key selection (must sum to 1.0)",
            },
        },
    )

    def generate(self, **kwargs) -> ExerciseData:
        """Generate a melody that ends on the tonic."""
        melody_length = kwargs.get("melody_length", 6)
        key = kwargs.get("key", "random")

        if key == "random":
            # Custom probabilities for key selection
            key_probabilities = kwargs.get(
                "key_probabilities",
                {
                    "C": 0.143,
                    "G": 0.143,
                    "D": 0.143,
                    "A": 0.143,
                    "F": 0.143,
                    "Bb": 0.143,
                    "Eb": 0.143,
                },
            )
            key = self.weighted_choice(key_probabilities)

        # Generate melody in the key
        melody_notes = self._generate_tonal_melody(key, melody_length)

        # The last note should be the tonic
        tonic_note = melody_notes[-1]

        # Create options (include tonic and some other notes from the melody)
        options = [tonic_note]
        other_notes = [note for note in melody_notes[:-1] if note != tonic_note]
        options.extend(random.sample(other_notes, min(3, len(other_notes))))

        # Shuffle options
        random.shuffle(options)

        # Generate audio using AudioSynthesizer
        audio_synthesizer = AudioSynthesizer()

        # Generate melodic sequence audio (multiple notes played one after the other)
        audio_path = audio_synthesizer.synthesize_notes(melody_notes, duration=0.8)
        target_audio_url = audio_synthesizer.get_audio_url(audio_path)

        correct_answer = tonic_note

        context = {
            "key": key,
            "melody_notes": melody_notes,
            "tonic_note": tonic_note,
            "audio_sequence": melody_notes,
        }

        return ExerciseData(
            key=f"Key: {key} - Find Home",
            scale=self._get_scale_notes(key),
            progression_audio=None,
            target_audio=target_audio_url,
            options=options,
            correct_answer=correct_answer,
            context=context,
        )

    def check_answer(self, answer: Any, context: dict[str, Any]) -> ExerciseResult:
        """Check if the tonic answer is correct."""
        correct_tonic = context.get("tonic_note", "")
        is_correct = str(answer) == correct_tonic

        feedback = self.get_feedback(is_correct, answer, correct_tonic)
        if is_correct:
            feedback = "Correct! That note feels like home and provides resolution."
        else:
            feedback = f"Incorrect. The tonic (home note) is {correct_tonic}. Notice how it feels stable and resolved."

        return ExerciseResult(
            is_correct=is_correct,
            user_answer=str(answer),
            correct_answer=correct_tonic,
            feedback=feedback,
            hints_used=[],
        )

    def _generate_tonal_melody(self, key: str, length: int) -> list[str]:
        """Generate a melody in the specified key that ends on tonic."""
        # Major scale patterns for different keys
        scale_patterns = {
            "C": ["C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5"],
            "G": ["G4", "A4", "B4", "C5", "D5", "E5", "F#5", "G5"],
            "D": ["D4", "E4", "F#4", "G4", "A4", "B4", "C#5", "D5"],
            "A": ["A4", "B4", "C#5", "D5", "E5", "F#5", "G#5", "A5"],
            "F": ["F4", "G4", "A4", "Bb4", "C5", "D5", "E5", "F5"],
            "Bb": ["Bb4", "C5", "D5", "Eb5", "F5", "G5", "A5", "Bb5"],
            "Eb": ["Eb4", "F4", "G4", "Ab4", "Bb4", "C5", "D5", "Eb5"],
        }

        scale = scale_patterns.get(key, scale_patterns["C"])

        # Generate melody notes (avoid too many leaps)
        melody = []
        current_note = scale[0]  # Start on tonic

        for _i in range(length - 1):
            melody.append(current_note)
            # Move to nearby notes in the scale
            current_index = scale.index(current_note)
            # Small step movement (up to 2 scale degrees)
            step = random.choice([-2, -1, 1, 2])
            new_index = max(0, min(len(scale) - 1, current_index + step))
            current_note = scale[new_index]

        # End on tonic
        melody.append(scale[0])

        return melody

    def _get_scale_notes(self, key: str) -> list[str]:
        """Get scale notes for the key."""
        scale_patterns = {
            "C": ["C", "D", "E", "F", "G", "A", "B"],
            "G": ["G", "A", "B", "C", "D", "E", "F#"],
            "D": ["D", "E", "F#", "G", "A", "B", "C#"],
            "A": ["A", "B", "C#", "D", "E", "F#", "G#"],
            "F": ["F", "G", "A", "Bb", "C", "D", "E"],
            "Bb": ["Bb", "C", "D", "Eb", "F", "G", "A"],
            "Eb": ["Eb", "F", "G", "Ab", "Bb", "C", "D"],
        }
        return scale_patterns.get(key, scale_patterns["C"])


class ScaleDegreesWithSolfègeExercise(BaseExercise):
    """Exercise: Scale Degrees with Solfège - Identify scale degrees."""

    metadata = ExerciseMetadata(
        id="scale_degrees_solfege",
        name="Scale Degrees with Solfège",
        description="Listen to a scale degree and identify its solfège syllable (Do, Re, Mi, etc.).",
        difficulty=2,
        category="tonal_center",
        tags=["scale", "degrees", "solfège"],
        estimated_time=600,
        prerequisites=["find_home_note"],
        learning_objectives=["Learn scale degrees", "Connect solfège to pitch"],
        input_type="multiple_choice",
        answer_format="solfège",
        requires_progression=False,
        requires_single_note=True,
        audio_duration=2,
        config_options={
            "key": {
                "type": "str",
                "default": "random",
                "options": ["C", "G", "D", "A", "F", "Bb", "Eb", "random"],
            },
            "degrees": {"type": "list", "default": [1, 2, 3, 4, 5, 6, 7]},
            "key_probabilities": {
                "type": "dict",
                "default": {
                    "C": 0.143,
                    "G": 0.143,
                    "D": 0.143,
                    "A": 0.143,
                    "F": 0.143,
                    "Bb": 0.143,
                    "Eb": 0.143,
                },
                "description": "Custom probabilities for key selection (must sum to 1.0)",
            },
            "degree_probabilities": {
                "type": "dict",
                "default": {
                    "1": 0.143,
                    "2": 0.143,
                    "3": 0.143,
                    "4": 0.143,
                    "5": 0.143,
                    "6": 0.143,
                    "7": 0.143,
                },
                "description": "Custom probabilities for scale degree selection (must sum to 1.0)",
            },
        },
    )

    def generate(self, **kwargs) -> ExerciseData:
        """Generate a scale degree to identify."""
        key = kwargs.get("key", "random")

        if key == "random":
            key = random.choice(["C", "G", "D", "A", "F", "Bb", "Eb"])

        # Custom probabilities for scale degree selection
        degree_probabilities = kwargs.get(
            "degree_probabilities",
            {
                "1": 0.143,
                "2": 0.143,
                "3": 0.143,
                "4": 0.143,
                "5": 0.143,
                "6": 0.143,
                "7": 0.143,
            },
        )

        # Choose a scale degree with weighted choice
        degree_str = self.weighted_choice(degree_probabilities)
        degree = int(degree_str)

        # Get the note for this degree in the key
        target_note = self._get_scale_degree_note(key, degree)

        # Solfège syllables
        solfege_map = {1: "Do", 2: "Re", 3: "Mi", 4: "Fa", 5: "Sol", 6: "La", 7: "Ti"}
        correct_solfege = solfege_map[degree]

        # Create options
        options = list(solfege_map.values())
        random.shuffle(options)

        # Generate audio using AudioSynthesizer
        audio_synthesizer = AudioSynthesizer()

        # Generate single note audio
        audio_path = audio_synthesizer.synthesize_notes([target_note], duration=2.0)
        target_audio_url = audio_synthesizer.get_audio_url(audio_path)

        context = {
            "key": key,
            "degree": degree,
            "target_note": target_note,
            "correct_solfege": correct_solfege,
        }

        return ExerciseData(
            key=f"Key: {key} - Degree {degree}",
            scale=self._get_scale_notes(key),
            progression_audio=None,
            target_audio=target_audio_url,
            options=options,
            correct_answer=correct_solfege,
            context=context,
        )

    def check_answer(self, answer: Any, context: dict[str, Any]) -> ExerciseResult:
        """Check if the solfège answer is correct."""
        correct_solfege = context.get("correct_solfege", "")
        is_correct = str(answer) == correct_solfege

        degree = context.get("degree", 1)
        feedback = self.get_feedback(is_correct, answer, correct_solfege)
        if is_correct:
            feedback = f"Correct! That's {correct_solfege}, the {degree}{self._ordinal_suffix(degree)} degree."
        else:
            feedback = f"Incorrect. The correct solfège is {correct_solfege} (degree {degree})."

        return ExerciseResult(
            is_correct=is_correct,
            user_answer=str(answer),
            correct_answer=correct_solfege,
            feedback=feedback,
            hints_used=[],
        )

    def _get_scale_degree_note(self, key: str, degree: int) -> str:
        """Get the note for a specific scale degree in a key."""
        scale_patterns = {
            "C": ["C4", "D4", "E4", "F4", "G4", "A4", "B4"],
            "G": ["G4", "A4", "B4", "C5", "D5", "E5", "F#5"],
            "D": ["D4", "E4", "F#4", "G4", "A4", "B4", "C#5"],
            "A": ["A4", "B4", "C#5", "D5", "E5", "F#5", "G#5"],
            "F": ["F4", "G4", "A4", "Bb4", "C5", "D5", "E5"],
            "Bb": ["Bb4", "C5", "D5", "Eb5", "F5", "G5", "A5"],
            "Eb": ["Eb4", "F4", "G4", "Ab4", "Bb4", "C5", "D5"],
        }

        scale = scale_patterns.get(key, scale_patterns["C"])
        return scale[degree - 1]

    def _get_scale_notes(self, key: str) -> list[str]:
        """Get scale notes for the key."""
        scale_patterns = {
            "C": ["C", "D", "E", "F", "G", "A", "B"],
            "G": ["G", "A", "B", "C", "D", "E", "F#"],
            "D": ["D", "E", "F#", "G", "A", "B", "C#"],
            "A": ["A", "B", "C#", "D", "E", "F#", "G#"],
            "F": ["F", "G", "A", "Bb", "C", "D", "E"],
            "Bb": ["Bb", "C", "D", "Eb", "F", "G", "A"],
            "Eb": ["Eb", "F", "G", "Ab", "Bb", "C", "D"],
        }
        return scale_patterns.get(key, scale_patterns["C"])

    def _ordinal_suffix(self, n: int) -> str:
        """Get ordinal suffix for numbers."""
        if 10 <= n % 100 <= 20:
            suffix = "th"
        else:
            suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
        return suffix


class LabelDoMiSolExercise(BaseExercise):
    """Exercise: Label Do-Mi-Sol - Identify tonic triad notes."""

    metadata = ExerciseMetadata(
        id="label_do_mi_sol",
        name="Label Do-Mi-Sol",
        description="Listen to a broken tonic triad and identify which note is Do, Mi, or Sol.",
        difficulty=2,
        category="tonal_center",
        tags=["triad", "tonic", "chords"],
        estimated_time=600,
        prerequisites=["scale_degrees_solfege"],
        learning_objectives=["Recognize tonic chord tones", "Build chord awareness"],
        input_type="multiple_choice",
        answer_format="solfège",
        requires_progression=False,
        requires_single_note=True,
        audio_duration=2,
        config_options={
            "key": {
                "type": "str",
                "default": "random",
                "options": ["C", "G", "D", "A", "F", "Bb", "Eb", "random"],
            },
            "triad_notes": {"type": "list", "default": ["Do", "Mi", "Sol"]},
            "triad_note_probabilities": {
                "type": "dict",
                "default": {"Do": 0.333, "Mi": 0.333, "Sol": 0.333},
                "description": "Custom probabilities for triad note selection (must sum to 1.0)",
            },
        },
    )

    def generate(self, **kwargs) -> ExerciseData:
        """Generate a tonic triad note to identify."""
        key = kwargs.get("key", "random")

        if key == "random":
            key = random.choice(["C", "G", "D", "A", "F", "Bb", "Eb"])

        # Custom probabilities for triad note selection
        triad_note_probabilities = kwargs.get(
            "triad_note_probabilities",
            {
                "Do": 0.333,  # 33.3% chance
                "Mi": 0.333,  # 33.3% chance
                "Sol": 0.333,  # 33.3% chance
            },
        )

        # Choose which triad note to play with weighted choice
        target_solfege = self.weighted_choice(triad_note_probabilities)

        # Get the actual note
        target_note = self._get_triad_note(key, target_solfege)

        # Create options
        options = ["Do", "Mi", "Sol"]
        random.shuffle(options)

        # Generate audio using AudioSynthesizer
        audio_synthesizer = AudioSynthesizer()

        # Generate single note audio
        audio_path = audio_synthesizer.synthesize_notes([target_note], duration=2.0)
        target_audio_url = audio_synthesizer.get_audio_url(audio_path)

        context = {
            "key": key,
            "target_solfege": target_solfege,
            "target_note": target_note,
        }

        return ExerciseData(
            key=f"Key: {key} - {target_solfege}",
            scale=self._get_scale_notes(key),
            progression_audio=None,
            target_audio=target_audio_url,
            options=options,
            correct_answer=target_solfege,
            context=context,
        )

    def check_answer(self, answer: Any, context: dict[str, Any]) -> ExerciseResult:
        """Check if the triad note answer is correct."""
        correct_solfege = context.get("target_solfege", "")
        is_correct = str(answer) == correct_solfege

        feedback = self.get_feedback(is_correct, answer, correct_solfege)
        if is_correct:
            feedback = f"Correct! That's {correct_solfege}, a note in the tonic triad."
        else:
            feedback = f"Incorrect. The correct answer is {correct_solfege}."

        return ExerciseResult(
            is_correct=is_correct,
            user_answer=str(answer),
            correct_answer=correct_solfege,
            feedback=feedback,
            hints_used=[],
        )

    def _get_triad_note(self, key: str, solfege: str) -> str:
        """Get the note for a specific solfège in the tonic triad."""
        # Tonic triad notes (Do, Mi, Sol) in different keys
        triad_patterns = {
            "C": {"Do": "C4", "Mi": "E4", "Sol": "G4"},
            "G": {"Do": "G4", "Mi": "B4", "Sol": "D5"},
            "D": {"Do": "D4", "Mi": "F#4", "Sol": "A4"},
            "A": {"Do": "A4", "Mi": "C#5", "Sol": "E5"},
            "F": {"Do": "F4", "Mi": "A4", "Sol": "C5"},
            "Bb": {"Do": "Bb4", "Mi": "D5", "Sol": "F5"},
            "Eb": {"Do": "Eb4", "Mi": "G4", "Sol": "Bb4"},
        }

        pattern = triad_patterns.get(key, triad_patterns["C"])
        return pattern.get(solfege, "C4")

    def _get_scale_notes(self, key: str) -> list[str]:
        """Get scale notes for the key."""
        scale_patterns = {
            "C": ["C", "D", "E", "F", "G", "A", "B"],
            "G": ["G", "A", "B", "C", "D", "E", "F#"],
            "D": ["D", "E", "F#", "G", "A", "B", "C#"],
            "A": ["A", "B", "C#", "D", "E", "F#", "G#"],
            "F": ["F", "G", "A", "Bb", "C", "D", "E"],
            "Bb": ["Bb", "C", "D", "Eb", "F", "G", "A"],
            "Eb": ["Eb", "F", "G", "Ab", "Bb", "C", "D"],
        }
        return scale_patterns.get(key, scale_patterns["C"])
