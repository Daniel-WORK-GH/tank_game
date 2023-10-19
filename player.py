from pygame import *
import consts
import math
from consts import colors

class Player:
    def __init__(self, name = "", x=0, y=0,
            width=consts.DEFAULT_PLAYER_WIDTH,
            height=consts.DEFAULT_PLAYER_HEIGHT,
            angle=0.0):
        self.name = name
        self.position = Vector2(x, y)
        self.bounds = Rect(round(x), round(y), width, height)
        self.velocity = Vector2(0, 0)

        self.angle = angle

        self.surface = surface.Surface((width, height), SRCALPHA, 32)


    def set_data(self, name, x, y, width, height, angle):
        self.name = name
        self.set_location(x, y)
        self.set_size(width, height)
        self.angle = angle


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
        speed = 0
        if keys[K_w]: speed = speed - 1
        if keys[K_a]: self.angle = self.angle + consts.PLAYER_ROTATION_SPEED * (clock.get_time() / 1000)
        if keys[K_d]: self.angle = self.angle - consts.PLAYER_ROTATION_SPEED * (clock.get_time() / 1000)
        if keys[K_s]: speed = speed + 1

        # Move player given set velocity
        direction = Vector2(-math.cos(math.radians(self.angle)), math.sin(math.radians(self.angle)))
        vel = speed * direction * (clock.get_time() / 1000)
        self.velocity = vel * consts.PLAYER_SPEED
        self.position += self.velocity
        
        # Update player bounds and draw position
        self.bounds.x = round(self.position.x)
        self.bounds.y = round(self.position.y)


    def draw(self, surface:Surface):
        self.surface = self.surface.convert_alpha()
        draw.rect(self.surface, colors.red, Rect(0, 0, self.bounds.w, self.bounds.h))

        rotatedsurface = transform.rotate(self.surface, self.angle)

        center = (rotatedsurface.get_width() / 2, rotatedsurface.get_height() / 2)

        surface.blit(transform.rotate(self.surface, self.angle), self.position - center)

