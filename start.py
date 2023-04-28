import numpy as np
import pygame
import pyaudio

# PyAudio configuration
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# Pygame configuration
WIDTH, HEIGHT = 800, 600
BG_COLOR = (0, 0, 0)
BAR_COLOR = (0, 255, 0)

# Initialize PyAudio
audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True, frames_per_buffer=CHUNK)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Audio Visualizer")
clock = pygame.time.Clock()


def draw_bars(data, num_bars=50):
    screen.fill(BG_COLOR)
    bar_width = WIDTH // num_bars
    bar_height_factor = HEIGHT // 300

    for i in range(num_bars):
        bar_height = int(data[i] * bar_height_factor)
        bar_x = i * bar_width
        pygame.draw.rect(screen, BAR_COLOR, (bar_x, HEIGHT -
                         bar_height, bar_width, bar_height))

    pygame.display.flip()


# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Read audio data
    data = np.frombuffer(stream.read(
        CHUNK, exception_on_overflow=False), dtype=np.int16)
    data = np.abs(np.fft.fft(data)[:CHUNK // 2]) / CHUNK

    draw_bars(data)
    clock.tick(30)

# Clean up
stream.stop_stream()
stream.close()
audio.terminate()
pygame.quit()
