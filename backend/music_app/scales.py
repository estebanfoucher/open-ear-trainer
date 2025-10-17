"""
Scale generation and manipulation using mingus.
"""

import mingus.core.notes as mingus_notes
import mingus.core.scales as mingus_scales


def get_major_scale(root: str) -> list[str]:
    """
    Get the notes of a major scale.

    Args:
        root: Root note (e.g., "C", "G", "F#")

    Returns:
        List[str]: List of notes in the major scale
    """
    scale = mingus_scales.Major(root)
    return [str(note) for note in scale.ascending()]


def get_minor_scale(root: str) -> list[str]:
    """
    Get the notes of a natural minor scale.

    Args:
        root: Root note (e.g., "A", "E", "D#")

    Returns:
        List[str]: List of notes in the minor scale
    """
    scale = mingus_scales.NaturalMinor(root)
    return [str(note) for note in scale.ascending()]


def get_harmonic_minor_scale(root: str) -> list[str]:
    """
    Get the notes of a harmonic minor scale.

    Args:
        root: Root note (e.g., "A", "E", "D#")

    Returns:
        List[str]: List of notes in the harmonic minor scale
    """
    scale = mingus_scales.HarmonicMinor(root)
    return [str(note) for note in scale.ascending()]


def get_melodic_minor_scale(root: str) -> list[str]:
    """
    Get the notes of a melodic minor scale.

    Args:
        root: Root note (e.g., "A", "E", "D#")

    Returns:
        List[str]: List of notes in the melodic minor scale
    """
    scale = mingus_scales.MelodicMinor(root)
    return [str(note) for note in scale.ascending()]


def get_scale_degree(scale: list[str], degree: int) -> str | None:
    """
    Get a specific degree of a scale.

    Args:
        scale: List of notes in the scale
        degree: Scale degree (1-7)

    Returns:
        Optional[str]: Note at the specified degree, or None if invalid
    """
    if 1 <= degree <= len(scale):
        return scale[degree - 1]
    return None


def get_scale_degree_name(degree: int) -> str:
    """
    Get the name of a scale degree.

    Args:
        degree: Scale degree (1-7)

    Returns:
        str: Degree name (e.g., "tonic", "supertonic", "mediant")
    """
    degree_names = {
        1: "tonic",
        2: "supertonic",
        3: "mediant",
        4: "subdominant",
        5: "dominant",
        6: "submediant",
        7: "leading tone",
    }
    return degree_names.get(degree, f"degree_{degree}")


def get_scale_mode(scale: list[str], mode: int) -> list[str]:
    """
    Get a mode of a scale.

    Args:
        scale: List of notes in the scale
        mode: Mode number (1-7)

    Returns:
        List[str]: Notes of the mode
    """
    if 1 <= mode <= 7:
        # Rotate the scale to start at the mode degree
        return scale[mode - 1 :] + scale[: mode - 1]
    return scale


def get_ionian_mode(root: str) -> list[str]:
    """Get Ionian mode (same as major scale)."""
    return get_major_scale(root)


def get_dorian_mode(root: str) -> list[str]:
    """Get Dorian mode."""
    scale = mingus_scales.Dorian(root)
    return [str(note) for note in scale]


def get_phrygian_mode(root: str) -> list[str]:
    """Get Phrygian mode."""
    scale = mingus_scales.Phrygian(root)
    return [str(note) for note in scale]


def get_lydian_mode(root: str) -> list[str]:
    """Get Lydian mode."""
    scale = mingus_scales.Lydian(root)
    return [str(note) for note in scale]


def get_mixolydian_mode(root: str) -> list[str]:
    """Get Mixolydian mode."""
    scale = mingus_scales.Mixolydian(root)
    return [str(note) for note in scale]


def get_aeolian_mode(root: str) -> list[str]:
    """Get Aeolian mode (same as natural minor scale)."""
    return get_minor_scale(root)


def get_locrian_mode(root: str) -> list[str]:
    """Get Locrian mode."""
    scale = mingus_scales.Locrian(root)
    return [str(note) for note in scale]


def is_note_in_scale(note: str, scale: list[str]) -> bool:
    """
    Check if a note is in a given scale.

    Args:
        note: Note to check
        scale: List of notes in the scale

    Returns:
        bool: True if the note is in the scale
    """
    return note in scale


def get_scale_type(scale: list[str]) -> str:
    """
    Determine the type of scale based on its notes.

    Args:
        scale: List of notes in the scale

    Returns:
        str: Scale type ("major", "minor", "unknown")
    """
    if len(scale) != 7:
        return "unknown"

    # Check if it's a major scale
    major_pattern = [2, 2, 1, 2, 2, 2, 1]  # Whole and half step pattern
    minor_pattern = [2, 1, 2, 2, 1, 2, 2]  # Natural minor pattern

    # Convert notes to semitones from root
    root = mingus_notes.note_to_int(scale[0])
    semitones = [mingus_notes.note_to_int(note) - root for note in scale]

    # Check patterns
    if semitones == [0, 2, 4, 5, 7, 9, 11]:  # Major scale pattern
        return "major"
    elif semitones == [0, 2, 3, 5, 7, 8, 10]:  # Natural minor pattern
        return "minor"

    return "unknown"
