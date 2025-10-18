# Contributing to Open Ear Trainer

Thank you for your interest in contributing to Open Ear Trainer! This guide will help you get started with contributing to the project.

## 🚀 Getting Started

### Prerequisites

Before contributing, make sure you have:

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- Git
- A GitHub account

### Development Setup

1. **Fork the repository** on GitHub
2. **Clone your fork:**
   ```bash
   git clone https://github.com/your-username/open-ear-trainer.git
   cd open-ear-trainer
   ```

3. **Set up the development environment:**
   ```bash
   make setup
   pre-commit install
   pre-commit install --hook-type pre-push
   ```

4. **Start the development environment:**
   ```bash
   python deploy.py docker --env dev
   ```

## 🎯 Types of Contributions

### 🎵 Adding New Exercises

Exercises are the core of the application. Here's how to add new ones:

#### 1. Choose the Right Level
- **Level 1**: Beginner exercises (intervals, basic chords)
- **Level 2**: Intermediate exercises (chord progressions, scales)
- **Level 3**: Advanced exercises (modal recognition, complex harmony)

#### 2. Create the Exercise File
Create a new file in the appropriate level directory:
```bash
backend/exercises/level1/my_new_exercise.py
```

#### 3. Implement the Exercise
```python
from exercises.base.exercise import BaseExercise
from exercises.base.metadata import ExerciseMetadata
from exercises.base.interval_exercise import IntervalExerciseData, IntervalExerciseResult

class MyNewExercise(BaseExercise):
    metadata = ExerciseMetadata(
        id="my_new_exercise",
        name="My New Exercise",
        description="A description of what this exercise teaches",
        difficulty=2,  # 1-5 scale
        prerequisites=["basic_intervals"],
        learning_objectives=[
            "Learn to identify perfect intervals",
            "Develop aural recognition skills"
        ],
        category="interval_recognition",
        tags=["intervals", "perfect", "melodic"]
    )
    
    def generate(self, **kwargs) -> IntervalExerciseData:
        # Generate exercise content
        # Return IntervalExerciseData with audio, options, etc.
        pass
    
    def check_answer(self, answer: str, context: dict) -> IntervalExerciseResult:
        # Validate user answer
        # Return IntervalExerciseResult with correctness and feedback
        pass
```

#### 4. Add Tests
Create tests in `backend/tests/test_exercises.py`:
```python
def test_my_new_exercise():
    exercise = MyNewExercise()
    data = exercise.generate()
    result = exercise.check_answer("Perfect Fifth", data.context)
    assert result.is_correct
```

### 🎨 Frontend Improvements

#### Adding New Components
1. Create components in `frontend/src/components/`
2. Use TypeScript for type safety
3. Follow React best practices
4. Add proper error handling

#### Styling Guidelines
- Use CSS modules or styled-components
- Follow the existing design system
- Ensure responsive design
- Test on multiple browsers

### 🔧 Backend Enhancements

#### API Endpoints
- Add new endpoints in `backend/api_app/views.py`
- Use Django REST Framework serializers
- Add proper error handling and validation
- Include API documentation

#### Music Theory Extensions
- Extend `backend/music_app/` with new theory functions
- Add support for new scales, chords, or progressions
- Ensure compatibility with existing exercises

### 🐳 Docker and Deployment

#### Docker Improvements
- Optimize Docker images for size and performance
- Add new environment configurations
- Improve build scripts and automation

#### CI/CD Enhancements
- Add new GitHub Actions workflows
- Improve testing and deployment pipelines
- Add security scanning and code quality checks

## 📝 Code Style and Standards

### Python (Backend)
- Use `ruff` for formatting and linting
- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Write docstrings for all public functions

### TypeScript/JavaScript (Frontend)
- Use ESLint and Prettier
- Follow React best practices
- Use functional components with hooks
- Implement proper error boundaries

### General Guidelines
- Write clear, descriptive commit messages
- Keep functions small and focused
- Add comments for complex logic
- Use meaningful variable and function names

## 🧪 Testing

### Running Tests
```bash
# Run all tests
make test

# Run specific test types
make test-unit        # Unit tests only
make test-integration # Integration tests only
make test-coverage    # Tests with coverage report

# Run frontend tests
cd frontend && npm test
```

### Writing Tests
- Write tests for all new functionality
- Aim for high test coverage
- Use descriptive test names
- Test both success and failure cases

### Test Structure
```python
def test_exercise_generation():
    """Test that exercise generates valid data."""
    exercise = MyExercise()
    data = exercise.generate()
    
    assert data is not None
    assert data.target_audio is not None
    assert len(data.options) > 0
    assert data.correct_answer in data.options
```

## 📋 Pull Request Process

### 1. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes
- Write your code following the style guidelines
- Add tests for new functionality
- Update documentation as needed
- Ensure all tests pass

### 3. Commit Your Changes
```bash
git add .
git commit -m "Add new interval recognition exercise

- Implement perfect fourth and fifth recognition
- Add audio generation for melodic intervals
- Include comprehensive test coverage
- Update documentation"
```

### 4. Push and Create PR
```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub with:
- Clear title and description
- Reference any related issues
- Include screenshots for UI changes
- List any breaking changes

### 5. Review Process
- Address any feedback from reviewers
- Make necessary changes
- Ensure CI/CD checks pass
- Update documentation if needed

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Clear description** of the issue
2. **Steps to reproduce** the problem
3. **Expected vs actual behavior**
4. **Environment details** (OS, browser, Python/Node versions)
5. **Screenshots or error messages** if applicable

### Bug Report Template
```markdown
## Bug Description
Brief description of the bug

## Steps to Reproduce
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

## Expected Behavior
What you expected to happen

## Actual Behavior
What actually happened

## Environment
- OS: [e.g. macOS, Windows, Linux]
- Browser: [e.g. Chrome, Firefox, Safari]
- Python version: [e.g. 3.11.0]
- Node version: [e.g. 18.17.0]

## Additional Context
Any other context about the problem
```

## 💡 Feature Requests

When suggesting new features:

1. **Check existing issues** to avoid duplicates
2. **Describe the use case** and why it's valuable
3. **Provide implementation ideas** if you have them
4. **Consider the impact** on existing functionality

### Feature Request Template
```markdown
## Feature Description
Brief description of the feature

## Use Case
Why would this feature be useful?

## Proposed Implementation
How do you think this could be implemented?

## Alternatives Considered
What other approaches have you considered?

## Additional Context
Any other context or screenshots
```

## 🏷️ Issue Labels

We use the following labels to categorize issues:

- `bug`: Something isn't working
- `enhancement`: New feature or request
- `documentation`: Improvements to documentation
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention is needed
- `question`: Further information is requested
- `wontfix`: This will not be worked on

## 📚 Resources

### Documentation
- [Django Documentation](https://docs.djangoproject.com/)
- [React Documentation](https://reactjs.org/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [mingus Documentation](https://bspaans.github.io/python-mingus/)

### Music Theory Resources
- [Music Theory for Musicians](https://www.musictheory.net/)
- [Ear Training Resources](https://www.teoria.com/)
- [Interval Recognition Guide](https://www.musictheoryacademy.com/)

### Development Tools
- [VS Code](https://code.visualstudio.com/) - Recommended editor
- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- [Postman](https://www.postman.com/) - API testing

## 🤝 Community Guidelines

### Code of Conduct
- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Respect different opinions and approaches

### Communication
- Use clear, descriptive language
- Be patient with questions
- Provide helpful feedback
- Share knowledge and resources

## 📞 Getting Help

If you need help:

1. **Check the documentation** first
2. **Search existing issues** for similar problems
3. **Ask in discussions** for general questions
4. **Create an issue** for bugs or feature requests
5. **Join our community** (if available)

## 🎉 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation
- Community highlights

Thank you for contributing to Open Ear Trainer! 🎵
