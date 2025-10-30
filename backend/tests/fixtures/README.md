# Test Fixtures

This directory contains test fixtures and sample data for the Open Ear Trainer testing suite.

## Structure

- `soundfonts/` - Sample soundfont files for audio testing
- `audio/` - Expected audio file samples for comparison
- `exercises/` - Exercise data fixtures
- `chapters/` - Chapter/lesson hierarchy fixtures

## Usage

These fixtures are used by the test suite to provide consistent test data across different test scenarios.

## Adding New Fixtures

When adding new fixtures:

1. Place them in the appropriate subdirectory
2. Update the relevant test files to use the new fixtures
3. Document the fixture in this README
4. Ensure fixtures are lightweight and don't slow down tests

## Fixture Guidelines

- Keep fixtures small and focused
- Use realistic but minimal data
- Avoid large binary files unless necessary
- Include both positive and negative test cases
- Document the purpose of each fixture
