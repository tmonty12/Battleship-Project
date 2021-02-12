import random
import pprint

WATER = 'w'
MISSED = 'm'
HIT = 'h'
SUNK = 's'
ATTEMPTED = 'a'
SHIPS = [
    { 'name': 'Carrier', 'length': 5 },
    { 'name': 'Battleship', 'length': 4 },
    { 'name': 'Destroyer', 'length': 3 },
    { 'name': 'Submarine', 'length': 3 },
    { 'name': 'Patrol Boat', 'length': 2 },
]

class Board:
    def __init__(self):
        self.ships = []
        
        self.generate_board()

    def generate_board(self):
        display = []
        for i in range(10):
            display.append([WATER for i in range(10)])
        self.display = display

    def place_ship(self, name, length, beg_coords, vertical=True):
        ship = Ship(name, length, beg_coords, vertical)
        if self.check_if_valid_placement(ship):
            return False
        else:
            for (coords, is_hit) in ship.coords_list:
                self.display[coords[1] - 1][coords[0]-1] = ship 
            self.ships.append(ship)
            return True
    
    def check_if_valid_placement(self, ship):
        for (coords, is_hit) in ship.coords_list:
            if coords[0] > 10 or coords[1] > 10:
                return True
            if isinstance(self.display[coords[1] - 1][coords[0]-1], Ship):
                return True
        return False
    
    def is_winner(self):
        return len(self.ships) == 0

    def attempt_coordinates(self, coords, player):
        row = coords[1] - 1
        column = coords[0] - 1
        if (row > 10 or row < 0 or
            column > 10 or column < 0):
            raise Exception(f'{player}: Invalid coordinates')
        target = self.display[row][column]
        if isinstance(target, Ship):
            outcome = target.register_hit(coords)
            if outcome == HIT:
                print(f'{player}: Confirmed hit!')
            elif outcome == ATTEMPTED:
                print(f'{player}: Already attempted these coordinates')
            else:
                if player == 'User':
                    print(f'{player}: Confirmed hit! Your enemy\'s ' + target.name + ' has been sunk!' )
                else:
                    print(f'{player}: Confirmed hit! The enemy has sunk your ' + target.name + '!' )
                self.ships.remove(target)

                if self.is_winner():
                    if player == 'User':
                        print(f'{player}: Congratulations! You have decimated the enemy\'s fleet.')
                    else:
                        print(f'{player}: The enemy has decimated your fleet.')

        elif target == MISSED:
            print(f'{player}: Already attempted these coordinates')
        else:
            print(f'{player}: Attempt missed')
            self.display[coords[1]-1][coords[0]-1] = MISSED       

class Ship:
    def __init__(self, name, length, beg_coords, vertical=True):
        self.name = name
        self.length = length
        
        self.generate_coords(length, vertical, beg_coords)
    
    def generate_coords(self, length, vertical, beg_coords):
        coords_list = [[beg_coords, False]]
        if vertical:
            for i in range(1, length):
                coords_list.append([(beg_coords[0], beg_coords[1]+i), False])
        else:
            for i in range(1, length):
                coords_list.append([(beg_coords[0]+i, beg_coords[1]), False])

        self.coords_list = coords_list
    
    def __repr__(self):
        return self.name
            
    def is_sunk(self):
        hits = 0
        for (coords, is_hit) in self.coords_list:
            if is_hit:
                hits += 1
        return hits == self.length
    
    def register_hit(self, targeted_coords):
        for i, (coords, is_hit) in enumerate(self.coords_list):
            if targeted_coords[0] == coords[0] and targeted_coords[1] == coords[1]:
                if is_hit:
                    return ATTEMPTED
                else:
                    self.coords_list[i][1] = True
                    if self.is_sunk():
                        return SUNK
                    return HIT

class AI:
    def __init__(self):
        self.attempts = []
        self.board = Board()

        self.generate_ships()
    
    def generate_ships(self):
        for ship in SHIPS: 
            vertical = True if random.randint(0, 1) == 1 else False

            is_placed = False
            while not is_placed:
                if vertical:
                    x = random.randint(1, 10)
                    y = random.randint(1, 11-ship['length'])
                else:
                    x = random.randint(0, 11-ship['length']) 
                    y = random.randint(1, 10)
            
                is_placed = self.board.place_ship(ship['name'], ship['length'], (x, y), vertical)
    
    def attempt_target(self, user_board):
        new_target = False
        while not new_target:
            new_target = True
            x = random.randint(1, 10) 
            y = random.randint(1, 10)
            for coords in self.attempts:
                if coords[0] == x and coords[1] == y:
                    new_target = False

        self.attempts.append((x, y))
        user_board.attempt_coordinates((x, y), 'Enemy')

def main():
    user_board = Board()
    user_board.place_ship('Carrier', 5, (2, 5))
    user_board.place_ship('Battleship', 4, (4, 2), vertical=False)
    user_board.place_ship('Destroyer', 3, (4, 7))
    user_board.place_ship('Submarine', 3, (8, 5))
    user_board.place_ship('Patrol Boat', 2, (9, 10), vertical=False)
    ai = AI()

    winner = False
    while not winner:
        x_coord = input('Input x-coordinate of target: ')
        y_coord = input('Input y-coordinate of target: ')
        ai.board.attempt_coordinates((int(x_coord), int(y_coord)), 'User')
        print("\nEnemy's board:")
        pprint.pprint(ai.board.display)

        ai.attempt_target(user_board)
        print("\nOwn board:")
        pprint.pprint(user_board.display)
        print("\n")
        if user_board.is_winner() or ai.board.is_winner():
            winner = True


if __name__ == "__main__":
    main()

    
