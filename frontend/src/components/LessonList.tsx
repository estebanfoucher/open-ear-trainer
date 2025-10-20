import React from 'react';

interface Lesson {
  id: number;
  title: string;
  description: string;
  order: number;
  estimated_minutes: number;
  exercise_count: number;
}

interface LessonListProps {
  chapterTitle: string;
  lessons: Lesson[];
  onSelectLesson: (lessonId: number) => void;
  onBack: () => void;
}

const LessonList: React.FC<LessonListProps> = ({ chapterTitle, lessons, onSelectLesson, onBack }) => {
  return (
    <div className="lesson-list">
      <button className="btn btn-secondary back-btn" onClick={onBack}>
        ← Back to Chapters
      </button>
      <h2>{chapterTitle}</h2>
      <div className="card-grid">
        {lessons.map((lesson) => (
          <div key={lesson.id} className="card lesson-card">
            <div className="lesson-number">Lesson {lesson.order}</div>
            <h3>{lesson.title}</h3>
            <p className="description">{lesson.description}</p>
            <div className="lesson-info">
              <span>⏱️ {lesson.estimated_minutes} min</span>
              <span>✏️ {lesson.exercise_count} exercises</span>
            </div>
            <button
              className="btn"
              onClick={() => onSelectLesson(lesson.id)}
            >
              Start Lesson
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default LessonList;
