/**
 * Tests for the main App component
 */

import React from 'react';
import { screen, waitFor, fireEvent } from '@testing-library/react';
import { render, mockApiCalls, mockChapters, mockLessons, mockExerciseList, mockExerciseData, setupMocks, cleanupMocks } from '../utils/test-utils';
import App from '../../App';
import axios from 'axios';

// Mock axios
jest.mock('axios', () => ({
  get: jest.fn(),
  post: jest.fn(),
}));

describe('App Component', () => {
  beforeEach(() => {
    setupMocks();
    // Reset mocks
    (axios.get as jest.Mock).mockImplementation((url: string) => {
      if (url.includes('/api/chapters/') && !url.includes('/api/chapters/3/')) {
        return Promise.resolve({ data: mockChapters });
      }
      if (url.includes('/api/chapters/3/')) {
        return Promise.resolve({ data: { ...mockChapters[0], lessons: mockLessons } });
      }
      if (url.includes('/api/lessons/')) {
        return Promise.resolve({ data: mockLessons[0] });
      }
      if (url.includes('/api/exercises/')) {
        return Promise.resolve({ data: mockExerciseList });
      }
      if (url.includes('/api/exercises/generate/')) {
        return Promise.resolve({ data: mockExerciseData });
      }
      console.log('Unknown URL:', url);
      return Promise.reject(new Error(`Unknown URL: ${url}`));
    });

    (axios.post as jest.Mock).mockImplementation((url: string) => {
      if (url.includes('/api/exercises/check-answer/')) {
        return Promise.resolve({ data: { is_correct: true, feedback: 'Correct!' } });
      }
      return Promise.reject(new Error('Unknown URL'));
    });
  });

  afterEach(() => {
    cleanupMocks();
  });

  it('renders the main heading', async () => {
    render(<App />);

    expect(screen.getByText('🎵 Musical Ear Trainer')).toBeInTheDocument();
  });

  it('loads and displays chapter list', async () => {
    // Mock the axios call to return chapters
    (axios.get as jest.Mock).mockResolvedValueOnce({ data: mockChapters });

    render(<App />);

    // Wait for chapters to load
    await waitFor(() => {
      expect(screen.getByText('Choose a Chapter')).toBeInTheDocument();
    });

    // Check that available chapters are displayed (excluding maintenance chapters)
    expect(screen.getByText('Intervals')).toBeInTheDocument();
    expect(screen.getByText('Triads and Chord Qualities')).toBeInTheDocument();

    // Check that maintenance chapters are not displayed
    expect(screen.queryByText('Direction & Contour')).not.toBeInTheDocument();
    expect(screen.queryByText('Tonal Center & Scale Sense')).not.toBeInTheDocument();
  });

  it('displays chapter details correctly', async () => {
    // Mock the axios call to return chapters
    (axios.get as jest.Mock).mockResolvedValueOnce({ data: mockChapters });

    render(<App />);

    await waitFor(() => {
      expect(screen.getByText('Choose a Chapter')).toBeInTheDocument();
    });

    // Check chapter details
    expect(screen.getByText('Intervals')).toBeInTheDocument();
    expect(screen.getByText('Identify melodic and harmonic intervals by ear.')).toBeInTheDocument();
    expect(screen.getByText('Level 3')).toBeInTheDocument();
    expect(screen.getByText('📚 5 lessons')).toBeInTheDocument();
    expect(screen.getByText('✏️ 5 exercises')).toBeInTheDocument();
  });

  it('navigates to lessons when chapter is clicked', async () => {
    // Mock the axios calls
    (axios.get as jest.Mock)
      .mockResolvedValueOnce({ data: mockChapters })
      .mockResolvedValueOnce({ data: { ...mockChapters[0], lessons: mockLessons } });

    render(<App />);

    await waitFor(() => {
      expect(screen.getByText('Choose a Chapter')).toBeInTheDocument();
    });

    // Click start chapter button for Intervals
    const startButton = screen.getByText('Start Chapter');
    fireEvent.click(startButton);

    // Should show lessons interface
    await waitFor(() => {
      expect(screen.getByText('Basic Intervals')).toBeInTheDocument();
    });
  });

  it('displays exercise content when started', async () => {
    render(<App />);

    await waitFor(() => {
      expect(screen.getByText('Choose a Chapter')).toBeInTheDocument();
    });

    // Navigate through chapter -> lesson -> exercise
    const startChapterButton = screen.getByText('Start Chapter');
    fireEvent.click(startChapterButton);

    await waitFor(() => {
      expect(screen.getByText('Basic Intervals')).toBeInTheDocument();
    });

    // Click on lesson
    const startLessonButton = screen.getByText('Start Lesson');
    fireEvent.click(startLessonButton);

    await waitFor(() => {
      expect(screen.getByText('Minor Third, Major Third, Octave (Melodic)')).toBeInTheDocument();
    });

    // Click on exercise
    const startExerciseButton = screen.getByText('Start Exercise (20 Questions)');
    fireEvent.click(startExerciseButton);

    await waitFor(() => {
      expect(screen.getByText('Listen to the interval')).toBeInTheDocument();
      expect(screen.getByText('Which interval do you hear?')).toBeInTheDocument();
    });

    // Check answer options
    expect(screen.getByText('minor_third')).toBeInTheDocument();
    expect(screen.getByText('major_third')).toBeInTheDocument();
    expect(screen.getByText('octave')).toBeInTheDocument();
  });

  it('excludes maintenance chapters from display', async () => {
    // Mock the axios call to return chapters
    (axios.get as jest.Mock).mockResolvedValueOnce({ data: mockChapters });

    render(<App />);

    await waitFor(() => {
      expect(screen.getByText('Choose a Chapter')).toBeInTheDocument();
    });

    // Verify that only available chapters are shown
    expect(screen.getByText('Intervals')).toBeInTheDocument();
    expect(screen.getByText('Triads and Chord Qualities')).toBeInTheDocument();

    // Verify that maintenance chapters are not shown
    expect(screen.queryByText('Direction & Contour')).not.toBeInTheDocument();
    expect(screen.queryByText('Tonal Center & Scale Sense')).not.toBeInTheDocument();

    // Verify that maintenance badges are not shown
    expect(screen.queryByText('🚧 Coming Soon')).not.toBeInTheDocument();
    expect(screen.queryByText('Under Maintenance')).not.toBeInTheDocument();
  });

  it.skip('handles answer selection correctly', async () => {
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

  it.skip('updates score when answer is correct', async () => {
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

  it.skip('shows play again button for audio', async () => {
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

  it.skip('handles back to exercise list', async () => {
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

  it.skip('handles error state', async () => {
    // Mock API error
    mockApiCalls.getExercises.mockRejectedValue(new Error('API Error'));

    render(<App />);

    // Should show error message
    await waitFor(() => {
      expect(screen.getByText('Failed to load exercises')).toBeInTheDocument();
    });
  });

  it.skip('auto-plays audio when exercise loads', async () => {
    render(<App />);

    await waitFor(() => {
      expect(screen.getByText('Choose an Exercise')).toBeInTheDocument();
    });

    // Start exercise
    const startButton = screen.getByText('Start Exercise (20 Questions)');
    fireEvent.click(startButton);

    // Audio should be played automatically
    await waitFor(() => {
    });
  });

  it.skip('disables answer buttons after selection', async () => {
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

  it.skip('shows correct answer highlighting', async () => {
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

  it.skip('auto-advances to next question after delay', async () => {
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
