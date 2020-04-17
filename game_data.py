import contextlib

with contextlib.redirect_stdout(None):
    import pygame

from enum import Enum, IntEnum

# constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
GRID_SIZE = (10, 10)


# Boats type
class BoatType(Enum):
    aircraft_carrier = 5
    cruiser = 4
    destroyer = 3
    torpedo_boat = 2


class Orientation(Enum):
    vertical = 0
    horizontal = 1


class BoatCellState(Enum):
    safe = 0
    touched = 1


class GridCellType(IntEnum):
    water = 0
    boat = 1
    guess = 2
    touched = 3
    missed = 4


# font
pygame.font.init()
font = {"bradbunr": "assets/font/BradBunR.ttf"}

NAME_FONT = pygame.font.Font(font["bradbunr"], 20)
SCORE_FONT = pygame.font.Font(font["bradbunr"], 26)
TITLE_FONT = pygame.font.Font(font["bradbunr"], 30)


def createTextObj(text: str, font_object: pygame.font.Font, color=(255, 255, 255)):
    """
    Creates a text object with a string and a font
    :param color: RGB color
    :type font_object: pygame.font.Font(font_name, 75)
    :param text: string to display
    :param font_object: font in which to display text
    :return: a surface with the text and its rect
    """
    textSurface = font_object.render(text, True, color)
    return textSurface, textSurface.get_rect()


# COLORS
colors = {"black": (0, 0, 0), "darkgray": (70, 70, 70), "gray": (128, 128, 128), "lightgray": (200, 200, 200),
          "white": (255, 255, 255), "red": (255, 0, 0),
          "darkred": (128, 0, 0), "green": (0, 255, 0), "darkgreen": (0, 128, 0), "blue": (0, 0, 255),
          "navy": (0, 0, 128), "darkblue": (0, 0, 128),
          "yellow": (255, 255, 0), "gold": (255, 215, 0), "orange": (255, 165, 0), "lilac": (229, 204, 255),
          "lightblue": (135, 206, 250), "teal": (0, 128, 128),
          "cyan": (0, 255, 255), "purple": (150, 0, 150), "pink": (238, 130, 238), "brown": (139, 69, 19),
          "lightbrown": (222, 184, 135), "lightgreen": (144, 238, 144),
          "turquoise": (64, 224, 208), "beige": (245, 245, 220), "honeydew": (240, 255, 240),
          "lavender": (230, 230, 250), "crimson": (220, 20, 60)}
