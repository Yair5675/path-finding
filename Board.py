import Mouse
import numpy as np


class Board:
    def __init__(self, array: np.ndarray, entrance=None):
        self.array = array
        if entrance is None:
            empty_count = 0
            entrance_index = 0
            for index, value in enumerate(self.array[:, 0]):
                if value == 1:
                    empty_count += 1
                elif empty_count > 0:
                    entrance_index = index - empty_count // 2 - 1
                    break
            self.mice = (Mouse.Mouse((entrance_index, 0), [(0, entrance_index)], ['R'], 'R', self.array),)
            self.space_size = empty_count
        else:
            self.mice = (Mouse.Mouse(entrance, [(entrance[1], entrance[0])], ['R'], 'R', self.array),)
            self.space_size = 10

    def move_mice(self):
        new_mice = self.mice[:]
        for num, mouse in enumerate(self.mice):
            moves = mouse.moves()
            for direction, point in moves.items():
                if direction == mouse.direction:
                    mouse.row, mouse.col = point
                    mouse.graphic_history.append((point[1], point[0]))
                    if len(moves) > 1:
                        mouse.history.append(direction)
                    # Blocking the path for future mice:
                    if mouse.direction == 'U':
                        mouse.row -= 1
                        self.array[mouse.room[0][0], mouse.room[0][1]:mouse.room[1][1] + 1].fill(0)
                    elif mouse.direction == 'D':
                        mouse.row += 1
                        self.array[mouse.room[1][0], mouse.room[0][1]:mouse.room[1][1] + 1].fill(0)
                    elif mouse.direction == 'L':
                        mouse.col -= 1
                        self.array[mouse.room[0][0]:mouse.room[1][0] + 1, mouse.room[0][1]].fill(0)
                    else:
                        mouse.col += 1
                        self.array[mouse.room[0][0]:mouse.room[1][0] + 1, mouse.room[1][1]].fill(0)
                    if (len(self.array) <= mouse.row or mouse.row < 0) or (len(self.array[0]) <= mouse.col or mouse.col < 0):
                        mouse.row, mouse.col = point
                    mouse.room = mouse.scan_room()
                else:
                    if self.array[point] == 1:
                        new_mice += (Mouse.Mouse(point, mouse.graphic_history + [(point[1], point[0])],
                                                 mouse.history + [direction], direction, self.array),)

            if mouse.direction not in tuple(moves.keys()):
                new_mice = list(new_mice)
                new_mice.remove(mouse)
                new_mice = tuple(new_mice)
        self.mice = new_mice[:]

    def mouse_won(self):
        for mouse in self.mice:
            if mouse.col == len(self.array[0]) - 1:
                return mouse

    def draw_mice(self, screen):
        for mouse in self.mice:
            mouse.draw_mouse(screen)
            mouse.draw_trail(screen)
