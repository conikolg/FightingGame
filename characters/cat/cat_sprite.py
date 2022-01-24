from typing import Any

import numpy as np
import pygame

from characters.cat.cat_standing_state import CatStandingState
from characters.sprite_animation import SpriteAnimation

tile_size = 64
base_image = pygame.image.load('../../assets/cat_fighter_base.png')


class CatFighter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Necessary for sprites
        self.image = pygame.Surface((tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.topleft = (100, 100)

        self.animations: dict[str, SpriteAnimation] = {
            # Load idle animation
            'idle': SpriteAnimation(
                [base_image.subsurface((tile_size * x, tile_size * 0, tile_size, tile_size)) for x in range(4)],
                np.ones(shape=(4,), dtype=float) / 10
            ),
            # Load walking animation
            'walk': SpriteAnimation(
                [base_image.subsurface((tile_size * x, tile_size * 1, tile_size, tile_size)) for x in range(8)],
                np.ones(shape=(8,), dtype=float) / 20
            )
        }

        # Cat state
        self.direction = 'right'
        self.current_state = CatStandingState(self)

        # Cat characteristics
        self.walk_speed = 5
        self.jump_speed = 15
        self.gravity = 1

    def update(self, *args: Any, **kwargs: Any) -> None:
        new_state = self.current_state.update(frametime=kwargs['frametime'])
        if new_state:
            self.current_state.on_exit()
            self.current_state = new_state
            new_state.on_enter()
