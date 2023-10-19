from pygame import *
import consts
import math
from consts import colors

class Player:
    def __init__(self, name = "", x=0, y=0,
            width=consts.DEFAULT_BODY_WIDTH,
            height=consts.DEFAULT_BODY_HEIGHT,
            headwidth=consts.DEFAULT_HEAD_WIDTH,
            headheight=consts.DEFAULT_HEAD_HEIGHT,
            angle=0.0, headangle=0.0):
        self.name = name
        self.position = Vector2(x, y)
        self.bounds = Rect(round(x), round(y), width, height)
        self.velocity = Vector2(0, 0)

        self.headsize = Vector2(headwidth, headheight)

        self.bodyangle = angle
        self.headangle = headangle

        self.bodysurface = surface.Surface((width, height), SRCALPHA, 32)
        self.headsurface = surface.Surface((width, height), SRCALPHA, 32)


    def set_data(self, name, x, y, width, height, headwidth, headheight, angle, headangle):
        self.name = name
        self.set_location(x, y)
        self.set_size(width, height, headwidth, headheight)
        self.bodyangle = angle
        self.headangle = headangle


    def set_location(self, x, y):
        self.position.x = x
        self.position.y = y
        self.bounds.x = round(x)
        self.bounds.y = round(y)


    def set_size(self, width, height, headwidth, headheight):
        self.bounds.width = width
        self.bounds.height = height
        self.headsize.x = headwidth
        self.headsize.y = headheight


    def update(self, clock:time.Clock, events:list[event.Event]):
        keys = key.get_pressed()

        # Check for user keyboard movement input
        speed = 0
        if keys[K_w]: speed = speed - 1
        if keys[K_a]: self.bodyangle += consts.HEAD_ROTATION * (clock.get_time() / 1000)
        if keys[K_d]: self.bodyangle -= consts.HEAD_ROTATION * (clock.get_time() / 1000)
        if keys[K_s]: speed = speed + 1

        # Check for head movement
        if keys[K_LEFT]: self.headangle += consts.BODY_ROTATION * (clock.get_time() / 1000)
        if keys[K_RIGHT]: self.headangle -= consts.BODY_ROTATION * (clock.get_time() / 1000)

        # Move player given set velocity
        direction = Vector2(-math.cos(math.radians(self.bodyangle)), math.sin(math.radians(self.bodyangle)))
        vel = speed * direction * (clock.get_time() / 1000)
        self.velocity = vel * consts.PLAYER_SPEED
        self.position += self.velocity
        
        # Update player bounds and draw position
        self.bounds.x = round(self.position.x)
        self.bounds.y = round(self.position.y)


    def draw(self, surface:Surface):
        self.bodysurface = self.bodysurface.convert_alpha()
        draw.rect(self.bodysurface, colors.red, Rect(0, 0, self.bounds.w, self.bounds.h))
        rotatedbody = transform.rotate(self.bodysurface, self.bodyangle)

        rotatedbodyhalf = (rotatedbody.get_width() / 2, rotatedbody.get_height() / 2)
        bodyhalf = (self.bodysurface.get_width() / 2, self.bodysurface.get_height() / 2)
        headhalf = (self.headsize.x / 2, self.headsize.y / 2)

        self.headsurface = self.headsurface.convert_alpha()
        draw.rect(self.headsurface, colors.black, Rect(
            bodyhalf[0] - headhalf[0],
            bodyhalf[1] - headhalf[1],
            self.headsize.x, self.headsize.y))
        
        cannonsize = (bodyhalf[0], headhalf[1] / 2)  
        draw.rect(self.headsurface, colors.black, Rect(
            bodyhalf[0],
            bodyhalf[1] - cannonsize[1] / 2,
            cannonsize[0], cannonsize[1]))
        rotatedhead = transform.rotate(self.headsurface, self.headangle + self.bodyangle)

        rotatedheadhalf = (rotatedhead.get_width() / 2, rotatedhead.get_height() / 2)

        surface.blit(rotatedbody, self.position - rotatedbodyhalf)
        surface.blit(rotatedhead, self.position - rotatedheadhalf)

