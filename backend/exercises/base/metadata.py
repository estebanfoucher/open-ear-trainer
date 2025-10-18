"""
Exercise metadata definitions for the ear trainer.
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class ExerciseMetadata:
    """Metadata for an exercise defining its properties and requirements."""

    # Basic identification
    id: str
    name: str
    description: str

    # Difficulty and progression
    difficulty: int  # 1-10 scale
    prerequisites: list[str]  # List of exercise IDs that must be completed first
    learning_objectives: list[str]  # What the student will learn

    # Exercise properties
    estimated_time: int  # Estimated time in seconds
    category: str  # e.g., "pitch_recognition", "rhythm", "harmony"
    tags: list[str]  # Searchable tags

    # UI configuration
    input_type: str  # "multiple_choice", "piano_keyboard", "text_input", etc.
    answer_format: str  # "scale_degree", "note_name", "chord_quality", etc.

    # Audio requirements
    requires_progression: bool = False  # Does it need chord progression?
    requires_single_note: bool = True  # Does it need single note playback?
    audio_duration: int = 2  # Default audio duration in seconds

    # Configuration options
    config_options: dict[str, Any] | None = None  # Exercise-specific configuration

    def __post_init__(self):
        """Initialize default values."""
        if self.config_options is None:
            self.config_options = {}


@dataclass
class ExerciseResult:
    """Result of an exercise attempt."""

    is_correct: bool
    user_answer: Any
    correct_answer: Any
    feedback: str
    hints_used: list[str] | None = None
    time_taken: int | None = None  # Time in seconds

    def __post_init__(self):
        """Initialize default values."""
        if self.hints_used is None:
            self.hints_used = []


@dataclass
class ExerciseData:
    """Data structure for exercise content."""

    # Context information
    key: str  # Musical key (e.g., "C major")
    scale: list[str]  # Scale notes

    # Audio files
    progression_audio: str | None = None  # URL to progression audio
    target_audio: str | None = None  # URL to target audio

    # Answer options
    options: list[Any] | None = None  # Available answer choices
    correct_answer: Any = None  # The correct answer

    # Additional context
    context: dict[str, Any] | None = None  # Additional exercise-specific data

    def __post_init__(self):
        """Initialize default values."""
        if self.options is None:
            self.options = []
        if self.context is None:
            self.context = {}
