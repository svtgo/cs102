import pathlib
import random
import typing as tp
from copy import deepcopy

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        # Copy from previous assignment
        grid = [[0 for i in range(self.cols)] for j in range(self.rows)]
        if randomize:
            for i in range(self.rows):
                for j in range(self.cols):
                    grid[i][j] = random.randint(0, 1)
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        # Copy from previous assignment
        neighbours = []
        r, w = cell
        a = self.rows - 1
        b = self.cols - 1
        for i in range(r - 1, r + 2):
            for j in range(w - 1, w + 2):
                if not (0 <= i <= a and 0 <= j <= b) or (i == r and j == w):
                    continue
                neighbours.append(self.curr_generation[i][j])
        return neighbours

    def get_next_generation(self) -> Grid:
        # Copy from previous assignment
        new_grid = deepcopy(self.curr_generation)
        for i in range(self.rows):
            for j in range(self.cols):
                k = sum(self.get_neighbours((i, j)))
                if self.curr_generation[i][j]:
                    if k < 2 or k > 3:
                        new_grid[i][j] = 0
                else:
                    if k == 3:
                        new_grid[i][j] = 1
        self.grid = new_grid
        return self.grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.max_generations:
            return False if self.generations < self.max_generations else True
        else:
            return False

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return True if self.curr_generation != self.prev_generation else False

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        f = open(filename, "r")
        file_list = [[int(col) for col in row.strip()] for row in f]
        f.close()

        game = GameOfLife((len(file_list), len(file_list[0])))
        game.curr_generation = file_list
        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        f = open(filename, "w")
        for row in self.curr_generation:
            for col in row:
                f.write(str(col))
            f.write("\n")
        f.close()
