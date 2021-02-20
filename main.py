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
ENEMY_CONFIRMED_HIT = 'Your enemy has a confirmed hit.'
ENEMY_SUNK_SHIP = 'Confirmed hit! The enemy has sunk your '

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
    
    def is_loser(self):
        num_sunk = 0
        for ship in self.ships:
            if ship.is_sunk():
                num_sunk += 1
            
        if num_sunk == len(self.ships):
            return True
        return False

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
                if player == 'User':
                    return 'Confirmed hit!'
                return ENEMY_CONFIRMED_HIT
            elif outcome == ATTEMPTED:
                 return 'You already attempted these coordinates.'
            else:
                if player == 'User':
                    return 'Confirmed hit! Your enemy\'s ' + target.name + ' has been sunk!'
                return ENEMY_SUNK_SHIP + target.name + '!'

        elif target == MISSED:
            return 'Coordinates already attempted.'
        else:
            self.display[coords[1]-1][coords[0]-1] = MISSED       
            if player == 'User':
                return 'Your attempt missed.'
            return 'The enemy\'s attempt missed.'


class Ship:
    def __init__(self, name, length, beg_coords, vertical=True):
        self.name = name
        self.length = length
        self.vertical = vertical
        
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
    
    def is_coords_hit(self, check_coords):
        for coords, is_hit in self.coords_list:
            if coords[0] == check_coords[0] and coords[1] == check_coords[1]:
                return is_hit
    
    def is_first_end(self, check_coords):
        coords, is_hit = self.coords_list[0]
        if coords[0] == check_coords[0] and coords[1] == check_coords[1]:
            return True
        return False

    def is_second_end(self, check_coords):
        coords, is_hit = self.coords_list[-1]
        if coords[0] == check_coords[0] and coords[1] == check_coords[1]:
            return True
        return False

class AI:
    def __init__(self):
        self.attempts = []
        self.targets = []
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
                    x = random.randint(1, 11-ship['length']) 
                    y = random.randint(1, 10)
            
                is_placed = self.board.place_ship(ship['name'], ship['length'], (x, y), vertical)
    
    def attempt_target(self, user_board):
        if len(self.targets) == 0:
            new_target = False
            while not new_target:
                new_target = True
                x = random.randint(1, 10) 
                y = random.randint(1, 10)
                for coords in self.attempts:
                    if coords[0] == x and coords[1] == y:
                        new_target = False
        else:
            new_target = self.targets.pop()
            x, y = new_target

        self.attempts.append((x, y))
        result = user_board.attempt_coordinates((x, y), 'Enemy')

        if result == ENEMY_CONFIRMED_HIT:
            self.add_coords_to_targets((x, y))
        elif result[:len(ENEMY_SUNK_SHIP)] == ENEMY_SUNK_SHIP:
            self.targets = []

        return result
    
    def add_coords_to_targets(self, coords):
        x, y = coords
        targets = [(x, y+1), (x+1, y), (x, y-1), (x-1, y)]

        for i, target in enumerate(targets):
            if target[0] < 1 or target[0] > 10 or target[1] < 1 or target[1] > 10:
                del targets[i]
            else:
                for coords in self.attempts:
                    if coords[0] == target[0] and coords[1] == target[1]:
                        del targets[i]
                
                for coords in self.targets:
                    if coords[0] == target[0] and coords[1] == target[1]:
                        del targets[i]
        
        self.targets.extend(targets)

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
        result = ai.board.attempt_coordinates((int(x_coord), int(y_coord)), 'User')
        print(result)
        print("\nEnemy's board:")
        pprint.pprint(ai.board.display)

        if ai.board.is_loser():
            print("Congratulations! You have decimated the enemy\'s fleet.")
            winner = True
        else:
            result = ai.attempt_target(user_board)
            print("\n" + result)
            print("\nOwn board:")
            pprint.pprint(user_board.display)
            
            if user_board.is_loser():
                print("The enemy has decimated your fleet!")
                winner = True
            
            print("\n")


if __name__ == "__main__":
    main()

    
