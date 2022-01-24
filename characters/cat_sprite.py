from typing import Any, Optional

import numpy as np
import pygame

from characters.sprite_animation import SpriteAnimation

tile_size = 64
base_image = pygame.image.load('assets/cat_fighter_base.png')


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


class CatState:
    def __init__(self, cat: CatFighter, *args, **kwargs):
        self.cat = cat

    def update(self, *args, **kwargs):
        pass

    def on_enter(self, *args, **kwargs):
        pass

    def on_exit(self, *args, **kwargs):
        pass


class CatStandingState(CatState):
    def __init__(self, cat: CatFighter, *args, **kwargs):
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


class CatWalkingState(CatState):
    def __init__(self, cat: CatFighter, *args, **kwargs):
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
            self.cat.animations['walk'].advance(frametime)
            image: pygame.Surface = self.cat.animations['walk'].get_current_frame()
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
