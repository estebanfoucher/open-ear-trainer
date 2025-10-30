import React from 'react';

interface Chapter {
  id: number;
  title: string;
  description: string;
  order: number;
  difficulty_level: number;
  lesson_count: number;
  exercise_count: number;
  is_maintenance?: boolean;
}

interface ChapterListProps {
  chapters: Chapter[];
  onSelectChapter: (chapterId: number) => void;
}

const ChapterList: React.FC<ChapterListProps> = ({ chapters, onSelectChapter }) => {
  return (
    <div className="chapter-list">
      <h2>Choose a Chapter</h2>
      <div className="card-grid">
        {chapters.map((chapter) => (
          <div key={chapter.id} className={`card chapter-card ${chapter.is_maintenance ? 'maintenance' : ''}`}>
            <div className="chapter-header">
              <h3>{chapter.title}</h3>
              <span className="difficulty-badge">Level {chapter.difficulty_level}</span>
            </div>
            <p className="description">{chapter.description}</p>
            <div className="chapter-stats">
              <span>📚 {chapter.lesson_count} lessons</span>
              <span>✏️ {chapter.exercise_count} exercises</span>
            </div>
            {chapter.is_maintenance ? (
              <div className="maintenance-status">
                <span className="maintenance-badge">🚧 Coming Soon</span>
                <button
                  className="btn btn-disabled"
                  disabled
                >
                  Under Maintenance
                </button>
              </div>
            ) : (
              <button
                className="btn"
                onClick={() => onSelectChapter(chapter.id)}
              >
                Start Chapter
              </button>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default ChapterList;
