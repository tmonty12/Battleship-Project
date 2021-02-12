import pygame
import sys
import math
from main import Board, Ship, AI
pygame.font.init()

SQUAREFONT = pygame.font.SysFont('comicsans', 30)

SQUARESIZE = 40
WIDTH = SQUARESIZE * 22
HEIGHT = SQUARESIZE * 11

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (169, 169, 169)
BLUE = (0, 0, 255)

ships = [
    { 'name': 'Carrier', 'length': 5 },
    { 'name': 'Battleship', 'length': 4 },
    { 'name': 'Destroyer', 'length': 3 },
    { 'name': 'Submarine', 'length': 3 },
    { 'name': 'Patrol Boat', 'length': 2 },
]

NUMTOALPH = {
    1 : 'A',
    2 : 'B',
    3 : 'C',
    4 : 'D',
    5 : 'E',
    6 : 'F',
    7 : 'G',
    8 : 'H',
    9 : 'I',
    10 : 'J',
}
WATER = 'w'
MISSED = 'm'

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Battleship")

def drawboard(ai_board, user_board):
    for r in range(len(ai_board.display) + 1):
        for c in range(len(ai_board.display) + 1):
            pygame.draw.rect(WIN, BLACK, (c*SQUARESIZE, r*SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.rect(WIN, WHITE, (c*SQUARESIZE+2, r*SQUARESIZE+2, SQUARESIZE-2, SQUARESIZE-2))
            if r == 0 and c != 0: # Letter row
                letter = SQUAREFONT.render(NUMTOALPH[c], 1, BLACK)
                WIN.blit(letter, (c*SQUARESIZE+SQUARESIZE/2 - letter.get_width()/2, SQUARESIZE/2 - letter.get_height()/2))
            elif c == 0 and r != 0: # Number row
                letter = SQUAREFONT.render(str(r).upper(), 1, BLACK)
                WIN.blit(letter, (SQUARESIZE/2 - letter.get_width()/2, r*SQUARESIZE+SQUARESIZE/2 - letter.get_height()/2))

    for r in range(len(user_board.display) + 1):
        for c in range(len(user_board.display) + 1):
            if r == 0 or c == 0:
                pygame.draw.rect(WIN, BLACK, (WIDTH/2+c*SQUARESIZE, r*SQUARESIZE, SQUARESIZE, SQUARESIZE))
                pygame.draw.rect(WIN, WHITE, (WIDTH/2+c*SQUARESIZE+2, r*SQUARESIZE+2, SQUARESIZE-2, SQUARESIZE-2))
                if r == 0 and c != 0: # Letter row
                    letter = SQUAREFONT.render(NUMTOALPH[c], 1, BLACK)
                    WIN.blit(letter, (WIDTH/2+c*SQUARESIZE+SQUARESIZE/2 - letter.get_width()/2, SQUARESIZE/2 - letter.get_height()/2))
                elif c == 0 and r != 0: # Number row
                    letter = SQUAREFONT.render(str(r).upper(), 1, BLACK)
                    WIN.blit(letter, (WIDTH/2+SQUARESIZE/2 - letter.get_width()/2, r*SQUARESIZE+SQUARESIZE/2 - letter.get_height()/2))
            else:
                val = user_board.display[r-1][c-1]
                if isinstance(val, Ship):
                    pygame.draw.rect(WIN, GREY, (WIDTH/2+c*SQUARESIZE, r*SQUARESIZE, SQUARESIZE, SQUARESIZE))
                else:
                    pygame.draw.rect(WIN, BLACK, (WIDTH/2+c*SQUARESIZE, r*SQUARESIZE, SQUARESIZE, SQUARESIZE))
                    pygame.draw.rect(WIN, BLUE, (WIDTH/2+c*SQUARESIZE+2, r*SQUARESIZE+2, SQUARESIZE-2, SQUARESIZE-2))

    
    pygame.display.update()

def main():
    user_board = Board()
    ai = AI()

    drawboard(ai.board, user_board)

    while len(ships) > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                if x > SQUARESIZE*12 and y > SQUARESIZE:
                    x -= SQUARESIZE*12
                    y -= SQUARESIZE

                    x = math.ceil(x/SQUARESIZE)
                    y = math.ceil(y/SQUARESIZE)

                    is_placed = user_board.place_ship(ships[0]['name'], ships[0]['length'], (x, y))
                    if is_placed:
                        ships.pop(0)
                        drawboard(ai.board, user_board)
            
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos

                if x > SQUARESIZE*12 and y > SQUARESIZE:
                    x -= SQUARESIZE*12
                    y -= SQUARESIZE

                    x = math.ceil(x/SQUARESIZE)
                    y = math.ceil(y/SQUARESIZE)

                    
if __name__ == "__main__":
    main()