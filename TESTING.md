# Testing Infrastructure

This document describes the comprehensive testing infrastructure for the Open Ear Trainer application.

## Overview

The testing infrastructure provides comprehensive coverage across all layers of the application:

- **Backend Tests**: Unit, integration, and API tests for Django backend
- **Frontend Tests**: Component, integration, and unit tests for React frontend
- **E2E Tests**: End-to-end tests using Playwright
- **Performance Tests**: Load and performance testing
- **Security Tests**: Security scanning and vulnerability assessment

## Test Structure

### Backend Tests (`backend/tests/`)

#### Unit Tests
- **Exercise Tests** (`test_exercises/`)
  - `test_base_exercise.py` - Base exercise class and metadata tests
  - `test_interval_exercises.py` - Interval exercise implementation tests
- **Audio Tests** (`test_audio/`)
  - `test_synthesizer.py` - Audio synthesis and soundfont tests
  - `test_soundfont_switching.py` - Soundfont switching functionality
- **API Tests** (`test_api/`)
  - `test_serializers.py` - API serializer validation tests
  - `test_views.py` - API endpoint tests
- **Structure Tests** (`test_structure/`)
  - `test_chapters_lessons.py` - Chapter/lesson hierarchy tests

#### Integration Tests
- **Workflow Tests** (`integration/`)
  - `test_exercise_workflow.py` - Complete exercise workflow tests
  - `test_api_contracts.py` - API contract and schema tests

#### Performance Tests
- **Load Tests** (`performance/`)
  - `test_audio_load.py` - Audio generation performance tests
  - `test_scaling.py` - Scalability tests for hierarchical structure

### Frontend Tests (`frontend/src/__tests__/`)

#### Component Tests
- `components/App.test.tsx` - Main application component tests
- `components/ExerciseList.test.tsx` - Exercise list component tests
- `components/ExercisePlayer.test.tsx` - Audio player component tests
- `components/AnswerOptions.test.tsx` - Answer selection component tests

#### Integration Tests
- `integration/` - API integration tests with MSW mocking

#### Test Utilities
- `utils/test-utils.tsx` - Shared test utilities and mocks

### E2E Tests (`e2e/`)

#### Test Suites
- `tests/exercise-flow.spec.ts` - Complete exercise flow tests
- `tests/chapter-navigation.spec.ts` - Chapter navigation tests (future feature)

#### Configuration
- `playwright.config.ts` - Playwright configuration
- `package.json` - E2E test dependencies

## Running Tests

### Backend Tests

```bash
# Run all backend tests
make test-backend

# Run specific test categories
make test-exercises    # Exercise tests
make test-api         # API tests
make test-audio       # Audio tests
make test-structure   # Structure tests

# Run with coverage
make test-coverage

# Run performance tests
make test-performance
```

### Frontend Tests

```bash
# Run frontend tests
make test-frontend

# Or directly
cd frontend && npm test
```

### E2E Tests

```bash
# Run E2E tests
make test-e2e

# Or directly
cd e2e && npm test
```

### All Tests

```bash
# Run all tests (backend, frontend, E2E)
make test-all
```

## Test Configuration

### Backend Configuration

- **Test Settings**: `backend/config/settings/test.py`
- **Pytest Config**: `pyproject.toml` (pytest section)
- **Test Fixtures**: `backend/tests/conftest.py`
- **Coverage Config**: `pyproject.toml` (coverage section)

### Frontend Configuration

- **Jest Config**: `frontend/jest.config.js`
- **Test Setup**: `frontend/src/setupTests.ts`
- **Package Config**: `frontend/package.json` (test scripts)

### E2E Configuration

- **Playwright Config**: `e2e/playwright.config.ts`
- **Test Dependencies**: `e2e/package.json`

## Test Data and Fixtures

### Backend Fixtures (`backend/tests/fixtures/`)

- **Exercises**: `exercises/sample_exercises.json`
- **Chapters**: `chapters/sample_chapters.json`
- **Audio**: Sample soundfont files and expected audio samples

### Frontend Mocks (`frontend/src/__tests__/utils/`)

- **API Mocks**: Mock API responses and axios
- **Audio Mocks**: Mock audio playback functionality
- **Component Mocks**: Mock components and utilities

## CI/CD Integration

### GitHub Actions Workflow (`.github/workflows/test.yml`)

The comprehensive testing pipeline includes:

1. **Backend Tests**
   - Unit tests with coverage
   - API tests
   - Audio tests
   - Structure tests
   - Integration tests
   - Linting and type checking

2. **Frontend Tests**
   - Component tests
   - Integration tests
   - Build verification

3. **E2E Tests**
   - Cross-browser testing
   - Complete user journey tests
   - Mobile responsiveness tests

4. **Performance Tests**
   - Load testing
   - Performance benchmarks

5. **Security Tests**
   - Security scanning
   - Vulnerability assessment

### Coverage Reporting

- **Backend**: Coverage reports generated and uploaded to Codecov
- **Frontend**: Coverage reports generated and uploaded to Codecov
- **Thresholds**: Minimum 70% coverage required

## Test Best Practices

### Backend Testing

1. **Use fixtures** for consistent test data
2. **Mock external dependencies** (audio files, network calls)
3. **Test edge cases** and error conditions
4. **Use descriptive test names** that explain the scenario
5. **Group related tests** in classes
6. **Use parametrized tests** for similar scenarios

### Frontend Testing

1. **Test user interactions** not implementation details
2. **Use data-testid** for reliable element selection
3. **Mock API calls** with MSW
4. **Test accessibility** with screen readers
5. **Test responsive behavior** on different screen sizes
6. **Use custom render** with providers

### E2E Testing

1. **Test complete user journeys** not individual features
2. **Use page object pattern** for complex interactions
3. **Test across multiple browsers** and devices
4. **Use realistic test data** that matches production
5. **Test error scenarios** and edge cases
6. **Keep tests independent** and parallelizable

## Debugging Tests

### Backend Debugging

```bash
# Run specific test with verbose output
pytest backend/tests/test_exercises/test_base_exercise.py::TestBaseExercise::test_exercise_initialization -v

# Run with debugging
pytest backend/tests/ --pdb

# Run with coverage and HTML report
pytest backend/tests/ --cov=backend --cov-report=html
```

### Frontend Debugging

```bash
# Run tests in watch mode
cd frontend && npm test

# Run specific test file
cd frontend && npm test -- --testPathPattern=App.test.tsx

# Run with debugging
cd frontend && npm test -- --verbose --no-coverage
```

### E2E Debugging

```bash
# Run with headed browser
cd e2e && npx playwright test --headed

# Run with debugging
cd e2e && npx playwright test --debug

# Run specific test
cd e2e && npx playwright test exercise-flow.spec.ts
```

## Performance Testing

### Audio Generation Performance

Tests verify that audio generation completes within acceptable time limits:
- Single audio file: < 5 seconds
- Multiple files: < 30 seconds for 10 files
- Cache effectiveness: > 80% hit rate

### API Performance

Tests verify API response times:
- Exercise list: < 1 second
- Exercise generation: < 10 seconds
- Answer checking: < 2 seconds

### Frontend Performance

Tests verify frontend performance:
- Initial load: < 3 seconds
- Component rendering: < 100ms
- Audio playback: < 500ms

## Security Testing

### Backend Security

- **Bandit**: Python security linting
- **Safety**: Dependency vulnerability scanning
- **Input validation**: Test for injection attacks
- **Authentication**: Test access controls

### Frontend Security

- **XSS prevention**: Test for cross-site scripting
- **CSRF protection**: Test for cross-site request forgery
- **Content Security Policy**: Test CSP compliance

## Future Enhancements

### Planned Improvements

1. **Visual Regression Testing**: Screenshot comparison tests
2. **Accessibility Testing**: Automated a11y testing
3. **Load Testing**: High-volume concurrent user testing
4. **Mobile Testing**: Native mobile app testing
5. **Internationalization Testing**: Multi-language support testing

### Test Coverage Goals

- **Backend**: > 90% coverage
- **Frontend**: > 85% coverage
- **E2E**: > 80% user journey coverage
- **Performance**: 100% critical path coverage

## Troubleshooting

### Common Issues

1. **Audio tests failing**: Check soundfont file availability
2. **E2E tests flaky**: Increase timeouts, check network stability
3. **Frontend tests slow**: Optimize mocks, reduce test data size
4. **Coverage gaps**: Add tests for uncovered code paths

### Getting Help

1. Check test logs for detailed error messages
2. Run tests locally to reproduce CI failures
3. Review test documentation and examples
4. Check GitHub Actions logs for CI-specific issues

## Contributing

When adding new tests:

1. **Follow naming conventions**: Use descriptive test names
2. **Add to appropriate category**: Unit, integration, or E2E
3. **Update documentation**: Add test descriptions
4. **Ensure CI passes**: All tests must pass in CI
5. **Maintain coverage**: Don't decrease overall coverage
6. **Add fixtures**: Use shared test data when possible
