# Open Ear Trainer

A scalable ear training web application for musicians built with Django and React. This application helps musicians develop their aural skills through interactive exercises with real-time audio generation.

## 🎵 Features

- **Interactive Ear Training**: Progressive exercises for interval recognition
- **Real-Time Audio Generation**: High-quality audio synthesis using FluidSynth and SoundFonts
- **Scalable Architecture**: Plugin-based exercise system with auto-discovery
- **Modern UI**: React frontend with TypeScript for optimal user experience
- **Docker Support**: Complete containerization for easy deployment
- **CI/CD Ready**: GitHub Actions workflows for automated deployment

## 🏗️ Project Structure

```
open-ear-trainer/
├── backend/                    # Django backend application
│   ├── api_app/               # REST API endpoints
│   ├── audio_app/             # Audio synthesis and generation
│   ├── music_app/             # Music theory (scales, chords, notes)
│   ├── exercises/             # Exercise system with plugins
│   │   ├── base/              # Base exercise classes and metadata
│   │   └── level1/            # Level 1 exercises (beginner)
│   ├── config/                # Django configuration
│   │   └── settings/          # Environment-specific settings
│   └── tests/                 # Backend tests
├── frontend/                  # React frontend application
│   ├── src/                   # React components and logic
│   ├── public/                # Static assets
│   └── build/                 # Production build output
├── docker/                    # Docker configuration
│   ├── Dockerfile             # Production Docker image
│   ├── docker-compose.yml     # Base compose configuration
│   ├── docker-compose.dev.yml # Development environment
│   ├── docker-compose.prod.yml# Production environment
│   ├── nginx/                 # Nginx configurations
│   └── scripts/               # Deployment and utility scripts
├── media/                     # Generated audio files
├── soundfonts/                # SoundFont files for audio synthesis
├── .github/                   # GitHub Actions workflows
├── deploy.py                  # CLI deployment script
├── Makefile                   # Development commands
└── pyproject.toml             # Python project configuration
```

## 🛠️ Main Dependencies

### Backend (Python)
- **Django 4.2+**: Web framework
- **Django REST Framework**: API development
- **mingus**: Music theory library
- **pyFluidSynth**: Audio synthesis
- **python-decouple**: Environment configuration
- **Pillow**: Image processing
- **psycopg2-binary**: PostgreSQL adapter

### Frontend (JavaScript/TypeScript)
- **React 18**: UI framework
- **TypeScript**: Type safety
- **Axios**: HTTP client
- **http-proxy-middleware**: Development proxy

### Development Tools
- **uv**: Python package management
- **ruff**: Linting and formatting
- **pytest**: Testing framework
- **pre-commit**: Git hooks
- **Docker & Docker Compose**: Containerization

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- uv (Python package manager)

### Development Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd open-ear-trainer
   ```

2. **Set up the environment:**
   ```bash
   make setup
   ```

3. **Start the development environment:**
   ```bash
   # Using Docker (recommended)
   python deploy.py docker --env dev

   # Or using Make
   make docker-run-dev

   # Or manually
   make run
   ```

4. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/api/exercises/

### Production Deployment

```bash
# Deploy with Docker
python deploy.py docker --env prod

# Deploy to GitHub Pages (frontend only)
python deploy.py github-pages

# Deploy to Railway (backend only)
python deploy.py railway

# Full deployment
python deploy.py full
```

## 🎯 Available Commands

### Development
```bash
make run              # Start both backend and frontend
make run-backend      # Start Django server only
make run-frontend     # Start React server only
make test             # Run all tests
make lint             # Run linting
make format           # Format code
make clean            # Clean cache files
```

### Docker
```bash
make docker-run-dev   # Development environment
make docker-run-prod  # Production environment
make docker-build     # Build Docker image
make docker-clean     # Clean up Docker resources
```

### Deployment
```bash
make deploy           # Full deployment
make deploy-docker    # Docker deployment
make deploy-github    # GitHub Pages deployment
make deploy-railway   # Railway deployment
```

## 🎼 Exercise System

The application uses a plugin-based exercise system that automatically discovers and registers exercises:

### Adding a New Exercise

1. Create a new file in `backend/exercises/level*/`
2. Inherit from `BaseExercise` and implement required methods
3. Define metadata with difficulty, prerequisites, and learning objectives
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

## 🎵 Audio System

The application generates high-quality audio using:

- **FluidSynth**: Real-time audio synthesis
- **SoundFonts**: Professional instrument sounds
- **mingus**: Music theory calculations
- **Caching**: Optimized audio file generation

### Supported Audio Formats
- WAV files for exercises
- Real-time audio generation
- Configurable audio quality and timing

## 🔧 Configuration

### Environment Variables

Copy the appropriate environment file to `.env`:

```bash
# For development
cp env.development.example .env

# For production
cp env.example .env
```

Then edit `.env` with your actual values:

```bash
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True  # False for production
ALLOWED_HOSTS=localhost,127.0.0.1

# Audio Configuration
SOUNDFONT_PATH=soundfonts/School_Piano_2024.sf2
AUDIO_CACHE_ENABLED=True
AUDIO_CACHE_MAX_SIZE=1000

# Frontend
REACT_APP_API_URL=http://localhost:8000
```

### Docker Configuration

The project includes multiple Docker configurations:

- **Development**: Hot reload, debug mode, simplified setup
- **Production**: Optimized, secure, with Nginx reverse proxy
- **Base**: Common configuration shared between environments

## 🧪 Testing

```bash
# Run all tests
make test

# Run specific test types
make test-unit        # Unit tests only
make test-integration # Integration tests only
make test-coverage    # Tests with coverage report

# Run linting
make lint
make format
```

## 📦 Deployment Options

### Docker (Recommended)
- Full-stack deployment with Nginx
- Production-ready configuration
- Easy scaling and management

### GitHub Pages
- Free frontend hosting
- Automatic deployment on push
- Perfect for demos and portfolios

### Railway
- Easy backend deployment
- Automatic scaling
- Built-in database support

### Custom VPS
- Full control over infrastructure
- Custom domain support
- Advanced configuration options

## 🤝 Contributing

We welcome contributions! Here's how to get started:

### 1. Fork and Clone
```bash
git clone https://github.com/your-username/open-ear-trainer.git
cd open-ear-trainer
```

### 2. Set Up Development Environment
```bash
make setup
pre-commit install
pre-commit install --hook-type pre-push
```

### 3. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 4. Make Your Changes
- Add new exercises in `backend/exercises/`
- Update frontend components in `frontend/src/`
- Add tests for new functionality
- Update documentation as needed

### 5. Test Your Changes
```bash
make test
make lint
make format
```

### 6. Submit a Pull Request
- Ensure all tests pass
- Update documentation
- Follow the existing code style
- Provide a clear description of your changes

### Development Guidelines

- **Code Style**: Use `ruff` for formatting and linting
- **Testing**: Write tests for new functionality
- **Documentation**: Update README and inline comments
- **Commits**: Use clear, descriptive commit messages
- **Exercises**: Follow the plugin architecture pattern

### Adding New Exercises

1. **Choose the appropriate level** (`level1/`, `level2/`, etc.)
2. **Inherit from `BaseExercise`**
3. **Implement required methods**:
   - `generate()`: Create exercise content
   - `check_answer()`: Validate user responses
4. **Define metadata** with difficulty, prerequisites, and objectives
5. **Add tests** for your exercise
6. **Update documentation**

### Adding New Features

1. **Backend**: Add new API endpoints in `api_app/`
2. **Frontend**: Create React components in `frontend/src/`
3. **Audio**: Extend the audio system in `audio_app/`
4. **Music Theory**: Add new theory functions in `music_app/`

## 📚 API Documentation

### Exercise Endpoints

- `GET /api/exercises/` - List all available exercises
- `GET /api/exercises/{id}/` - Get exercise details
- `GET /api/exercises/{id}/generate/` - Generate new exercise instance
- `POST /api/exercises/{id}/check/` - Check user answer

### Audio Endpoints

- `GET /media/audio/{filename}/` - Serve generated audio files

### Example API Usage

```javascript
// Get available exercises
const exercises = await fetch('/api/exercises/').then(r => r.json());

// Generate a new exercise
const exercise = await fetch('/api/exercises/interval_recognition/generate/').then(r => r.json());

// Check an answer
const result = await fetch('/api/exercises/interval_recognition/check/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ answer: 'Perfect Fifth', context: exercise.context })
}).then(r => r.json());
```

## 🐛 Troubleshooting

### Common Issues

1. **Audio not playing**: Check that the proxy is configured correctly
2. **Docker build fails**: Ensure all dependencies are properly installed
3. **Tests failing**: Run `make clean` and try again
4. **Frontend not connecting**: Verify the API URL configuration

### Getting Help

- Check the [Deployment Guide](DEPLOYMENT.md) for detailed setup instructions
- Review the [GitHub Issues](https://github.com/estebanfoucher/open-ear-trainer/issues) for known problems
- Create a new issue with detailed information about your problem

## 📄 License

MIT License - Free to use and modify. See [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- **mingus**: Music theory library
- **FluidSynth**: Audio synthesis engine
- **School Piano SoundFont**: High-quality piano sounds
- **Django & React**: Web frameworks
- **Docker**: Containerization platform

## 🎯 Roadmap

### Planned Features
- [ ] User authentication and progress tracking
- [ ] Advanced exercises (chord progressions, modal recognition)
- [ ] Mobile app support
- [ ] Collaborative learning features
- [ ] Custom exercise creation tools

### Current Status
- ✅ Basic interval recognition exercises
- ✅ Audio generation and playback
- ✅ Docker deployment
- ✅ CI/CD pipeline
- 🔄 User progress tracking (in development)
- 🔄 Advanced exercises (planned)

---

**Happy ear training! 🎵**

For more information, see the [Deployment Guide](DEPLOYMENT.md) or [Contributing Guidelines](CONTRIBUTING.md).
# Force new deployment Sun Oct 19 11:58:31 CEST 2025
