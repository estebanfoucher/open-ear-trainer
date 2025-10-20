# Quick Start: Curriculum Navigation

## Setup

1. **Apply migrations and seed data:**
```bash
cd backend
python manage.py migrate
python manage.py seed_curriculum
```

2. **Start the backend:**
```bash
# From backend directory
python manage.py runserver
```

3. **Start the frontend:**
```bash
# From frontend directory
npm start
```

## Using the Application

### User Journey

1. **View Chapters**
   - Open http://localhost:3000
   - See a grid of available chapters
   - Each chapter shows:
     - Title and description
     - Difficulty level badge
     - Number of lessons and exercises

2. **Browse Lessons**
   - Click "Start Chapter" on any chapter
   - See all lessons within that chapter
   - Each lesson shows:
     - Estimated completion time
     - Number of exercises
     - Learning objectives

3. **Select Exercise**
   - Click "Start Lesson" on any lesson
   - See all exercises in that lesson
   - Breadcrumb shows: Chapter → Lesson
   - Each exercise shows:
     - Order number and difficulty
     - Exercise description

4. **Complete Exercise**
   - Click "Start Exercise (20 Questions)"
   - Answer 20 questions
   - Auto-advance after each answer
   - See final score

5. **Navigate Back**
   - Use "Back to..." buttons at each level
   - Or complete all questions to return automatically

## API Examples

### Get all chapters
```bash
curl http://localhost:8000/api/chapters/ | jq
```

### Get chapter with lessons
```bash
curl http://localhost:8000/api/chapters/3/ | jq
```

### Get lesson with exercises
```bash
curl http://localhost:8000/api/lessons/1/ | jq
```

### Start an exercise (existing endpoint)
```bash
curl "http://localhost:8000/api/exercises/minor_third_major_third_octave_melodic/generate/?question_number=1" | jq
```

## Admin Interface

1. **Access admin:**
   - URL: http://localhost:8000/admin/
   - Create superuser if needed: `python manage.py createsuperuser`

2. **Manage content:**
   - Chapters: Add/edit/delete chapters
   - Lessons: Add/edit/delete lessons within chapters
   - Exercises: Link exercise types to lessons

3. **Publishing:**
   - Set `is_published=True` to make content visible
   - Unpublished content won't appear in the API or frontend

## Adding New Content

### Example: Add a new lesson

```python
# In Django shell or management command
from api_app.models import Chapter, Lesson, Exercise

# Get existing chapter
chapter = Chapter.objects.get(title="Intervals")

# Create new lesson
lesson = Lesson.objects.create(
    chapter=chapter,
    title="Advanced Intervals",
    description="Practice all interval types",
    order=6,
    learning_objectives="Master all intervals",
    estimated_minutes=25,
    is_published=True
)

# Create exercise
Exercise.objects.create(
    lesson=lesson,
    exercise_type="combined_intervals_melodic",  # Must exist in registry
    title="All Intervals Challenge",
    description="Identify all melodic intervals",
    order=1,
    difficulty_level=5,
    is_published=True
)
```

### Example: Add a new chapter

```python
from api_app.models import Chapter

chapter = Chapter.objects.create(
    title="Triads & Chord Qualities",
    description="Identify major, minor, diminished, and augmented triads",
    order=4,
    difficulty_level=4,
    is_published=True
)
```

## Troubleshooting

### "No chapters showing"
- Check that chapters have `is_published=True`
- Run seed command: `python manage.py seed_curriculum`
- Verify API response: `curl http://localhost:8000/api/chapters/`

### "Exercise not found"
- Ensure `exercise_type` in Exercise model matches an ID in `SimpleExerciseRegistry`
- Check available exercises: `curl http://localhost:8000/api/exercises/`

### "Frontend not connecting"
- Verify backend is running on port 8000
- Check `REACT_APP_API_URL` environment variable
- Check browser console for CORS errors

## Current Available Content

After running `seed_curriculum`:

### Chapter 1: Direction & Contour
- No lessons yet (placeholder for future content)

### Chapter 2: Tonal Center & Scale Sense
- No lessons yet (placeholder for future content)

### Chapter 3: Intervals
- ✅ 5 Lessons
- ✅ 5 Exercises
- Fully functional interval recognition exercises

## Next Steps

1. **Create more content** in Django admin
2. **Implement exercises** for Chapters 1 and 2
3. **Add user progress tracking** (future feature)
4. **Add prerequisites** between lessons (future feature)
5. **Add achievement system** (future feature)

## Development Commands

```bash
# Create new migration after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Seed curriculum data
python manage.py seed_curriculum

# Run tests
pytest backend/tests/

# Check linting
ruff check backend/

# Format code
ruff format backend/
```
