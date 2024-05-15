import pygame
import sys
import random
from objs import Cell

# Initialize Pygame
pygame.init()

instructions = """
r = new_maze
p = pathfinding
i = instant_maze/instant_path
s = speed maze
d = debug
"""
print(instructions)
# Constants for screen dimensions
WIDTH = random.choice([800, 1000, 900, 1024])
DEBUG = False

# Set up the display
screen = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption('Pygame Template')
clock = pygame.time.Clock()
font = pygame.font.Font(None, 16)

def reset():
    global grid, visited, current, queue, speed, cols, WIDTH
    cols = random.randint(5, WIDTH//10)
    while WIDTH % cols != 0:
        if cols > WIDTH//10:
            cols = WIDTH//10
        else:
            cols -= 1
    speed = random.randint(1, cols//5)
    w = WIDTH // cols
    grid = [Cell(x, y, w) for y in range(0, WIDTH, w) for x in range(0, WIDTH, w)]
    visited = set()
    current = random.choice(grid)
    queue = [current]
    current.visited = True
    visited.add(current)
    current.current = True

    global maze_complete, pathfinding, current_path, current_path_cell, pathfinding_trigger, open_set, closed_set, instant_maze, instant_path, path_complete, path_end, direction_of_travel
    pathfinding_trigger = False
    pathfinding = False
    current_path_cell = grid[0]
    path_end = grid[-1]
    direction_of_travel = None
    open_set = [current_path_cell]
    closed_set = set()
    current_path = []

    current_path_cell.calc_h(path_end)

    pathfinding_trigger  = False
    pathfinding = False
    path_complete = False
    instant_maze = False
    instant_path = False
    maze_complete = False

# Main game loop
running = True
reset()
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset()
            if event.key == pygame.K_p:
                pathfinding_trigger = True
            if event.key == pygame.K_d:
                DEBUG = not DEBUG
            if event.key == pygame.K_s:
                speed = 10000
            if event.key == pygame.K_i:
                if maze_complete:
                    instant_path = not instant_path
                else:
                    instant_maze = not instant_maze


    # Game logic
    if len(visited) < len(grid):
        while len(visited) < len(grid):
            for i in range(min(speed, len(grid) - len(visited))):
                available_cells = current.check_neighbours(grid, cols)
                if available_cells:
                    if queue[-1] != current:
                        queue.append(current)
                    next_cell = random.choice(available_cells)
                    next_cell = current.transition(next_cell)
                    visited.add(next_cell)
                    current = next_cell
                    queue.append(current)
                else:
                    if queue:
                        current.current = False
                        current = queue.pop()
                        current.current = True
            if not instant_maze:
                break
    else: # A* Pathfinding
        current.current = False
        maze_complete = True
        
        if pathfinding_trigger:
            pathfinding = True
            pathfinding_trigger = False
        
        if  pathfinding and open_set:
            while open_set and not path_complete:
                next_path_options = current_path_cell.find_path(grid, cols)
                if next_path_options:
                    
                    open_set.remove(current_path_cell)
                    closed_set.add(current_path_cell)

                    for neighbour in next_path_options:
                        neighbour:Cell = neighbour
                        
                        if neighbour in closed_set:
                            continue
                        
                        temp_g = current_path_cell.path_g + 1

                        if neighbour in open_set:
                            if temp_g < neighbour.path_g:
                                neighbour.path_g = temp_g
                        else:
                            neighbour.path_g = temp_g
                            open_set.append(neighbour)
                        
                        neighbour.calc_h(path_end)
                        neighbour.path_previous = current_path_cell
                    
                    best_f_index = 0
                    for i in range(len(open_set)):
                        if open_set[i].path_f < open_set[best_f_index].path_f:
                            best_f_index = i

                    current_path_cell: Cell = open_set[best_f_index]

                    if current_path_cell == path_end:
                        print("Path found!")
                        print(f"Path length: {len(current_path)}")
                        print(f"{(len(closed_set)/len(grid)*100):.2f}% of cells checked for path.")
                        path_complete = True
                        break

                else:
                    open_set.remove(current_path_cell)
                    closed_set.add(current_path_cell)
                    best_f_index = 0
                    for i in range(len(open_set)):
                        if open_set[i].path_f < open_set[best_f_index].path_f:
                            best_f_index = i
                    
                    current_path_cell: Cell = open_set[best_f_index]

                if not instant_path:
                    break
                
    # Drawing
    screen.fill("#A7BEAE")
    
    if pathfinding and DEBUG:
        
        for c in open_set:
            pygame.draw.rect(screen, "green", c.cell)
        for c in closed_set:
            pygame.draw.rect(screen, "red", c.cell)
        
        pygame.draw.rect(screen, "blue", current_path_cell.cell)
        
    for cell in grid:
        cell.show(screen, DEBUG)
        if DEBUG:
            text = font.render(str(grid.index(cell)), True, (255, 255, 255))
            screen.blit(text, (cell.center_pos[0]-text.get_width()//2, cell.center_pos[1]-text.get_height()//2))
    
    if pathfinding:

        current_path = []
        temp_current = current_path_cell
        while temp_current.path_previous:
            current_path.append(temp_current)
            temp_current = temp_current.path_previous
        current_path.append(temp_current)

        for i in range(len(current_path)-1, 0, -1):
            pygame.draw.line(screen, "yellow", current_path[i].center_pos, current_path[i-1].center_pos, current_path[i].w//3)
    
    pygame.display.flip()
    clock.tick(60)

# Clean up
pygame.quit()
sys.exit()
