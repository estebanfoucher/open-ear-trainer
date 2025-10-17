# Open Ear Trainer

A scalable ear training web application for musicians built with Django and React.

## Architecture

This project implements a highly scalable, plugin-based architecture for progressive course development:

- **Backend**: Django + DRF with music theory using mingus and audio synthesis with FluidSynth
- **Frontend**: React + TypeScript
- **Exercise System**: Plugin-based with auto-discovery and metadata-driven configuration
- **Course Progression**: Structured learning paths with prerequisites and adaptive recommendations

## Current Status

✅ **Completed:**
- Project structure and configuration (uv, ruff, pytest, pre-commit)
- Django backend with REST API
- Music theory module (scales, chords, progressions)
- Exercise framework with metadata system
- Dynamic exercise registry with auto-discovery
- Audio synthesis with FluidSynth and SoundFont support
- React frontend with TypeScript
- Interval Recognition exercise with staggered timing
- Real piano sounds using School_Piano_2024.sf2 SoundFont

🚧 **In Progress:**
- Course progression framework
- Additional exercises and levels

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- uv (Python package manager)

### Setup

1. **Clone and setup environment:**
   ```bash
   git clone <repository>
   cd open-ear-trainer
   make setup
   ```

2. **SoundFont is included:**
   - School_Piano_2024.sf2 is already included in the `soundfonts/` directory
   - No additional setup required for audio generation

3. **Run development servers:**
   ```bash
   make run  # Runs both backend and frontend
   # Or separately:
   make run-backend   # Django server on :8000
   make run-frontend  # React server on :3000
   ```

### Development Commands

```bash
make install     # Install dependencies
make test        # Run tests
make lint        # Run linting
make format      # Format code
make clean       # Clean cache files
```

## API Endpoints

- `GET /api/exercises/` - List all exercises
- `GET /api/exercises/{id}/` - Get exercise details
- `GET /api/exercises/{id}/generate/` - Generate new exercise instance
- `POST /api/exercises/{id}/check/` - Check answer
- `GET /api/audio/{filename}/` - Serve audio files

## Exercise System

The exercise system is designed for easy extensibility:

### Adding a New Exercise

1. Create a new file in `backend/exercises/level*/`
2. Inherit from `BaseExercise` and implement required methods
3. Define metadata with difficulty, prerequisites, learning objectives
4. The exercise is automatically discovered and available via API

### Example Exercise Structure

```python
class MyExercise(BaseExercise):
    metadata = ExerciseMetadata(
        id="my_exercise",
        name="My Exercise",
        description="Description of what the exercise does",
        difficulty=3,
        prerequisites=["note_identification"],
        learning_objectives=["Learn to identify intervals"],
        category="interval_recognition",
        tags=["intervals", "melodic"]
    )
    
    def generate(self, **kwargs) -> ExerciseData:
        # Generate exercise content
        pass
    
    def check_answer(self, answer, context) -> ExerciseResult:
        # Validate user answer
        pass
```

## Planned Exercises

### Level 1 (Beginner)
- ✅ Interval Recognition (octave, minor third, major third) with staggered timing
- 🔄 Chord Quality (major vs minor)
- 🔄 Note Identification in Major Scale

### Level 2 (Intermediate)  
- 🔄 Scale Degree Identification in Minor Scales
- 🔄 Chord Progression Recognition
- 🔄 Seventh Chord Qualities

### Level 3 (Advanced)
- 🔄 Melodic Dictation
- 🔄 Harmonic Dictation
- 🔄 Modal Recognition

## Technology Stack

### Backend
- **Django 5.2** - Web framework
- **Django REST Framework** - API
- **mingus** - Music theory
- **pyFluidSynth** - Audio synthesis
- **uv** - Package management
- **ruff** - Linting and formatting
- **pytest** - Testing

### Frontend
- **React 18** - UI framework
- **TypeScript** - Type safety
- **Axios** - HTTP client
- **React Scripts** - Development and build tools

## License

MIT License - Free to use and modify.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add your exercise or feature
4. Write tests
5. Submit a pull request

The architecture is designed to make adding new exercises as simple as possible while maintaining code quality and scalability.