from pygame import *
import consts
from consts import colors

class Player:
    def __init__(self, name = "", x=0, y=0,
            width=consts.DEFAULT_PLAYER_SIZE,
            height=consts.DEFAULT_PLAYER_SIZE):
        self.name = name
        self.position = Vector2(x, y)
        self.bounds = Rect(round(x), round(y), width, height)
        self.velocity = Vector2(0, 0)


    def set_data(self, name, x, y, width, height):
        self.name = name
        self.set_location(x, y)
        self.set_size(width, height)


    def set_location(self, x, y):
        self.position.x = x
        self.position.y = y
        self.bounds.x = round(x)
        self.bounds.y = round(y)


    def set_size(self, width, height):
        self.bounds.width = width
        self.bounds.height = height


    def update(self, clock:time.Clock, events:list[event.Event]):
        keys = key.get_pressed()

        # Check for user keyboard movement input
        x, y = 0, 0
        if keys[K_w]: y = y - 1
        if keys[K_a]: x = x - 1
        if keys[K_d]: x = x + 1
        if keys[K_s]: y = y + 1

        # Move player given set velocity
        vel = Vector2(x, y) * (clock.get_time() / 1000)
        self.velocity = vel * consts.PLAYER_SPEED
        self.position += self.velocity
        
        # Update player bounds and draw position
        self.bounds.x = round(self.position.x)
        self.bounds.y = round(self.position.y)


    def draw(self, surface):
        draw.rect(surface, colors.red, self.bounds)

