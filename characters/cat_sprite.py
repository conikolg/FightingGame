from typing import Any, Optional

import numpy as np
import pygame

from characters.sprite_animation import SpriteAnimation

tile_size = 64
base_image = pygame.image.load('assets/cat/cat_fighter_base.png')


class Cat(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Necessary for sprites
        self.image = pygame.Surface((tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (600, 600)

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
            ),
            # Load jumping animation
            'jump': SpriteAnimation(
                [base_image.subsurface((tile_size * x, tile_size * 2, tile_size, tile_size)) for x in range(4)],
                [0.05, 0.05, 0.5, 100.0]  # I want it to get stuck at a frame while in the air
            ),
            # Load landing animation
            'landing': SpriteAnimation(
                [base_image.subsurface((tile_size * x, tile_size * 2, tile_size, tile_size)) for x in range(4, 8)],
                [0.0, 0.00, 0.70, 0.05]  # I want it to get stuck at a frame when landing
            )
        }

        # Cat state
        self.direction = 'right'
        self.current_state = CatStandingState(self)

        # Cat characteristics
        self.walk_speed = 5.0
        self.jump_speed = 20.0
        self.landing_threshold = self.jump_speed * 1.5
        self.gravity = .8

    def update(self, *args: Any, **kwargs: Any) -> None:
        new_state = self.current_state.update(frametime=kwargs['frametime'])
        if new_state:
            self.current_state.on_exit()
            self.current_state = new_state
            new_state.on_enter()


class CatState:
    def __init__(self, cat: Cat, *args, **kwargs):
        self.cat = cat

    def update(self, *args, **kwargs):
        pass

    def on_enter(self, *args, **kwargs):
        pass

    def on_exit(self, *args, **kwargs):
        pass


class CatStandingState(CatState):
    def __init__(self, cat: Cat, *args, **kwargs):
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

        # Did the player jump?
        if keymap[pygame.K_w]:
            return CatJumpingState(self.cat)

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
    def __init__(self, cat: Cat, *args, **kwargs):
        super().__init__(cat)

        # Additional state of the cat
        self.x_speed = None

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

        # Did the player jump?
        if keymap[pygame.K_w]:
            return CatJumpingState(self.cat)

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


class CatJumpingState(CatState):
    def __init__(self, cat: Cat, *args, **kwargs):
        super().__init__(cat)

        # Additional state of the cat
        self.x_speed = None
        self.y_speed = None

    def on_enter(self, *args, **kwargs):
        self.y_speed = self.cat.jump_speed
        self.cat.animations['jump'].reset()
        image: pygame.Surface = self.cat.animations['jump'].get_current_frame()
        if self.cat.direction == 'right':
            self.cat.image = image
        else:
            self.cat.image = pygame.transform.flip(image, True, False)

    def update(self, *args, **kwargs):
        # Get state of the keyboard
        keymap = pygame.key.get_pressed()

        # Move horizontally
        self.x_speed = 0
        if keymap[pygame.K_a]:
            self.cat.direction = 'left'
            self.x_speed -= self.cat.walk_speed
        if keymap[pygame.K_d]:
            self.cat.direction = 'right'
            self.x_speed += self.cat.walk_speed

        # Be affected by gravity
        self.y_speed -= self.cat.gravity

        # Move
        self.cat.rect.move_ip(self.x_speed, -self.y_speed)

        # See if we hit the ground TODO: make actual ground
        ground_y = 600
        if self.cat.rect.bottom >= ground_y:
            # The cat is on the ground
            self.cat.rect.bottom = ground_y
            # Cat needs to land if going too fast
            if self.y_speed <= -self.cat.landing_threshold:
                return CatLandingState(self.cat)
            # Cat can just start walking otherwise
            else:
                return CatWalkingState(self.cat)

        # Still jumping/falling, animate
        frametime: float = kwargs['frametime']
        self.cat.animations['jump'].advance(frametime)
        image: pygame.Surface = self.cat.animations['jump'].get_current_frame()
        # Which direction is he going?
        if keymap[pygame.K_d]:
            self.x_speed = self.cat.walk_speed
            self.cat.direction = 'right'
            self.cat.image = image
        else:
            self.x_speed = -self.cat.walk_speed
            self.cat.direction = 'left'
            self.cat.image = pygame.transform.flip(image, True, False)

        return None


class CatLandingState(CatState):
    def __init__(self, cat: Cat, *args, **kwargs):
        super().__init__(cat)

    def on_enter(self, *args, **kwargs):
        self.cat.animations['landing'].reset()
        image: pygame.Surface = self.cat.animations['landing'].get_current_frame()
        if self.cat.direction == 'right':
            self.cat.image = image
        else:
            self.cat.image = pygame.transform.flip(image, True, False)

    def update(self, *args, **kwargs):
        # Recovering from landing...
        frametime: float = kwargs['frametime']
        self.cat.animations['landing'].advance(frametime)

        # Has enough time passed in the landing animation?
        if self.cat.animations['landing'].repetitions > 0:
            return CatStandingState(self.cat)

        # Otherwise, still recovering.
        image: pygame.Surface = self.cat.animations['landing'].get_current_frame()
        if self.cat.direction == 'right':
            self.cat.image = image
        else:
            self.cat.image = pygame.transform.flip(image, True, False)
        return None
