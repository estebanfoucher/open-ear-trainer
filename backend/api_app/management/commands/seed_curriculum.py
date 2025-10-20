"""
Management command to seed initial curriculum data.
"""

from django.core.management.base import BaseCommand

from api_app.models import Chapter, Exercise, Lesson


class Command(BaseCommand):
    help = "Seed initial curriculum data from ROADMAP.md"

    def handle(self, *args, **options):
        self.stdout.write("Seeding curriculum data...")

        # Chapter 1: Sound Awareness & Direction
        chapter1, created = Chapter.objects.get_or_create(
            order=1,
            defaults={
                "title": "Sound Awareness & Direction",
                "description": "Build basic auditory discrimination — pitch direction, contour, and tonal focus.",
                "difficulty_level": 1,
                "is_published": True,
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created Chapter: {chapter1.title}"))

        # Chapter 2: Tonal Center & Scale Sense
        chapter2, created = Chapter.objects.get_or_create(
            order=2,
            defaults={
                "title": "Tonal Center & Scale Sense",
                "description": "Internalize tonic, dominant, and mediant relationships (Do–Mi–Sol) and basic scale steps.",
                "difficulty_level": 2,
                "is_published": True,
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created Chapter: {chapter2.title}"))

        # Chapter 3: Intervals
        chapter3, created = Chapter.objects.get_or_create(
            order=3,
            defaults={
                "title": "Intervals",
                "description": "Identify melodic and harmonic intervals by ear.",
                "difficulty_level": 3,
                "is_published": True,
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created Chapter: {chapter3.title}"))

        # Chapter 4: Triads and Chord Qualities
        chapter4, created = Chapter.objects.get_or_create(
            order=4,
            defaults={
                "title": "Triads and Chord Qualities",
                "description": "Recognize and sing major, minor, diminished, and augmented triads in root and inversion.",
                "difficulty_level": 3,
                "is_published": True,
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created Chapter: {chapter4.title}"))

        # Chapter 1 Lessons
        lesson1_1, created = Lesson.objects.get_or_create(
            chapter=chapter1,
            order=1,
            defaults={
                "title": "Hearing Up vs. Down",
                "description": "Learn to identify if the second note is higher or lower than the first.",
                "learning_objectives": "Recognize pitch direction, build basic auditory discrimination",
                "estimated_minutes": 15,
                "is_published": True,
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created Lesson: {lesson1_1.title}"))

        lesson1_2, created = Lesson.objects.get_or_create(
            chapter=chapter1,
            order=2,
            defaults={
                "title": "Step or Leap",
                "description": "Distinguish between stepwise motion and leaps in melodies.",
                "learning_objectives": "Recognize interval size qualitatively, distinguish steps from leaps",
                "estimated_minutes": 15,
                "is_published": True,
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created Lesson: {lesson1_2.title}"))

        lesson1_3, created = Lesson.objects.get_or_create(
            chapter=chapter1,
            order=3,
            defaults={
                "title": "Recognizing Patterns",
                "description": "Identify melodic shapes and patterns in short phrases.",
                "learning_objectives": "Establish pattern recognition, build auditory memory",
                "estimated_minutes": 20,
                "is_published": True,
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created Lesson: {lesson1_3.title}"))

        # Chapter 2 Lessons
        lesson2_1, created = Lesson.objects.get_or_create(
            chapter=chapter2,
            order=1,
            defaults={
                "title": "The Tonic (Do)",
                "description": "Learn to identify the 'home note' in melodies and recognize resolution.",
                "learning_objectives": "Recognize tonic stability, identify resolution",
                "estimated_minutes": 15,
                "is_published": True,
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created Lesson: {lesson2_1.title}"))

        lesson2_2, created = Lesson.objects.get_or_create(
            chapter=chapter2,
            order=2,
            defaults={
                "title": "Major Scale Construction",
                "description": "Learn scale degrees and their solfège syllables.",
                "learning_objectives": "Learn scale degrees, connect solfège to pitch",
                "estimated_minutes": 15,
                "is_published": True,
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created Lesson: {lesson2_2.title}"))

        lesson2_3, created = Lesson.objects.get_or_create(
            chapter=chapter2,
            order=3,
            defaults={
                "title": "Tonal Triads",
                "description": "Learn to identify and sing tonic chord tones (Do-Mi-Sol).",
                "learning_objectives": "Recognize tonic chord tones, build chord awareness",
                "estimated_minutes": 15,
                "is_published": True,
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created Lesson: {lesson2_3.title}"))

        # Chapter 3 Lessons (existing)
        lesson3_1, created = Lesson.objects.get_or_create(
            chapter=chapter3,
            order=1,
            defaults={
                "title": "Melodic Intervals: Thirds and Octave",
                "description": "Learn to identify melodic minor thirds, major thirds, and octaves.",
                "learning_objectives": "Recognize melodic intervals by ear",
                "estimated_minutes": 15,
                "is_published": True,
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created Lesson: {lesson3_1.title}"))

        lesson3_2, created = Lesson.objects.get_or_create(
            chapter=chapter3,
            order=2,
            defaults={
                "title": "Melodic Intervals: Perfect Fourths, Fifths, and Octave",
                "description": "Learn to identify perfect fourths, fifths, and octaves melodically.",
                "learning_objectives": "Recognize perfect intervals by ear",
                "estimated_minutes": 15,
                "is_published": True,
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created Lesson: {lesson3_2.title}"))

        lesson3_3, created = Lesson.objects.get_or_create(
            chapter=chapter3,
            order=3,
            defaults={
                "title": "Harmonic Intervals: Thirds and Octave",
                "description": "Learn to identify minor thirds, major thirds, and octaves played harmonically.",
                "learning_objectives": "Recognize harmonic intervals by ear",
                "estimated_minutes": 15,
                "is_published": True,
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created Lesson: {lesson3_3.title}"))

        lesson3_4, created = Lesson.objects.get_or_create(
            chapter=chapter3,
            order=4,
            defaults={
                "title": "Harmonic Intervals: Perfect Fourths, Fifths, and Octave",
                "description": "Learn to identify perfect fourths, fifths, and octaves played harmonically.",
                "learning_objectives": "Recognize perfect harmonic intervals by ear",
                "estimated_minutes": 15,
                "is_published": True,
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created Lesson: {lesson3_4.title}"))

        lesson3_5, created = Lesson.objects.get_or_create(
            chapter=chapter3,
            order=5,
            defaults={
                "title": "Combined Interval Recognition",
                "description": "Practice identifying all learned intervals together.",
                "learning_objectives": "Master interval recognition across all learned intervals",
                "estimated_minutes": 20,
                "is_published": True,
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created Lesson: {lesson3_5.title}"))

        # Chapter 4 Lessons
        lesson4_1, created = Lesson.objects.get_or_create(
            chapter=chapter4,
            order=1,
            defaults={
                "title": "Major vs. Minor Chords",
                "description": "Learn to distinguish major and minor chord qualities.",
                "learning_objectives": "Distinguish major from minor, recognize emotional character",
                "estimated_minutes": 15,
                "is_published": True,
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created Lesson: {lesson4_1.title}"))

        lesson4_2, created = Lesson.objects.get_or_create(
            chapter=chapter4,
            order=2,
            defaults={
                "title": "Diminished & Augmented",
                "description": "Learn to identify all four triad types: major, minor, diminished, and augmented.",
                "learning_objectives": "Distinguish all triad types, hear tension vs stability",
                "estimated_minutes": 20,
                "is_published": True,
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created Lesson: {lesson4_2.title}"))

        lesson4_3, created = Lesson.objects.get_or_create(
            chapter=chapter4,
            order=3,
            defaults={
                "title": "Suspended Chords",
                "description": "Learn to identify suspended chords and distinguish them from major and minor triads.",
                "learning_objectives": "Recognize suspended chords, distinguish from triads",
                "estimated_minutes": 20,
                "is_published": True,
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created Lesson: {lesson4_3.title}"))

        lesson4_4, created = Lesson.objects.get_or_create(
            chapter=chapter4,
            order=4,
            defaults={
                "title": "Inversions",
                "description": "Learn to identify triads in different inversions by their bass note.",
                "learning_objectives": "Recognize inversions, identify bass influence",
                "estimated_minutes": 20,
                "is_published": True,
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created Lesson: {lesson4_4.title}"))

        # Chapter 1 Exercises
        exercise1_1_1, created = Exercise.objects.get_or_create(
            lesson=lesson1_1,
            order=1,
            defaults={
                "exercise_type": "high_or_low_direction",
                "title": "High or Low?",
                "description": "Listen to two tones and identify if the second note is higher or lower than the first.",
                "difficulty_level": 1,
                "config": {},
                "is_published": True,
            },
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS(f"Created Exercise: {exercise1_1_1.title}")
            )

        exercise1_2_1, created = Exercise.objects.get_or_create(
            lesson=lesson1_2,
            order=1,
            defaults={
                "exercise_type": "step_vs_leap",
                "title": "Step vs. Leap Challenge",
                "description": "Listen to two notes and identify if the interval is a step (2nd) or leap (3rd or larger).",
                "difficulty_level": 1,
                "config": {},
                "is_published": True,
            },
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS(f"Created Exercise: {exercise1_2_1.title}")
            )

        exercise1_3_1, created = Exercise.objects.get_or_create(
            lesson=lesson1_3,
            order=1,
            defaults={
                "exercise_type": "melodic_shapes",
                "title": "Melodic Shapes",
                "description": "Listen to a short melodic phrase and identify its shape (arch, zigzag, ascending, descending).",
                "difficulty_level": 2,
                "config": {},
                "is_published": True,
            },
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS(f"Created Exercise: {exercise1_3_1.title}")
            )

        # Chapter 2 Exercises
        exercise2_1_1, created = Exercise.objects.get_or_create(
            lesson=lesson2_1,
            order=1,
            defaults={
                "exercise_type": "find_home_note",
                "title": "Find Home Note",
                "description": "Listen to a melody and identify which note feels like 'home' (the tonic).",
                "difficulty_level": 2,
                "config": {},
                "is_published": True,
            },
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS(f"Created Exercise: {exercise2_1_1.title}")
            )

        exercise2_2_1, created = Exercise.objects.get_or_create(
            lesson=lesson2_2,
            order=1,
            defaults={
                "exercise_type": "scale_degrees_solfege",
                "title": "Scale Degrees with Solfège",
                "description": "Listen to a scale degree and identify its solfège syllable (Do, Re, Mi, etc.).",
                "difficulty_level": 2,
                "config": {},
                "is_published": True,
            },
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS(f"Created Exercise: {exercise2_2_1.title}")
            )

        exercise2_3_1, created = Exercise.objects.get_or_create(
            lesson=lesson2_3,
            order=1,
            defaults={
                "exercise_type": "label_do_mi_sol",
                "title": "Label Do-Mi-Sol",
                "description": "Listen to a broken tonic triad and identify which note is Do, Mi, or Sol.",
                "difficulty_level": 2,
                "config": {},
                "is_published": True,
            },
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS(f"Created Exercise: {exercise2_3_1.title}")
            )

        # Chapter 3 Exercises (existing)
        exercise3_1_1, created = Exercise.objects.get_or_create(
            lesson=lesson3_1,
            order=1,
            defaults={
                "exercise_type": "minor_third_major_third_octave_melodic",
                "title": "Minor Third, Major Third, and Octave (Melodic)",
                "description": "Identify melodic intervals: minor third, major third, and octave.",
                "difficulty_level": 1,
                "config": {},
                "is_published": True,
            },
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS(f"Created Exercise: {exercise3_1_1.title}")
            )

        exercise3_2_1, created = Exercise.objects.get_or_create(
            lesson=lesson3_2,
            order=1,
            defaults={
                "exercise_type": "perfect_fourth_fifth_octave_melodic",
                "title": "Perfect Fourth, Perfect Fifth, and Octave (Melodic)",
                "description": "Identify melodic intervals: perfect fourth, perfect fifth, and octave.",
                "difficulty_level": 2,
                "config": {},
                "is_published": True,
            },
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS(f"Created Exercise: {exercise3_2_1.title}")
            )

        exercise3_3_1, created = Exercise.objects.get_or_create(
            lesson=lesson3_3,
            order=1,
            defaults={
                "exercise_type": "minor_third_major_third_octave_harmonic",
                "title": "Minor Third, Major Third, and Octave (Harmonic)",
                "description": "Identify harmonic intervals: minor third, major third, and octave.",
                "difficulty_level": 2,
                "config": {},
                "is_published": True,
            },
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS(f"Created Exercise: {exercise3_3_1.title}")
            )

        exercise3_4_1, created = Exercise.objects.get_or_create(
            lesson=lesson3_4,
            order=1,
            defaults={
                "exercise_type": "perfect_fourth_fifth_octave_harmonic",
                "title": "Perfect Fourth, Perfect Fifth, and Octave (Harmonic)",
                "description": "Identify harmonic intervals: perfect fourth, perfect fifth, and octave.",
                "difficulty_level": 3,
                "config": {},
                "is_published": True,
            },
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS(f"Created Exercise: {exercise3_4_1.title}")
            )

        exercise3_5_1, created = Exercise.objects.get_or_create(
            lesson=lesson3_5,
            order=1,
            defaults={
                "exercise_type": "combined_intervals_melodic",
                "title": "Combined Melodic Intervals",
                "description": "Identify all learned melodic intervals in combination.",
                "difficulty_level": 4,
                "config": {},
                "is_published": True,
            },
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS(f"Created Exercise: {exercise3_5_1.title}")
            )

        # Chapter 4 Exercises
        exercise4_1_1, created = Exercise.objects.get_or_create(
            lesson=lesson4_1,
            order=1,
            defaults={
                "exercise_type": "major_vs_minor_chords",
                "title": "Happy or Sad?",
                "description": "Listen to a triad and identify if it sounds happy (major) or sad (minor).",
                "difficulty_level": 2,
                "config": {},
                "is_published": True,
            },
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS(f"Created Exercise: {exercise4_1_1.title}")
            )

        exercise4_2_1, created = Exercise.objects.get_or_create(
            lesson=lesson4_2,
            order=1,
            defaults={
                "exercise_type": "triad_fifth_quality",
                "title": "Fifth Quality",
                "description": "Listen to a triad with a major third and identify the quality of its fifth: diminished, perfect, or augmented.",
                "difficulty_level": 3,
                "config": {},
                "is_published": True,
            },
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS(f"Created Exercise: {exercise4_2_1.title}")
            )

        exercise4_3_1, created = Exercise.objects.get_or_create(
            lesson=lesson4_3,
            order=1,
            defaults={
                "exercise_type": "suspended_chord_exercise",
                "title": "Suspended Chord Exercise",
                "description": "Listen to a chord and identify its type: suspended 4th, suspended 2nd, minor third, or major third.",
                "difficulty_level": 3,
                "config": {},
                "is_published": True,
            },
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS(f"Created Exercise: {exercise4_3_1.title}")
            )

        exercise4_4_1, created = Exercise.objects.get_or_create(
            lesson=lesson4_4,
            order=1,
            defaults={
                "exercise_type": "identify_bass_note",
                "title": "Identify Bass Note",
                "description": "Listen to a triad in inversion and identify which note is in the bass (lowest).",
                "difficulty_level": 3,
                "config": {},
                "is_published": True,
            },
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS(f"Created Exercise: {exercise4_3_1.title}")
            )

        self.stdout.write(self.style.SUCCESS("Successfully seeded curriculum data!"))
