import pygame
import sys
import math
import pprint
from main import Board, Ship, AI
pygame.font.init()

SQUAREFONT = pygame.font.SysFont('arial', 28)
HEADERFONT = pygame.font.SysFont('calibri', 36)
DIRECTIONSFONT = pygame.font.SysFont('times new roman', 30)

SQUARESIZE = 40
WIDTH = SQUARESIZE * 22
HEIGHT = SQUARESIZE * 15

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (169, 169, 169)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

ships = [
    { 'name': 'Carrier', 'length': 5, 'vertical': True },
    { 'name': 'Battleship', 'length': 4, 'vertical': True },
    { 'name': 'Destroyer', 'length': 3, 'vertical': True },
    { 'name': 'Submarine', 'length': 3, 'vertical': True },
    { 'name': 'Patrol Boat', 'length': 2, 'vertical': True },
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

def draw_board(ai_board, user_board):
    '''Draws the Enemy and User boards on the GUI, given the state of the game'''

    # Iterate over every square of AI Board
    for r in range(len(ai_board.display) + 1):
        for c in range(len(ai_board.display) + 1):
            if r == 0 or c == 0:
                pygame.draw.rect(WIN, BLACK, (c*SQUARESIZE, (r+4)*SQUARESIZE, SQUARESIZE, SQUARESIZE))
                pygame.draw.rect(WIN, WHITE, (c*SQUARESIZE+2, (r+4)*SQUARESIZE+2, SQUARESIZE-2, SQUARESIZE-2))
                if r == 0 and c != 0: # Letter row
                    letter = SQUAREFONT.render(NUMTOALPH[c], 1, BLACK)
                    WIN.blit(letter, (c*SQUARESIZE+SQUARESIZE/2 - letter.get_width()/2, 9*SQUARESIZE/2 - letter.get_height()/2))
                elif c == 0 and r != 0: # Number row
                    letter = SQUAREFONT.render(str(r).upper(), 1, BLACK)
                    WIN.blit(letter, (SQUARESIZE/2 - letter.get_width()/2, (9/2+r)*SQUARESIZE - letter.get_height()/2))
            else:
                val = ai_board.display[r-1][c-1]
                if isinstance(val, Ship): # Square contains ship
                    if val.is_sunk(): # Draw ship on AI Board if sunk
                        draw_ship_square((c*SQUARESIZE, (r+4)*SQUARESIZE), (c, r), ai_board)
                        pygame.draw.circle(WIN, RED, ((c+1)*SQUARESIZE - SQUARESIZE/2, (r+5)*SQUARESIZE+1 - SQUARESIZE/2), SQUARESIZE/4)
                    else:
                        pygame.draw.rect(WIN, BLACK, (c*SQUARESIZE, (r+4)*SQUARESIZE, SQUARESIZE, SQUARESIZE))
                        pygame.draw.rect(WIN, BLUE, (c*SQUARESIZE+2, (r+4)*SQUARESIZE+2, SQUARESIZE-2, SQUARESIZE-2))
                        if val.is_coords_hit((c, r)): # Ship is hit in square
                            pygame.draw.circle(WIN, RED, ((c+1)*SQUARESIZE - SQUARESIZE/2, (r+5)*SQUARESIZE+1 - SQUARESIZE/2), SQUARESIZE/4)
                else:
                    pygame.draw.rect(WIN, BLACK, (c*SQUARESIZE, (r+4)*SQUARESIZE, SQUARESIZE, SQUARESIZE))
                    pygame.draw.rect(WIN, BLUE, (c*SQUARESIZE+2, (r+4)*SQUARESIZE+2, SQUARESIZE-2, SQUARESIZE-2))
                    if val == MISSED: # Mark missed square
                        pygame.draw.circle(WIN, YELLOW, ((c+1)*SQUARESIZE - SQUARESIZE/2, (r+5)*SQUARESIZE+1 - SQUARESIZE/2), SQUARESIZE/4)

    # Iterate over every square of user board
    for r in range(len(user_board.display) + 1):
        for c in range(len(user_board.display) + 1):
            if r == 0 or c == 0:
                pygame.draw.rect(WIN, BLACK, (WIDTH/2+c*SQUARESIZE, (4*SQUARESIZE)+r*SQUARESIZE, SQUARESIZE, SQUARESIZE))
                pygame.draw.rect(WIN, WHITE, (WIDTH/2+c*SQUARESIZE+2, (4*SQUARESIZE)+r*SQUARESIZE+2, SQUARESIZE-2, SQUARESIZE-2))
                if r == 0 and c != 0: # Letter row
                    letter = SQUAREFONT.render(NUMTOALPH[c], 1, BLACK)
                    WIN.blit(letter, (WIDTH/2+c*SQUARESIZE+SQUARESIZE/2 - letter.get_width()/2, (4*SQUARESIZE)+SQUARESIZE/2 - letter.get_height()/2))
                elif c == 0 and r != 0: # Number row
                    letter = SQUAREFONT.render(str(r).upper(), 1, BLACK)
                    WIN.blit(letter, (WIDTH/2+SQUARESIZE/2 - letter.get_width()/2, (4*SQUARESIZE)+r*SQUARESIZE+SQUARESIZE/2 - letter.get_height()/2))
            else:
                val = user_board.display[r-1][c-1]
                pygame.draw.rect(WIN, BLACK, (WIDTH/2+c*SQUARESIZE, (4*SQUARESIZE)+r*SQUARESIZE, SQUARESIZE, SQUARESIZE))
                if isinstance(val, Ship): # Ship square
                    draw_ship_square((WIDTH/2+c*SQUARESIZE, (4*SQUARESIZE)+r*SQUARESIZE), (c, r), user_board)
                    if val.is_coords_hit((c,r)): # Ship square is hit
                        pygame.draw.circle(WIN, RED, (WIDTH/2+(c+1)*SQUARESIZE - SQUARESIZE/2, (4*SQUARESIZE)+(r+1)*SQUARESIZE+1 - SQUARESIZE/2), SQUARESIZE/4)
                    else:
                        pygame.draw.circle(WIN, BLACK, (WIDTH/2+(c+1)*SQUARESIZE - SQUARESIZE/2, (4*SQUARESIZE)+(r+1)*SQUARESIZE+1 - SQUARESIZE/2), SQUARESIZE/5)
                else:
                    pygame.draw.rect(WIN, BLUE, (WIDTH/2+c*SQUARESIZE+2, (4*SQUARESIZE)+r*SQUARESIZE+2, SQUARESIZE-2, SQUARESIZE-2))
                    if val == MISSED: # Mark AI misses
                        pygame.draw.circle(WIN, YELLOW, (WIDTH/2+(c+1)*SQUARESIZE - SQUARESIZE/2, (4*SQUARESIZE)+(r+1)*SQUARESIZE+1 - SQUARESIZE/2), SQUARESIZE/4)

    pygame.display.update()

def draw_ship(ship, coords, user_board):
    '''Draws the ship where the user is hovering before placement'''

    if ship['vertical']:
        if coords[1] + ship['length'] <= 11:
            for i in range(ship['length']):
                if i == 0:
                    pygame.draw.rect(WIN, GREY, (WIDTH/2+coords[0]*SQUARESIZE+2, (4*SQUARESIZE)+(coords[1]+i)*SQUARESIZE, SQUARESIZE-2, SQUARESIZE), border_top_left_radius=50, border_top_right_radius=50)
                elif i == ship['length'] - 1:
                    pygame.draw.rect(WIN, GREY, (WIDTH/2+coords[0]*SQUARESIZE+2, (4*SQUARESIZE)+(coords[1]+i)*SQUARESIZE, SQUARESIZE-2, SQUARESIZE), border_bottom_left_radius=50, border_bottom_right_radius=50)
                else:
                    pygame.draw.rect(WIN, GREY, (WIDTH/2+coords[0]*SQUARESIZE+2, (4*SQUARESIZE)+(coords[1]+i)*SQUARESIZE, SQUARESIZE-2, SQUARESIZE))
                pygame.draw.circle(WIN, BLACK, (WIDTH/2+coords[0]*SQUARESIZE+SQUARESIZE/2, (4*SQUARESIZE)+(coords[1]+i)*SQUARESIZE+SQUARESIZE/2), SQUARESIZE/5)
    else:
        if coords[0] + ship['length'] <= 11:
            for i in range(ship['length']):
                if i == 0:
                    pygame.draw.rect(WIN, GREY, (WIDTH/2+(coords[0]+i)*SQUARESIZE, (4*SQUARESIZE)+coords[1]*SQUARESIZE+2, SQUARESIZE, SQUARESIZE-2), border_top_left_radius=50, border_bottom_left_radius=50)
                elif i == ship['length'] - 1:
                    pygame.draw.rect(WIN, GREY, (WIDTH/2+(coords[0]+i)*SQUARESIZE, (4*SQUARESIZE)+coords[1]*SQUARESIZE+2, SQUARESIZE, SQUARESIZE-2), border_bottom_right_radius=50, border_top_right_radius=50)
                else:
                    pygame.draw.rect(WIN, GREY, (WIDTH/2+(coords[0]+i)*SQUARESIZE, (4*SQUARESIZE)+coords[1]*SQUARESIZE+2, SQUARESIZE, SQUARESIZE-2))
                pygame.draw.circle(WIN, BLACK, (WIDTH/2+(coords[0]+i)*SQUARESIZE+SQUARESIZE/2, (4*SQUARESIZE)+coords[1]*SQUARESIZE+SQUARESIZE/2), SQUARESIZE/5)
    
    pygame.display.update()

def draw_header(header_text):
    '''Draws the header text to the GUI'''

    pygame.draw.rect(WIN, WHITE, (0,0,WIDTH, SQUARESIZE*3))

    pygame.draw.rect(WIN, BLACK, (0, 3*SQUARESIZE, WIDTH/2+2, SQUARESIZE))
    pygame.draw.rect(WIN, WHITE, (2, 3*SQUARESIZE+2, WIDTH/2-2, SQUARESIZE-2))
    pygame.draw.rect(WIN, BLACK, (WIDTH/2, 3*SQUARESIZE, WIDTH/2+2, SQUARESIZE))
    pygame.draw.rect(WIN, WHITE, (WIDTH/2+2, 3*SQUARESIZE+2, WIDTH/2-2, SQUARESIZE-2))
    
    enemy_text = HEADERFONT.render('Enemy', 1, BLACK)
    user_text = HEADERFONT.render('Player', 1, BLACK)
    WIN.blit(enemy_text, (WIDTH/4 - enemy_text.get_width()/2, 7/2*SQUARESIZE - enemy_text.get_height()/2))
    WIN.blit(user_text, (3*WIDTH/4 - user_text.get_width()/2, 7/2*SQUARESIZE - enemy_text.get_height()/2))

    header_text = DIRECTIONSFONT.render(header_text, 1, BLACK)
    WIN.blit(header_text, (WIDTH/2 - header_text.get_width()/2, 3/2*SQUARESIZE - header_text.get_height()/2))

    pygame.display.update()

def draw_ship_square(location, coords, board):
    '''Draws the ship square given the location. Ends are curved'''

    square = board.display[coords[1]-1][coords[0]-1]
    if square.vertical:
        if square.is_first_end(coords):
            pygame.draw.rect(WIN, BLUE, (location[0]+2, location[1]+2, SQUARESIZE-2, SQUARESIZE-2))
            pygame.draw.rect(WIN, GREY, (location[0]+2, location[1], SQUARESIZE-2, SQUARESIZE), border_top_left_radius=50, border_top_right_radius=50)
        elif square.is_second_end(coords):
            pygame.draw.rect(WIN, BLUE, (location[0]+2, location[1]+2, SQUARESIZE-2, SQUARESIZE-2))
            pygame.draw.rect(WIN, GREY, (location[0]+2, location[1], SQUARESIZE-2, SQUARESIZE), border_bottom_left_radius=50, border_bottom_right_radius=50)
        else:
            pygame.draw.rect(WIN, GREY, (location[0]+2, location[1], SQUARESIZE-2, SQUARESIZE))
    else:
        if square.is_first_end(coords):
            pygame.draw.rect(WIN, BLUE, (location[0]+2, location[1]+2, SQUARESIZE-2, SQUARESIZE-2))
            pygame.draw.rect(WIN, GREY, (location[0], location[1]+2, SQUARESIZE, SQUARESIZE-2), border_top_left_radius=50, border_bottom_left_radius=50)
        elif square.is_second_end(coords):
            pygame.draw.rect(WIN, BLUE, (location[0]+2, location[1]+2, SQUARESIZE-2, SQUARESIZE-2))
            pygame.draw.rect(WIN, GREY, (location[0], location[1]+2, SQUARESIZE, SQUARESIZE-2), border_bottom_right_radius=50, border_top_right_radius=50)
        else:
            pygame.draw.rect(WIN, GREY, (location[0], location[1]+2, SQUARESIZE, SQUARESIZE-2))


def main():
    '''Main function of the game'''

    # Instantiates the game
    user_board = Board()
    ai = AI()
    draw_header('Place your ships. Use space to rotate a ship.')
    draw_board(ai.board, user_board)

    run = True
    while run: # Overall pygame loop
        # Loop for the user to place ships
        while len(ships) > 0:
            x, y = pygame.mouse.get_pos()

            if x > SQUARESIZE*12 and y > 5*SQUARESIZE:
                x -= SQUARESIZE*12
                y -= SQUARESIZE*5

                x = math.ceil(x/SQUARESIZE)
                y = math.ceil(y/SQUARESIZE)
                
                
                draw_ship(ships[0], (x, y), user_board)
            
            
            for event in pygame.event.get():
                draw_board(ai.board, user_board)
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos

                    if x > SQUARESIZE*12 and y > 5*SQUARESIZE:
                        x -= SQUARESIZE*12
                        y -= 5*SQUARESIZE

                        x = math.ceil(x/SQUARESIZE)
                        y = math.ceil(y/SQUARESIZE)

                        is_placed = user_board.place_ship(ships[0]['name'], ships[0]['length'], (x, y), ships[0]['vertical'])
                        if is_placed:
                            ships.pop(0)
        
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        ships[0]['vertical'] = not ships[0]['vertical']


        
        winner = False
        while not winner: # Gameplay loop
            draw_board(ai.board, user_board)
            draw_header('Your turn, select a set of the enemy\'s coordinates.')

            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos

                    if x < SQUARESIZE*12 and x > SQUARESIZE and y > SQUARESIZE*5:
                        x -= SQUARESIZE
                        y -= SQUARESIZE*5

                        x = math.ceil(x/SQUARESIZE)
                        y = math.ceil(y/SQUARESIZE)

                        result = ai.board.attempt_coordinates((x, y), 'User')
                        draw_board(ai.board, user_board)
                        draw_header(result)

                        if ai.board.is_loser():
                            pygame.time.wait(1250)
                            draw_header('Congratulations, you have decimated the enemy\'s fleet!')
                            pygame.time.wait(2000)
                            winner = True
                            run = False
                        else:
                            print("\nEnemy's board:")
                            pprint.pprint(ai.board.display)

                            pygame.time.wait(1250)
                            result = ai.attempt_target(user_board)
                            draw_board(ai.board, user_board)
                            draw_header(result)

                            if user_board.is_loser():
                                pygame.time.wait(1250)
                                draw_header('The enemy has decimated your fleet.')
                                pygame.time.wait(2000)
                                winner = True
                                run = False

                            print("\nOwn board:")
                            pprint.pprint(user_board.display)
                            print("\n")

                            pygame.time.wait(1250)
                            
                                                
if __name__ == "__main__":
    main()