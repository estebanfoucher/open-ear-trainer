"""
Tests for audio synthesizer functionality.
"""

import os
import wave

from audio_app.synthesizer import AudioSynthesizer


class TestAudioSynthesizer:
    """Test AudioSynthesizer class."""

    def test_synthesizer_initialization_without_soundfont(self):
        """Test synthesizer initialization without soundfont."""
        synthesizer = AudioSynthesizer()
        assert synthesizer.soundfont_path is None
        assert synthesizer.cache_enabled is False  # Disabled in test settings

    def test_synthesizer_initialization_with_soundfont(self, test_soundfont_path):
        """Test synthesizer initialization with soundfont."""
        synthesizer = AudioSynthesizer(soundfont_path=test_soundfont_path)
        assert synthesizer.soundfont_path == test_soundfont_path

    def test_synthesizer_initialization_with_nonexistent_soundfont(self):
        """Test synthesizer initialization with nonexistent soundfont."""
        synthesizer = AudioSynthesizer(soundfont_path="/nonexistent/path.sf2")
        assert synthesizer.soundfont_path is None

    def test_synthesizer_cache_settings(self):
        """Test synthesizer cache configuration."""
        synthesizer = AudioSynthesizer()
        assert synthesizer.cache_enabled is False  # Disabled in test settings
        assert synthesizer.cache_max_size == 1000

    def test_generate_cache_key(self):
        """Test cache key generation."""
        synthesizer = AudioSynthesizer()

        key1 = synthesizer._generate_cache_key("test_content")
        key2 = synthesizer._generate_cache_key("test_content")
        key3 = synthesizer._generate_cache_key("different_content")

        assert key1 == key2  # Same content should generate same key
        assert key1 != key3  # Different content should generate different key
        assert len(key1) == 32  # MD5 hash length

    def test_get_cache_path(self, temp_media_dir):
        """Test cache path generation."""
        synthesizer = AudioSynthesizer()
        cache_key = "test_key"
        cache_path = synthesizer._get_cache_path(cache_key)

        expected_path = os.path.join(temp_media_dir, "audio", "cache", "test_key.wav")
        assert cache_path == expected_path

    def test_is_cached_false_when_cache_disabled(self):
        """Test that caching is disabled when cache_enabled is False."""
        synthesizer = AudioSynthesizer()
        synthesizer.cache_enabled = False

        assert synthesizer._is_cached("any_key") is False

    def test_synthesize_notes_basic(self, audio_synthesizer, temp_media_dir):
        """Test basic note synthesis."""
        notes = ["C-4", "E-4", "G-4"]
        duration = 1.5

        audio_path = audio_synthesizer.synthesize_notes(notes, duration)

        # Check that file was created
        assert os.path.exists(audio_path)
        assert audio_path.endswith(".wav")

        # Check that file is in media directory
        assert temp_media_dir in audio_path

    def test_synthesize_notes_with_output_path(self, audio_synthesizer, temp_media_dir):
        """Test note synthesis with custom output path."""
        notes = ["C-4", "E-4"]
        duration = 1.0
        custom_path = os.path.join(temp_media_dir, "custom_audio.wav")

        audio_path = audio_synthesizer.synthesize_notes(notes, duration, custom_path)

        assert audio_path == custom_path
        assert os.path.exists(custom_path)

    def test_synthesize_chord(self, audio_synthesizer, temp_media_dir):
        """Test chord synthesis."""
        chord_notes = ["C-4", "E-4", "G-4"]
        duration = 2.0

        audio_path = audio_synthesizer.synthesize_chord(chord_notes, duration)

        assert os.path.exists(audio_path)
        assert audio_path.endswith(".wav")

    def test_synthesize_interval(self, audio_synthesizer, temp_media_dir):
        """Test interval synthesis."""
        note1 = "C-4"
        note2 = "E-4"
        duration = 1.5

        audio_path = audio_synthesizer.synthesize_interval(note1, note2, duration)

        assert os.path.exists(audio_path)
        assert audio_path.endswith(".wav")

    def test_synthesize_melodic_interval(self, audio_synthesizer, temp_media_dir):
        """Test melodic interval synthesis."""
        note1 = "C-4"
        note2 = "E-4"
        note_duration = 1.0
        gap_duration = 0.5

        audio_path = audio_synthesizer.synthesize_melodic_interval(
            note1, note2, note_duration, gap_duration
        )

        assert os.path.exists(audio_path)
        assert audio_path.endswith(".wav")

    def test_synthesize_harmonic_interval(self, audio_synthesizer, temp_media_dir):
        """Test harmonic interval synthesis."""
        note1 = "C-4"
        note2 = "E-4"
        duration = 1.0

        audio_path = audio_synthesizer.synthesize_harmonic_interval(
            note1, note2, duration
        )

        assert os.path.exists(audio_path)
        assert audio_path.endswith(".wav")

    def test_synthesize_staggered_interval(self, audio_synthesizer, temp_media_dir):
        """Test staggered interval synthesis."""
        note1 = "C-4"
        note2 = "E-4"
        root_duration = 1.5
        second_duration = 1.0
        delay_ms = 400

        audio_path = audio_synthesizer.synthesize_staggered_interval(
            note1, note2, root_duration, second_duration, delay_ms
        )

        assert os.path.exists(audio_path)
        assert audio_path.endswith(".wav")

    def test_synthesize_progression(self, audio_synthesizer, temp_media_dir):
        """Test chord progression synthesis."""
        progression = [
            ["C-4", "E-4", "G-4"],  # C major
            ["F-4", "A-4", "C-5"],  # F major
            ["G-4", "B-4", "D-5"],  # G major
            ["C-4", "E-4", "G-4"],  # C major
        ]
        chord_duration = 1.0

        audio_path = audio_synthesizer.synthesize_progression(
            progression, chord_duration
        )

        assert os.path.exists(audio_path)
        assert audio_path.endswith(".wav")

    def test_audio_file_validity(self, audio_synthesizer, temp_media_dir):
        """Test that generated audio files are valid WAV files."""
        notes = ["C-4", "E-4"]
        audio_path = audio_synthesizer.synthesize_notes(notes, 1.0)

        # Try to open as WAV file
        with wave.open(audio_path, "rb") as wav_file:
            assert wav_file.getnchannels() == 1  # Mono
            assert wav_file.getsampwidth() == 2  # 16-bit
            assert wav_file.getframerate() == 44100  # 44.1kHz
            assert wav_file.getnframes() > 0  # Has audio data

    def test_cache_disabled_behavior(self, temp_media_dir):
        """Test behavior when caching is disabled."""
        synthesizer = AudioSynthesizer()
        synthesizer.cache_enabled = False

        notes = ["C-4", "E-4"]
        duration = 1.0

        # Generate same audio twice
        audio_path1 = synthesizer.synthesize_notes(notes, duration)
        audio_path2 = synthesizer.synthesize_notes(notes, duration)

        # Should create different files when caching is disabled
        assert audio_path1 != audio_path2
        assert os.path.exists(audio_path1)
        assert os.path.exists(audio_path2)

    def test_get_audio_url(self, audio_synthesizer, temp_media_dir):
        """Test audio URL generation."""
        notes = ["C-4", "E-4"]
        audio_path = audio_synthesizer.synthesize_notes(notes, 1.0)

        audio_url = audio_synthesizer.get_audio_url(audio_path)

        # Should return API endpoint format
        assert audio_url.startswith("/api/audio/")
        assert audio_url.endswith("/")
        assert ".wav" in audio_url

    def test_note_to_midi_number(self):
        """Test note to MIDI number conversion."""
        synthesizer = AudioSynthesizer()

        # Test various notes
        assert synthesizer._note_to_midi_number("C-4") == 60  # Middle C
        assert synthesizer._note_to_midi_number("A-4") == 69  # A4 (440 Hz)
        assert synthesizer._note_to_midi_number("C-5") == 72  # C5
        assert synthesizer._note_to_midi_number("F#-4") == 66  # F#4
        assert synthesizer._note_to_midi_number("Bb-4") == 70  # Bb4

    def test_note_to_frequency(self):
        """Test note to frequency conversion."""
        synthesizer = AudioSynthesizer()

        # Test A4 (should be 440 Hz)
        assert abs(synthesizer._note_to_frequency("A-4") - 440.0) < 0.1

        # Test C4 (should be ~261.63 Hz)
        assert abs(synthesizer._note_to_frequency("C-4") - 261.63) < 0.1

        # Test C5 (should be ~523.25 Hz, one octave above C4)
        assert abs(synthesizer._note_to_frequency("C-5") - 523.25) < 0.1

    def test_generate_piano_tone(self):
        """Test piano tone generation."""
        synthesizer = AudioSynthesizer()
        import numpy as np

        frequency = 440.0  # A4
        duration = 0.1
        sample_rate = 44100
        t = np.linspace(0, duration, int(sample_rate * duration), False)

        audio = synthesizer._generate_piano_tone(frequency, t)

        assert len(audio) == len(t)
        assert np.max(np.abs(audio)) <= 1.0  # Should be normalized
        assert np.min(audio) >= -1.0  # Should be in valid range

    def test_synthesizer_with_mock_audio(self, mock_audio_generation, temp_media_dir):
        """Test synthesizer with mocked audio generation for faster tests."""
        synthesizer = AudioSynthesizer()

        # This should use the mocked version
        notes = ["C-4", "E-4", "G-4"]
        audio_path = synthesizer.synthesize_notes(notes, 2.0)

        assert os.path.exists(audio_path)
        assert audio_path.endswith(".wav")

        # Check that it's a minimal WAV file (44 bytes header)
        from pathlib import Path

        file_size = Path(audio_path).stat().st_size
        assert file_size >= 44  # At least WAV header size

    def test_synthesizer_error_handling(self):
        """Test synthesizer error handling."""
        synthesizer = AudioSynthesizer()

        # Test with invalid notes (should not crash)
        try:
            audio_path = synthesizer.synthesize_notes(["invalid_note"], 1.0)
            # Should still create a file (with fallback behavior)
            assert os.path.exists(audio_path)
        except Exception as e:
            # If it raises an exception, it should be a reasonable one
            assert isinstance(e, ValueError | KeyError | TypeError)

    def test_synthesizer_performance(self, audio_synthesizer, temp_media_dir):
        """Test synthesizer performance with multiple files."""
        import time

        start_time = time.time()

        # Generate multiple audio files
        for i in range(5):
            notes = [f"C-{4 + i % 2}", f"E-{4 + i % 2}"]
            audio_path = audio_synthesizer.synthesize_notes(notes, 0.5)
            assert os.path.exists(audio_path)

        end_time = time.time()
        duration = end_time - start_time

        # Should complete in reasonable time (less than 5 seconds for 5 files)
        assert duration < 5.0, f"Audio generation took too long: {duration:.2f}s"
