from typing import Optional

import pygame

from characters.cat.cat_sprite import CatFighter
from characters.cat.cat_standing_state import CatStandingState
from characters.cat.cat_state import CatState


class CatWalkingState(CatState):
    def __init__(self, cat: CatFighter):
        super().__init__(cat)

        # Additional state of the cat
        self.x_speed = 0

    def on_enter(self, *args, **kwargs):
        self.cat.animations['walk'].reset()
        image: pygame.Surface = self.cat.animations['walk'].get_current_frame()
        if self.cat.direction == 'right':
            self.cat.image = image
        else:
            self.cat.image = pygame.transform.flip(image, True, False)

    def update(self, *args, **kwargs) -> Optional[CatState]:
        # Get state of keyboard
        keymap = pygame.key.get_pressed()

        # Is the cat walking?
        if keymap[pygame.K_a] or keymap[pygame.K_d]:
            # Animate walking
            frametime: float = kwargs['frametime']
            self.cat.animations['idle'].advance(frametime)
            image: pygame.Surface = self.cat.animations['idle'].get_current_frame()
            # Which direction is he walking?
            if keymap[pygame.K_d]:
                self.x_speed = self.cat.walk_speed
                self.cat.direction = 'right'
                self.cat.image = image
            else:
                self.x_speed = -self.cat.walk_speed
                self.cat.direction = 'left'
                self.cat.image = pygame.transform.flip(image, True, False)

            # Actually move the cat
            self.cat.rect.move_ip(self.x_speed, 0)

            # State has not changed - still walking
            return None

        # Cat must be standing
        return CatStandingState(self.cat)
