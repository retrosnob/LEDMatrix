import pygame
import sys
import inspect


class Matrix:

    def __init__(self, rows = 72, cols = 120):

        if not callable('update'):
            print('You must define a function called update. The matrix will call it repeatedly to get the changes to your matrix.')
            sys.exit()

        if not callable('start'):
            print('You must define a function called start. The matrix will call it once to get the starting state of the matrix.')
            sys.exit()


        self.rows = rows
        self.cols = cols
        self.matrix = [[(32, 32, 32) for c in range(cols)] for r in range(rows)]
        self.border = 5
        self.pixel_width = 5
        self.pixel_padding = 5

        self.api_event_queue = []

        if rows > 72 or cols > 120:
            print('Max size is 72 rows, 120 columns')
            sys.exit()

        # All rectangle 5 x 5
        # width x height of matrix
        # 120 x 72 (largest possible)
        # 72 x 120
        # 120 x 36

        # Width can be 240, 144, 72, 36
        # Height can be 144, 72, 36

        self.screen_width = self.cols * (self.pixel_width + self.pixel_padding) + 2 * self.border
        self.screen_height = self.rows * (self.pixel_width + self.pixel_padding) + 2 * self.border
        self.screen_size = self.screen_width, self.screen_height 

        # Initialise pygame.
        pygame.init()
        pygame.display.set_caption('LED Matrix')
        self.screen = pygame.display.set_mode(self.screen_size)

        # Create the surface to draw on.
        # We will draw to a surface and then blit it all at once.
        self.surface = pygame.Surface(self.screen_size)
        self.surface.set_colorkey((0,0,0))
        self.run()

    def run(self):
        self.running = True
        while self.running:
            # Process the pygame event queue.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            # CALL TO FUNCTIONS DEFINED BY USER
            update()
            draw()
            # *********************************

    def clear(self):
        for r in range(self.rows):
            for c in range(self.cols):
                self.pixel(r, c)

    def pixel(self, x, y, colour = (32, 32, 32)):
        if x >= self.cols:
            raise ValueError('x value ({}) too large. It must be in the range 0-{}'.format(x, self.cols-1))
        if y >= self.rows:
            raise ValueError('y value ({}) too large. It must be in the range 0-{}'.format(y, self.rows-1))
        if x < 0:
            raise ValueError('x value ({}) too small. It must be in the range 0-{}'.format(x, self.cols-1))
        if y < 0:
            raise ValueError('y value ({}) too small. It must be in the range 0-{}'.format(y, self.rows-1))
        
        self.matrix[x][y] = colour

    def _matrix_to_surface(self):
        for r in range(self.rows):
            for c in range(self.cols):
                print(self.matrix[r][c])
                x, y = self.convert_index_to_surface_coords(r, c)
                rect = pygame.Rect(x, y, self.pixel_width, self.pixel_width)
                pygame.draw.rect(self.surface, self.matrix[r][c], rect)

    def convert_index_to_surface_coords(self, r, c):
        return (self.pixel_padding + self.pixel_width) * r, (self.pixel_padding + self.pixel_width) * c

    def draw(self):
        self._matrix_to_surface()
        self.screen.blit(self.surface, (0, 0))
        pygame.display.update()

if __name__ == '__main__':
    m = Matrix()
    m.pixel(34, 62, (255,0,0))
    m.draw()