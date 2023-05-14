import pygame
from PIL import Image

# Initialize pygame:
pygame.init()

images = ('beginner maze.png', 'hard maze.png', 'hug maze.png', 'maze.png', 'another maze.png', 'm.png',
          'very very hard maze.png')


def load_image(image_index, threshold):
    image = Image.open(fr'mazes\{images[image_index]}')
    size = image.size
    if size[1] > 800:
        size = size[0]//2, size[1]//2
    elif size[0] < 200 or size[1] < 200:
        size = size[0] * 2, size[1] * 2
    image = image.resize(size)
    image_array = image.convert('L').point(lambda x: 0 if x < threshold else 255, '1')
    pygame_image = pygame.image.load(fr'mazes\{images[image_index]}')
    pygame_image = pygame.transform.scale(pygame_image, size)
    screen = pygame.display.set_mode((size[0], size[1] + 60))
    return image_array, pygame_image, screen, size


RED = 255, 0, 0
GREEN = 0, 255, 0
WHITE = 255, 255, 255
BLACK = 0, 0, 0

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 40)
