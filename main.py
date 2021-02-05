WATER = 'w'
MISSED = 'm'
HIT = 'h'
SUNK = 's'
ATTEMPTED = 'a'

class Board:
    def __init__(self):
        self.board = self.generate_board()
        self.ships = []

    @staticmethod
    def generate_board():
        board = []
        for i in range(10):
            board.append([WATER for i in range(10)])
        return board

    def place_ship(self, name, length, beg_coords, vertical=True):
        ship = Ship(name, length, beg_coords, vertical)
        if self.check_if_ship(ship):
            raise Exception('Already ship placed in that location')
        else:
            for (coords, is_hit) in ship.coords_list:
                self.board[coords[1] - 1][coords[0]-1] = ship 
            self.ships.append(ship)
    
    def check_if_ship(self, ship):
        for (coords, is_hit) in ship.coords_list:
            if isinstance(self.board[coords[1] - 1][coords[0]-1], Ship):
                return True
        return False
    
    def is_winner(self):
        return len(self.ships) == 0

    def attempt_coordinates(self, coords):
        row = coords[1] - 1
        column = coords[0] - 1
        if (row > 10 or row < 0 or
            column > 10 or column < 0):
            raise Exception('Invalid coordinates')
        target = self.board[row][column]
        if isinstance(target, Ship):
            outcome = target.register_hit(coords)
            if outcome == HIT:
                print('Confirmed hit!')
            elif outcome == ATTEMPTED:
                print('Already attempted these coordinates')
            else:
                print('Confirmed hit! Your enemy\'s ' + target.name + ' has been sunk!' )
                self.ships.remove(target)

                if self.is_winner():
                    print('Congratulations! You have decimated the enemy\'s fleet.')

        elif target == MISSED:
            print('Already attempted these coordinates')
        else:
            print('Attempt missed')
            self.board[coords[1]-1][coords[0]-1] = MISSED       

class Ship:
    def __init__(self, name, length, beg_coords, vertical=True):
        self.name = name
        self.length = length
        self.coords_list = self.generate_coords(length, vertical, beg_coords)
    
    @staticmethod
    def generate_coords(length, vertical, beg_coords):
        coords_list = [[beg_coords, False]]
        if vertical:
            for i in range(1, length):
                coords_list.append([(beg_coords[0], beg_coords[1]+i), False])
        else:
            for i in range(1, length):
                coords_list.append([(beg_coords[0]+i, beg_coords[1]), False])
        return coords_list
    
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

def main():
    board = Board()
    board.place_ship('Carrier', 5, (2, 5))
    board.place_ship('Battleship', 4, (4, 2), vertical=False)
    board.place_ship('Destroyer', 3, (4, 7))
    board.place_ship('Submarine', 3, (8, 5))
    board.place_ship('Patrol Boat', 2, (9, 10), vertical=False)

    winner = False

    while not winner:
        x_coord = input('Input x-coordinate of target: ')
        y_coord = input('Input y-coordinate of target: ')

        board.attempt_coordinates((int(x_coord), int(y_coord)))

        if board.is_winner():
            winner = True


if __name__ == "__main__":
    main()