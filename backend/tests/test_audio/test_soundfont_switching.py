"""
Tests for soundfont switching functionality.
"""

import os

from audio_app.synthesizer import AudioSynthesizer


class TestSoundfontSwitching:
    """Test soundfont switching and configuration."""

    def test_synthesizer_with_different_soundfont_paths(self, temp_media_dir):
        """Test synthesizer with different soundfont paths."""
        # Test with None (no soundfont)
        synthesizer1 = AudioSynthesizer(soundfont_path=None)
        assert synthesizer1.soundfont_path is None

        # Test with nonexistent path
        synthesizer2 = AudioSynthesizer(soundfont_path="/nonexistent/path.sf2")
        assert synthesizer2.soundfont_path is None

        # Test with empty string
        synthesizer3 = AudioSynthesizer(soundfont_path="")
        assert synthesizer3.soundfont_path is None

    def test_soundfont_switching_at_runtime(self, temp_media_dir):
        """Test changing soundfont path at runtime."""
        synthesizer = AudioSynthesizer()

        # Initially no soundfont
        assert synthesizer.soundfont_path is None

        # Create dummy soundfont files
        soundfont1 = os.path.join(temp_media_dir, "soundfont1.sf2")
        soundfont2 = os.path.join(temp_media_dir, "soundfont2.sf2")

        with open(soundfont1, "w") as f:
            f.write("soundfont1 content")
        with open(soundfont2, "w") as f:
            f.write("soundfont2 content")

        # Switch to first soundfont
        synthesizer.soundfont_path = soundfont1
        assert synthesizer.soundfont_path == soundfont1

        # Switch to second soundfont
        synthesizer.soundfont_path = soundfont2
        assert synthesizer.soundfont_path == soundfont2

        # Switch back to None
        synthesizer.soundfont_path = None
        assert synthesizer.soundfont_path is None

    def test_audio_generation_with_different_soundfonts(self, temp_media_dir):
        """Test audio generation with different soundfont configurations."""
        # Create dummy soundfont files
        soundfont1 = os.path.join(temp_media_dir, "piano.sf2")
        soundfont2 = os.path.join(temp_media_dir, "organ.sf2")

        with open(soundfont1, "w") as f:
            f.write("piano soundfont")
        with open(soundfont2, "w") as f:
            f.write("organ soundfont")

        # Test with first soundfont
        synthesizer1 = AudioSynthesizer(soundfont_path=soundfont1)
        audio1 = synthesizer1.synthesize_notes(["C-4", "E-4"], 1.0)
        assert os.path.exists(audio1)

        # Test with second soundfont
        synthesizer2 = AudioSynthesizer(soundfont_path=soundfont2)
        audio2 = synthesizer2.synthesize_notes(["C-4", "E-4"], 1.0)
        assert os.path.exists(audio2)

        # Test without soundfont (should use synthetic)
        synthesizer3 = AudioSynthesizer(soundfont_path=None)
        audio3 = synthesizer3.synthesize_notes(["C-4", "E-4"], 1.0)
        assert os.path.exists(audio3)

    def test_soundfont_validation(self, temp_media_dir):
        """Test soundfont file validation."""
        # Create a valid-looking soundfont file
        valid_soundfont = os.path.join(temp_media_dir, "valid.sf2")
        with open(valid_soundfont, "w") as f:
            f.write("RIFF" + " " * 1000)  # Minimal RIFF header

        synthesizer = AudioSynthesizer(soundfont_path=valid_soundfont)
        assert synthesizer.soundfont_path == valid_soundfont

        # Test with non-existent file
        nonexistent = os.path.join(temp_media_dir, "nonexistent.sf2")
        synthesizer2 = AudioSynthesizer(soundfont_path=nonexistent)
        assert synthesizer2.soundfont_path is None

    def test_soundfont_environment_detection(self, monkeypatch):
        """Test soundfont behavior in different environments."""
        # Test Docker environment
        monkeypatch.setenv("DOCKER", "true")
        synthesizer1 = AudioSynthesizer()
        # Should use synthetic sounds in Docker
        audio1 = synthesizer1.synthesize_notes(["C-4", "E-4"], 1.0)
        assert os.path.exists(audio1)

        # Test headless environment (no DISPLAY)
        monkeypatch.delenv("DOCKER", raising=False)
        monkeypatch.delenv("DISPLAY", raising=False)
        synthesizer2 = AudioSynthesizer()
        # Should use synthetic sounds in headless environment
        audio2 = synthesizer2.synthesize_notes(["C-4", "E-4"], 1.0)
        assert os.path.exists(audio2)

    def test_soundfont_fallback_behavior(self, temp_media_dir):
        """Test fallback behavior when soundfont fails."""
        # Create a soundfont file that will cause FluidSynth to fail
        bad_soundfont = os.path.join(temp_media_dir, "bad.sf2")
        with open(bad_soundfont, "w") as f:
            f.write("invalid soundfont content")

        synthesizer = AudioSynthesizer(soundfont_path=bad_soundfont)

        # Should fallback to synthetic sounds when FluidSynth fails
        audio = synthesizer.synthesize_notes(["C-4", "E-4"], 1.0)
        assert os.path.exists(audio)

    def test_multiple_synthesizers_different_soundfonts(self, temp_media_dir):
        """Test multiple synthesizers with different soundfonts."""
        # Create different soundfont files
        soundfonts = []
        for i in range(3):
            soundfont_path = os.path.join(temp_media_dir, f"soundfont_{i}.sf2")
            with open(soundfont_path, "w") as f:
                f.write(f"soundfont {i} content")
            soundfonts.append(soundfont_path)

        # Create synthesizers with different soundfonts
        synthesizers = []
        for soundfont in soundfonts:
            synthesizer = AudioSynthesizer(soundfont_path=soundfont)
            synthesizers.append(synthesizer)

        # Generate audio with each synthesizer
        audio_files = []
        for synthesizer in synthesizers:
            audio = synthesizer.synthesize_notes(["C-4", "E-4"], 1.0)
            audio_files.append(audio)
            assert os.path.exists(audio)

        # All files should exist
        assert len(audio_files) == 3
        for audio in audio_files:
            assert os.path.exists(audio)

    def test_soundfont_configuration_persistence(self, temp_media_dir):
        """Test that soundfont configuration persists across operations."""
        soundfont_path = os.path.join(temp_media_dir, "persistent.sf2")
        with open(soundfont_path, "w") as f:
            f.write("persistent soundfont")

        synthesizer = AudioSynthesizer(soundfont_path=soundfont_path)

        # Perform multiple operations
        for i in range(5):
            audio = synthesizer.synthesize_notes(
                [f"C-{4 + i % 2}", f"E-{4 + i % 2}"], 0.5
            )
            assert os.path.exists(audio)
            # Soundfont path should remain the same
            assert synthesizer.soundfont_path == soundfont_path

    def test_soundfont_switching_affects_audio_generation(self, temp_media_dir):
        """Test that switching soundfonts affects audio generation."""
        # Create different soundfont files
        soundfont1 = os.path.join(temp_media_dir, "piano.sf2")
        soundfont2 = os.path.join(temp_media_dir, "strings.sf2")

        with open(soundfont1, "w") as f:
            f.write("piano soundfont content")
        with open(soundfont2, "w") as f:
            f.write("strings soundfont content")

        synthesizer = AudioSynthesizer()

        # Generate audio with first soundfont
        synthesizer.soundfont_path = soundfont1
        audio1 = synthesizer.synthesize_notes(["C-4", "E-4"], 1.0)

        # Generate audio with second soundfont
        synthesizer.soundfont_path = soundfont2
        audio2 = synthesizer.synthesize_notes(["C-4", "E-4"], 1.0)

        # Both should exist and be different files
        assert os.path.exists(audio1)
        assert os.path.exists(audio2)
        assert audio1 != audio2
