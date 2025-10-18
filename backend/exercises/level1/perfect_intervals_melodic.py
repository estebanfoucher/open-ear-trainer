"""
Exercise: Perfect Fourth, Perfect Fifth, Octave (Melodic)

This exercise plays two notes with staggered timing (root note starts first,
then second note begins 400ms later) and asks the student to identify the interval:
perfect fourth (P4), perfect fifth (P5), or octave (8ve).
The exercise consists of 20 questions with random intervals and root notes.
"""

from exercises.base.interval_exercise import BaseIntervalExercise


class PerfectFourthPerfectFifthOctaveMelodicExercise(BaseIntervalExercise):
    """
    Exercise for recognizing perfect fourth, perfect fifth, and octave intervals with melodic timing.
    """

    def __init__(self):
        super().__init__(
            intervals=["perfect_fourth", "perfect_fifth", "octave"],
            exercise_type="perfect_fourth_fifth_octave",
            timing="melodic",
        )
