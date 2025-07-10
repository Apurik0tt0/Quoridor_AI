import pygame
from pygame.locals import *
from Q20 import Quoridor

board_size = 5
num_walls = 4

# Initialize Pygame and set up the game window
WIDTH = HEIGHT = 600
FRAME_SIZE = 40
WINDOW_WIDTH = WIDTH + FRAME_SIZE*2 + 400
WINDOW_HEIGHT = HEIGHT + FRAME_SIZE*2
BOARD_COLOR = (150, 75, 0)  # Brown color for the board
FRAME_COLOR = (255, 255, 255)  # White color for the frame
LOG_COLOR = (255, 0, 0)  # Red color for Player 1's moves
LOG2_COLOR = (0, 0, 255)  # Blue color for Player 2's moves
BOTH_COLOR = (128, 0, 128)  # Purple
WALLS_COLOR = (0, 0, 0)  # White color for the frame



if __name__ == "__main__":
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Quoridor Game")



    game = Quoridor(board_size)

    running = True
    clock = pygame.time.Clock()

    current_move = None  # Track the current move

    move_counter = 0


    stop_game = False

    while running:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        game.draw_board()
        #game.draw_log()
        #pygame.display.update()

    input("Press any key to terminate")
    pygame.quit()
