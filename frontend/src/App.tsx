import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

interface Exercise {
  id: string;
  name: string;
  description: string;
  difficulty: number;
  category: string;
  tags: string[];
  estimated_time: number;
  prerequisites: string[];
  learning_objectives: string[];
  input_type: string;
  answer_format: string;
}

interface ExerciseData {
  key: string;
  scale: string[];
  progression_audio: string | null;
  target_audio: string | null;
  options: string[];
  correct_answer: string;
  context: any;
}

interface AnswerResult {
  is_correct: boolean;
  user_answer: string;
  correct_answer: string;
  feedback: string;
  hints_used: string[];
  time_taken?: number;
}

const App: React.FC = () => {
  const [exercises, setExercises] = useState<Exercise[]>([]);
  const [selectedExercise, setSelectedExercise] = useState<Exercise | null>(null);
  const [exerciseData, setExerciseData] = useState<ExerciseData | null>(null);
  const [selectedAnswer, setSelectedAnswer] = useState<string>('');
  const [result, setResult] = useState<AnswerResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>('');

  // 20-question exercise state
  const [currentQuestion, setCurrentQuestion] = useState<number>(1);
  const [totalQuestions] = useState<number>(20);
  const [score, setScore] = useState<{correct: number, total: number}>({correct: 0, total: 0});
  const [, setQuestionHistory] = useState<Array<{question: number, answer: string, correct: boolean, correctAnswer: string}>>([]);

  useEffect(() => {
    fetchExercises();
  }, []);

  const fetchExercises = async () => {
    try {
      setLoading(true);
      const response = await axios.get('/api/exercises/');
      setExercises(response.data);
    } catch (err) {
      setError('Failed to load exercises');
      console.error('Error fetching exercises:', err);
    } finally {
      setLoading(false);
    }
  };

  const generateExercise = async (exerciseId: string, questionNumber: number = 1) => {
    try {
      setLoading(true);
      setError('');
      setResult(null);
      setSelectedAnswer('');

      const response = await axios.get(`/api/exercises/${exerciseId}/generate/?question_number=${questionNumber}`);
      setExerciseData(response.data);

      // Auto-play the audio when question loads
      if (response.data.target_audio) {
        setTimeout(() => {
          playAudio(response.data.target_audio);
        }, 500); // Small delay to ensure audio is ready
      }
    } catch (err) {
      setError('Failed to generate exercise');
      console.error('Error generating exercise:', err);
    } finally {
      setLoading(false);
    }
  };

  // Note: checkAnswer function is available but not used in current implementation
  // const checkAnswer = async (exerciseId: string, answer: string) => {
  //   try {
  //     setLoading(true);
  //     const response = await axios.post(`/api/exercises/${exerciseId}/check/`, {
  //       answer: answer,
  //       context: exerciseData?.context
  //     });
  //     setResult(response.data);
  //   } catch (err) {
  //     setError('Failed to check answer');
  //     console.error('Error checking answer:', err);
  //   } finally {
  //     setLoading(false);
  //   }
  // };

  const playAudio = (audioUrl: string) => {
    if (audioUrl) {
      const audio = new Audio(audioUrl);
      audio.play().catch(err => {
        console.error('Error playing audio:', err);
        setError('Failed to play audio');
      });
    }
  };

  const handleAnswerClick = (answer: string) => {
    if (!selectedExercise || !exerciseData) return;

    setSelectedAnswer(answer);

    // Check if answer is correct
    const isCorrect = answer === exerciseData.correct_answer;

    // Update score
    setScore(prev => ({
      correct: prev.correct + (isCorrect ? 1 : 0),
      total: prev.total + 1
    }));

    // Add to history
    setQuestionHistory(prev => [...prev, {
      question: currentQuestion,
      answer: answer,
      correct: isCorrect,
      correctAnswer: exerciseData.correct_answer
    }]);

    // Show result briefly, then auto-advance
    setResult({
      is_correct: isCorrect,
      user_answer: answer,
      correct_answer: exerciseData.correct_answer,
      feedback: isCorrect ? "Correct!" : `Incorrect. The correct answer was ${exerciseData.correct_answer.replace('_', ' ')}.`,
      hints_used: []
    });

    // Auto-advance to next question after 2 seconds
    setTimeout(() => {
      if (currentQuestion < totalQuestions) {
        setCurrentQuestion(prev => prev + 1);
        generateExercise(selectedExercise.id, currentQuestion + 1);
      } else {
        // Exercise completed
        setCurrentQuestion(1);
        setScore({correct: 0, total: 0});
        setQuestionHistory([]);
        setSelectedExercise(null);
      }
    }, 2000);
  };

  const startExercise = (exercise: Exercise) => {
    setSelectedExercise(exercise);
    setCurrentQuestion(1);
    setScore({correct: 0, total: 0});
    setQuestionHistory([]);
    generateExercise(exercise.id, 1);
  };

  return (
    <div className="container">
      <h1>🎵 Musical Ear Trainer</h1>

      {error && <div className="error">{error}</div>}

      {loading && <div className="loading">Loading...</div>}

      {!selectedExercise ? (
        <div className="card">
          <h2>Choose an Exercise</h2>
          <div className="exercise-list">
            {exercises.map((exercise) => (
              <div key={exercise.id} className="card">
                <h3>{exercise.name}</h3>
                <p>{exercise.description}</p>
                <p><strong>Difficulty:</strong> {exercise.difficulty}/10</p>
                <p><strong>Category:</strong> {exercise.category}</p>
                <p><strong>Estimated time:</strong> {exercise.estimated_time} seconds</p>
                <button
                  className="btn"
                  onClick={() => startExercise(exercise)}
                >
                  Start Exercise (20 Questions)
                </button>
              </div>
            ))}
          </div>
        </div>
      ) : (
        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
            <h2>{selectedExercise.name}</h2>
            <div style={{ textAlign: 'right' }}>
              <div style={{ fontSize: '18px', fontWeight: 'bold' }}>
                Question {currentQuestion}/{totalQuestions}
              </div>
              <div style={{ fontSize: '16px', color: '#666' }}>
                Score: {score.correct}/{score.total}
              </div>
            </div>
          </div>

          {exerciseData && (
            <div>
              <div className="audio-player">
                <h3>Listen to the interval</h3>
                <p style={{ color: '#666', marginBottom: '16px' }}>
                  Two notes will play automatically. Listen carefully!
                </p>
                <div className="audio-controls">
                  {exerciseData.target_audio && (
                    <button
                      className="btn btn-secondary"
                      onClick={() => playAudio(exerciseData.target_audio!)}
                    >
                      🔄 Play Again
                    </button>
                  )}
                </div>
              </div>

              <div>
                <h3>What interval do you hear?</h3>
                <div className="exercise-options">
                  {exerciseData.options.map((option) => (
                    <button
                      key={option}
                      className={`option-btn ${
                        selectedAnswer === option ? 'selected' : ''
                      } ${
                        result ? (
                          option === exerciseData.correct_answer ? 'correct' :
                          option === selectedAnswer && !result.is_correct ? 'incorrect' : ''
                        ) : ''
                      }`}
                      onClick={() => handleAnswerClick(option)}
                      disabled={!!result}
                    >
                      {option.replace('_', ' ').toUpperCase()}
                    </button>
                  ))}
                </div>

                {result && (
                  <div className={`feedback ${result.is_correct ? 'correct' : 'incorrect'}`}>
                    {result.feedback}
                  </div>
                )}
              </div>
            </div>
          )}

          <button
            className="btn btn-secondary"
            onClick={() => {
              setSelectedExercise(null);
              setCurrentQuestion(1);
              setScore({correct: 0, total: 0});
              setQuestionHistory([]);
            }}
            style={{ marginTop: '20px' }}
          >
            Back to Exercise List
          </button>
        </div>
      )}
    </div>
  );
};

export default App;
