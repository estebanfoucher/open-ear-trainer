"""
Tests for hierarchical chapter/lesson/exercise structure.
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class Chapter:
    """Chapter model for organizing lessons."""

    id: str
    name: str
    description: str
    difficulty: int
    lessons: list["Lesson"]
    prerequisites: list[str] = None
    estimated_time: int = 0
    learning_objectives: list[str] = None

    def __post_init__(self):
        if self.prerequisites is None:
            self.prerequisites = []
        if self.learning_objectives is None:
            self.learning_objectives = []


@dataclass
class Lesson:
    """Lesson model for organizing exercises."""

    id: str
    name: str
    description: str
    difficulty: int
    exercises: list[str]  # Exercise IDs
    chapter_id: str
    prerequisites: list[str] = None
    estimated_time: int = 0
    learning_objectives: list[str] = None
    completion_criteria: dict[str, Any] = None

    def __post_init__(self):
        if self.prerequisites is None:
            self.prerequisites = []
        if self.learning_objectives is None:
            self.learning_objectives = []
        if self.completion_criteria is None:
            self.completion_criteria = {"min_score": 80, "min_attempts": 1}


class ChapterLessonRegistry:
    """Registry for managing chapters, lessons, and exercises."""

    def __init__(self):
        self.chapters: dict[str, Chapter] = {}
        self.lessons: dict[str, Lesson] = {}
        self.exercises: dict[str, Any] = {}  # Will hold exercise instances

    def add_chapter(self, chapter: Chapter):
        """Add a chapter to the registry."""
        self.chapters[chapter.id] = chapter
        for lesson in chapter.lessons:
            self.lessons[lesson.id] = lesson

    def get_chapter(self, chapter_id: str) -> Chapter | None:
        """Get a chapter by ID."""
        return self.chapters.get(chapter_id)

    def get_lesson(self, lesson_id: str) -> Lesson | None:
        """Get a lesson by ID."""
        return self.lessons.get(lesson_id)

    def get_chapters(self) -> list[Chapter]:
        """Get all chapters."""
        return list(self.chapters.values())

    def get_lessons_in_chapter(self, chapter_id: str) -> list[Lesson]:
        """Get all lessons in a chapter."""
        chapter = self.get_chapter(chapter_id)
        return chapter.lessons if chapter else []

    def get_exercises_in_lesson(self, lesson_id: str) -> list[str]:
        """Get all exercise IDs in a lesson."""
        lesson = self.get_lesson(lesson_id)
        return lesson.exercises if lesson else []

    def validate_prerequisites(
        self, chapter_id: str, completed_chapters: list[str]
    ) -> bool:
        """Validate if prerequisites are met for a chapter."""
        chapter = self.get_chapter(chapter_id)
        if not chapter:
            return False

        return all(prereq in completed_chapters for prereq in chapter.prerequisites)

    def get_next_lesson(
        self, chapter_id: str, completed_lessons: list[str]
    ) -> Lesson | None:
        """Get the next lesson to complete in a chapter."""
        lessons = self.get_lessons_in_chapter(chapter_id)
        for lesson in lessons:
            if lesson.id not in completed_lessons and all(
                prereq in completed_lessons for prereq in lesson.prerequisites
            ):
                return lesson
        return None

    def calculate_chapter_progress(
        self, chapter_id: str, completed_lessons: list[str]
    ) -> float:
        """Calculate progress percentage for a chapter."""
        lessons = self.get_lessons_in_chapter(chapter_id)
        if not lessons:
            return 0.0

        completed_count = sum(1 for lesson in lessons if lesson.id in completed_lessons)
        return (completed_count / len(lessons)) * 100.0


class TestChapterModel:
    """Test Chapter model."""

    def test_chapter_creation(self):
        """Test basic chapter creation."""
        chapter = Chapter(
            id="chapter_1",
            name="Basic Intervals",
            description="Learn to identify basic intervals",
            difficulty=1,
            lessons=[],
        )

        assert chapter.id == "chapter_1"
        assert chapter.name == "Basic Intervals"
        assert chapter.difficulty == 1
        assert chapter.lessons == []
        assert chapter.prerequisites == []
        assert chapter.learning_objectives == []

    def test_chapter_with_prerequisites(self):
        """Test chapter with prerequisites."""
        chapter = Chapter(
            id="chapter_2",
            name="Advanced Intervals",
            description="Learn advanced intervals",
            difficulty=3,
            lessons=[],
            prerequisites=["chapter_1"],
            learning_objectives=["Master all intervals"],
        )

        assert chapter.prerequisites == ["chapter_1"]
        assert chapter.learning_objectives == ["Master all intervals"]

    def test_chapter_with_lessons(self):
        """Test chapter with lessons."""
        lesson1 = Lesson(
            id="lesson_1_1",
            name="Perfect Intervals",
            description="Learn perfect intervals",
            difficulty=1,
            exercises=["perfect_fourth_fifth_octave_melodic"],
            chapter_id="chapter_1",
        )

        lesson2 = Lesson(
            id="lesson_1_2",
            name="Third Intervals",
            description="Learn third intervals",
            difficulty=2,
            exercises=["minor_third_major_third_octave_melodic"],
            chapter_id="chapter_1",
        )

        chapter = Chapter(
            id="chapter_1",
            name="Basic Intervals",
            description="Learn basic intervals",
            difficulty=1,
            lessons=[lesson1, lesson2],
        )

        assert len(chapter.lessons) == 2
        assert chapter.lessons[0].id == "lesson_1_1"
        assert chapter.lessons[1].id == "lesson_1_2"


class TestLessonModel:
    """Test Lesson model."""

    def test_lesson_creation(self):
        """Test basic lesson creation."""
        lesson = Lesson(
            id="lesson_1_1",
            name="Perfect Intervals",
            description="Learn perfect intervals",
            difficulty=1,
            exercises=["perfect_fourth_fifth_octave_melodic"],
            chapter_id="chapter_1",
        )

        assert lesson.id == "lesson_1_1"
        assert lesson.name == "Perfect Intervals"
        assert lesson.difficulty == 1
        assert lesson.exercises == ["perfect_fourth_fifth_octave_melodic"]
        assert lesson.chapter_id == "chapter_1"
        assert lesson.prerequisites == []
        assert lesson.learning_objectives == []

    def test_lesson_with_completion_criteria(self):
        """Test lesson with custom completion criteria."""
        lesson = Lesson(
            id="lesson_1_1",
            name="Perfect Intervals",
            description="Learn perfect intervals",
            difficulty=1,
            exercises=["perfect_fourth_fifth_octave_melodic"],
            chapter_id="chapter_1",
            completion_criteria={"min_score": 90, "min_attempts": 3},
        )

        assert lesson.completion_criteria["min_score"] == 90
        assert lesson.completion_criteria["min_attempts"] == 3

    def test_lesson_with_prerequisites(self):
        """Test lesson with prerequisites."""
        lesson = Lesson(
            id="lesson_1_2",
            name="Third Intervals",
            description="Learn third intervals",
            difficulty=2,
            exercises=["minor_third_major_third_octave_melodic"],
            chapter_id="chapter_1",
            prerequisites=["lesson_1_1"],
            learning_objectives=["Identify minor and major thirds"],
        )

        assert lesson.prerequisites == ["lesson_1_1"]
        assert lesson.learning_objectives == ["Identify minor and major thirds"]


class TestChapterLessonRegistry:
    """Test ChapterLessonRegistry."""

    def test_registry_initialization(self):
        """Test registry initialization."""
        registry = ChapterLessonRegistry()

        assert registry.chapters == {}
        assert registry.lessons == {}
        assert registry.exercises == {}

    def test_add_chapter(self):
        """Test adding a chapter to the registry."""
        registry = ChapterLessonRegistry()

        lesson1 = Lesson(
            id="lesson_1_1",
            name="Perfect Intervals",
            description="Learn perfect intervals",
            difficulty=1,
            exercises=["perfect_fourth_fifth_octave_melodic"],
            chapter_id="chapter_1",
        )

        lesson2 = Lesson(
            id="lesson_1_2",
            name="Third Intervals",
            description="Learn third intervals",
            difficulty=2,
            exercises=["minor_third_major_third_octave_melodic"],
            chapter_id="chapter_1",
        )

        chapter = Chapter(
            id="chapter_1",
            name="Basic Intervals",
            description="Learn basic intervals",
            difficulty=1,
            lessons=[lesson1, lesson2],
        )

        registry.add_chapter(chapter)

        assert "chapter_1" in registry.chapters
        assert "lesson_1_1" in registry.lessons
        assert "lesson_1_2" in registry.lessons
        assert registry.chapters["chapter_1"] == chapter
        assert registry.lessons["lesson_1_1"] == lesson1
        assert registry.lessons["lesson_1_2"] == lesson2

    def test_get_chapter(self):
        """Test getting a chapter by ID."""
        registry = ChapterLessonRegistry()

        chapter = Chapter(
            id="chapter_1",
            name="Basic Intervals",
            description="Learn basic intervals",
            difficulty=1,
            lessons=[],
        )

        registry.add_chapter(chapter)

        retrieved_chapter = registry.get_chapter("chapter_1")
        assert retrieved_chapter == chapter

        nonexistent_chapter = registry.get_chapter("nonexistent")
        assert nonexistent_chapter is None

    def test_get_lesson(self):
        """Test getting a lesson by ID."""
        registry = ChapterLessonRegistry()

        lesson = Lesson(
            id="lesson_1_1",
            name="Perfect Intervals",
            description="Learn perfect intervals",
            difficulty=1,
            exercises=["perfect_fourth_fifth_octave_melodic"],
            chapter_id="chapter_1",
        )

        chapter = Chapter(
            id="chapter_1",
            name="Basic Intervals",
            description="Learn basic intervals",
            difficulty=1,
            lessons=[lesson],
        )

        registry.add_chapter(chapter)

        retrieved_lesson = registry.get_lesson("lesson_1_1")
        assert retrieved_lesson == lesson

        nonexistent_lesson = registry.get_lesson("nonexistent")
        assert nonexistent_lesson is None

    def test_get_lessons_in_chapter(self):
        """Test getting lessons in a chapter."""
        registry = ChapterLessonRegistry()

        lesson1 = Lesson(
            id="lesson_1_1",
            name="Perfect Intervals",
            description="Learn perfect intervals",
            difficulty=1,
            exercises=["perfect_fourth_fifth_octave_melodic"],
            chapter_id="chapter_1",
        )

        lesson2 = Lesson(
            id="lesson_1_2",
            name="Third Intervals",
            description="Learn third intervals",
            difficulty=2,
            exercises=["minor_third_major_third_octave_melodic"],
            chapter_id="chapter_1",
        )

        chapter = Chapter(
            id="chapter_1",
            name="Basic Intervals",
            description="Learn basic intervals",
            difficulty=1,
            lessons=[lesson1, lesson2],
        )

        registry.add_chapter(chapter)

        lessons = registry.get_lessons_in_chapter("chapter_1")
        assert len(lessons) == 2
        assert lesson1 in lessons
        assert lesson2 in lessons

        # Test with nonexistent chapter
        lessons = registry.get_lessons_in_chapter("nonexistent")
        assert lessons == []

    def test_get_exercises_in_lesson(self):
        """Test getting exercises in a lesson."""
        registry = ChapterLessonRegistry()

        lesson = Lesson(
            id="lesson_1_1",
            name="Perfect Intervals",
            description="Learn perfect intervals",
            difficulty=1,
            exercises=[
                "perfect_fourth_fifth_octave_melodic",
                "perfect_fourth_fifth_octave_harmonic",
            ],
            chapter_id="chapter_1",
        )

        chapter = Chapter(
            id="chapter_1",
            name="Basic Intervals",
            description="Learn basic intervals",
            difficulty=1,
            lessons=[lesson],
        )

        registry.add_chapter(chapter)

        exercises = registry.get_exercises_in_lesson("lesson_1_1")
        assert exercises == [
            "perfect_fourth_fifth_octave_melodic",
            "perfect_fourth_fifth_octave_harmonic",
        ]

        # Test with nonexistent lesson
        exercises = registry.get_exercises_in_lesson("nonexistent")
        assert exercises == []

    def test_validate_prerequisites(self):
        """Test prerequisite validation."""
        registry = ChapterLessonRegistry()

        # Chapter with no prerequisites
        chapter1 = Chapter(
            id="chapter_1",
            name="Basic Intervals",
            description="Learn basic intervals",
            difficulty=1,
            lessons=[],
        )

        # Chapter with prerequisites
        chapter2 = Chapter(
            id="chapter_2",
            name="Advanced Intervals",
            description="Learn advanced intervals",
            difficulty=3,
            lessons=[],
            prerequisites=["chapter_1"],
        )

        registry.add_chapter(chapter1)
        registry.add_chapter(chapter2)

        # Test chapter with no prerequisites
        assert registry.validate_prerequisites("chapter_1", []) is True
        assert registry.validate_prerequisites("chapter_1", ["chapter_2"]) is True

        # Test chapter with prerequisites - not met
        assert registry.validate_prerequisites("chapter_2", []) is False

        # Test chapter with prerequisites - met
        assert registry.validate_prerequisites("chapter_2", ["chapter_1"]) is True

        # Test chapter with prerequisites - partially met
        assert (
            registry.validate_prerequisites("chapter_2", ["chapter_1", "chapter_3"])
            is True
        )

        # Test nonexistent chapter
        assert registry.validate_prerequisites("nonexistent", ["chapter_1"]) is False

    def test_get_next_lesson(self):
        """Test getting the next lesson to complete."""
        registry = ChapterLessonRegistry()

        lesson1 = Lesson(
            id="lesson_1_1",
            name="Perfect Intervals",
            description="Learn perfect intervals",
            difficulty=1,
            exercises=["perfect_fourth_fifth_octave_melodic"],
            chapter_id="chapter_1",
        )

        lesson2 = Lesson(
            id="lesson_1_2",
            name="Third Intervals",
            description="Learn third intervals",
            difficulty=2,
            exercises=["minor_third_major_third_octave_melodic"],
            chapter_id="chapter_1",
            prerequisites=["lesson_1_1"],
        )

        chapter = Chapter(
            id="chapter_1",
            name="Basic Intervals",
            description="Learn basic intervals",
            difficulty=1,
            lessons=[lesson1, lesson2],
        )

        registry.add_chapter(chapter)

        # No lessons completed - should get first lesson
        next_lesson = registry.get_next_lesson("chapter_1", [])
        assert next_lesson == lesson1

        # First lesson completed - should get second lesson
        next_lesson = registry.get_next_lesson("chapter_1", ["lesson_1_1"])
        assert next_lesson == lesson2

        # Both lessons completed - should return None
        next_lesson = registry.get_next_lesson(
            "chapter_1", ["lesson_1_1", "lesson_1_2"]
        )
        assert next_lesson is None

        # Test with nonexistent chapter
        next_lesson = registry.get_next_lesson("nonexistent", [])
        assert next_lesson is None

    def test_calculate_chapter_progress(self):
        """Test calculating chapter progress."""
        registry = ChapterLessonRegistry()

        lesson1 = Lesson(
            id="lesson_1_1",
            name="Perfect Intervals",
            description="Learn perfect intervals",
            difficulty=1,
            exercises=["perfect_fourth_fifth_octave_melodic"],
            chapter_id="chapter_1",
        )

        lesson2 = Lesson(
            id="lesson_1_2",
            name="Third Intervals",
            description="Learn third intervals",
            difficulty=2,
            exercises=["minor_third_major_third_octave_melodic"],
            chapter_id="chapter_1",
        )

        lesson3 = Lesson(
            id="lesson_1_3",
            name="Combined Intervals",
            description="Learn combined intervals",
            difficulty=3,
            exercises=["combined_intervals_melodic"],
            chapter_id="chapter_1",
        )

        chapter = Chapter(
            id="chapter_1",
            name="Basic Intervals",
            description="Learn basic intervals",
            difficulty=1,
            lessons=[lesson1, lesson2, lesson3],
        )

        registry.add_chapter(chapter)

        # No lessons completed
        progress = registry.calculate_chapter_progress("chapter_1", [])
        assert progress == 0.0

        # One lesson completed (33.33%)
        progress = registry.calculate_chapter_progress("chapter_1", ["lesson_1_1"])
        assert abs(progress - 33.33) < 0.1

        # Two lessons completed (66.67%)
        progress = registry.calculate_chapter_progress(
            "chapter_1", ["lesson_1_1", "lesson_1_2"]
        )
        assert abs(progress - 66.67) < 0.1

        # All lessons completed (100%)
        progress = registry.calculate_chapter_progress(
            "chapter_1", ["lesson_1_1", "lesson_1_2", "lesson_1_3"]
        )
        assert progress == 100.0

        # Test with nonexistent chapter
        progress = registry.calculate_chapter_progress("nonexistent", ["lesson_1_1"])
        assert progress == 0.0


class TestHierarchicalStructureIntegration:
    """Test integration of hierarchical structure."""

    def test_complete_learning_path(self):
        """Test a complete learning path through chapters and lessons."""
        registry = ChapterLessonRegistry()

        # Create lessons
        lesson1_1 = Lesson(
            id="lesson_1_1",
            name="Perfect Intervals",
            description="Learn perfect intervals",
            difficulty=1,
            exercises=["perfect_fourth_fifth_octave_melodic"],
            chapter_id="chapter_1",
        )

        lesson1_2 = Lesson(
            id="lesson_1_2",
            name="Third Intervals",
            description="Learn third intervals",
            difficulty=2,
            exercises=["minor_third_major_third_octave_melodic"],
            chapter_id="chapter_1",
            prerequisites=["lesson_1_1"],
        )

        lesson2_1 = Lesson(
            id="lesson_2_1",
            name="Combined Intervals",
            description="Learn combined intervals",
            difficulty=3,
            exercises=["combined_intervals_melodic"],
            chapter_id="chapter_2",
        )

        # Create chapters
        chapter1 = Chapter(
            id="chapter_1",
            name="Basic Intervals",
            description="Learn basic intervals",
            difficulty=1,
            lessons=[lesson1_1, lesson1_2],
        )

        chapter2 = Chapter(
            id="chapter_2",
            name="Advanced Intervals",
            description="Learn advanced intervals",
            difficulty=3,
            lessons=[lesson2_1],
            prerequisites=["chapter_1"],
        )

        registry.add_chapter(chapter1)
        registry.add_chapter(chapter2)

        # Simulate learning progress
        completed_chapters = []
        completed_lessons = []

        # Start with chapter 1
        assert registry.validate_prerequisites("chapter_1", completed_chapters) is True

        # Complete first lesson
        next_lesson = registry.get_next_lesson("chapter_1", completed_lessons)
        assert next_lesson == lesson1_1
        completed_lessons.append("lesson_1_1")

        # Complete second lesson
        next_lesson = registry.get_next_lesson("chapter_1", completed_lessons)
        assert next_lesson == lesson1_2
        completed_lessons.append("lesson_1_2")

        # Chapter 1 complete
        progress = registry.calculate_chapter_progress("chapter_1", completed_lessons)
        assert progress == 100.0
        completed_chapters.append("chapter_1")

        # Now can access chapter 2
        assert registry.validate_prerequisites("chapter_2", completed_chapters) is True

        # Complete chapter 2 lesson
        next_lesson = registry.get_next_lesson("chapter_2", completed_lessons)
        assert next_lesson == lesson2_1
        completed_lessons.append("lesson_2_1")

        # Chapter 2 complete
        progress = registry.calculate_chapter_progress("chapter_2", completed_lessons)
        assert progress == 100.0
        completed_chapters.append("chapter_2")

    def test_prerequisite_validation_complex(self):
        """Test complex prerequisite validation scenarios."""
        registry = ChapterLessonRegistry()

        # Create a complex structure with multiple prerequisites
        lesson1_1 = Lesson(
            id="lesson_1_1",
            name="Basic Perfect Intervals",
            description="Learn basic perfect intervals",
            difficulty=1,
            exercises=["perfect_fourth_fifth_octave_melodic"],
            chapter_id="chapter_1",
        )

        lesson1_2 = Lesson(
            id="lesson_1_2",
            name="Basic Third Intervals",
            description="Learn basic third intervals",
            difficulty=2,
            exercises=["minor_third_major_third_octave_melodic"],
            chapter_id="chapter_1",
            prerequisites=["lesson_1_1"],
        )

        lesson2_1 = Lesson(
            id="lesson_2_1",
            name="Advanced Perfect Intervals",
            description="Learn advanced perfect intervals",
            difficulty=3,
            exercises=["perfect_fourth_fifth_octave_harmonic"],
            chapter_id="chapter_2",
            prerequisites=["lesson_1_1", "lesson_1_2"],
        )

        chapter1 = Chapter(
            id="chapter_1",
            name="Basic Intervals",
            description="Learn basic intervals",
            difficulty=1,
            lessons=[lesson1_1, lesson1_2],
        )

        chapter2 = Chapter(
            id="chapter_2",
            name="Advanced Intervals",
            description="Learn advanced intervals",
            difficulty=3,
            lessons=[lesson2_1],
            prerequisites=["chapter_1"],
        )

        registry.add_chapter(chapter1)
        registry.add_chapter(chapter2)

        # Test various completion scenarios
        completed_lessons = []

        # Can't access lesson 1_2 without completing 1_1
        next_lesson = registry.get_next_lesson("chapter_1", completed_lessons)
        assert next_lesson == lesson1_1

        # Complete lesson 1_1
        completed_lessons.append("lesson_1_1")

        # Now can access lesson 1_2
        next_lesson = registry.get_next_lesson("chapter_1", completed_lessons)
        assert next_lesson == lesson1_2

        # Complete lesson 1_2
        completed_lessons.append("lesson_1_2")

        # Chapter 1 complete, can access chapter 2
        completed_chapters = ["chapter_1"]
        assert registry.validate_prerequisites("chapter_2", completed_chapters) is True

        # Can access lesson 2_1 (prerequisites met)
        next_lesson = registry.get_next_lesson("chapter_2", completed_lessons)
        assert next_lesson == lesson2_1
