import pygame
import sys
import threading
import queue
import time

class Matrix:

    # Define a custom event
    DRAW_PIXEL_EVENT = pygame.USEREVENT + 1

    def __init__(self, rows = 72, cols = 120):
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

# API thread function that processes the commands in the queue
def api_thread(command_queue):
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Pygame API Event Example")
    WHITE = (255, 255, 255)

    running = True
    while running:
        # Fill the screen with a white background
        screen.fill(WHITE)

        # Check for Pygame events (e.g., window close, custom events)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                command_queue.put({"action": "stop"})
            
            # Handle custom draw rectangle event
            if event.type == DRAW_RECTANGLE_EVENT:
                pygame.draw.rect(screen, event.color, event.rect)

        # Update the screen
        pygame.display.flip()

        # Process any API calls in the command queue
        try:
            command = command_queue.get_nowait()  # Non-blocking queue check
        except queue.Empty:
            command = None

        if command:
            if command['action'] == "draw_rectangle":
                # Create and post a custom event for drawing a rectangle
                event = pygame.event.Event(DRAW_RECTANGLE_EVENT, {
                    "rect": pygame.Rect(command['x'], command['y'], command['width'], command['height']),
                    "color": command['color']
                })
                pygame.event.post(event)

            elif command['action'] == "stop":
                running = False

        time.sleep(0.01)  # Small delay to avoid busy-waiting

    pygame.quit()

    def api_thread(self):
        while True:
            for event in api_event_queue:
                pygame.event.post(pygame.event.Event(pygame.USEREVENT + 1, 'EVENT'))

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