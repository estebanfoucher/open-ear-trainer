"""
Exercise: Perfect Fourth, Perfect Fifth, Octave (Harmonic)

This exercise plays two notes simultaneously and asks the student to identify the interval:
perfect fourth (P4), perfect fifth (P5), or octave (8ve).
The exercise consists of 20 questions with random intervals and root notes.
"""

from exercises.base.interval_exercise import BaseIntervalExercise


class PerfectFourthPerfectFifthOctaveHarmonicExercise(BaseIntervalExercise):
    """
    Exercise for recognizing perfect fourth, perfect fifth, and octave intervals with harmonic timing.
    """

    def __init__(self):
        super().__init__(
            intervals=["perfect_fourth", "perfect_fifth", "octave"],
            exercise_type="perfect_fourth_fifth_octave",
            timing="harmonic",
        )
