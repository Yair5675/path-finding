import numpy as np
from constants import *


class InvalidDirection(Exception):
    def __init__(self, direction):
        self.dir = direction

    def __str__(self):
        return f'U, D, L or R was expected yet "{self.dir}" was given'


class Mouse:
    def __init__(self, starting_point, graphic_history, history, direction, map_array):
        self.row, self.col = starting_point
        self.history = history
        self.graphic_history = graphic_history
        self.direction = direction
        if len(self.direction) != 1 or self.direction not in 'UDLR':
            raise InvalidDirection(self.direction)
        self.array = map_array
        self.room = self.scan_room()  # (upper_wall, left_wall), (lower_wall, right_wall)

    def draw_trail(self, screen):
        if self.col == len(self.array[0]) - 1:
            color = GREEN
        else:
            color = RED
        for index in range(len(self.graphic_history[:-1])):
            pygame.draw.line(screen, color, self.graphic_history[index], self.graphic_history[index + 1], 2)

    def draw_mouse(self, screen):
        pygame.draw.circle(screen, RED, (self.col, self.row), 4)

    def scan_room(self):
        room: np.ndarray
        upper_wall = lower_wall = self.row
        right_wall = left_wall = self.col

        # Finding the upper wall of the room:
        while self.array[upper_wall, self.col] == 1 and upper_wall >= 0:
            upper_wall -= 1
        if upper_wall < 0:
            upper_wall += 1
        # Finding the lower wall of the room:
        try:
            while self.array[lower_wall, self.col] == 1:
                lower_wall += 1
        except IndexError:
            lower_wall -= 1
        # Finding the right wall of the room:
        try:
            while self.array[self.row, right_wall] == 1:
                right_wall += 1
        except IndexError:
            right_wall -= 1
        # Finding the left wall of the room:
        while self.array[self.row, left_wall] == 1 and left_wall >= 0:
            left_wall -= 1
        if left_wall < 0:
            left_wall += 1

        # Adjusting the right side of the room:
        right_spaces_count = np.count_nonzero(self.array[upper_wall:lower_wall + 1, self.col:right_wall + 1], axis=0)
        try:
            normal_space_count = right_spaces_count[0]
        except IndexError:
            pass
        else:
            for index, value in enumerate(right_spaces_count[1:], start=1):
                if value != normal_space_count:
                    right_wall = self.col + index
                    break
        # Adjusting the left side of the room:
        left_spaces_count = np.count_nonzero(self.array[upper_wall:lower_wall + 1, self.col:left_wall + 1:-1], axis=0)
        try:
            normal_space_count = left_spaces_count[0]
        except IndexError:
            pass
        else:
            for index, value in enumerate(left_spaces_count[1:], start=1):
                if value != normal_space_count:
                    left_wall = self.col - index
                    break
        # Adjusting the upper side of the room:
        up_spaces_count = np.count_nonzero(self.array[self.row:upper_wall + 1:-1, left_wall:right_wall + 1], axis=1)
        try:
            normal_space_count = up_spaces_count[0]
        except IndexError:
            pass
        else:
            for index, value in enumerate(up_spaces_count[1:], start=1):
                if value != normal_space_count:
                    upper_wall = self.row - index
                    break
        # Adjusting the lower side of the room:
        down_spaces_count = np.count_nonzero(self.array[self.row:lower_wall + 1, left_wall:right_wall + 1], axis=1)
        try:
            normal_space_count = down_spaces_count[0]
        except IndexError:
            pass
        else:
            for index, value in enumerate(down_spaces_count[1:], start=1):
                if value != normal_space_count:
                    lower_wall = self.row + index + 1
                    if lower_wall >= len(self.array):
                        lower_wall -= 1
                    break
        room = (upper_wall, left_wall), (lower_wall, right_wall)
        return room

    def moves(self):
        try:
            if self.graphic_history[-1] == self.graphic_history[-2]:
                return {}
        except IndexError:
            pass
        # Firstly, moving the mouse to the center of the segment it's in:
        self.row, self.col = (self.room[1][0] + self.room[0][0])//2, (self.room[1][1] + self.room[0][1])//2

        # Looking for available moves:
        moves = {}
        # Moving Up:
        if self.array[self.room[0][0], self.col] == 1:
            moves['U'] = self.room[0][0], self.col
        # Moving Down:
        if self.array[self.room[1][0], self.col] == 1:
            moves['D'] = self.room[1][0], self.col
        # Moving left:
        if self.array[self.row, self.room[0][1]] == 1:
            moves['L'] = self.row, self.room[0][1]
        # Moving Right:
        if self.array[self.row, self.room[1][1]] == 1:
            moves['R'] = self.row, self.room[1][1]

        # Removing the move backwards:
        try:
            if self.direction == 'U':
                del moves['D']
            elif self.direction == 'D':
                del moves['U']
            elif self.direction == 'L':
                del moves['R']
            elif self.direction == 'R':
                del moves['L']
        except KeyError:
            pass

        # Removing repeating moves:
        moves_ = moves.copy()
        for direction, point in moves_.items():
            if (point[1], point[0]) in self.graphic_history:
                del moves[direction]
        return moves

    def block_passage(self):
        new_array = self.array[:, :]
        if self.direction == 'U' or self.direction == 'D':
            index = self.col
            while new_array[self.row, index] == 1:
                index += 1
                if index >= len(self.array[0]):
                    break
            new_array[self.row, self.col:index].fill(0)
            index = self.col
            while new_array[self.row, index] == 1 and index >= 0:
                index -= 1
            new_array[self.row, index:self.col + 1].fill(0)
        else:
            index = self.row
            while new_array[index, self.col] == 1 and index >= 0:
                index += 1
                if index >= len(self.array):
                    break
            new_array[self.row:index, self.col].fill(0)
            index = self.row
            while new_array[index, self.col] == 1:
                index -= 1
            new_array[index:self.row + 1, self.col].fill(0)
        self.array = new_array[:, :]
        return new_array[:, :]
