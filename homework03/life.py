import pathlib
import random
import copy
import typing as tp

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
        grid = []
        for i in range(self.cell_height):
            grid.append([0] * self.cell_width)
        if randomize:
            for i in range(self.cell_height):
                for j in range(self.cell_width):
                    grid[i][j] = random.randint(0, 1)
        return grid
        pass

    def get_neighbours(self, cell: Cell) -> Cells:
        # Copy from previous assignment
        n = []
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if (
                    (i >= 0)
                    and (i <= self.cell_height - 1)
                    and (j >= 0)
                    and (j <= self.cell_width - 1)
                    and not (i == cell[0] and j == cell[1])
                ):
                    n.append(self.grid[i][j])
        return n
        pass

    def get_next_generation(self) -> Grid:
        # Copy from previous assignment
        new_grid = copy.deepcopy(self.grid)
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                pos = (i, j)
                neigh = 0
                for k in range(len(self.get_neighbours(pos))):
                    if self.get_neighbours(pos)[k] == 1:
                        neigh += 1
                if self.grid[i][j] == 1:
                    if neigh != 2 and neigh != 3:
                        new_grid[i][j] = 0
                else:
                    if neigh == 3:
                        new_grid[i][j] = 1
        return new_grid
        pass

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.generations += 1
        self.prev_generation, self.curr_generation = (
            self.curr_generation,
            self.get_next_generation(),
        )
        pass

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        return self.generations >= self.max_generations
        pass

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return not self.curr_generation == self.prev_generation
        pass

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        height = 0
        grid = []
        f = open(filename)
        for line in f:
            row = [int(i) for i in line if i != "\n"]
            grid.append(row)
            height += 1
        width = len(row)
        start_from_file = GameOfLife((height, width), False)
        start_from_file.prev_generation = GameOfLife.create_grid(start_from_file)
        start_from_file.curr_generation = grid
        f.close()

        return start_from_file
        pass

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        f = open(filename, "w")
        for i in range(self.rows):
            for j in range(self.cols):
                f.write(str(self.curr_generation[i][j]))
            f.write("\n")
        f.close()
        pass
