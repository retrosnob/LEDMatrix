# main.py
import pygame
import api_module
import time

# Initialize Pygame (must run in the main thread)
pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Pygame API Event Example")

# Colors
WHITE = (255, 255, 255)

# Start the API (which handles API requests in a separate thread)
command_queue, api_thread = api_module.start_api()

# Main Pygame event loop (runs on the main thread)
running = True
while running:
    screen.fill(WHITE)

    # Process Pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            api_module.stop(command_queue)

        # Handle custom event to draw a rectangle
        if event.type == api_module.DRAW_RECTANGLE_EVENT:
            pygame.draw.rect(screen, event.color, event.rect)

    # Update the display
    pygame.display.flip()

    # Small delay to limit the frame rate
    pygame.time.delay(10)

# Wait for the API thread to finish before exiting
api_thread.join()

# Quit Pygame
pygame.quit()