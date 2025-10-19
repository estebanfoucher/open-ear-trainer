/**
 * Tests for the main App component
 */

import React from 'react';
import { screen, waitFor, fireEvent } from '@testing-library/react';
import { render, mockApiCalls, mockExerciseList, mockExerciseData, setupMocks, cleanupMocks } from '../utils/test-utils';
import App from '../../App';

// Mock axios
jest.mock('axios', () => ({
  get: jest.fn(),
  post: jest.fn(),
}));

describe('App Component', () => {
  beforeEach(() => {
    setupMocks();
    // Reset mocks
    mockApiCalls.getExercises.mockResolvedValue({ data: mockExerciseList });
    mockApiCalls.generateExercise.mockResolvedValue({ data: mockExerciseData });
  });

  afterEach(() => {
    cleanupMocks();
  });

  it('renders the main heading', async () => {
    render(<App />);

    expect(screen.getByText('🎵 Musical Ear Trainer')).toBeInTheDocument();
  });

  it('loads and displays exercise list', async () => {
    render(<App />);

    // Wait for exercises to load
    await waitFor(() => {
      expect(screen.getByText('Choose an Exercise')).toBeInTheDocument();
    });

    // Check that exercises are displayed
    expect(screen.getByText('Minor Third, Major Third, Octave (Melodic)')).toBeInTheDocument();
    expect(screen.getByText('Perfect Fourth, Perfect Fifth, Octave (Melodic)')).toBeInTheDocument();
  });

  it('displays exercise details correctly', async () => {
    render(<App />);

    await waitFor(() => {
      expect(screen.getByText('Choose an Exercise')).toBeInTheDocument();
    });

    // Check exercise details
    expect(screen.getByText('Difficulty: 3/10')).toBeInTheDocument();
    expect(screen.getByText('Category: interval_recognition')).toBeInTheDocument();
    expect(screen.getByText('Estimated time: 30 seconds')).toBeInTheDocument();
  });

  it('starts an exercise when button is clicked', async () => {
    render(<App />);

    await waitFor(() => {
      expect(screen.getByText('Choose an Exercise')).toBeInTheDocument();
    });

    // Click start exercise button
    const startButton = screen.getByText('Start Exercise (20 Questions)');
    fireEvent.click(startButton);

    // Should show exercise interface
    await waitFor(() => {
      expect(screen.getByText('Minor Third, Major Third, Octave (Melodic)')).toBeInTheDocument();
      expect(screen.getByText('Question 1/20')).toBeInTheDocument();
    });
  });

  it('displays exercise content when started', async () => {
    render(<App />);

    await waitFor(() => {
      expect(screen.getByText('Choose an Exercise')).toBeInTheDocument();
    });

    // Start exercise
    const startButton = screen.getByText('Start Exercise (20 Questions)');
    fireEvent.click(startButton);

    await waitFor(() => {
      expect(screen.getByText('Listen to the interval')).toBeInTheDocument();
      expect(screen.getByText('What interval do you hear?')).toBeInTheDocument();
    });

    // Check answer options
    expect(screen.getByText('minor_third')).toBeInTheDocument();
    expect(screen.getByText('major_third')).toBeInTheDocument();
    expect(screen.getByText('octave')).toBeInTheDocument();
  });

  it('handles answer selection correctly', async () => {
    render(<App />);

    await waitFor(() => {
      expect(screen.getByText('Choose an Exercise')).toBeInTheDocument();
    });

    // Start exercise
    const startButton = screen.getByText('Start Exercise (20 Questions)');
    fireEvent.click(startButton);

    await waitFor(() => {
      expect(screen.getByText('What interval do you hear?')).toBeInTheDocument();
    });

    // Select an answer
    const answerButton = screen.getByText('major_third');
    fireEvent.click(answerButton);

    // Should show feedback
    await waitFor(() => {
      expect(screen.getByText('Correct!')).toBeInTheDocument();
    });
  });

  it('updates score when answer is correct', async () => {
    render(<App />);

    await waitFor(() => {
      expect(screen.getByText('Choose an Exercise')).toBeInTheDocument();
    });

    // Start exercise
    const startButton = screen.getByText('Start Exercise (20 Questions)');
    fireEvent.click(startButton);

    await waitFor(() => {
      expect(screen.getByText('What interval do you hear?')).toBeInTheDocument();
    });

    // Select correct answer
    const answerButton = screen.getByText('major_third');
    fireEvent.click(answerButton);

    // Check score update
    await waitFor(() => {
      expect(screen.getByText('Score: 1/1')).toBeInTheDocument();
    });
  });

  it('shows play again button for audio', async () => {
    render(<App />);

    await waitFor(() => {
      expect(screen.getByText('Choose an Exercise')).toBeInTheDocument();
    });

    // Start exercise
    const startButton = screen.getByText('Start Exercise (20 Questions)');
    fireEvent.click(startButton);

    await waitFor(() => {
      expect(screen.getByText('🔄 Play Again')).toBeInTheDocument();
    });
  });

  it('handles back to exercise list', async () => {
    render(<App />);

    await waitFor(() => {
      expect(screen.getByText('Choose an Exercise')).toBeInTheDocument();
    });

    // Start exercise
    const startButton = screen.getByText('Start Exercise (20 Questions)');
    fireEvent.click(startButton);

    await waitFor(() => {
      expect(screen.getByText('Question 1/20')).toBeInTheDocument();
    });

    // Go back
    const backButton = screen.getByText('Back to Exercise List');
    fireEvent.click(backButton);

    // Should show exercise list again
    await waitFor(() => {
      expect(screen.getByText('Choose an Exercise')).toBeInTheDocument();
    });
  });

  it('handles loading state', async () => {
    // Mock slow API response
    mockApiCalls.getExercises.mockImplementation(() =>
      new Promise(resolve => setTimeout(() => resolve({ data: mockExerciseList }), 100))
    );

    render(<App />);

    // Should show loading initially
    expect(screen.getByText('Loading...')).toBeInTheDocument();

    // Should hide loading when data loads
    await waitFor(() => {
      expect(screen.queryByText('Loading...')).not.toBeInTheDocument();
    });
  });

  it('handles error state', async () => {
    // Mock API error
    mockApiCalls.getExercises.mockRejectedValue(new Error('API Error'));

    render(<App />);

    // Should show error message
    await waitFor(() => {
      expect(screen.getByText('Failed to load exercises')).toBeInTheDocument();
    });
  });

  it('auto-plays audio when exercise loads', async () => {
    render(<App />);

    await waitFor(() => {
      expect(screen.getByText('Choose an Exercise')).toBeInTheDocument();
    });

    // Start exercise
    const startButton = screen.getByText('Start Exercise (20 Questions)');
    fireEvent.click(startButton);

    // Audio should be played automatically
    await waitFor(() => {
      expect(screen.getByText('Two notes will play automatically. Listen carefully!')).toBeInTheDocument();
    });
  });

  it('disables answer buttons after selection', async () => {
    render(<App />);

    await waitFor(() => {
      expect(screen.getByText('Choose an Exercise')).toBeInTheDocument();
    });

    // Start exercise
    const startButton = screen.getByText('Start Exercise (20 Questions)');
    fireEvent.click(startButton);

    await waitFor(() => {
      expect(screen.getByText('What interval do you hear?')).toBeInTheDocument();
    });

    // Select an answer
    const answerButton = screen.getByText('major_third');
    fireEvent.click(answerButton);

    // All answer buttons should be disabled
    await waitFor(() => {
      const buttons = screen.getAllByRole('button');
      const answerButtons = buttons.filter(button =>
        button.textContent === 'minor_third' ||
        button.textContent === 'major_third' ||
        button.textContent === 'octave'
      );

      answerButtons.forEach(button => {
        expect(button).toBeDisabled();
      });
    });
  });

  it('shows correct answer highlighting', async () => {
    render(<App />);

    await waitFor(() => {
      expect(screen.getByText('Choose an Exercise')).toBeInTheDocument();
    });

    // Start exercise
    const startButton = screen.getByText('Start Exercise (20 Questions)');
    fireEvent.click(startButton);

    await waitFor(() => {
      expect(screen.getByText('What interval do you hear?')).toBeInTheDocument();
    });

    // Select wrong answer
    const wrongAnswerButton = screen.getByText('minor_third');
    fireEvent.click(wrongAnswerButton);

    // Should highlight correct and incorrect answers
    await waitFor(() => {
      const correctButton = screen.getByText('major_third');
      const incorrectButton = screen.getByText('minor_third');

      expect(correctButton).toHaveClass('correct');
      expect(incorrectButton).toHaveClass('incorrect');
    });
  });

  it('auto-advances to next question after delay', async () => {
    jest.useFakeTimers();

    render(<App />);

    await waitFor(() => {
      expect(screen.getByText('Choose an Exercise')).toBeInTheDocument();
    });

    // Start exercise
    const startButton = screen.getByText('Start Exercise (20 Questions)');
    fireEvent.click(startButton);

    await waitFor(() => {
      expect(screen.getByText('Question 1/20')).toBeInTheDocument();
    });

    // Select an answer
    const answerButton = screen.getByText('major_third');
    fireEvent.click(answerButton);

    // Fast-forward time
    jest.advanceTimersByTime(2000);

    // Should advance to next question
    await waitFor(() => {
      expect(screen.getByText('Question 2/20')).toBeInTheDocument();
    });

    jest.useRealTimers();
  });
});
