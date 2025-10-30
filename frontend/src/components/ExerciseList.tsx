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
  lessonTheoryTitle?: string;
  lessonTheoryMarkdown?: string;
  exercises: Exercise[];
  onSelectExercise: (exerciseType: string) => void;
  onOpenTheory?: () => void;
  onBack: () => void;
}

const ExerciseList: React.FC<ExerciseListProps> = ({
  lessonTitle,
  chapterTitle,
  lessonTheoryTitle,
  lessonTheoryMarkdown,
  exercises,
  onSelectExercise,
  onOpenTheory,
  onBack,
}) => {
  return (
    <div className="exercise-list" style={{ display: 'block' }}>
      <button className="btn btn-secondary back-btn" onClick={onBack}>
        ← Back to Lessons
      </button>
      <div className="breadcrumb">
        {chapterTitle} → {lessonTitle}
      </div>
      {lessonTheoryTitle || lessonTheoryMarkdown ? (
        <>
          <h2>Theory</h2>
          <div className="card" style={{ textAlign: 'left', marginBottom: '20px' }}>
            <div className="exercise-header">
              <span className="exercise-number">#T1</span>
            </div>
            <h3>{lessonTheoryTitle || 'Theory module'}</h3>
            <p className="description">Open the theory module to read the lesson.</p>
            {onOpenTheory && (
              <button
                className="btn"
                onClick={onOpenTheory}
                style={{ marginTop: '12px' }}
              >
                Open Theory
              </button>
            )}
          </div>
        </>
      ) : null}
      <h2>Exercises</h2>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
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
