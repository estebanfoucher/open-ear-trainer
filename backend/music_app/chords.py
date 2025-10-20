"""
Chord generation and manipulation using mingus.
"""

import mingus.core.chords as mingus_chords
import mingus.core.progressions as mingus_progressions


def get_chord(root: str, quality: str) -> list[str]:
    """
    Get the notes of a chord.

    Args:
        root: Root note (e.g., "C", "G", "F#")
        quality: Chord quality (e.g., "major", "minor", "diminished", "augmented")

    Returns:
        List[str]: List of notes in the chord
    """
    # Use mingus triad function instead of Chord class
    if quality == "major":
        chord_notes = mingus_chords.major_triad(root)
    elif quality == "minor":
        chord_notes = mingus_chords.minor_triad(root)
    elif quality == "diminished":
        chord_notes = mingus_chords.diminished_triad(root)
    elif quality == "augmented":
        chord_notes = mingus_chords.augmented_triad(root)
    else:
        # Default to major
        chord_notes = mingus_chords.major_triad(root)

    return [str(note) for note in chord_notes]


def get_major_chord(root: str) -> list[str]:
    """Get a major chord."""
    return get_chord(root, "major")


def get_minor_chord(root: str) -> list[str]:
    """Get a minor chord."""
    return get_chord(root, "minor")


def get_diminished_chord(root: str) -> list[str]:
    """Get a diminished chord."""
    return get_chord(root, "diminished")


def get_augmented_chord(root: str) -> list[str]:
    """Get an augmented chord."""
    return get_chord(root, "augmented")


def get_dominant_seventh_chord(root: str) -> list[str]:
    """Get a dominant seventh chord."""
    return get_chord(root, "7")


def get_major_seventh_chord(root: str) -> list[str]:
    """Get a major seventh chord."""
    return get_chord(root, "maj7")


def get_minor_seventh_chord(root: str) -> list[str]:
    """Get a minor seventh chord."""
    return get_chord(root, "m7")


def get_progression(key: str, roman_numerals: list[str]) -> list[list[str]]:
    """
    Get a chord progression in a given key.

    Args:
        key: Key (e.g., "C", "Am", "G")
        roman_numerals: List of roman numerals (e.g., ["I", "IV", "V", "I"])

    Returns:
        List[List[str]]: List of chords in the progression
    """
    progression = mingus_progressions.to_chords(roman_numerals, key)
    result = []
    for chord in progression:
        if hasattr(chord, "ascending"):
            result.append([str(note) for note in chord.ascending()])
        else:
            # If it's already a list or tuple
            result.append([str(note) for note in chord])
    return result


def get_common_progressions() -> dict[str, list[str]]:
    """
    Get common chord progressions.

    Returns:
        Dict[str, List[str]]: Dictionary of progression names and roman numerals
    """
    return {
        "I-IV-V-I": ["I", "IV", "V", "I"],
        "I-vi-IV-V": ["I", "vi", "IV", "V"],
        "ii-V-I": ["ii", "V", "I"],
        "I-V-vi-IV": ["I", "V", "vi", "IV"],
        "vi-IV-I-V": ["vi", "IV", "I", "V"],
        "I-IV-vi-V": ["I", "IV", "vi", "V"],
        "I-vi-ii-V": ["I", "vi", "ii", "V"],
        "I-iii-vi-IV": ["I", "iii", "vi", "IV"],
    }


def get_chord_quality(chord: list[str]) -> str:
    """
    Determine the quality of a chord based on its notes.

    Args:
        chord: List of notes in the chord

    Returns:
        str: Chord quality ("major", "minor", "diminished", "augmented", "unknown")
    """
    if len(chord) < 3:
        return "unknown"

    # Convert to intervals from root
    root = chord[0]
    intervals = []

    for note in chord[1:]:
        # Calculate interval in semitones
        interval = (ord(note[0]) - ord(root[0])) % 12
        intervals.append(interval)

    # Check for common chord qualities
    if intervals == [4, 7]:  # Major third + perfect fifth
        return "major"
    elif intervals == [3, 7]:  # Minor third + perfect fifth
        return "minor"
    elif intervals == [3, 6]:  # Minor third + diminished fifth
        return "diminished"
    elif intervals == [4, 8]:  # Major third + augmented fifth
        return "augmented"

    return "unknown"


def get_chord_inversion(chord: list[str], inversion: int) -> list[str]:
    """
    Get a chord inversion.

    Args:
        chord: List of notes in the chord
        inversion: Inversion number (0 = root position, 1 = first inversion, etc.)

    Returns:
        List[str]: Chord with specified inversion
    """
    if inversion <= 0 or inversion >= len(chord):
        return chord

    # For simplicity, we'll just rotate the chord
    return chord[inversion:] + chord[:inversion]


def get_chord_symbol(chord: list[str]) -> str:
    """
    Get the chord symbol for a chord.

    Args:
        chord: List of notes in the chord

    Returns:
        str: Chord symbol (e.g., "C", "Am", "F#m7")
    """
    if not chord:
        return ""

    root = chord[0]
    quality = get_chord_quality(chord)

    if quality == "major":
        return root
    elif quality == "minor":
        return f"{root}m"
    elif quality == "diminished":
        return f"{root}dim"
    elif quality == "augmented":
        return f"{root}aug"
    else:
        return root


def is_chord_major(chord: list[str]) -> bool:
    """Check if a chord is major."""
    return get_chord_quality(chord) == "major"


def is_chord_minor(chord: list[str]) -> bool:
    """Check if a chord is minor."""
    return get_chord_quality(chord) == "minor"


def get_chord_notes_in_octave(chord: list[str], octave: int = 4) -> list[str]:
    """
    Get chord notes in a specific octave.

    Args:
        chord: List of chord notes
        octave: Octave number

    Returns:
        List[str]: Chord notes with octave specification
    """
    return [f"{note}-{octave}" for note in chord]


def get_suspended_chord(root: str, suspension_type: str) -> list[str]:
    """
    Get a suspended chord using mingus.

    Args:
        root: Root note (e.g., "C", "G", "F#")
        suspension_type: Type of suspension ("sus2" or "sus4")

    Returns:
        List[str]: List of notes in the suspended chord
    """
    if suspension_type == "sus2":
        chord_notes = mingus_chords.suspended_second_triad(root)
    elif suspension_type == "sus4":
        chord_notes = mingus_chords.suspended_fourth_triad(root)
    else:
        # Default to sus4
        chord_notes = mingus_chords.suspended_fourth_triad(root)

    return [str(note) for note in chord_notes]


def get_chord_notes_with_octaves(
    root: str, chord_type: str, octave: int = 4
) -> list[str]:
    """
    Get chord notes with proper octave handling for audio synthesis using mingus.

    Args:
        root: Root note (e.g., "C", "G", "F#")
        chord_type: Type of chord ("major", "minor", "diminished", "augmented", "sus2", "sus4", "3m", "3M")
        octave: Base octave number

    Returns:
        List[str]: List of chord notes in format "Note-Octave"
    """
    # Get chord notes using mingus
    if chord_type == "major":
        chord_notes = mingus_chords.major_triad(root)
    elif chord_type == "minor":
        chord_notes = mingus_chords.minor_triad(root)
    elif chord_type == "diminished":
        chord_notes = mingus_chords.diminished_triad(root)
    elif chord_type == "augmented":
        chord_notes = mingus_chords.augmented_triad(root)
    elif chord_type == "sus2":
        chord_notes = mingus_chords.suspended_second_triad(root)
    elif chord_type == "sus4":
        chord_notes = mingus_chords.suspended_fourth_triad(root)
    elif chord_type == "3m":
        chord_notes = mingus_chords.minor_triad(root)
    elif chord_type == "3M":
        chord_notes = mingus_chords.major_triad(root)
    else:
        # Default to major
        chord_notes = mingus_chords.major_triad(root)

    # Convert to string list
    chord_notes = [str(note) for note in chord_notes]

    # Add octave information for audio synthesis
    return _add_octaves_to_chord_notes(chord_notes, octave)


def get_fifth_quality_chord(
    root: str, fifth_quality: str, octave: int = 4
) -> list[str]:
    """
    Get a major triad with specific fifth quality (for FifthQualityExercise).
    This is a specialized function for the fifth quality exercise.

    Args:
        root: Root note (e.g., "C", "G", "F#")
        fifth_quality: Fifth quality ("5dim", "5J", or "5aug")
        octave: Base octave number

    Returns:
        List[str]: List of chord notes in format "Note-Octave"
    """
    # Start with major triad from mingus
    chord_notes = mingus_chords.major_triad(root)
    chord_notes = [str(note) for note in chord_notes]

    # Modify the fifth based on quality
    if fifth_quality == "5dim":
        # Replace perfect fifth with diminished fifth
        chord_notes[2] = _get_note_with_interval(root, 6)  # diminished fifth
    elif fifth_quality == "5aug":
        # Replace perfect fifth with augmented fifth
        chord_notes[2] = _get_note_with_interval(root, 8)  # augmented fifth
    # For "5J", keep the perfect fifth from mingus

    # Add octave information for audio synthesis
    return _add_octaves_to_chord_notes(chord_notes, octave)


def _add_octaves_to_chord_notes(chord_notes: list[str], octave: int) -> list[str]:
    """
    Add octave information to chord notes for audio synthesis.

    Args:
        chord_notes: List of note names without octaves
        octave: Base octave number

    Returns:
        List[str]: List of chord notes in format "Note-Octave"
    """

    # Convert flats to sharps for consistent indexing
    def normalize_note(note: str) -> str:
        """Convert flat notes to sharp equivalents."""
        flat_to_sharp = {"Db": "C#", "Eb": "D#", "Gb": "F#", "Ab": "G#", "Bb": "A#"}
        return flat_to_sharp.get(note, note)

    note_order = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

    # Normalize all notes to sharps
    normalized_notes = [normalize_note(note) for note in chord_notes]
    root = normalized_notes[0]
    root_index = note_order.index(root)

    # Calculate octaves for each note
    octaves = [octave] * len(chord_notes)

    for i, note in enumerate(normalized_notes[1:], 1):  # Skip root
        note_index = note_order.index(note)
        if note_index < root_index:
            octaves[i] = octave + 1
        octaves[i] = max(1, min(7, octaves[i]))

    # Build chord notes with octaves (use original note names, not normalized)
    return [f"{note}-{octaves[i]}" for i, note in enumerate(chord_notes)]


def _get_note_with_interval(root: str, semitones: int) -> str:
    """
    Get a note that is a specific number of semitones above the root.

    Args:
        root: Root note (e.g., "C", "G", "F#")
        semitones: Number of semitones above root

    Returns:
        str: Note name
    """

    # Convert flats to sharps for consistent indexing
    def normalize_note(note: str) -> str:
        """Convert flat notes to sharp equivalents."""
        flat_to_sharp = {"Db": "C#", "Eb": "D#", "Gb": "F#", "Ab": "G#", "Bb": "A#"}
        return flat_to_sharp.get(note, note)

    note_order = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    normalized_root = normalize_note(root)
    root_index = note_order.index(normalized_root)
    target_index = (root_index + semitones) % 12
    return note_order[target_index]


def get_chord_display_name(chord_type: str) -> str:
    """
    Get display name for chord type.

    Args:
        chord_type: Chord type identifier

    Returns:
        str: Human-readable chord type name
    """
    display_names = {
        "major": "major",
        "minor": "minor",
        "diminished": "diminished",
        "augmented": "augmented",
        "sus2": "suspended 2nd",
        "sus4": "suspended 4th",
        "3m": "minor",
        "3M": "major",
        "5dim": "diminished fifth",
        "5J": "perfect fifth",
        "5aug": "augmented fifth",
    }
    return display_names.get(chord_type, chord_type)
