import pygame

PROGRAM_NAME = "Game"
SCREEN_SIZE = (1280, 720)
FONT = pygame.font.SysFont('timesnewroman',  36)
FPS_CAP = 60

DEFAULT_BODY_WIDTH = 48
DEFAULT_BODY_HEIGHT = 32
DEFAULT_HEAD_WIDTH = 24
DEFAULT_HEAD_HEIGHT = 20
PLAYER_SPEED = 48
HEAD_ROTATION = 60
BODY_ROTATION = 50
PLAYER_COOLDOWN = 4 # sec

DEFAULT_TILE_SIZE = 32

BUFFER_SIZE = 1024
SERVER_DEBUG_MSGS = False
SERVER_OTHERS_DEBUG_MSGS = True # For any incoming users on other devices
SERVER_PORT = 20_001
CLIENT_PORT = 20_001

ROCKET_LIFE_TIME = 0.3 # sec

DEBUG_MAP = False

DEBUG_MENU = False

class colors:
    white = (255, 255, 255)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    black = (0, 0, 0)

    tank_body = (84, 92, 96)
    tank_head = (171, 163, 159)

    rocket = (255,206,0)

    grass = (86, 125, 70)

    transparent_dark_gray = (100, 100, 100, 0)
    black_rgba = (0, 0, 0, 255)