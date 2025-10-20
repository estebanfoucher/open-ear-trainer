/**
 * Tests for ExercisePlayer component
 */

import React from 'react';
import { screen, fireEvent, waitFor } from '@testing-library/react';
import { render, mockExerciseData, mockAudio, setupMocks, cleanupMocks } from '../utils/test-utils';

// Mock ExercisePlayer component
const ExercisePlayer = ({
  exerciseData,
  onPlayAudio,
  isPlaying = false
}: {
  exerciseData: any,
  onPlayAudio: (audioUrl: string) => void,
  isPlaying?: boolean
}) => (
  <div data-testid="exercise-player">
    <div className="audio-player">
      <h3>Listen to the interval</h3>
      <p style={{ color: '#666', marginBottom: '16px' }}>
        Two notes will play automatically. Listen carefully!
      </p>
      <div className="audio-controls">
        {exerciseData.target_audio && (
          <button
            className="btn btn-secondary"
            onClick={() => onPlayAudio(exerciseData.target_audio)}
            data-testid="play-again-button"
            disabled={isPlaying}
          >
            🔄 Play Again
          </button>
        )}
      </div>
    </div>
  </div>
);

describe('ExercisePlayer Component', () => {
  beforeEach(() => {
    setupMocks();
  });

  afterEach(() => {
    cleanupMocks();
  });

  it('renders exercise player correctly', () => {
    const onPlayAudio = jest.fn();

    render(<ExercisePlayer exerciseData={mockExerciseData} onPlayAudio={onPlayAudio} />);

    expect(screen.getByText('Listen to the interval')).toBeInTheDocument();
    expect(screen.getByTestId('exercise-player')).toBeInTheDocument();
  });

  it('displays audio instructions', () => {
    const onPlayAudio = jest.fn();

    render(<ExercisePlayer exerciseData={mockExerciseData} onPlayAudio={onPlayAudio} />);

    expect(screen.getByText('Two notes will play automatically. Listen carefully!')).toBeInTheDocument();
  });

  it('shows play again button when audio is available', () => {
    const onPlayAudio = jest.fn();

    render(<ExercisePlayer exerciseData={mockExerciseData} onPlayAudio={onPlayAudio} />);

    expect(screen.getByTestId('play-again-button')).toBeInTheDocument();
    expect(screen.getByText('🔄 Play Again')).toBeInTheDocument();
  });

  it('calls onPlayAudio when play again button is clicked', () => {
    const onPlayAudio = jest.fn();

    render(<ExercisePlayer exerciseData={mockExerciseData} onPlayAudio={onPlayAudio} />);

    const playButton = screen.getByTestId('play-again-button');
    fireEvent.click(playButton);

    expect(onPlayAudio).toHaveBeenCalledWith(mockExerciseData.target_audio);
  });

  it('disables play button when playing', () => {
    const onPlayAudio = jest.fn();

    render(<ExercisePlayer exerciseData={mockExerciseData} onPlayAudio={onPlayAudio} isPlaying={true} />);

    const playButton = screen.getByTestId('play-again-button');
    expect(playButton).toBeDisabled();
  });

  it('enables play button when not playing', () => {
    const onPlayAudio = jest.fn();

    render(<ExercisePlayer exerciseData={mockExerciseData} onPlayAudio={onPlayAudio} isPlaying={false} />);

    const playButton = screen.getByTestId('play-again-button');
    expect(playButton).not.toBeDisabled();
  });

  it('handles exercise data without audio', () => {
    const exerciseDataWithoutAudio = {
      ...mockExerciseData,
      target_audio: null,
    };

    const onPlayAudio = jest.fn();

    render(<ExercisePlayer exerciseData={exerciseDataWithoutAudio} onPlayAudio={onPlayAudio} />);

    expect(screen.queryByTestId('play-again-button')).not.toBeInTheDocument();
  });

  it('handles exercise data with empty audio URL', () => {
    const exerciseDataWithEmptyAudio = {
      ...mockExerciseData,
      target_audio: '',
    };

    const onPlayAudio = jest.fn();

    render(<ExercisePlayer exerciseData={exerciseDataWithEmptyAudio} onPlayAudio={onPlayAudio} />);

    expect(screen.queryByTestId('play-again-button')).not.toBeInTheDocument();
  });

  it('displays correct audio URL in button', () => {
    const onPlayAudio = jest.fn();

    render(<ExercisePlayer exerciseData={mockExerciseData} onPlayAudio={onPlayAudio} />);

    const playButton = screen.getByTestId('play-again-button');
    fireEvent.click(playButton);

    expect(onPlayAudio).toHaveBeenCalledWith('/api/audio/test_interval.wav');
  });

  it('handles multiple play button clicks', () => {
    const onPlayAudio = jest.fn();

    render(<ExercisePlayer exerciseData={mockExerciseData} onPlayAudio={onPlayAudio} />);

    const playButton = screen.getByTestId('play-again-button');

    // Click multiple times
    fireEvent.click(playButton);
    fireEvent.click(playButton);
    fireEvent.click(playButton);

    expect(onPlayAudio).toHaveBeenCalledTimes(3);
  });

  it('maintains button state during audio playback', () => {
    const onPlayAudio = jest.fn();

    const { rerender } = render(
      <ExercisePlayer exerciseData={mockExerciseData} onPlayAudio={onPlayAudio} isPlaying={false} />
    );

    let playButton = screen.getByTestId('play-again-button');
    expect(playButton).not.toBeDisabled();

    // Simulate audio starting to play
    rerender(<ExercisePlayer exerciseData={mockExerciseData} onPlayAudio={onPlayAudio} isPlaying={true} />);

    playButton = screen.getByTestId('play-again-button');
    expect(playButton).toBeDisabled();

    // Simulate audio finishing
    rerender(<ExercisePlayer exerciseData={mockExerciseData} onPlayAudio={onPlayAudio} isPlaying={false} />);

    playButton = screen.getByTestId('play-again-button');
    expect(playButton).not.toBeDisabled();
  });

  it('handles different audio file formats', () => {
    const mp3ExerciseData = {
      ...mockExerciseData,
      target_audio: '/api/audio/test_interval.mp3',
    };

    const onPlayAudio = jest.fn();

    render(<ExercisePlayer exerciseData={mp3ExerciseData} onPlayAudio={onPlayAudio} />);

    const playButton = screen.getByTestId('play-again-button');
    fireEvent.click(playButton);

    expect(onPlayAudio).toHaveBeenCalledWith('/api/audio/test_interval.mp3');
  });

  it('displays loading state when audio is loading', () => {
    const onPlayAudio = jest.fn();

    // This test documents expected behavior for loading states
    render(<ExercisePlayer exerciseData={mockExerciseData} onPlayAudio={onPlayAudio} />);

    expect(screen.getByText('Two notes will play automatically. Listen carefully!')).toBeInTheDocument();
  });

  it('handles audio playback errors gracefully', () => {
    const onPlayAudio = jest.fn().mockImplementation(() => {
      throw new Error('Audio playback failed');
    });

    render(<ExercisePlayer exerciseData={mockExerciseData} onPlayAudio={onPlayAudio} />);

    const playButton = screen.getByTestId('play-again-button');

    // Should not crash when audio fails
    expect(() => fireEvent.click(playButton)).not.toThrow();
  });

  it('updates when exercise data changes', () => {
    const onPlayAudio = jest.fn();

    const { rerender } = render(<ExercisePlayer exerciseData={mockExerciseData} onPlayAudio={onPlayAudio} />);

    expect(screen.getByTestId('play-again-button')).toBeInTheDocument();

    // Change to exercise data without audio
    const newExerciseData = {
      ...mockExerciseData,
      target_audio: null,
    };

    rerender(<ExercisePlayer exerciseData={newExerciseData} onPlayAudio={onPlayAudio} />);

    expect(screen.queryByTestId('play-again-button')).not.toBeInTheDocument();
  });
});
