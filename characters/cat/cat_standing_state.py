from typing import Optional

import pygame

from characters.cat.cat_sprite import CatFighter
from characters.cat.cat_state import CatState
from characters.cat.cat_walking_state import CatWalkingState


class CatStandingState(CatState):
    def __init__(self, cat: CatFighter):
        super().__init__(cat)

    def on_enter(self, *args, **kwargs):
        self.cat.animations['idle'].reset()
        image: pygame.Surface = self.cat.animations['idle'].get_current_frame()
        if self.cat.direction == 'right':
            self.cat.image = image
        else:
            self.cat.image = pygame.transform.flip(image, True, False)

    def update(self, *args, **kwargs) -> Optional[CatState]:
        # Get state of keyboard
        keymap = pygame.key.get_pressed()

        # Is the cat walking?
        if keymap[pygame.K_a] or keymap[pygame.K_d]:
            return CatWalkingState(self.cat)

        # Cat must be standing
        frametime: float = kwargs['frametime']
        self.cat.animations['idle'].advance(frametime)
        image: pygame.Surface = self.cat.animations['idle'].get_current_frame()
        if self.cat.direction == 'right':
            self.cat.image = image
        else:
            self.cat.image = pygame.transform.flip(image, True, False)

        # State has not changed - still standing
        return None
