import random
import time
import pygame

class PipePair:
    def __init__(self, interval):
        self.col = 15
        self.top_pipe_bottom = random.randint(0, 10)
        self.interval = interval
        self.last_update = time.monotonic()
    def get_bottom_top(self):
        return self.top_pipe_bottom + 5
    def update(self):
        time_now = time.monotonic()
        if (time_now - self.last_update >= self.interval):
            self.col -= 1
            self.last_update = time_now

class Bird:
    def __init__(self, interval):
        self.row = 8
        self.col = 5
        self.interval = interval
        self.last_update = time.monotonic()

    def move_up(self):
        self.row -= 1
    def fall(self):
        self.row += 1
    def update(self, key):
        time_now = time.monotonic()
        moved = False
        if (time_now - self.last_update >= self.interval):
            if (key == True):
                self.move_up()
                moved = True
            else:
                self.fall()
            self.last_update = time_now
        return moved


class Grid:
    def __init__(self):
        self.width= 16
        self.height = 16
        self.bird = Bird(0.5)
        self.pipe_pairs = []
        self.distance_between_pipe_pairs = 5
        

    def add_pipe(self):
        num_pipe_pairs = len(self.pipe_pairs)
        if num_pipe_pairs == 0 or self.pipe_pairs[num_pipe_pairs - 1].col < (self.width - self.distance_between_pipe_pairs):
            self.pipe_pairs.append(PipePair(1))

    def remove_pipe(self):
        if len(self.pipe_pairs) > 0:
            if self.pipe_pairs[0].col < 0:
                self.pipe_pairs.pop(0)

    def scroll(self):
        num_pipes_bird_passed = 0
        for pipe_pair in self.pipe_pairs:
            pipe_previously_in_front = pipe_pair.col >= self.bird.col
            pipe_pair.update()
            pipe_now_behind = pipe_pair.col < self.bird.col
            if pipe_previously_in_front and pipe_now_behind:
                num_pipes_bird_passed += 1
        return num_pipes_bird_passed

    def collision(self):
        bird_row = self.bird.row
        for pipe_pair in self.pipe_pairs:
            if self.bird.col == pipe_pair.col:
                if bird_row <= pipe_pair.top_pipe_bottom or bird_row >= pipe_pair.get_bottom_top():
                    return True
        if bird_row < 0 or bird_row >= self.height:
            return True 
        return False
    

class Game:
    def __init__(self):
        self.grid = Grid()
        self.width_in_pixels = 512
        self.height_in_pixels = 512
        self.pixels_per_cell = self.width_in_pixels / self.grid.width
        self.colors = {
            'black' : (0,0,0),
            'white' : (255,255,255),
            'blue' : (0, 0, 255)
        }
        pygame.init()
        self.screen = pygame.display.set_mode((self.width_in_pixels, self.height_in_pixels))
        self.reward = 0
        self.font = pygame.font.SysFont(None, 48)

    def run(self):
        up_key_pressed = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return  

            ###PAUSE


            ###PAUSE
            
                
            keys = pygame.key.get_pressed()
            up_key_pressed = keys[pygame.K_UP] or up_key_pressed
            if self.grid.bird.update(up_key_pressed):
                up_key_pressed = False
           
            self.grid.add_pipe()
            self.reward += self.grid.scroll()
            self.grid.remove_pipe()
            if self.grid.collision():
                pygame.quit()
            self.render()

    def render(self):
        for row in range(self.grid.height):
            for col in range(self.grid.width):
                pygame.draw.rect(self.screen, self.colors['white'], (col * self.pixels_per_cell, row * self.pixels_per_cell, self.pixels_per_cell, self.pixels_per_cell))

        for pipe_pair in self.grid.pipe_pairs:
            pygame.draw.rect(self.screen, self.colors['black'], (pipe_pair.col * self.pixels_per_cell, 0, self.pixels_per_cell, self.pixels_per_cell * (pipe_pair.top_pipe_bottom + 1)))
            pygame.draw.rect(self.screen, self.colors['black'], (pipe_pair.col * self.pixels_per_cell, pipe_pair.get_bottom_top() * self.pixels_per_cell, self.pixels_per_cell, self.pixels_per_cell * (self.grid.height - pipe_pair.get_bottom_top() + 1)))

        bird = self.grid.bird
        pygame.draw.rect(self.screen, self.colors['blue'], (bird.col * self.pixels_per_cell, bird.row * self.pixels_per_cell, self.pixels_per_cell, self.pixels_per_cell))

        text_surface = self.font.render(str(self.reward), True, self.colors['black'])
        self.screen.blit(text_surface, (0, 0))
        
        pygame.display.flip()


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()








