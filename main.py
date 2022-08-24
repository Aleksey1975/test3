from random import randint
import time

COORDS = (1, 2, 3, 4, 5, 6)


class WrogShipException(Exception):
    ...


class RepeatException(Exception):
    def __str__(self):
        return "Вы уже стреляли в эту клетку!"


class Dot:
    def __init__(self, x, y, wounded=False):
        self.x = x
        self.y = y
        self.wounded = wounded

    def __repr__(self):
        return f'({self.x}, {self.y})'

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Ship:
    def __init__(self, dot, len_, horizontal):
        self.dot = dot
        self.len_ = len_
        self.horizontal = horizontal
        self.lives = len_

    @property
    def ship_dots(self):
        ship_dots = []
        for i in range(self.len_):
            if self.horizontal:
                ship_dots.append(Dot(self.dot.x, self.dot.y + i))
            else:
                ship_dots.append(Dot(self.dot.x + i, self.dot.y))

        return ship_dots


class Board:
    NEAR = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1), (0, 0), (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]

    def __init__(self):
        self.board = [['◯'] * 8 for _ in range(8)]
        self.ships = []
        self.busy = []

    def try_add_ship_to_board(self):
        for i in range(1, 999999):
            if not i % 1000:
                print(f'Размещение кораблей на поле {self.name}, попытка №', i // 1000)
            for len_ in (3, 2, 2, 1, 1, 1, 1):
                try:
                    while True:
                        hori = randint(0, 1)
                        if hori:
                            y = randint(1, 6 - len_)
                            x = randint(1, 6)
                        else:
                            x = randint(1, 6 - len_)
                            y = randint(1, 6)
                        candidat = Ship(Dot(x, y), len_, hori)
                        if len_ != 3:
                            break
                        else:
                            if hori and x in (1, 6):
                                break
                            elif not hori and y in (1, 6):
                                break

                    self.check_countur(candidat)
                    self.add_ship_to_board(candidat)

                    if len(self.ships) == 7:
                        break
                except WrogShipException:
                    break

            if len(self.ships) == 7:
                break
            else:
                self.ships = []
                self.board = [['◯'] * 8 for _ in range(8)]

    def check_countur(self, ship):
        for dot in ship.ship_dots:
            for x, y in self.NEAR:
                if self.board[dot.x + x][dot.y + y] == '▇':
                    raise WrogShipException

    def add_ship_to_board(self, ship):
        self.ships.append(ship)
        for ship in self.ships:
            for dot in ship.ship_dots:
                self.board[dot.x][dot.y] = '▇'


    @classmethod
    def print_boards(cls):
        ub = user_board.board
        cb = comp_board.board

        print('-' * 60)
        print('         Поле игрока         ', '         Поле компьютера')
        print()
        print('    1   2   3   4   5   6    ', '        1   2   3   4   5   6')
        for i in range(1, 7):
            print(i, '|', end=' ')
            for j in range(1, 7):
                print(ub[i][j], end=' | ')
            print(' *** ', i, '| ', end='')
            for j in range(1, 7):
                if cb[i][j] == '▇':
                    print('◯', end=' | ')
                else:
                    print(cb[i][j], end=' | ')
            print('\n')
        print('-' * 60)

    def check_shot(self, x, y):
        for i in range(len(self.ships)):
            for j in range(len(self.ships[i].ship_dots)):
                if self.ships[i].ship_dots[j] == Dot(x, y):
                    self.ships[i].ship_dots[j] = True
                    self.board[x][y] = 'X'
                    self.ships[i].lives -= 1
                    if self.ships[i].lives == 0:
                        clean()
                        if self == user_board:
                            clean()
                            print('Ходит комьютер')
                            time.sleep(1)
                            print(x, y)
                            time.sleep(1)
                            clean()
                        print('Потоплен!')
                        time.sleep(1)
                    else:
                        clean()
                        if self == user_board:
                            clean()
                            print('Ходит комьютер')
                            time.sleep(1)
                            print(x, y)
                            time.sleep(1)
                            clean()
                        print('Ранен!')
                        time.sleep(1)
                        clean()

        L = 0
        for ship in self.ships:
            L += ship.lives
        if L == 0:
            clean()
            print(f'Выиграл {self.reversed_name}!')
            return False
        return True


def clean():
    print('\n' * 50)
    Board.print_boards()


user_board = Board()
comp_board = Board()
user_board.name = 'игрока'
comp_board.name = 'компьютера'
comp_board.reversed_name = 'игрок'
user_board.reversed_name = 'компьютер'

print('                      Игра "Морской бой"')
print('Цель игры - поразить все корабли на поле противника.')
print('Выстрел производится указанием двух коодинат через')
print(' пробел, сначала по вертикали, потом по диагонали.\n')
Board.print_boards()
print('Для начала игры нажмите "Enter"')

input()

comp_board.try_add_ship_to_board()
user_board.try_add_ship_to_board()

print('\n' * 50)

Board.print_boards()

GAME = True

while GAME:
    while GAME:  # Ход игрока
        try:
            clean()
            x, y = map(int, input('Ходит игрок:\n   ').split())
        except:
            clean()
            print('Введите две координаты через пробел!')
            time.sleep(2)
            continue

        if x not in COORDS or y not in COORDS:
            clean()
            print('Вы вышли за границы поля!')
            time.sleep(2)
            continue

        try:
            if comp_board.board[x][y] in ('T', 'X'):
                raise RepeatException
        except RepeatException as e:
            clean()
            print(e)
            time.sleep(2)
            continue

        if comp_board.board[x][y] == '◯':
            comp_board.board[x][y] = 'T'
            clean()
            print('Промах!')
            time.sleep(2)
            break

        else:
            try:
                GAME = comp_board.check_shot(x, y)
                if not GAME: break
            except RepeatException as e:
                clean()
                print(e)
                continue

    while GAME:  # Ход компьютера

        x = randint(1, 6)
        y = randint(1, 6)

        try:
            if user_board.board[x][y] in ('T', 'X'):
                raise RepeatException
        except RepeatException as e:
            continue

        if user_board.board[x][y] == '◯':
            user_board.board[x][y] = 'T'
            clean()
            print('Ходит компьютер')
            time.sleep(1)
            print(x, y)
            time.sleep(2)
            clean()
            print('Промах!')
            time.sleep(2)
            break

        else:
            try:
                GAME = user_board.check_shot(x, y)
                if not GAME: break
                time.sleep(2)
            except RepeatException as e:
                continue




