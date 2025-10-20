import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import ChapterList from './components/ChapterList';
import LessonList from './components/LessonList';
import ExerciseList from './components/ExerciseList';

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

interface Chapter {
  id: number;
  title: string;
  description: string;
  order: number;
  difficulty_level: number;
  lesson_count: number;
  exercise_count: number;
}

interface Lesson {
  id: number;
  title: string;
  description: string;
  order: number;
  learning_objectives: string;
  estimated_minutes: number;
  chapter_id: number;
  chapter_title: string;
  exercises: CurriculumExercise[];
}

interface LessonSummary {
  id: number;
  title: string;
  description: string;
  order: number;
  estimated_minutes: number;
  exercise_count: number;
}

interface CurriculumExercise {
  id: number;
  title: string;
  description: string;
  exercise_type: string;
  order: number;
  difficulty_level: number;
  config: any;
  is_published: boolean;
}

type ViewType = 'chapters' | 'lessons' | 'exercises' | 'exercise';

const App: React.FC = () => {
  // Navigation state
  const [currentView, setCurrentView] = useState<ViewType>('chapters');
  const [chapters, setChapters] = useState<Chapter[]>([]);
  const [selectedChapter, setSelectedChapter] = useState<Chapter | null>(null);
  const [lessonsInChapter, setLessonsInChapter] = useState<LessonSummary[]>([]);
  const [selectedLesson, setSelectedLesson] = useState<Lesson | null>(null);

  // Exercise state
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
    fetchChapters();
  }, []);

  const fetchChapters = async () => {
    try {
      setLoading(true);
      const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';
      const response = await axios.get(`${apiUrl}/api/chapters/`);
      setChapters(response.data);
    } catch (err) {
      setError('Failed to load chapters');
      console.error('Error fetching chapters:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectChapter = async (chapterId: number) => {
    try {
      setLoading(true);
      const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';
      const response = await axios.get(`${apiUrl}/api/chapters/${chapterId}/`);
      setSelectedChapter(response.data);
      setLessonsInChapter(response.data.lessons);
      setCurrentView('lessons');
    } catch (err) {
      setError('Failed to load lessons');
      console.error('Error fetching lessons:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectLesson = async (lessonId: number) => {
    try {
      setLoading(true);
      const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';
      const response = await axios.get(`${apiUrl}/api/lessons/${lessonId}/`);
      setSelectedLesson(response.data);
      setCurrentView('exercises');
    } catch (err) {
      setError('Failed to load exercises');
      console.error('Error fetching exercises:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectExercise = (exerciseType: string) => {
    // Find the exercise in the old registry format
    const exercise: Exercise = {
      id: exerciseType,
      name: exerciseType.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
      description: 'Interval recognition exercise',
      difficulty: 1,
      category: 'intervals',
      tags: [],
      estimated_time: 600,
      prerequisites: [],
      learning_objectives: [],
      input_type: 'multiple_choice',
      answer_format: 'interval_name',
    };
    startExercise(exercise);
  };

  const generateExercise = async (exerciseId: string, questionNumber: number = 1) => {
    try {
      setLoading(true);
      setError('');
      setResult(null);
      setSelectedAnswer('');

      const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';
      const response = await axios.get(`${apiUrl}/api/exercises/${exerciseId}/generate/?question_number=${questionNumber}`);
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

  const playAudio = (audioUrl: string) => {
    if (audioUrl) {
      // Construct full URL if it's a relative path
      const fullAudioUrl = audioUrl.startsWith('http')
        ? audioUrl
        : `${process.env.REACT_APP_API_URL || 'http://localhost:8000'}${audioUrl}`;

      const audio = new Audio(fullAudioUrl);
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
        setCurrentView('exercises');
      }
    }, 2000);
  };

  const startExercise = (exercise: Exercise) => {
    setSelectedExercise(exercise);
    setCurrentQuestion(1);
    setScore({correct: 0, total: 0});
    setQuestionHistory([]);
    setCurrentView('exercise');
    generateExercise(exercise.id, 1);
  };

  const handleBackToChapters = () => {
    setCurrentView('chapters');
    setSelectedChapter(null);
    setLessonsInChapter([]);
  };

  const handleBackToLessons = () => {
    setCurrentView('lessons');
    setSelectedLesson(null);
  };

  const handleBackToExercises = () => {
    setCurrentView('exercises');
    setSelectedExercise(null);
  };

  return (
    <div className="container">
      <h1>🎵 Musical Ear Trainer</h1>

      {error && <div className="error">{error}</div>}

      {loading && <div className="loading">Loading...</div>}

      {currentView === 'chapters' && (
        <ChapterList
          chapters={chapters}
          onSelectChapter={handleSelectChapter}
        />
      )}

      {currentView === 'lessons' && selectedChapter && (
        <LessonList
          chapterTitle={selectedChapter.title}
          lessons={lessonsInChapter}
          onSelectLesson={handleSelectLesson}
          onBack={handleBackToChapters}
        />
      )}

      {currentView === 'exercises' && selectedLesson && (
        <ExerciseList
          lessonTitle={selectedLesson.title}
          chapterTitle={selectedLesson.chapter_title}
          exercises={selectedLesson.exercises}
          onSelectExercise={handleSelectExercise}
          onBack={handleBackToLessons}
        />
      )}

      {currentView === 'exercise' && selectedExercise && (
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
                      {option}
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
            onClick={handleBackToExercises}
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
