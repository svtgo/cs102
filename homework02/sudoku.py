import random

def read_sudoku(filename):
    digits = [c for c in open(filename).read() if c in '123456789.']
    grid = group(digits, 9)
    return grid


def display(values):
    width = 2
    line = '+'.join(['-' * (width * 3)] * 3)
    for row in range(9):
        print(''.join(values[row][col].center(
            width) + ('|' if str(col) in '25' else '') for col in range(9)))
        if str(row) in '25':
            print(line)
    print()


def group(values, n):
    a = []
    for i in range(0, len(values), n):
        a.append(values[i:i + n])
    return a


def get_row(grid, pos):
    return grid[pos[0]]


def get_col(grid, pos):
    return [grid[i][pos[1]] for i in range(len(grid))]


def get_block(grid, pos):
    row = pos[0] // 3 * 3
    col = pos[1] // 3 * 3
    block = []
    for i in range(3):
        for j in range(3):
            block.append(grid[row + i][col + j])
    return block


def find_empty_positions(grid):
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == '.':
                return (row, col)

    return (-1, -1)


def find_possible_values(grid, pos):
    a_ll = set('123456789')
    row = set(get_row(grid, pos))
    col = set(get_col(grid, pos))
    block = set(get_block(grid, pos))
    new = a_ll - row - col - block
    return new


def solve(grid):
    pos = find_empty_positions(grid)
    if pos == (-1, -1):
        return grid
    row, col = pos
    for new in find_possible_values(grid, pos):
        grid[row][col] = new
        solved_sud = solve(grid)
        if solved_sud:
            return solved_sud
        else:
            grid[row][col] = '.'

    return []


def check_solution(solution):
    for row in range(len(solution)):
        if set(get_row(solution, (row, 0))) != set('123456789'):
            return False
    for col in range(len(solution)):
        if set(get_col(solution, (0, col))) != set('123456789'):
            return False
        for row in (0, 3, 6):
            for col in (0, 3, 6):
                if set(get_block(solution, (row, col))) != set('123456789'):
                    return False
    return True


def generate_sudoku(N):
    grid = solve([['.'] * 9 for _ in range(9)])
    N = 81 - min(81, max(0, N))
    while N:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if grid[row][col] != '.':
            grid[row][col] = '.'
            N -= 1
    return grid


if __name__ == '__main__':
    for fname in ['puzzle1.txt', 'puzzle2.txt', 'puzzle3.txt']:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        display(solution)
