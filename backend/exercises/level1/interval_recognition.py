"""
Exercise: Minor Third, Major Third, Octave (Melodic)

This exercise plays two notes with staggered timing (root note starts first,
then second note begins 400ms later) and asks the student to identify the interval:
octave (8ve), minor third (m3), or major third (M3).
The exercise consists of 20 questions with random intervals and root notes.
"""

from exercises.base.interval_exercise import BaseIntervalExercise


class MinorThirdMajorThirdOctaveMelodicExercise(BaseIntervalExercise):
    """
    Exercise for recognizing minor third, major third, and octave intervals with melodic timing.
    """
    
    def __init__(self):
        super().__init__(
            intervals=["minor_third", "major_third", "octave"],
            exercise_type="minor_third_major_third_octave",
            timing="melodic"
        )


# Keep the old class name for backward compatibility
IntervalRecognitionExercise = MinorThirdMajorThirdOctaveMelodicExercise