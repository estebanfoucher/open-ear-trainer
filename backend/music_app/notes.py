"""
Note utilities for music theory operations.
"""

import mingus.core.intervals as mingus_intervals
import mingus.core.notes as mingus_notes


def get_note_name(note: str) -> str:
    """
    Get the base note name from a note string.

    Args:
        note: Note string (e.g., "C-4", "F#", "Bb")

    Returns:
        str: Base note name (e.g., "C", "F", "B")
    """
    # Use note_to_int and convert back to note name
    note_int = mingus_notes.note_to_int(note)
    return mingus_notes.int_to_note(note_int)


def get_note_number(note: str) -> int:
    """
    Get the MIDI note number for a note.

    Args:
        note: Note string (e.g., "C-4", "F#", "Bb")

    Returns:
        int: MIDI note number (0-127)
    """
    # Convert note format for mingus (e.g., "A-4" -> "A")
    base_note = note.split("-")[0] if "-" in note else note
    return mingus_notes.note_to_int(base_note)


def transpose_note(note: str, semitones: int) -> str:
    """
    Transpose a note by a number of semitones.

    Args:
        note: Note string (e.g., "C-4", "F#", "Bb")
        semitones: Number of semitones to transpose (positive or negative)

    Returns:
        str: Transposed note
    """
    # Parse note and octave
    if "-" in note:
        base_note, octave_str = note.split("-")
        octave = int(octave_str)
    else:
        base_note = note
        octave = 4  # Default octave

    # Get base note number (0-11)
    base_number = mingus_notes.note_to_int(base_note)

    # Calculate new note and octave
    total_semitones = base_number + semitones
    new_note_number = total_semitones % 12
    octave_change = total_semitones // 12

    # Convert back to note
    new_note = mingus_notes.int_to_note(new_note_number)
    new_octave = octave + octave_change

    return f"{new_note}-{new_octave}"


def note_distance(note1: str, note2: str) -> int:
    """
    Calculate the distance in semitones between two notes.

    Args:
        note1: First note
        note2: Second note

    Returns:
        int: Distance in semitones
    """
    return mingus_notes.note_to_int(note2) - mingus_notes.note_to_int(note1)


def get_interval(note1: str, note2: str) -> str:
    """
    Get the interval between two notes.

    Args:
        note1: First note
        note2: Second note

    Returns:
        str: Interval name (e.g., "major_third", "perfect_fifth")
    """
    return mingus_intervals.determine(note1, note2)


def get_notes_in_octave(octave: int = 4) -> list[str]:
    """
    Get all natural notes in a specific octave.

    Args:
        octave: Octave number (default: 4)

    Returns:
        List[str]: List of notes in the octave
    """
    notes = ["C", "D", "E", "F", "G", "A", "B"]
    return [f"{note}-{octave}" for note in notes]


def get_chromatic_notes_in_octave(octave: int = 4) -> list[str]:
    """
    Get all chromatic notes in a specific octave.

    Args:
        octave: Octave number (default: 4)

    Returns:
        List[str]: List of chromatic notes in the octave
    """
    notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    return [f"{note}-{octave}" for note in notes]


def is_sharp_note(note: str) -> bool:
    """
    Check if a note is sharp.

    Args:
        note: Note string

    Returns:
        bool: True if the note is sharp
    """
    return "#" in note


def is_flat_note(note: str) -> bool:
    """
    Check if a note is flat.

    Args:
        note: Note string

    Returns:
        bool: True if the note is flat
    """
    return "b" in note


def normalize_note(note: str) -> str:
    """
    Normalize a note to a standard format.

    Args:
        note: Note string

    Returns:
        str: Normalized note
    """
    # Remove any whitespace and convert to uppercase
    note = note.strip().upper()

    # Handle common variations
    if note == "BB":
        return "A#"
    elif note == "EB":
        return "D#"
    elif note == "FB":
        return "E"
    elif note == "CB":
        return "B"

    return note
