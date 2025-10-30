"""
Pytest configuration and fixtures for backend tests.
"""

import os
import tempfile

import pytest
from audio_app.synthesizer import AudioSynthesizer
from django.conf import settings


@pytest.fixture
def temp_media_dir():
    """Create a temporary media directory for tests."""
    temp_dir = tempfile.mkdtemp()
    original_media_root = settings.MEDIA_ROOT
    settings.MEDIA_ROOT = temp_dir

    yield temp_dir

    # Cleanup
    settings.MEDIA_ROOT = original_media_root
    import shutil

    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def test_soundfont_path():
    """Get path to test soundfont file."""
    # For now, return None - we'll create a minimal test soundfont later
    return None


@pytest.fixture
def audio_synthesizer(test_soundfont_path, temp_media_dir):
    """Create an AudioSynthesizer instance for testing."""
    return AudioSynthesizer(soundfont_path=test_soundfont_path)


@pytest.fixture
def sample_audio_file(audio_synthesizer, temp_media_dir):
    """Create a sample audio file for testing."""
    # Generate a simple audio file
    audio_path = audio_synthesizer.synthesize_notes(notes=["C-4", "E-4"], duration=1.0)
    return audio_path


@pytest.fixture
def exercise_registry():
    """Create a test exercise registry."""
    from api_app.views import SimpleExerciseRegistry

    return SimpleExerciseRegistry()


@pytest.fixture
def sample_exercise_data():
    """Create sample exercise data for testing."""
    from exercises.base.metadata import ExerciseData

    return ExerciseData(
        key="C major",
        scale=["C", "D", "E", "F", "G", "A", "B"],
        target_audio="/api/audio/test.wav",
        options=["minor_third", "major_third", "octave"],
        correct_answer="major_third",
        context={"root_note": "C-4", "interval": "major_third"},
    )


@pytest.fixture
def sample_exercise_result():
    """Create sample exercise result for testing."""
    from exercises.base.metadata import ExerciseResult

    return ExerciseResult(
        is_correct=True,
        user_answer="major_third",
        correct_answer="major_third",
        feedback="Correct! Well done!",
        hints_used=[],
        time_taken=5,
    )


@pytest.fixture
def sample_exercise_metadata():
    """Create sample exercise metadata for testing."""
    from exercises.base.metadata import ExerciseMetadata

    return ExerciseMetadata(
        id="test_exercise",
        name="Test Exercise",
        description="A test exercise for unit testing",
        difficulty=3,
        prerequisites=[],
        learning_objectives=["Learn to identify intervals"],
        estimated_time=30,
        category="interval_recognition",
        tags=["intervals", "melodic", "test"],
        input_type="multiple_choice",
        answer_format="interval_name",
        requires_progression=False,
        requires_single_note=True,
        audio_duration=2,
        config_options={"key": "C", "octave": 4},
    )


@pytest.fixture(autouse=True)
def cleanup_audio_files():
    """Clean up audio files after each test."""
    yield

    # Clean up any audio files created during tests
    if hasattr(settings, "MEDIA_ROOT") and settings.MEDIA_ROOT:
        audio_dir = os.path.join(settings.MEDIA_ROOT, "audio")
        if os.path.exists(audio_dir):
            import shutil

            shutil.rmtree(audio_dir, ignore_errors=True)


@pytest.fixture
def mock_audio_generation(monkeypatch):
    """Mock audio generation for faster tests."""

    def mock_synthesize_notes(self, notes, duration=2.0, output_path=None):
        # Create a minimal WAV file
        if output_path is None:
            import tempfile

            fd, output_path = tempfile.mkstemp(suffix=".wav", prefix="test_")
            os.close(fd)

        # Create a minimal WAV file header
        with open(output_path, "wb") as f:
            # Minimal WAV header (44 bytes)
            f.write(b"RIFF")
            f.write((36).to_bytes(4, "little"))  # File size - 8
            f.write(b"WAVE")
            f.write(b"fmt ")
            f.write((16).to_bytes(4, "little"))  # Format chunk size
            f.write((1).to_bytes(2, "little"))  # Audio format (PCM)
            f.write((1).to_bytes(2, "little"))  # Number of channels
            f.write((44100).to_bytes(4, "little"))  # Sample rate
            f.write((88200).to_bytes(4, "little"))  # Byte rate
            f.write((2).to_bytes(2, "little"))  # Block align
            f.write((16).to_bytes(2, "little"))  # Bits per sample
            f.write(b"data")
            f.write((0).to_bytes(4, "little"))  # Data size (empty)

        return output_path

    monkeypatch.setattr(AudioSynthesizer, "synthesize_notes", mock_synthesize_notes)
    monkeypatch.setattr(AudioSynthesizer, "synthesize_chord", mock_synthesize_notes)
    monkeypatch.setattr(AudioSynthesizer, "synthesize_interval", mock_synthesize_notes)
    monkeypatch.setattr(
        AudioSynthesizer, "synthesize_melodic_interval", mock_synthesize_notes
    )
    monkeypatch.setattr(
        AudioSynthesizer, "synthesize_harmonic_interval", mock_synthesize_notes
    )
    monkeypatch.setattr(
        AudioSynthesizer, "synthesize_staggered_interval", mock_synthesize_notes
    )
    monkeypatch.setattr(
        AudioSynthesizer, "synthesize_progression", mock_synthesize_notes
    )


@pytest.fixture
def chapter_lesson_structure():
    """Create a sample chapter/lesson structure for testing."""
    return {
        "chapters": [
            {
                "id": "chapter_1",
                "name": "Basic Intervals",
                "description": "Learn to identify basic intervals",
                "difficulty": 1,
                "lessons": [
                    {
                        "id": "lesson_1_1",
                        "name": "Perfect Intervals",
                        "description": "Learn perfect fourth, fifth, and octave",
                        "difficulty": 1,
                        "exercises": [
                            "perfect_fourth_fifth_octave_melodic",
                            "perfect_fourth_fifth_octave_harmonic",
                        ],
                    },
                    {
                        "id": "lesson_1_2",
                        "name": "Third Intervals",
                        "description": "Learn minor and major thirds",
                        "difficulty": 2,
                        "exercises": [
                            "minor_third_major_third_octave_melodic",
                            "minor_third_major_third_octave_harmonic",
                        ],
                    },
                ],
            },
            {
                "id": "chapter_2",
                "name": "Advanced Intervals",
                "description": "Learn more complex intervals",
                "difficulty": 3,
                "lessons": [
                    {
                        "id": "lesson_2_1",
                        "name": "Combined Intervals",
                        "description": "Practice with all intervals",
                        "difficulty": 4,
                        "exercises": ["combined_intervals_melodic"],
                    }
                ],
            },
        ]
    }
