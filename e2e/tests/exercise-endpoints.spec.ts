import { test, expect } from '@playwright/test';

test.describe('Exercise ID Consistency', () => {
  test('should catch exercise ID mismatches between database and registry', async ({ page }) => {
    // This test specifically validates that all exercise IDs in the database
    // match the exercise registry, which would catch the type of error we just fixed

    // Get all exercises from the registry
    const exercisesResponse = await page.request.get('/api/exercises/');
    expect(exercisesResponse.status()).toBe(200);

    const registryExercises = await exercisesResponse.json();
    const registryExerciseIds = new Set(registryExercises.map((ex: any) => ex.id));

    // Get all chapters and lessons to find all exercise IDs in the database
    const chaptersResponse = await page.request.get('/api/chapters/');
    expect(chaptersResponse.status()).toBe(200);

    const chapters = await chaptersResponse.json();
    const databaseExerciseIds = new Set<string>();

    for (const chapter of chapters) {
      const chapterDetailResponse = await page.request.get(`/api/chapters/${chapter.id}/`);
      expect(chapterDetailResponse.status()).toBe(200);

      const chapterDetail = await chapterDetailResponse.json();

      for (const lesson of chapterDetail.lessons) {
        const lessonDetailResponse = await page.request.get(`/api/lessons/${lesson.id}/`);
        expect(lessonDetailResponse.status()).toBe(200);

        const lessonDetail = await lessonDetailResponse.json();

        for (const exercise of lessonDetail.exercises) {
          databaseExerciseIds.add(exercise.exercise_type);
        }
      }
    }

    // Check that all database exercise IDs exist in the registry
    for (const exerciseId of databaseExerciseIds) {
      expect(registryExerciseIds.has(exerciseId)).toBe(true);
    }

    // Check that all registry exercise IDs exist in the database
    for (const exerciseId of registryExerciseIds) {
      expect(databaseExerciseIds.has(exerciseId)).toBe(true);
    }
  });
});
