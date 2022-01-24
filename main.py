import pygame

from characters.cat_sprite import Cat

pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('Fighting Game')

clock = pygame.time.Clock()
target_framerate = 60

players = pygame.sprite.Group()
players.add(Cat())


def main():
    running = True
    while running:
        # Handle all events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Do all updates - pass how many seconds the previous frame took to render
        players.update(frametime=float(clock.get_time()) / 1000)

        # Draw the new frame
        screen.fill((222, 134, 223))
        players.draw(screen)

        # Frame is done
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()
