import random
import time
import pygame

class PipePair:
    def __init__(self, interval):
        self.col = 15
        self.top_pipe_bottom = random.randint(1, 11)
        self.interval = interval
        self.last_update = time.monotonic()
    def get_bottom(self):
        return self.top_pipe_bottom + 4
    def update(self):
        time_now = time.monotonic()
        if (time_now - self.last_update >= self.interval):
            self.col -= 1
            self.last_update = time_now

class Bird:
    def __init__(self, interval):
        self.row = 8
        self.col = 5

    def move_up(self):
        self.row -= 1
    def fall(self):
        self.row += 1
    

class Grid:
    def __init__(self):
        self.width= 16
        self.height = 16
        self.bird = Bird()
        self.pipe_pairs = []
        

    def add_pipe(self):
        num_pipe_pairs = len(self.pipe_pairs)
        if num_pipe_pairs == 0 or self.pipe_pairs[num_pipe_pairs - 1].col < 14:
            self.pipe_pairs.append(PipePair(0.25))

    def remove_pipe(self):
        if len(self.pipe_pairs) > 0:
            if self.pipe_pairs[0].col == 0:
                self.pipe_pairs.pop(0)

    def scroll(self):
        for pipe_pair in self.pipe_pairs:
            pipe_pair.update()

class Game:
    def __init__(self):
        self.grid = Grid()
        self.pygame = pygame.init()
        self.width_in_pixels = 512
        self.height_in_pixels = 512
        self.pixels_per_cell = self.width_in_pixels / self.grid.width
        self.screen = self.pygame.display.set_mode(self.width_in_pixels, self.height_in_pixels)
        self.colors = {
            'black' : (0,0,0),
            'white' : (255,255,255)
        }

    def run(self):
        self.grid.add_pipe()
        self.grid.scroll()
        self.grid.remove_pipe()
        self.render()

    def render(self):
        for row in self.grid.height:
            for col in self.grid.width:
                self.pygame.draw.rect(self.screen, self.colors['black'], ())


def main():
    print("hi")


if __name__ == "__main__":
    main()








