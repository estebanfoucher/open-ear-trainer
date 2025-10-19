/**
 * Tests for ExerciseList component
 */

import React from 'react';
import { screen, fireEvent } from '@testing-library/react';
import { render, mockExerciseList, setupMocks, cleanupMocks } from '../utils/test-utils';

// Mock ExerciseList component (since it's not extracted yet)
const ExerciseList = ({ exercises, onStartExercise }: {
  exercises: any[],
  onStartExercise: (exercise: any) => void
}) => (
  <div data-testid="exercise-list">
    <h2>Choose an Exercise</h2>
    <div className="exercise-list">
      {exercises.map((exercise) => (
        <div key={exercise.id} className="card" data-testid={`exercise-${exercise.id}`}>
          <h3>{exercise.name}</h3>
          <p>{exercise.description}</p>
          <p><strong>Difficulty:</strong> {exercise.difficulty}/10</p>
          <p><strong>Category:</strong> {exercise.category}</p>
          <p><strong>Estimated time:</strong> {exercise.estimated_time} seconds</p>
          <button
            className="btn"
            onClick={() => onStartExercise(exercise)}
            data-testid={`start-${exercise.id}`}
          >
            Start Exercise (20 Questions)
          </button>
        </div>
      ))}
    </div>
  </div>
);

describe('ExerciseList Component', () => {
  beforeEach(() => {
    setupMocks();
  });

  afterEach(() => {
    cleanupMocks();
  });

  it('renders exercise list correctly', () => {
    const onStartExercise = jest.fn();

    render(<ExerciseList exercises={mockExerciseList} onStartExercise={onStartExercise} />);

    expect(screen.getByText('Choose an Exercise')).toBeInTheDocument();
    expect(screen.getByTestId('exercise-list')).toBeInTheDocument();
  });

  it('displays all exercises', () => {
    const onStartExercise = jest.fn();

    render(<ExerciseList exercises={mockExerciseList} onStartExercise={onStartExercise} />);

    expect(screen.getByText('Minor Third, Major Third, Octave (Melodic)')).toBeInTheDocument();
    expect(screen.getByText('Perfect Fourth, Perfect Fifth, Octave (Melodic)')).toBeInTheDocument();
  });

  it('displays exercise details correctly', () => {
    const onStartExercise = jest.fn();

    render(<ExerciseList exercises={mockExerciseList} onStartExercise={onStartExercise} />);

    // Check first exercise details
    expect(screen.getByText('Learn to identify minor third, major third, and octave intervals')).toBeInTheDocument();
    expect(screen.getByText('Difficulty: 3/10')).toBeInTheDocument();
    expect(screen.getByText('Category: interval_recognition')).toBeInTheDocument();
    expect(screen.getByText('Estimated time: 30 seconds')).toBeInTheDocument();
  });

  it('calls onStartExercise when start button is clicked', () => {
    const onStartExercise = jest.fn();

    render(<ExerciseList exercises={mockExerciseList} onStartExercise={onStartExercise} />);

    const startButton = screen.getByTestId('start-minor_third_major_third_octave_melodic');
    fireEvent.click(startButton);

    expect(onStartExercise).toHaveBeenCalledWith(mockExerciseList[0]);
  });

  it('renders start buttons for all exercises', () => {
    const onStartExercise = jest.fn();

    render(<ExerciseList exercises={mockExerciseList} onStartExercise={onStartExercise} />);

    expect(screen.getByTestId('start-minor_third_major_third_octave_melodic')).toBeInTheDocument();
    expect(screen.getByTestId('start-perfect_fourth_fifth_octave_melodic')).toBeInTheDocument();
  });

  it('handles empty exercise list', () => {
    const onStartExercise = jest.fn();

    render(<ExerciseList exercises={[]} onStartExercise={onStartExercise} />);

    expect(screen.getByText('Choose an Exercise')).toBeInTheDocument();
    expect(screen.getByTestId('exercise-list')).toBeInTheDocument();
    expect(screen.queryByRole('button')).not.toBeInTheDocument();
  });

  it('displays exercise tags', () => {
    const onStartExercise = jest.fn();

    render(<ExerciseList exercises={mockExerciseList} onStartExercise={onStartExercise} />);

    // Tags should be displayed (if implemented in the component)
    // This test documents expected behavior
    expect(screen.getByText('interval_recognition')).toBeInTheDocument();
  });

  it('handles exercise with no prerequisites', () => {
    const onStartExercise = jest.fn();

    render(<ExerciseList exercises={mockExerciseList} onStartExercise={onStartExercise} />);

    // All exercises in mock data have empty prerequisites
    expect(screen.getByTestId('start-minor_third_major_third_octave_melodic')).toBeInTheDocument();
    expect(screen.getByTestId('start-perfect_fourth_fifth_octave_melodic')).toBeInTheDocument();
  });

  it('displays learning objectives', () => {
    const onStartExercise = jest.fn();

    render(<ExerciseList exercises={mockExerciseList} onStartExercise={onStartExercise} />);

    // Learning objectives should be displayed (if implemented)
    expect(screen.getByText('Identify minor third intervals')).toBeInTheDocument();
    expect(screen.getByText('Identify major third intervals')).toBeInTheDocument();
    expect(screen.getByText('Identify octave intervals')).toBeInTheDocument();
  });

  it('handles long exercise names', () => {
    const longNameExercise = {
      ...mockExerciseList[0],
      name: 'Very Long Exercise Name That Might Cause Layout Issues In The UI Component',
    };

    const onStartExercise = jest.fn();

    render(<ExerciseList exercises={[longNameExercise]} onStartExercise={onStartExercise} />);

    expect(screen.getByText(longNameExercise.name)).toBeInTheDocument();
  });

  it('handles special characters in exercise names', () => {
    const specialCharExercise = {
      ...mockExerciseList[0],
      name: 'Exercise with Special Characters: ♪ ♫ ♬ ♭ ♮ ♯',
    };

    const onStartExercise = jest.fn();

    render(<ExerciseList exercises={[specialCharExercise]} onStartExercise={onStartExercise} />);

    expect(screen.getByText(specialCharExercise.name)).toBeInTheDocument();
  });
});
