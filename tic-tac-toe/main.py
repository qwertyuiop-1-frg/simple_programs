# 1. Класс, который будет описывать одну клетку поля:
class Cell:
    def __init__(self, cell_number):
        self.is_busy = False
        self.cell_number = cell_number
        self.sign = '_'

    def swap_to_x(self):
        self.is_busy = True
        self.sign = 'X'

    def swap_to_o(self):
        self.is_busy = True
        self.sign = 'O'

# 2. Класс, который будет описывать поле игры.
class Board:
    field = [Cell(i) for i in range(9)]

    def change_cell(self, pos, which_player):
        if not self.field[pos].is_busy:
            if which_player:
                self.field[pos].swap_to_x()
            else: self.field[pos].swap_to_o()
            return True
        return False

    def check_game_instance(self, which_player):
        win_combinations = ((0, 1, 2),(3, 4, 5), (6, 7 ,8), (0, 3 ,6),
                            (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))

        if which_player:
            filled_cells = tuple(cell.cell_number for cell in self.field if cell.sign == 'X')
            for combination in win_combinations:
                if set(combination).issubset(set(filled_cells)):
                    return True
        else:
            filled_cells = tuple(cell.cell_number for cell in self.field if cell.sign == 'O')
            for combination in win_combinations:
                if set(combination).issubset(set(filled_cells)):
                    return True
        return False

    def check_if_board_full(self):
        for cell in self.field:
            if not cell.is_busy:
                return False
        return True




# 3. Класс, который описывает поведение игрока:
class Player:
    def __init__(self, name):
        self.name = name
        self.wins_amt = 0

    def player_turn(self):
        try:
            place = int(input('Выберите в какую клетку сделать ход: '))
            place -= 1
            if 8 >= place >= 0:
                return place
            else:
                print('Число должно бытьв пределах от 1 до 9!')
                return self.player_turn()
        except ValueError:
            print('Некорректный ввод!')
            return self.player_turn()


# 4. Класс, который управляет ходом игры:
class Game:
    def __init__(self, name_1, name_2):
        self.game_instance = False
        self.players = [Player(name_1), Player(name_2)]
        self.field_info = Board()

    def show_board(self):
        counter = 0
        for row in range(0, 3):
            for column in range(0,3):
                if column != 2:
                    print(f'{self.field_info.field[counter].sign}|', end='')
                else: print(f'{self.field_info.field[counter].sign}', end='')
                counter += 1
            print()

    def start_game(self):
        game_end = False
        is_first_players_turn = True
        while not game_end:
            self.show_board()
            if is_first_players_turn:
                turn = self.players[0].player_turn()
                self.field_info.change_cell(turn, self.players[0])
                res = self.field_info.check_game_instance(is_first_players_turn)
                if res:
                    print(f'{self.players[0].name} Win!')
                    self.players[0].wins_amt += 1
                    game_end = True
            else:
                turn = self.players[1].player_turn()
                self.field_info.change_cell(turn, is_first_players_turn)
                res = self.field_info.check_game_instance(is_first_players_turn)
                if res:
                    print(f'{self.players[0].name} Win!')
                    self.players[1].wins_amt += 1
                    game_end = True
            is_full = self.field_info.check_if_board_full()
            if is_full:
                print('Draw!')
                game_end = True
            if is_first_players_turn:
                is_first_players_turn = False
            else: is_first_players_turn = True

    def main_game_starter(self, play=True):
        while play:
            self.start_game()
            print(f'Игра окончена! текущий счёт:\n'
                  f'{self.players[0].name} - {self.players[0].wins_amt}\n'
                  f'{self.players[1].name} - {self.players[1].wins_amt}\n')
            usr_input = input('Хотите ли продолжить? Да/Нет: ')
            if usr_input == 'Нет':
                play = False
            elif usr_input == 'Да':
                for i in range(9):
                    Cell(i).is_busy = False
                    Cell(i).sign = None
                    Board.field = [Cell(i) for i in range(9)]
                continue
            else:
                print('Некорректный ввод, остановка программы')


game_starter = Game('Андрей', 'Аркаша')
game_starter.main_game_starter()
