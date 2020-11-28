import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        screen.clear()

        height, width = screen.getmaxyx()

        string = ""
        for row in range(height):
            for col in range(width):
                if row == 0 or row == (height - 1):
                    if col == 0 or col == width:
                        string += "+"
                    else:
                        string += "-"
                elif row < (height - 1) and row > 0:
                    if col == 0 or col == (width - 1):
                        string += "|"
                    else:
                        string += " "
            try:
                screen.addstr(string)
            except curses.error:
                pass
            string = ""

        self.draw_grid(screen)

        screen.refresh()
        screen.getch()

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        height, width = screen.getmaxyx()

        dx = (width - self.life.cols) // 2
        dy = (height - self.life.rows) // 2

        for n_row, row in enumerate(self.life.curr_generation):
            for n_col, col in enumerate(row):
                if col:
                    try:
                        screen.addstr(n_row + dy, n_col + dx, "*")
                    except curses.error:
                        pass

    def run(self) -> None:
        screen = curses.initscr()
        curses.wrapper(self.draw_borders)
        while self.life.is_changing and not self.life.is_max_generations_exceeded:
            self.life.step()
            self.draw_borders(screen)
        curses.endwin()
