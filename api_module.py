# api_module.py
import queue
import pygame
import threading
import time

# Define a custom event type for drawing the rectangle
DRAW_RECTANGLE_EVENT = pygame.USEREVENT + 1

# Function to handle API logic (runs in a separate thread)
def api_thread(command_queue):
    while True:
        try:
            command = command_queue.get_nowait()  # Non-blocking queue check
        except queue.Empty:
            command = None

        if command:
            if command['action'] == "draw_rectangle":
                # Post an event to the main Pygame thread to draw the rectangle
                event = pygame.event.Event(DRAW_RECTANGLE_EVENT, {
                    "rect": pygame.Rect(command['x'], command['y'], command['width'], command['height']),
                    "color": command['color']
                })
                pygame.event.post(event)

            elif command['action'] == "stop":
                break

        time.sleep(0.01)  # Small delay to prevent busy-waiting

# Function to start the API thread
def start_api():
    command_queue = queue.Queue()
    thread = threading.Thread(target=api_thread, args=(command_queue,))
    thread.start()
    return command_queue, thread

# API function to draw a rectangle
def draw_rectangle(command_queue, x, y, width, height, color):
    command_queue.put({
        "action": "draw_rectangle",
        "x": x,
        "y": y,
        "width": width,
        "height": height,
        "color": color
    })

# API function to stop the API thread
def stop(command_queue):
    command_queue.put({"action": "stop"})