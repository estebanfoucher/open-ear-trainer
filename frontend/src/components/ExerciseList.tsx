import React from 'react';

interface Exercise {
  id: number;
  title: string;
  description: string;
  exercise_type: string;
  order: number;
  difficulty_level: number;
}

interface ExerciseListProps {
  lessonTitle: string;
  chapterTitle: string;
  exercises: Exercise[];
  onSelectExercise: (exerciseType: string) => void;
  onBack: () => void;
}

const ExerciseList: React.FC<ExerciseListProps> = ({
  lessonTitle,
  chapterTitle,
  exercises,
  onSelectExercise,
  onBack,
}) => {
  return (
    <div className="exercise-list">
      <button className="btn btn-secondary back-btn" onClick={onBack}>
        ← Back to Lessons
      </button>
      <div className="breadcrumb">
        {chapterTitle} → {lessonTitle}
      </div>
      <h2>Exercises</h2>
      <div className="card-grid">
        {exercises.map((exercise) => (
          <div key={exercise.id} className="card exercise-card">
            <div className="exercise-header">
              <span className="exercise-number">#{exercise.order}</span>
              <span className="difficulty-badge">Level {exercise.difficulty_level}</span>
            </div>
            <h3>{exercise.title}</h3>
            <p className="description">{exercise.description}</p>
            <button
              className="btn"
              onClick={() => onSelectExercise(exercise.exercise_type)}
            >
              Start Exercise (20 Questions)
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ExerciseList;
