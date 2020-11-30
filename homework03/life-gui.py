import pygame
from pygame.locals import *

from life import GameOfLife
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed
        self.screen = pygame.display.set_mode(
            (self.life.cols * self.cell_size, self.life.rows * self.cell_size)
        )

    def draw_lines(self) -> None:
        # Copy from previous assignment
        width = self.life.cols * self.cell_size
        height = self.life.rows * self.cell_size
        for x in range(0, width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, height))
        for y in range(0, height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (width, y))

    def draw_grid(self) -> None:
        # Copy from previous assignment
        for i in range(self.life.rows):
            for j in range(self.life.cols):
                x = j * self.cell_size + 1
                y = i * self.cell_size + 1
                a = self.cell_size - 1
                b = self.cell_size - 1
                if self.life.curr_generation[i][j]:
                    pygame.draw.rect(self.screen, pygame.Color("green"), (x, y, a, b))
                else:
                    pygame.draw.rect(self.screen, pygame.Color("white"), (x, y, a, b))

    def run(self) -> None:
        # Copy from previous assignment
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        pause = False
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    pause = True

            self.draw_lines()

            if pause:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        pause = False
                    elif event.type == pygame.MOUSEBUTTONUP:
                        pos = pygame.mouse.get_pos()
                        x = pos[0] // self.cell_size
                        y = pos[1] // self.cell_size
                        if self.life.curr_generation[y][x]:
                            self.life.curr_generation[y][x] = 0
                        else:
                            self.life.curr_generation[y][x] = 1
                        self.draw_grid()
                        pygame.display.flip()
            else:

                # Отрисовка списка клеток
                # Выполнение одного шага игры (обновление состояния ячеек)
                self.life.step()
                self.draw_grid()

                pygame.display.flip()
                clock.tick(self.speed)
        pygame.quit()


if __name__ == "__main__":
    game = GameOfLife((12, 16), max_generations=50)
    gui = GUI(game)
    gui.run()
