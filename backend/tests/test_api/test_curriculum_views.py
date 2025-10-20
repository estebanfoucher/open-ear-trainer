"""
Tests for curriculum navigation API views (chapters, lessons, exercises).
"""

from api_app.models import Chapter, Exercise, Lesson
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class TestChapterListView(TestCase):
    """Tests for the ChapterListView."""

    def setUp(self):
        """Set up test client and create test data."""
        self.client = APIClient()
        self.url = reverse("api:chapter-list")

        # Create test chapters
        self.chapter1 = Chapter.objects.create(
            title="Test Chapter 1",
            description="Test description 1",
            order=1,
            difficulty_level=1,
            is_published=True,
        )
        self.chapter2 = Chapter.objects.create(
            title="Test Chapter 2",
            description="Test description 2",
            order=2,
            difficulty_level=2,
            is_published=True,
        )
        self.chapter3 = Chapter.objects.create(
            title="Unpublished Chapter",
            description="Should not appear",
            order=3,
            difficulty_level=3,
            is_published=False,
        )

    def test_chapter_list_get(self):
        """Test getting list of published chapters."""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Only published chapters
        self.assertEqual(response.data[0]["title"], "Test Chapter 1")
        self.assertEqual(response.data[1]["title"], "Test Chapter 2")

    def test_chapter_list_includes_counts(self):
        """Test that chapter list includes lesson and exercise counts."""
        # Create lesson and exercise for chapter1
        lesson = Lesson.objects.create(
            chapter=self.chapter1,
            title="Test Lesson",
            description="Test description",
            order=1,
            is_published=True,
        )
        Exercise.objects.create(
            lesson=lesson,
            exercise_type="test_exercise",
            title="Test Exercise",
            order=1,
            is_published=True,
        )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        chapter_data = response.data[0]
        self.assertEqual(chapter_data["lesson_count"], 1)
        self.assertEqual(chapter_data["exercise_count"], 1)

    def test_chapter_list_ordering(self):
        """Test that chapters are ordered by order field."""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["order"], 1)
        self.assertEqual(response.data[1]["order"], 2)


class TestChapterDetailView(TestCase):
    """Tests for the ChapterDetailView."""

    def setUp(self):
        """Set up test client and create test data."""
        self.client = APIClient()

        # Create test chapter
        self.chapter = Chapter.objects.create(
            title="Test Chapter",
            description="Test description",
            order=1,
            difficulty_level=1,
            is_published=True,
        )

        # Create lessons
        self.lesson1 = Lesson.objects.create(
            chapter=self.chapter,
            title="Test Lesson 1",
            description="Test description 1",
            order=1,
            estimated_minutes=15,
            is_published=True,
        )
        self.lesson2 = Lesson.objects.create(
            chapter=self.chapter,
            title="Test Lesson 2",
            description="Test description 2",
            order=2,
            estimated_minutes=20,
            is_published=True,
        )

        self.url = reverse("api:chapter-detail", kwargs={"chapter_id": self.chapter.id})

    def test_chapter_detail_get(self):
        """Test getting chapter detail with lessons."""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Chapter")
        self.assertEqual(len(response.data["lessons"]), 2)
        self.assertEqual(response.data["lessons"][0]["title"], "Test Lesson 1")

    def test_chapter_detail_get_nonexistent(self):
        """Test getting nonexistent chapter returns 404."""
        url = reverse("api:chapter-detail", kwargs={"chapter_id": 9999})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("error", response.data)

    def test_chapter_detail_get_unpublished(self):
        """Test that unpublished chapters return 404."""
        unpublished_chapter = Chapter.objects.create(
            title="Unpublished",
            description="Test",
            order=99,
            is_published=False,
        )
        url = reverse(
            "api:chapter-detail", kwargs={"chapter_id": unpublished_chapter.id}
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestLessonDetailView(TestCase):
    """Tests for the LessonDetailView."""

    def setUp(self):
        """Set up test client and create test data."""
        self.client = APIClient()

        # Create test chapter and lesson
        self.chapter = Chapter.objects.create(
            title="Test Chapter",
            description="Test description",
            order=1,
            is_published=True,
        )
        self.lesson = Lesson.objects.create(
            chapter=self.chapter,
            title="Test Lesson",
            description="Test description",
            order=1,
            learning_objectives="Test objectives",
            estimated_minutes=15,
            is_published=True,
        )

        # Create exercises
        self.exercise1 = Exercise.objects.create(
            lesson=self.lesson,
            exercise_type="test_exercise_1",
            title="Test Exercise 1",
            description="Test description 1",
            order=1,
            difficulty_level=1,
            is_published=True,
        )
        self.exercise2 = Exercise.objects.create(
            lesson=self.lesson,
            exercise_type="test_exercise_2",
            title="Test Exercise 2",
            description="Test description 2",
            order=2,
            difficulty_level=2,
            is_published=True,
        )

        self.url = reverse("api:lesson-detail", kwargs={"lesson_id": self.lesson.id})

    def test_lesson_detail_get(self):
        """Test getting lesson detail with exercises."""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Lesson")
        self.assertEqual(response.data["chapter_id"], self.chapter.id)
        self.assertEqual(response.data["chapter_title"], "Test Chapter")
        self.assertEqual(len(response.data["exercises"]), 2)
        self.assertEqual(response.data["exercises"][0]["title"], "Test Exercise 1")

    def test_lesson_detail_get_nonexistent(self):
        """Test getting nonexistent lesson returns 404."""
        url = reverse("api:lesson-detail", kwargs={"lesson_id": 9999})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("error", response.data)

    def test_lesson_detail_get_unpublished(self):
        """Test that unpublished lessons return 404."""
        unpublished_lesson = Lesson.objects.create(
            chapter=self.chapter,
            title="Unpublished",
            description="Test",
            order=99,
            is_published=False,
        )
        url = reverse("api:lesson-detail", kwargs={"lesson_id": unpublished_lesson.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_lesson_detail_includes_chapter_info(self):
        """Test that lesson detail includes chapter information."""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("chapter_id", response.data)
        self.assertIn("chapter_title", response.data)
        self.assertEqual(response.data["chapter_title"], "Test Chapter")


class TestCurriculumIntegration(TestCase):
    """Integration tests for curriculum navigation flow."""

    def setUp(self):
        """Set up test client and create full curriculum structure."""
        self.client = APIClient()

        # Create full structure: Chapter -> Lesson -> Exercise
        self.chapter = Chapter.objects.create(
            title="Integration Test Chapter",
            description="Test description",
            order=1,
            difficulty_level=1,
            is_published=True,
        )

        self.lesson = Lesson.objects.create(
            chapter=self.chapter,
            title="Integration Test Lesson",
            description="Test description",
            order=1,
            estimated_minutes=15,
            is_published=True,
        )

        self.exercise = Exercise.objects.create(
            lesson=self.lesson,
            exercise_type="minor_third_major_third_octave_melodic",
            title="Integration Test Exercise",
            description="Test description",
            order=1,
            difficulty_level=1,
            is_published=True,
        )

    def test_full_navigation_flow(self):
        """Test navigating from chapters -> lessons -> exercises."""
        # 1. Get chapter list
        chapters_response = self.client.get(reverse("api:chapter-list"))
        self.assertEqual(chapters_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(chapters_response.data), 1)

        # 2. Get chapter detail
        chapter_id = chapters_response.data[0]["id"]
        chapter_response = self.client.get(
            reverse("api:chapter-detail", kwargs={"chapter_id": chapter_id})
        )
        self.assertEqual(chapter_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(chapter_response.data["lessons"]), 1)

        # 3. Get lesson detail
        lesson_id = chapter_response.data["lessons"][0]["id"]
        lesson_response = self.client.get(
            reverse("api:lesson-detail", kwargs={"lesson_id": lesson_id})
        )
        self.assertEqual(lesson_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(lesson_response.data["exercises"]), 1)

        # 4. Verify exercise data
        exercise_data = lesson_response.data["exercises"][0]
        self.assertEqual(
            exercise_data["exercise_type"], "minor_third_major_third_octave_melodic"
        )
        self.assertEqual(exercise_data["title"], "Integration Test Exercise")

    def test_counts_are_accurate(self):
        """Test that lesson/exercise counts are accurate."""
        # Add another lesson and exercises
        lesson2 = Lesson.objects.create(
            chapter=self.chapter,
            title="Second Lesson",
            description="Test",
            order=2,
            is_published=True,
        )
        Exercise.objects.create(
            lesson=lesson2,
            exercise_type="test_exercise",
            title="Test",
            order=1,
            is_published=True,
        )

        # Check chapter list
        response = self.client.get(reverse("api:chapter-list"))
        chapter_data = response.data[0]
        self.assertEqual(chapter_data["lesson_count"], 2)
        self.assertEqual(chapter_data["exercise_count"], 2)

        # Check chapter detail
        response = self.client.get(
            reverse("api:chapter-detail", kwargs={"chapter_id": self.chapter.id})
        )
        self.assertEqual(len(response.data["lessons"]), 2)

        # Check lesson detail
        response = self.client.get(
            reverse("api:lesson-detail", kwargs={"lesson_id": lesson2.id})
        )
        self.assertEqual(len(response.data["exercises"]), 1)
