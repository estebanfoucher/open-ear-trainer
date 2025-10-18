"""
Audio synthesis using FluidSynth for generating WAV files from MIDI.
"""

import hashlib
import logging
import os
import tempfile

from django.conf import settings

logger = logging.getLogger(__name__)


class AudioSynthesizer:
    """
    Audio synthesizer using FluidSynth to convert MIDI to WAV files.

    This class handles the synthesis of audio files from MIDI data
    using FluidSynth and SoundFont files.
    """

    def __init__(self, soundfont_path: str | None = None):
        """
        Initialize the audio synthesizer.

        Args:
            soundfont_path: Path to the SoundFont file (.sf2)
        """
        self.soundfont_path = soundfont_path or getattr(
            settings, "SOUNDFONT_PATH", None
        )
        self.cache_enabled = getattr(settings, "AUDIO_CACHE_ENABLED", True)
        self.cache_max_size = getattr(settings, "AUDIO_CACHE_MAX_SIZE", 1000)

        # Resolve relative path to absolute path
        if self.soundfont_path and not os.path.isabs(self.soundfont_path):
            # If it's a relative path, make it relative to the backend directory
            backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.soundfont_path = os.path.join(backend_dir, self.soundfont_path)

        if not self.soundfont_path or not os.path.exists(self.soundfont_path):
            logger.warning(f"SoundFont not found at {self.soundfont_path}")
            self.soundfont_path = None

    def _generate_cache_key(self, content: str) -> str:
        """
        Generate a cache key for audio content.

        Args:
            content: String representation of the audio content

        Returns:
            str: MD5 hash of the content
        """
        return hashlib.md5(content.encode()).hexdigest()

    def _get_cache_path(self, cache_key: str) -> str:
        """
        Get the cache file path for a given cache key.

        Args:
            cache_key: Cache key for the audio file

        Returns:
            str: Full path to the cached audio file
        """
        cache_dir = os.path.join(settings.MEDIA_ROOT, "audio", "cache")
        os.makedirs(cache_dir, exist_ok=True)
        return os.path.join(cache_dir, f"{cache_key}.wav")

    def _is_cached(self, cache_key: str) -> bool:
        """
        Check if an audio file is cached.

        Args:
            cache_key: Cache key to check

        Returns:
            bool: True if the file is cached
        """
        if not self.cache_enabled:
            return False

        cache_path = self._get_cache_path(cache_key)
        return os.path.exists(cache_path)

    def _get_cached_audio(self, cache_key: str) -> str:
        """
        Get the path to a cached audio file.

        Args:
            cache_key: Cache key for the audio file

        Returns:
            str: Path to the cached audio file
        """
        return self._get_cache_path(cache_key)

    def _cache_audio(self, cache_key: str, audio_path: str) -> str:
        """
        Cache an audio file.

        Args:
            cache_key: Cache key for the audio file
            audio_path: Path to the audio file to cache

        Returns:
            str: Path to the cached audio file
        """
        if not self.cache_enabled:
            return audio_path

        cache_path = self._get_cache_path(cache_key)
        cache_dir = os.path.dirname(cache_path)
        os.makedirs(cache_dir, exist_ok=True)

        # Copy the file to cache
        import shutil

        shutil.copy2(audio_path, cache_path)

        return cache_path

    def synthesize_notes(
        self, notes: list[str], duration: float = 2.0, output_path: str | None = None
    ) -> str:
        """
        Synthesize audio from a list of notes.

        Args:
            notes: List of note strings
            duration: Duration of each note in seconds
            output_path: Output file path (optional)

        Returns:
            str: Path to the generated audio file
        """
        # Generate cache key
        content = f"notes:{','.join(notes)}:duration:{duration}"
        cache_key = self._generate_cache_key(content)

        # Check cache first
        if self._is_cached(cache_key):
            return self._get_cached_audio(cache_key)

        # Generate audio file
        if output_path is None:
            # Create file in media directory instead of temp directory
            media_dir = os.path.join(settings.MEDIA_ROOT, "audio")
            os.makedirs(media_dir, exist_ok=True)
            fd, output_path = tempfile.mkstemp(
                suffix=".wav", prefix="notes_", dir=media_dir
            )
            os.close(fd)

        # For now, create a placeholder WAV file
        # In a full implementation, you'd use FluidSynth here
        self._create_placeholder_wav(output_path, duration)

        # Cache the result
        if self.cache_enabled:
            output_path = self._cache_audio(cache_key, output_path)

        return output_path

    def synthesize_chord(
        self, chord_notes: list[str], duration: float = 2.0, output_path: str | None = None
    ) -> str:
        """
        Synthesize audio from a chord.

        Args:
            chord_notes: List of notes in the chord
            duration: Duration of the chord in seconds
            output_path: Output file path (optional)

        Returns:
            str: Path to the generated audio file
        """
        # Generate cache key
        content = f"chord:{','.join(chord_notes)}:duration:{duration}"
        cache_key = self._generate_cache_key(content)

        # Check cache first
        if self._is_cached(cache_key):
            return self._get_cached_audio(cache_key)

        # Generate audio file
        if output_path is None:
            # Create file in media directory instead of temp directory
            media_dir = os.path.join(settings.MEDIA_ROOT, "audio")
            os.makedirs(media_dir, exist_ok=True)
            fd, output_path = tempfile.mkstemp(
                suffix=".wav", prefix="chord_", dir=media_dir
            )
            os.close(fd)

        # Create placeholder WAV file
        self._create_placeholder_wav(output_path, duration)

        # Cache the result
        if self.cache_enabled:
            output_path = self._cache_audio(cache_key, output_path)

        return output_path

    def synthesize_interval(
        self, note1: str, note2: str, duration: float = 2.0, output_path: str | None = None
    ) -> str:
        """
        Synthesize audio from an interval (two notes).

        Args:
            note1: First note of the interval
            note2: Second note of the interval
            duration: Duration of the interval in seconds
            output_path: Output file path (optional)

        Returns:
            str: Path to the generated audio file
        """
        return self.synthesize_chord([note1, note2], duration, output_path)

    def synthesize_melodic_interval(
        self,
        note1: str,
        note2: str,
        note_duration: float = 1.0,
        gap_duration: float = 0.5,
        output_path: str | None = None,
    ) -> str:
        """
        Synthesize audio from a melodic interval (two notes played one after the other).

        Args:
            note1: First note of the interval
            note2: Second note of the interval
            note_duration: Duration of each note in seconds
            gap_duration: Duration of silence between notes in seconds
            output_path: Output file path (optional)

        Returns:
            str: Path to the generated audio file
        """
        # Generate cache key
        content = f"melodic_interval:{note1}:{note2}:duration:{note_duration}:gap:{gap_duration}"
        cache_key = self._generate_cache_key(content)

        # Check cache first
        if self._is_cached(cache_key):
            return self._get_cached_audio(cache_key)

        # Generate audio file
        if output_path is None:
            # Create file in media directory instead of temp directory
            media_dir = os.path.join(settings.MEDIA_ROOT, "audio")
            os.makedirs(media_dir, exist_ok=True)
            fd, output_path = tempfile.mkstemp(
                suffix=".wav", prefix="melodic_interval_", dir=media_dir
            )
            os.close(fd)

        # Create melodic interval WAV file
        self._create_melodic_interval_wav(
            output_path, note1, note2, note_duration, gap_duration
        )

        # Cache the result
        if self.cache_enabled:
            output_path = self._cache_audio(cache_key, output_path)

        return output_path

    def synthesize_harmonic_interval(
        self, note1: str, note2: str, duration: float = 0.5, output_path: str = None
    ) -> str:
        """
        Synthesize audio from a harmonic interval (two notes played simultaneously).

        Args:
            note1: First note of the interval
            note2: Second note of the interval
            duration: Duration of the interval in seconds
            output_path: Output file path (optional)

        Returns:
            str: Path to the generated audio file
        """
        # Generate cache key
        content = f"harmonic_interval:{note1}:{note2}:duration:{duration}"
        cache_key = self._generate_cache_key(content)

        # Check cache first
        if self._is_cached(cache_key):
            return self._get_cached_audio(cache_key)

        # Generate audio file
        if output_path is None:
            # Create file in media directory instead of temp directory
            media_dir = os.path.join(settings.MEDIA_ROOT, "audio")
            os.makedirs(media_dir, exist_ok=True)
            fd, output_path = tempfile.mkstemp(
                suffix=".wav", prefix="harmonic_interval_", dir=media_dir
            )
            os.close(fd)

        # Create harmonic interval WAV file
        self._create_harmonic_interval_wav(output_path, note1, note2, duration)

        # Cache the result
        if self.cache_enabled:
            output_path = self._cache_audio(cache_key, output_path)

        return output_path

    def synthesize_staggered_interval(
        self,
        note1: str,
        note2: str,
        root_duration: float = 1.5,
        second_duration: float = 1.5,
        delay_ms: int = 400,
        output_path: str | None = None,
    ) -> str:
        """
        Synthesize audio from a staggered interval (root note starts before second note).

        Args:
            note1: Root note (starts first)
            note2: Second note (starts after delay)
            root_duration: Duration of the root note in seconds
            second_duration: Duration of the second note in seconds
            delay_ms: Delay in milliseconds before second note starts
            output_path: Output file path (optional)

        Returns:
            str: Path to the generated audio file
        """
        # Generate cache key
        content = f"staggered_interval:{note1}:{note2}:root:{root_duration}:second:{second_duration}:delay:{delay_ms}"
        cache_key = self._generate_cache_key(content)

        # Check cache first
        if self._is_cached(cache_key):
            return self._get_cached_audio(cache_key)

        # Generate audio file
        if output_path is None:
            # Create file in media directory instead of temp directory
            media_dir = os.path.join(settings.MEDIA_ROOT, "audio")
            os.makedirs(media_dir, exist_ok=True)
            fd, output_path = tempfile.mkstemp(
                suffix=".wav", prefix="staggered_interval_", dir=media_dir
            )
            os.close(fd)

        # Create staggered interval WAV file
        self._create_staggered_interval_wav(
            output_path, note1, note2, root_duration, second_duration, delay_ms
        )

        # Cache the result
        if self.cache_enabled:
            output_path = self._cache_audio(cache_key, output_path)

        return output_path

    def synthesize_progression(
        self,
        progression: list[list[str]],
        chord_duration: float = 1.5,
        output_path: str | None = None,
    ) -> str:
        """
        Synthesize audio from a chord progression.

        Args:
            progression: List of chords (each chord is a list of notes)
            chord_duration: Duration of each chord in seconds
            output_path: Output file path (optional)

        Returns:
            str: Path to the generated audio file
        """
        # Generate cache key
        content = f"progression:{len(progression)}:duration:{chord_duration}"
        cache_key = self._generate_cache_key(content)

        # Check cache first
        if self._is_cached(cache_key):
            return self._get_cached_audio(cache_key)

        # Generate audio file
        if output_path is None:
            # Create file in media directory instead of temp directory
            media_dir = os.path.join(settings.MEDIA_ROOT, "audio")
            os.makedirs(media_dir, exist_ok=True)
            fd, output_path = tempfile.mkstemp(
                suffix=".wav", prefix="progression_", dir=media_dir
            )
            os.close(fd)

        # Calculate total duration
        total_duration = len(progression) * chord_duration

        # Create placeholder WAV file
        self._create_placeholder_wav(output_path, total_duration)

        # Cache the result
        if self.cache_enabled:
            output_path = self._cache_audio(cache_key, output_path)

        return output_path

    def _create_placeholder_wav(self, output_path: str, duration: float):
        """
        Create a placeholder WAV file for testing.

        In a real implementation, this would use FluidSynth to generate
        actual audio from MIDI data.

        Args:
            output_path: Path where to save the WAV file
            duration: Duration of the audio in seconds
        """
        import wave

        import numpy as np

        # Audio parameters
        sample_rate = 44100
        num_samples = int(sample_rate * duration)

        # Generate a simple sine wave as placeholder
        frequency = 440  # A4
        t = np.linspace(0, duration, num_samples, False)
        audio_data = np.sin(2 * np.pi * frequency * t)

        # Convert to 16-bit integers
        audio_data = (audio_data * 32767).astype(np.int16)

        # Write WAV file
        with wave.open(output_path, "w") as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(audio_data.tobytes())

        logger.info(f"Created placeholder WAV file: {output_path}")

    def _create_melodic_interval_wav(
        self,
        output_path: str,
        note1: str,
        note2: str,
        note_duration: float,
        gap_duration: float,
    ):
        """
        Create a WAV file for a melodic interval using FluidSynth with real piano sounds.

        Args:
            output_path: Path where to save the WAV file
            note1: First note of the interval
            note2: Second note of the interval
            note_duration: Duration of each note in seconds
            gap_duration: Duration of silence between notes in seconds
        """
        try:
            # Try to use FluidSynth for real piano sounds
            if self.soundfont_path and os.path.exists(self.soundfont_path):
                self._create_fluidsynth_interval(
                    output_path, note1, note2, note_duration, gap_duration
                )
            else:
                # Fallback to synthetic piano sounds
                self._create_synthetic_interval(
                    output_path, note1, note2, note_duration, gap_duration
                )
        except Exception as e:
            logger.warning(f"FluidSynth failed, using synthetic sounds: {e}")
            self._create_synthetic_interval(
                output_path, note1, note2, note_duration, gap_duration
            )

    def _create_fluidsynth_interval(
        self,
        output_path: str,
        note1: str,
        note2: str,
        note_duration: float,
        gap_duration: float,
    ):
        """Create interval using FluidSynth with real piano sounds."""
        import fluidsynth

        # Initialize FluidSynth
        fs = fluidsynth.Synth()
        fs.start(driver="file", filename=output_path)

        # Load SoundFont
        sfid = fs.sfload(self.soundfont_path)
        fs.program_select(0, sfid, 0, 0)  # Use piano (program 0)

        # Convert notes to MIDI numbers
        midi1 = self._note_to_midi_number(note1)
        midi2 = self._note_to_midi_number(note2)

        # Play first note
        fs.noteon(0, midi1, 100)
        fs.sleep(note_duration)
        fs.noteoff(0, midi1)

        # Add gap
        fs.sleep(gap_duration)

        # Play second note
        fs.noteon(0, midi2, 100)
        fs.sleep(note_duration)
        fs.noteoff(0, midi2)

        # Clean up
        fs.delete()

        logger.info(f"Created FluidSynth melodic interval WAV file: {output_path}")

    def _create_synthetic_interval(
        self,
        output_path: str,
        note1: str,
        note2: str,
        note_duration: float,
        gap_duration: float,
    ):
        """Create interval using synthetic piano sounds (fallback)."""
        import wave

        import numpy as np

        # Audio parameters
        sample_rate = 44100
        note_samples = int(sample_rate * note_duration)
        gap_samples = int(sample_rate * gap_duration)

        # Convert notes to frequencies
        freq1 = self._note_to_frequency(note1)
        freq2 = self._note_to_frequency(note2)

        # Generate time arrays
        t1 = np.linspace(0, note_duration, note_samples, False)
        t2 = np.linspace(0, note_duration, note_samples, False)

        # Generate audio for each note with piano-like envelope
        audio1 = self._generate_piano_tone(freq1, t1)
        audio2 = self._generate_piano_tone(freq2, t2)

        # Create silence for the gap
        silence = np.zeros(gap_samples)

        # Combine: note1 + silence + note2
        combined_audio = np.concatenate([audio1, silence, audio2])

        # Convert to 16-bit integers
        audio_data = (combined_audio * 32767).astype(np.int16)

        # Write WAV file
        with wave.open(output_path, "w") as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(audio_data.tobytes())

        logger.info(f"Created synthetic melodic interval WAV file: {output_path}")

    def _create_harmonic_interval_wav(
        self, output_path: str, note1: str, note2: str, duration: float
    ):
        """
        Create a WAV file for a harmonic interval (two notes played simultaneously).

        Args:
            output_path: Path where to save the WAV file
            note1: First note of the interval
            note2: Second note of the interval
            duration: Duration of the interval in seconds
        """
        try:
            # Try to use FluidSynth for real piano sounds
            if self.soundfont_path and os.path.exists(self.soundfont_path):
                self._create_fluidsynth_harmonic_interval(
                    output_path, note1, note2, duration
                )
            else:
                # Fallback to synthetic piano sounds
                self._create_synthetic_harmonic_interval(
                    output_path, note1, note2, duration
                )
        except Exception as e:
            logger.warning(f"FluidSynth failed, using synthetic sounds: {e}")
            self._create_synthetic_harmonic_interval(
                output_path, note1, note2, duration
            )

    def _create_fluidsynth_harmonic_interval(
        self, output_path: str, note1: str, note2: str, duration: float
    ):
        """Create harmonic interval using FluidSynth with real piano sounds."""
        import fluidsynth

        # Initialize FluidSynth
        fs = fluidsynth.Synth()
        fs.start(driver="file", filename=output_path)

        # Load SoundFont
        sfid = fs.sfload(self.soundfont_path)
        fs.program_select(0, sfid, 0, 0)  # Use piano (program 0)

        # Convert notes to MIDI numbers
        midi1 = self._note_to_midi_number(note1)
        midi2 = self._note_to_midi_number(note2)

        # Play both notes simultaneously
        fs.noteon(0, midi1, 100)
        fs.noteon(0, midi2, 100)
        fs.sleep(duration)
        fs.noteoff(0, midi1)
        fs.noteoff(0, midi2)

        # Clean up
        fs.delete()

        logger.info(f"Created FluidSynth harmonic interval WAV file: {output_path}")

    def _create_synthetic_harmonic_interval(
        self, output_path: str, note1: str, note2: str, duration: float
    ):
        """Create harmonic interval using synthetic piano sounds (fallback)."""
        import wave

        import numpy as np

        # Audio parameters
        sample_rate = 44100
        total_samples = int(sample_rate * duration)

        # Convert notes to frequencies
        freq1 = self._note_to_frequency(note1)
        freq2 = self._note_to_frequency(note2)

        # Generate time array
        t = np.linspace(0, duration, total_samples, False)

        # Generate audio for both notes
        audio1 = self._generate_piano_tone(freq1, t)
        audio2 = self._generate_piano_tone(freq2, t)

        # Mix both notes together
        combined_audio = (audio1 + audio2) / 2  # Average to prevent clipping

        # Convert to 16-bit integers
        audio_data = (combined_audio * 32767).astype(np.int16)

        # Write WAV file
        with wave.open(output_path, "w") as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(audio_data.tobytes())

        logger.info(f"Created synthetic harmonic interval WAV file: {output_path}")

    def _create_staggered_interval_wav(
        self,
        output_path: str,
        note1: str,
        note2: str,
        root_duration: float,
        second_duration: float,
        delay_ms: int,
    ):
        """
        Create a WAV file for a staggered interval (root note starts before second note).

        Args:
            output_path: Path where to save the WAV file
            note1: Root note (starts first)
            note2: Second note (starts after delay)
            root_duration: Duration of the root note in seconds
            second_duration: Duration of the second note in seconds
            delay_ms: Delay in milliseconds before second note starts
        """
        try:
            # Try to use FluidSynth for real piano sounds
            if self.soundfont_path and os.path.exists(self.soundfont_path):
                self._create_fluidsynth_staggered_interval(
                    output_path, note1, note2, root_duration, second_duration, delay_ms
                )
            else:
                # Fallback to synthetic piano sounds
                self._create_synthetic_staggered_interval(
                    output_path, note1, note2, root_duration, second_duration, delay_ms
                )
        except Exception as e:
            logger.warning(f"FluidSynth failed, using synthetic sounds: {e}")
            self._create_synthetic_staggered_interval(
                output_path, note1, note2, root_duration, second_duration, delay_ms
            )

    def _create_fluidsynth_staggered_interval(
        self,
        output_path: str,
        note1: str,
        note2: str,
        root_duration: float,
        second_duration: float,
        delay_ms: int,
    ):
        """Create staggered interval using FluidSynth with real piano sounds."""
        import fluidsynth

        # Initialize FluidSynth
        fs = fluidsynth.Synth()
        fs.start(driver="file", filename=output_path)

        # Load SoundFont
        sfid = fs.sfload(self.soundfont_path)
        fs.program_select(0, sfid, 0, 0)  # Use piano (program 0)

        # Convert notes to MIDI numbers
        midi1 = self._note_to_midi_number(note1)
        midi2 = self._note_to_midi_number(note2)

        # Play root note first
        fs.noteon(0, midi1, 100)
        fs.sleep(root_duration)
        fs.noteoff(0, midi1)

        # Add delay before second note
        delay_seconds = delay_ms / 1000.0
        fs.sleep(delay_seconds)

        # Play second note
        fs.noteon(0, midi2, 100)
        fs.sleep(second_duration)
        fs.noteoff(0, midi2)

        # Clean up
        fs.delete()

        logger.info(f"Created FluidSynth staggered interval WAV file: {output_path}")

    def _create_synthetic_staggered_interval(
        self,
        output_path: str,
        note1: str,
        note2: str,
        root_duration: float,
        second_duration: float,
        delay_ms: int,
    ):
        """Create staggered interval using synthetic piano sounds (fallback)."""
        import wave

        import numpy as np

        # Audio parameters
        sample_rate = 44100
        delay_seconds = delay_ms / 1000.0

        # Calculate total duration
        total_duration = max(root_duration, delay_seconds + second_duration)
        total_samples = int(sample_rate * total_duration)

        # Convert notes to frequencies
        freq1 = self._note_to_frequency(note1)
        freq2 = self._note_to_frequency(note2)

        # Generate time arrays
        t1 = np.linspace(0, root_duration, int(sample_rate * root_duration), False)
        t2 = np.linspace(0, second_duration, int(sample_rate * second_duration), False)

        # Generate audio for each note with piano-like envelope
        audio1 = self._generate_piano_tone(freq1, t1)
        audio2 = self._generate_piano_tone(freq2, t2)

        # Create the combined audio array
        combined_audio = np.zeros(total_samples)

        # Add root note at the beginning
        root_samples = len(audio1)
        combined_audio[:root_samples] = audio1

        # Add second note after delay
        delay_samples = int(sample_rate * delay_seconds)
        second_start = delay_samples
        second_end = second_start + len(audio2)
        if second_end <= total_samples:
            combined_audio[second_start:second_end] += audio2

        # Convert to 16-bit integers
        audio_data = (combined_audio * 32767).astype(np.int16)

        # Write WAV file
        with wave.open(output_path, "w") as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(audio_data.tobytes())

        logger.info(f"Created synthetic staggered interval WAV file: {output_path}")

    def _note_to_midi_number(self, note: str) -> int:
        """
        Convert a note string to MIDI note number.

        Args:
            note: Note string (e.g., "C-4", "F#-5")

        Returns:
            int: MIDI note number (0-127)
        """
        # Parse note and octave
        if "-" in note:
            base_note, octave_str = note.split("-")
            octave = int(octave_str)
        else:
            base_note = note
            octave = 4  # Default octave

        # Note mapping (C=0, C#=1, D=2, etc.)
        note_map = {
            "C": 0,
            "C#": 1,
            "Db": 1,
            "D": 2,
            "D#": 3,
            "Eb": 3,
            "E": 4,
            "F": 5,
            "F#": 6,
            "Gb": 6,
            "G": 7,
            "G#": 8,
            "Ab": 8,
            "A": 9,
            "A#": 10,
            "Bb": 10,
            "B": 11,
        }

        # Calculate MIDI number
        note_semitones = note_map.get(base_note, 0)
        midi_number = (octave + 1) * 12 + note_semitones

        return midi_number

    def _note_to_frequency(self, note: str) -> float:
        """
        Convert a note string to frequency in Hz.

        Args:
            note: Note string (e.g., "C-4", "F#-5")

        Returns:
            float: Frequency in Hz
        """
        # A4 = 440 Hz
        a4_freq = 440.0

        # Note mapping (C=0, C#=1, D=2, etc.)
        note_map = {
            "C": 0,
            "C#": 1,
            "Db": 1,
            "D": 2,
            "D#": 3,
            "Eb": 3,
            "E": 4,
            "F": 5,
            "F#": 6,
            "Gb": 6,
            "G": 7,
            "G#": 8,
            "Ab": 8,
            "A": 9,
            "A#": 10,
            "Bb": 10,
            "B": 11,
        }

        # Parse note and octave
        if "-" in note:
            note_name, octave_str = note.split("-")
            octave = int(octave_str)
        else:
            note_name = note
            octave = 4  # Default octave

        # Calculate semitones from A4
        note_semitones = note_map.get(note_name, 9)  # Default to A
        octave_semitones = (octave - 4) * 12
        total_semitones = note_semitones + octave_semitones - 9  # A4 is reference

        # Calculate frequency
        frequency = a4_freq * (2 ** (total_semitones / 12.0))

        return frequency

    def _generate_piano_tone(self, frequency: float, time_array):
        """
        Generate a piano-like tone with attack and decay envelope.

        Args:
            frequency: Frequency in Hz
            time_array: Time array for the note

        Returns:
            np.ndarray: Audio samples
        """
        import numpy as np

        # Generate base sine wave
        audio = np.sin(2 * np.pi * frequency * time_array)

        # Add harmonics for piano-like sound
        audio += 0.3 * np.sin(2 * np.pi * frequency * 2 * time_array)  # Octave
        audio += 0.1 * np.sin(2 * np.pi * frequency * 3 * time_array)  # Fifth

        # Apply piano-like envelope (quick attack, slow decay)
        envelope = np.exp(-time_array * 3) * (1 - np.exp(-time_array * 20))

        # Apply envelope
        audio *= envelope

        # Normalize
        if np.max(np.abs(audio)) > 0:
            audio = audio / np.max(np.abs(audio)) * 0.7

        return audio

    def get_audio_url(self, audio_path: str) -> str:
        """
        Get the URL for an audio file.

        Args:
            audio_path: Path to the audio file

        Returns:
            str: URL to access the audio file
        """
        # Convert absolute path to relative path from MEDIA_ROOT
        media_root_str = str(settings.MEDIA_ROOT)
        if audio_path.startswith(media_root_str):
            relative_path = os.path.relpath(audio_path, media_root_str)
            return f"{settings.MEDIA_URL}{relative_path}"

        return audio_path
