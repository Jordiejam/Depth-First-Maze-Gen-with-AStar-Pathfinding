import pygame
from functools import cached_property

class Cell():

    def __init__(self, x, y, w):
        self.pos = pygame.Vector2(x, y)
        self.w = w
        self.cell = pygame.Rect(self.pos.x, self.pos.y, w, w)
        self.center_pos = self.cell.center

        self.walls = {
            'top': True,
            'right': True,
            'bottom': True,
            'left': True
        }

        self.walls_pos = {
            'top': ((self.pos.x, self.pos.y), (self.pos.x + w, self.pos.y)),
            'right': ((self.pos.x + w, self.pos.y), (self.pos.x + w, self.pos.y + w)),
            'bottom': ((self.pos.x, self.pos.y + w), (self.pos.x + w, self.pos.y + w)),
            'left': ((self.pos.x, self.pos.y), (self.pos.x, self.pos.y + w))
        }

        self.visited = False
        self.current = False

        self.path_end = False
        self.path_previous = None
        self.path_g = 0
        self.path_h = 0

    
    def show(self, screen, DEBUG=False):
        if self.visited and not DEBUG:
            pygame.draw.rect(screen, "#B85042", self.cell)
        
        if self.current:
            pygame.draw.rect(screen, "limegreen", self.cell)
        
        if self.path_end:
            pygame.draw.rect(screen, "red", self.cell)
        
        for side, bool in self.walls.items():
            if bool:
                pygame.draw.line(screen, "#E7E8D1", self.walls_pos[side][0], self.walls_pos[side][1], 2)
    
    def check_neighbours(self, grid:list, num_cols):
        idx = grid.index(self)
        available_neighbours = []

        if idx >= num_cols: # top
            if not grid[idx - num_cols].visited:
                available_neighbours.append(grid[idx - num_cols])
        if idx < len(grid) - num_cols: # bottom
            if not grid[idx + num_cols].visited:
                available_neighbours.append(grid[idx + num_cols])
        if idx % num_cols != 0: # left
            if not grid[idx - 1].visited:
                available_neighbours.append(grid[idx - 1])
        if idx % num_cols != num_cols - 1: # right
            if not grid[idx + 1].visited:
                available_neighbours.append(grid[idx + 1])
        
        return available_neighbours

    def transition(self, next_cell):
        if self.pos.x > next_cell.pos.x: # next cell is to the left
            self.walls['left'] = False
            next_cell.walls['right'] = False
        elif self.pos.x < next_cell.pos.x: # next cell is to the right
            self.walls['right'] = False
            next_cell.walls['left'] = False
        elif self.pos.y > next_cell.pos.y: # next cell is above
            self.walls['top'] = False
            next_cell.walls['bottom'] = False
        elif self.pos.y < next_cell.pos.y: # next cell is below
            self.walls['bottom'] = False
            next_cell.walls['top'] = False
        
        self.current = False
        next_cell.current = True
        next_cell.visited = True

        return next_cell

    def find_path(self, grid:list, num_cols:int):

        idx = grid.index(self)
        if self.path_previous is not None:
            path_previous_idx = grid.index(self.path_previous)
        
        available_paths = []

        if idx >= num_cols and not self.walls['top']: # top
            if self.path_previous:
                if path_previous_idx != idx - num_cols:
                    available_paths.append(grid[idx - num_cols])
            else:
                available_paths.append(grid[idx - num_cols])
        if idx < len(grid) - num_cols and not self.walls['bottom']: # bottom
                if self.path_previous:
                    if path_previous_idx != idx + num_cols:
                        available_paths.append(grid[idx + num_cols])
                else:
                    available_paths.append(grid[idx + num_cols])
        if idx % num_cols != 0 and not self.walls['left']: # left
                if self.path_previous:
                    if path_previous_idx != idx - 1:
                        available_paths.append(grid[idx - 1])
                else:
                    available_paths.append(grid[idx - 1])
        if idx % num_cols != num_cols - 1 and not self.walls['right']: # right
                if self.path_previous:
                    if path_previous_idx != idx + 1:
                        available_paths.append(grid[idx + 1])
                else:
                    available_paths.append(grid[idx + 1])
        
        return available_paths

    def calc_h(self, end_cell):
        self.h = abs(self.center_pos[0] - end_cell.center_pos[0]) + abs(self.center_pos[1] - end_cell.center_pos[1])
    
    @cached_property
    def path_f(self):
        return self.path_g + self.h
            
        

        

if __name__ == "__main__":
    print(800%5)