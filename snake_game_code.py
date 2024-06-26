# Author: SdataROY
# Created: May 9, 2024

import pygame
import random

pygame.init()
square_width = 750
pixel_width = 50
screen = pygame.display.set_mode([square_width] * 2)
clock = pygame.time.Clock()
running = True
font = pygame.font.Font(None, 36)  # Initialize font; default font, size 36
game_over_font = pygame.font.Font(None, 72)  # Larger font for "Game Over"

def generate_starting_position(exclude_positions=[]):
    while True:
        position = (random.randrange(pixel_width // 2, square_width - pixel_width // 2, pixel_width),
                    random.randrange(pixel_width // 2, square_width - pixel_width // 2, pixel_width))
        if all(position != (part.x, part.y) for part in exclude_positions):
            return position

def reset():
    global snake_length, snake, snake_pixel, target, snake_direction, game_over
    snake_pixel = pygame.Rect([0, 0, pixel_width - 2, pixel_width - 2])
    snake_pixel.center = generate_starting_position()
    snake = [snake_pixel.copy()]
    snake_length = 1
    target = pygame.Rect([0, 0, pixel_width - 2, pixel_width - 2])
    target.center = generate_starting_position([part for part in snake])
    game_over = False

def is_out_of_bounds(rect):
    return rect.bottom > square_width or rect.top < 0 or rect.left < 0 or rect.right > square_width

def check_self_collision(snake_parts):
    head = snake_parts[-1]
    return any(head.colliderect(part) for part in snake_parts[:-1])

snake_pixel = pygame.Rect([0, 0, pixel_width - 2, pixel_width - 2])
snake_pixel.center = generate_starting_position()
snake = [snake_pixel.copy()]
snake_direction = (0, 0)
snake_length = 1
target = pygame.Rect([0, 0, pixel_width - 2, pixel_width - 2])
target.center = generate_starting_position([part for part in snake])
game_over = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if game_over:
                if event.key in [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]:
                    reset()
            else:
                if event.key == pygame.K_w and snake_direction != (0, pixel_width):
                    snake_direction = (0, -pixel_width)
                elif event.key == pygame.K_s and snake_direction != (0, -pixel_width):
                    snake_direction = (0, pixel_width)
                elif event.key == pygame.K_a and snake_direction != (pixel_width, 0):
                    snake_direction = (-pixel_width, 0)
                elif event.key == pygame.K_d and snake_direction != (-pixel_width, 0):
                    snake_direction = (pixel_width, 0)

    screen.fill((31, 31, 46))  # Dark blue background

    if not game_over:
        snake_pixel.move_ip(snake_direction)
        snake.append(snake_pixel.copy())
        snake = snake[-snake_length:]
        if is_out_of_bounds(snake_pixel) or check_self_collision(snake):
            game_over = True
        elif snake_pixel.center == target.center:
            target.center = generate_starting_position([part for part in snake])
            snake_length += 1
            snake.append(snake_pixel.copy())

    for snake_part in snake:
        pygame.draw.rect(screen, (51, 153, 255), snake_part)
    pygame.draw.rect(screen, (255, 153, 102), target)

    if game_over:
        game_over_text = game_over_font.render("Game Over!", True, (255, 255, 255))
        screen.blit(game_over_text, (square_width / 2 - game_over_text.get_width() / 2, square_width / 2 - game_over_text.get_height() / 2))

    # Score Display in the top left corner
    score_text = font.render("Score: {}".format(snake_length - 1), True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(10)

pygame.quit()
