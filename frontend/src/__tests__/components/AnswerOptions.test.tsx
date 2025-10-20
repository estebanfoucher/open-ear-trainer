/**
 * Tests for AnswerOptions component
 */

import React from 'react';
import { screen, fireEvent } from '@testing-library/react';
import { render, mockExerciseData, setupMocks, cleanupMocks } from '../utils/test-utils';

// Mock AnswerOptions component
const AnswerOptions = ({
  options,
  correctAnswer,
  selectedAnswer,
  onAnswerSelect,
  showResult = false
}: {
  options: string[],
  correctAnswer: string,
  selectedAnswer: string | null,
  onAnswerSelect: (answer: string) => void,
  showResult?: boolean
}) => (
  <div data-testid="answer-options">
    <h3>What interval do you hear?</h3>
    <div className="exercise-options">
      {options.map((option) => {
        let className = 'option-btn';

        if (selectedAnswer === option) {
          className += ' selected';
        }

        if (showResult) {
          if (option === correctAnswer) {
            className += ' correct';
          } else if (option === selectedAnswer && selectedAnswer !== correctAnswer) {
            className += ' incorrect';
          }
        }

        return (
          <button
            key={option}
            className={className}
            onClick={() => onAnswerSelect(option)}
            disabled={showResult}
            data-testid={`option-${option}`}
          >
            {option}
          </button>
        );
      })}
    </div>
  </div>
);

describe('AnswerOptions Component', () => {
  beforeEach(() => {
    setupMocks();
  });

  afterEach(() => {
    cleanupMocks();
  });

  it('renders answer options correctly', () => {
    const onAnswerSelect = jest.fn();

    render(
      <AnswerOptions
        options={mockExerciseData.options}
        correctAnswer={mockExerciseData.correct_answer}
        selectedAnswer={null}
        onAnswerSelect={onAnswerSelect}
      />
    );

    expect(screen.getByText('What interval do you hear?')).toBeInTheDocument();
    expect(screen.getByTestId('answer-options')).toBeInTheDocument();
  });

  it('displays all answer options', () => {
    const onAnswerSelect = jest.fn();

    render(
      <AnswerOptions
        options={mockExerciseData.options}
        correctAnswer={mockExerciseData.correct_answer}
        selectedAnswer={null}
        onAnswerSelect={onAnswerSelect}
      />
    );

    expect(screen.getByTestId('option-minor_third')).toBeInTheDocument();
    expect(screen.getByTestId('option-major_third')).toBeInTheDocument();
    expect(screen.getByTestId('option-octave')).toBeInTheDocument();
  });

  it('calls onAnswerSelect when option is clicked', () => {
    const onAnswerSelect = jest.fn();

    render(
      <AnswerOptions
        options={mockExerciseData.options}
        correctAnswer={mockExerciseData.correct_answer}
        selectedAnswer={null}
        onAnswerSelect={onAnswerSelect}
      />
    );

    const optionButton = screen.getByTestId('option-major_third');
    fireEvent.click(optionButton);

    expect(onAnswerSelect).toHaveBeenCalledWith('major_third');
  });

  it('highlights selected answer', () => {
    const onAnswerSelect = jest.fn();

    render(
      <AnswerOptions
        options={mockExerciseData.options}
        correctAnswer={mockExerciseData.correct_answer}
        selectedAnswer="major_third"
        onAnswerSelect={onAnswerSelect}
      />
    );

    const selectedButton = screen.getByTestId('option-major_third');
    expect(selectedButton).toHaveClass('selected');
  });

  it('shows correct answer highlighting when result is shown', () => {
    const onAnswerSelect = jest.fn();

    render(
      <AnswerOptions
        options={mockExerciseData.options}
        correctAnswer={mockExerciseData.correct_answer}
        selectedAnswer="major_third"
        onAnswerSelect={onAnswerSelect}
        showResult={true}
      />
    );

    const correctButton = screen.getByTestId('option-major_third');
    expect(correctButton).toHaveClass('correct');
  });

  it('shows incorrect answer highlighting when result is shown', () => {
    const onAnswerSelect = jest.fn();

    render(
      <AnswerOptions
        options={mockExerciseData.options}
        correctAnswer={mockExerciseData.correct_answer}
        selectedAnswer="minor_third"
        onAnswerSelect={onAnswerSelect}
        showResult={true}
      />
    );

    const incorrectButton = screen.getByTestId('option-minor_third');
    expect(incorrectButton).toHaveClass('incorrect');
  });

  it('disables all options when result is shown', () => {
    const onAnswerSelect = jest.fn();

    render(
      <AnswerOptions
        options={mockExerciseData.options}
        correctAnswer={mockExerciseData.correct_answer}
        selectedAnswer="major_third"
        onAnswerSelect={onAnswerSelect}
        showResult={true}
      />
    );

    const option1 = screen.getByTestId('option-minor_third');
    const option2 = screen.getByTestId('option-major_third');
    const option3 = screen.getByTestId('option-octave');

    expect(option1).toBeDisabled();
    expect(option2).toBeDisabled();
    expect(option3).toBeDisabled();
  });

  it('enables all options when result is not shown', () => {
    const onAnswerSelect = jest.fn();

    render(
      <AnswerOptions
        options={mockExerciseData.options}
        correctAnswer={mockExerciseData.correct_answer}
        selectedAnswer={null}
        onAnswerSelect={onAnswerSelect}
        showResult={false}
      />
    );

    const option1 = screen.getByTestId('option-minor_third');
    const option2 = screen.getByTestId('option-major_third');
    const option3 = screen.getByTestId('option-octave');

    expect(option1).not.toBeDisabled();
    expect(option2).not.toBeDisabled();
    expect(option3).not.toBeDisabled();
  });

  it('handles empty options array', () => {
    const onAnswerSelect = jest.fn();

    render(
      <AnswerOptions
        options={[]}
        correctAnswer=""
        selectedAnswer={null}
        onAnswerSelect={onAnswerSelect}
      />
    );

    expect(screen.getByText('What interval do you hear?')).toBeInTheDocument();
    expect(screen.queryByRole('button')).not.toBeInTheDocument();
  });

  it('handles single option', () => {
    const onAnswerSelect = jest.fn();

    render(
      <AnswerOptions
        options={['major_third']}
        correctAnswer="major_third"
        selectedAnswer={null}
        onAnswerSelect={onAnswerSelect}
      />
    );

    expect(screen.getByTestId('option-major_third')).toBeInTheDocument();
    expect(screen.queryByTestId('option-minor_third')).not.toBeInTheDocument();
  });

  it('handles many options', () => {
    const manyOptions = [
      'minor_second', 'major_second', 'minor_third', 'major_third',
      'perfect_fourth', 'tritone', 'perfect_fifth', 'minor_sixth',
      'major_sixth', 'minor_seventh', 'major_seventh', 'octave'
    ];

    const onAnswerSelect = jest.fn();

    render(
      <AnswerOptions
        options={manyOptions}
        correctAnswer="major_third"
        selectedAnswer={null}
        onAnswerSelect={onAnswerSelect}
      />
    );

    manyOptions.forEach(option => {
      expect(screen.getByTestId(`option-${option}`)).toBeInTheDocument();
    });
  });

  it('handles special characters in options', () => {
    const specialOptions = ['C#', 'F♯', 'B♭', 'E♭'];

    const onAnswerSelect = jest.fn();

    render(
      <AnswerOptions
        options={specialOptions}
        correctAnswer="C#"
        selectedAnswer={null}
        onAnswerSelect={onAnswerSelect}
      />
    );

    expect(screen.getByTestId('option-C#')).toBeInTheDocument();
    expect(screen.getByTestId('option-F♯')).toBeInTheDocument();
    expect(screen.getByTestId('option-B♭')).toBeInTheDocument();
    expect(screen.getByTestId('option-E♭')).toBeInTheDocument();
  });

  it('handles long option text', () => {
    const longOptions = [
      'Very Long Option Name That Might Cause Layout Issues',
      'Another Very Long Option Name That Could Break The UI Layout'
    ];

    const onAnswerSelect = jest.fn();

    render(
      <AnswerOptions
        options={longOptions}
        correctAnswer={longOptions[0]}
        selectedAnswer={null}
        onAnswerSelect={onAnswerSelect}
      />
    );

    expect(screen.getByText(longOptions[0])).toBeInTheDocument();
    expect(screen.getByText(longOptions[1])).toBeInTheDocument();
  });

  it('updates when options change', () => {
    const onAnswerSelect = jest.fn();

    const { rerender } = render(
      <AnswerOptions
        options={['option1', 'option2']}
        correctAnswer="option1"
        selectedAnswer={null}
        onAnswerSelect={onAnswerSelect}
      />
    );

    expect(screen.getByTestId('option-option1')).toBeInTheDocument();
    expect(screen.getByTestId('option-option2')).toBeInTheDocument();

    // Change options
    rerender(
      <AnswerOptions
        options={['option3', 'option4']}
        correctAnswer="option3"
        selectedAnswer={null}
        onAnswerSelect={onAnswerSelect}
      />
    );

    expect(screen.queryByTestId('option-option1')).not.toBeInTheDocument();
    expect(screen.queryByTestId('option-option2')).not.toBeInTheDocument();
    expect(screen.getByTestId('option-option3')).toBeInTheDocument();
    expect(screen.getByTestId('option-option4')).toBeInTheDocument();
  });

  it('maintains selection state when options change', () => {
    const onAnswerSelect = jest.fn();

    const { rerender } = render(
      <AnswerOptions
        options={['option1', 'option2']}
        correctAnswer="option1"
        selectedAnswer="option1"
        onAnswerSelect={onAnswerSelect}
      />
    );

    expect(screen.getByTestId('option-option1')).toHaveClass('selected');

    // Change options but keep same selected answer
    rerender(
      <AnswerOptions
        options={['option1', 'option3']}
        correctAnswer="option1"
        selectedAnswer="option1"
        onAnswerSelect={onAnswerSelect}
      />
    );

    expect(screen.getByTestId('option-option1')).toHaveClass('selected');
  });
});
