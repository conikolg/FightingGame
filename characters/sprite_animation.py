import numpy as np
import pygame


class SpriteAnimation:
    def __init__(self, frames: list[pygame.Surface], timings: list[float]):
        """
        Create an animation object that maintains its own timing and progress state.
        :param frames: a list of pygame.Surface objects
        :param timings: a list of floats indicating how long each frame is to be displayed in seconds
        """

        assert len(frames) == len(timings)

        self.frames = frames
        self.timings = timings
        self.time_offsets: np.ndarray[float] = np.cumsum(self.timings)
        self.current_time_offset = 0
        self.repetitions = 0

    def reset(self) -> None:
        """
        Resets the timer so the animation begins on the first frame of the loop with
        the full duration of the first frame remaining. Clears the repetition counter.
        :return:
        """
        self.current_time_offset = 0
        self.repetitions = 0

    def get_current_frame(self) -> pygame.Surface:
        """
        Computes which frame should be displayed and returns it.
        :return: a pygame.Surface object
        """
        frame_index = self.time_offsets.searchsorted(self.current_time_offset)
        return self.frames[frame_index]

    def advance(self, seconds: float) -> None:
        """
        Advances the animation's internal timer by the given number of seconds.
        :param seconds: a float indicating how many seconds to advance the animation by
        """
        self.current_time_offset += seconds
        if self.current_time_offset > sum(self.timings):
            self.current_time_offset = self.current_time_offset % sum(self.timings)
            self.repetitions += 1
