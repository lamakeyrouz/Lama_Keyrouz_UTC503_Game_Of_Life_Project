import pygame, sys, random

# Size of screen
size = (width, height) = 600, 350

# Initialize pygame
pygame.init()

# Display window
window = pygame.display.set_mode(size)

# Get number of columns and main_rows according to the width and height of window and the scale set
scale = 10
main_columns = int(window.get_width()/scale)
main_rows = int(window.get_height()/scale)

# Lambda helper to get the coordinates of the cell in the main column or row at the position specified
location = lambda col_or_row, position, main_col_or_row: (col_or_row + position + main_col_or_row) % main_col_or_row

# Start with a randomly generated grid of 0's and 1's
def get_random_grid():
    grid = []
    for i in range(main_rows):
        row_cells = []
        for j in range(main_columns):
            row_cells.append(random.randint(0, 1))
        grid.append(row_cells)
    return grid

# Count the neighbors of a specific cell
def count(grid, cell_row, cell_col):
    total = 0
    # Iterate through the previous, same, and next cells of the row
    for i in range(-1, 2):
        # Iterate through the previous, same, and next cells of the column
        for j in range(-1, 2):
            # Get the value of the cell in the main grid and add it to the total of neighbors
            col = location(cell_col, j, main_columns)
            row = location(cell_row, i, main_rows)
            total += grid[row][col]
    # Remove the same cell from the total (because we only want neighbors)
    total -= grid[cell_row][cell_col]
    return total

# Generating an empty grid (grid of only 0's) of the same size as the main grid
def get_empty_grid():
    tempGrid = []
    for row in range(main_rows):
        arr = []
        for col in range(main_columns):
            arr.append(0)
        tempGrid.append(arr)
    return tempGrid

# Color the cells according to their value.
def color_cells(grid):
    for col in range(main_columns):
        for row in range(main_rows):
            # Coordinates of cell in the grid
            x = col * scale
            y = row * scale

            # If the value is 1: Color white
            if grid[row][col] == 1:
                pygame.draw.rect(window, (255, 255, 255), (x, y, scale, scale))

            # If the value is 0: Color black
            elif grid[row][col] == 0:
                pygame.draw.rect(window, (0, 0, 0), (x, y, scale, scale))

            # Draw a grey line between the cells for clarity
            pygame.draw.line(window, (20, 20, 20), (x, y), (x, height))
            pygame.draw.line(window, (20, 20, 20), (x, y), (width, y))

# Check the 4 rules of the game of life and refill the grid accordingly to move to the next generation
def proceed_to_next_generation(grid):
    # Get a new grid
    empty_grid = get_empty_grid()

    for col in range(main_columns):
        for row in range(main_rows):
            # Get number of neighbors
            neighbors = count(grid, row, col)

            # Get state of cell
            # If value 1: Cell is alive
            # If value 0: Cell is dead
            state = grid[row][col]

            # If the cell is dead (value = 0) and has 3 neighbors: Reincarnate the cell
            if state == 0 and neighbors == 3 :
                empty_grid[row][col] = 1

            # If the cell is alive (value = 1) and has less than two neighbors: kill the cell
            # Or
            # If the cell is alive (value = 1) and has more than three neighbors: kill the cell
            elif state == 1 and (neighbors < 2 or neighbors > 3):
                empty_grid[row][col] = 0

            # Else keep the cell with the same state
            else:
                empty_grid[row][col] = state
    return empty_grid

# MAIN GRID OF GAME GENERATED RANDOMLY
main_grid = get_random_grid()

# Iterate forever
while True:

    # If exited quite pygame and system
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Fill the window with black color
    window.fill((0, 0, 0))

    # Color the cells of the main grid appropriately
    color_cells(main_grid)

    # Proceed to the next generation
    main_grid = proceed_to_next_generation(main_grid)

    # Display changes
    pygame.display.flip()

