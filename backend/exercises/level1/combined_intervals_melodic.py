"""
Exercise: Combined Intervals (Melodic)

This exercise plays two notes with staggered timing (root note starts first,
then second note begins 400ms later) and asks the student to identify the interval:
minor third (m3), major third (M3), perfect fourth (P4), perfect fifth (P5), or octave (8ve).
The exercise consists of 20 questions with random intervals and root notes.
"""

from exercises.base.interval_exercise import BaseIntervalExercise


class CombinedIntervalsMelodicExercise(BaseIntervalExercise):
    """
    Exercise for recognizing minor third, major third, perfect fourth, perfect fifth, and octave intervals with melodic timing.
    """

    def __init__(self):
        super().__init__(
            intervals=[
                "minor_third",
                "major_third",
                "perfect_fourth",
                "perfect_fifth",
                "octave",
            ],
            exercise_type="combined_intervals",
            timing="melodic",
        )
