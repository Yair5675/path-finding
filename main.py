import Board
import numpy as np
from constants import *

# The frame-rate (affects the speed):
fps = 50

chosen_maze = int(input('Type a number between 1-7:\n')) - 1
image, pygame_image, screen, SIZE = load_image(chosen_maze, 100 if chosen_maze != 3 else 150)
map_array = np.asarray(image, int)
board = Board.Board(map_array)

show_solving =\
    input("Would you like to see the program solving the maze (if not the program will solve it off-screen)?\n").lower() ==\
    'yes'

running = True
if show_solving:
    search = True
    while running:
        screen.fill(WHITE)
        screen.blit(pygame_image, (0, 0))
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                map_array = np.asarray(image, int)
                board = Board.Board(map_array)
                search = True
            elif event.key == pygame.K_UP:
                fps += 10
            elif event.key == pygame.K_DOWN and fps > 10:
                fps -= 10

        if search:
            # Searching for the exit:
            m = board.mouse_won()
            if m is None:
                board.move_mice()
                board.draw_mice(screen)
            else:
                search = False
        else:
            m.draw_trail(screen)

        # Writing instructions:
        message = font.render('Press ENTER to start over', True, BLACK)
        message_rect = message.get_rect(top=SIZE[1], centerx=SIZE[0]//2)
        screen.blit(message, message_rect)
        message = font.render('Use the arrows to toggle speed', True, BLACK)
        message_rect = message.get_rect(top=message_rect.bottom, centerx=message_rect.centerx)
        screen.blit(message, message_rect)
        
        pygame.display.update()
        clock.tick(fps)
else:
    # The program finds the right path off-screen
    while board.mouse_won() is None:
        board.move_mice()
    # Once the path is found it will be displayed:
    m = board.mouse_won()
    while running:
        screen.blit(pygame_image, (0, 0))
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            running = False
        m.draw_trail(screen)
        pygame.display.update()
        clock.tick(fps)
