"""
Exercise: Minor Third, Major Third, Octave (Harmonic)

This exercise plays two notes simultaneously and asks the student to identify the interval:
octave (8ve), minor third (m3), or major third (M3).
The exercise consists of 20 questions with random intervals and root notes.
"""

from exercises.base.interval_exercise import BaseIntervalExercise


class MinorThirdMajorThirdOctaveHarmonicExercise(BaseIntervalExercise):
    """
    Exercise for recognizing minor third, major third, and octave intervals with harmonic timing.
    """
    
    def __init__(self):
        super().__init__(
            intervals=["minor_third", "major_third", "octave"],
            exercise_type="minor_third_major_third_octave",
            timing="harmonic"
        )
