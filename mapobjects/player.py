from pygame import *
import consts
import math
import linehelper
from consts import colors
from mapobjects import transform


class Player:
    def __init__(self, name = "", x=1, y=1,
            width=consts.DEFAULT_BODY_WIDTH,
            height=consts.DEFAULT_BODY_HEIGHT,
            headwidth=consts.DEFAULT_HEAD_WIDTH,
            headheight=consts.DEFAULT_HEAD_HEIGHT,
            angle=0.0, headangle=0.0):
        self.name = name
        self.health = 100
        self.position = Vector2(x, y)
        self.bounds = Rect(round(x), round(y), width, height)
        self.velocity = Vector2(0, 0)

        self.elapsedcooldown = 0
        self.shot = None

        self.headsize = Vector2(headwidth, headheight)

        self.bodyangle = angle
        self.headangle = headangle

        self.bodypoints = [ 
            (0, 0),
            (0, height),
            (width, height),
            (width, 0),
        ]
        self.headpoints = [
            (0, 0),
            (0, headheight),
            (headwidth, headheight),
            (headwidth, 0),
        ]
        self.cannonpoints = [
            (0, -headheight / 6),
            (width / 2, -headheight / 6),
            (width / 2, headheight / 6),
            (0, headheight / 6),
        ]

        self.bodypoints = transform.centerPolygon(self.bodypoints)
        self.headpoints = transform.centerPolygon(self.headpoints)


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


    def get_current_edges(self):
        bodypoints = transform.transformPolygon(self.bodypoints, self.position, self.bodyangle) 
        yield (bodypoints[0], bodypoints[1])
        yield (bodypoints[1], bodypoints[2])
        yield (bodypoints[2], bodypoints[3])
        yield (bodypoints[3], bodypoints[0])

    
    def apply_damage(self):
        self.health = 0


    def set_size(self, width, height, headwidth, headheight):
        self.bounds.width = width
        self.bounds.height = height
        self.headsize.x = headwidth
        self.headsize.y = headheight


    def update(self, clock:time.Clock, events:list[event.Event]):
        keys = key.get_pressed()

        # Check for user keyboard movement input
        speed = 0
        bodyangle = 0
        if keys[K_w]: speed = speed - 1
        if keys[K_a]: bodyangle += consts.BODY_ROTATION * (clock.get_time() / 1000)
        if keys[K_d]: bodyangle -= consts.BODY_ROTATION * (clock.get_time() / 1000)
        if keys[K_s]: speed = speed + 1
        self.bodyangle += bodyangle

        # Check for head movement
        headangle = 0
        if keys[K_LEFT]: headangle += consts.HEAD_ROTATION * (clock.get_time() / 1000)
        if keys[K_RIGHT]: headangle -= consts.HEAD_ROTATION * (clock.get_time() / 1000)
        self.headangle += headangle + bodyangle

        # Move player given set velocity
        direction = Vector2(-math.cos(math.radians(self.bodyangle)), math.sin(math.radians(self.bodyangle)))
        vel = speed * direction * (clock.get_time() / 1000)
        self.velocity = vel * consts.PLAYER_SPEED
        self.position += self.velocity
        
        # Update player bounds and draw position
        self.bounds.x = round(self.position.x)
        self.bounds.y = round(self.position.y)

        # Handle shooting
        self.shot = None
        self.elapsedcooldown += (clock.get_time() / 1000)
        if self.elapsedcooldown > consts.PLAYER_COOLDOWN:
            if keys[K_SPACE]:
                lookdir = Vector2(-math.cos(math.radians(self.headangle)), math.sin(math.radians(self.headangle)))
                self.shot = Rocket(self.name, self.position, lookdir)


    def draw(self, surface:Surface):
        bodypoints = transform.transformPolygon(self.bodypoints, self.position, self.bodyangle)  
        headpoints = transform.transformPolygon(self.headpoints, self.position, self.headangle)
        cannonpoints = transform.transformPolygon(self.cannonpoints, self.position, self.headangle)

        draw.polygon(surface, colors.tank_body, bodypoints)
        draw.polygon(surface, colors.tank_head, headpoints)
        draw.polygon(surface, colors.tank_head, cannonpoints)


class Rocket:
    def __init__(self, sourceplayer:str, start:Vector2, direction:Vector2):
        self.player = sourceplayer
        self.start = start
        self.direction = direction
        self.checkedcollide = False


    def check_collide(self, playerlist:list[Player]):
        if self.checkedcollide: return
        self.checkedcollide = True

        self.direction = linehelper.extend_point(self.start, self.direction, 10_000)

        for player in playerlist:
            for edge in player.get_current_edges():
                if linehelper.line_line_intersect(*edge, *self.direction):
                    player.apply_damage()
                    break


    def draw(self, surface:Surface):
        draw.line(surface, color.rocket, *self.start, self.direction)