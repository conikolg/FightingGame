from typing import Any

import numpy as np
import pygame

from sprite_animation import SpriteAnimation

tile_size = 64
base_image = pygame.image.load('assets/cat_fighter_base.png')


class CatFighter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Necessary for sprites
        self.image = pygame.Surface((tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.topleft = (100, 100)

        self.animations = {
            # Load idle animation
            'idle': SpriteAnimation(
                [base_image.subsurface((tile_size * x, tile_size * 0, tile_size, tile_size)) for x in range(4)],
                np.ones(shape=(4,), dtype=float) / 10
            ),
            # Load walking animation. 0.125 sec between each frame.
            'walk': SpriteAnimation(
                [base_image.subsurface((tile_size * x, tile_size * 1, tile_size, tile_size)) for x in range(8)],
                np.ones(shape=(8,), dtype=float) / 20
            )
        }

        # Cat state
        self.x_speed = 0
        self.y_speed = 0
        self.is_grounded = False
        self.current_animation = 'walk'

        # Cat characteristics
        self.walk_speed = 5
        self.jump_speed = 15
        self.gravity = 1

    def update(self, *args: Any, **kwargs: Any) -> None:
        # How much time passed since last update
        frametime: float = kwargs['frametime']
        # Get current state of all keys
        keymap = pygame.key.get_pressed()

        # Handle horizontal movement
        self.x_speed = 0
        if keymap[pygame.K_RIGHT] or keymap[pygame.K_d]:
            self.x_speed += self.walk_speed
        if keymap[pygame.K_LEFT] or keymap[pygame.K_a]:
            self.x_speed -= self.walk_speed

        # Handle jumping
        if keymap[pygame.K_UP] or keymap[pygame.K_w]:
            if self.is_grounded:
                self.y_speed = self.jump_speed
                self.is_grounded = False

        # Be affected by gravity
        self.y_speed -= self.gravity

        # Move this sprite's rectangle
        self.rect.move_ip(self.x_speed, -self.y_speed)

        # Check if we are grounded
        if self.rect.bottom >= 500:
            self.rect.bottom = 500
            self.y_speed = 0
            self.is_grounded = True

        # Choose what image this sprite should look like
        self.animations[self.current_animation].advance(frametime)
        self.image = self.animations[self.current_animation].get_current_frame()
