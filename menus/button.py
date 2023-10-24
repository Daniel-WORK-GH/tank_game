from pygame import *
import consts

class Button:
    def __init__(self, text:str, onclick=None, position:Vector2=None, size:Vector2=None):
        self.text = text
        self.position = position
        self.bounds:Rect = None
        self.onclick = onclick

        if not self.position:
            self.position = Vector2(0, 0)

        if size:
            self.bounds = Rect(
                self.position[0] - size[0] / 2,
                self.position[1] - size[1] / 2,
                *size)

        if not self.bounds:
            self.create_bounds_from_text()

        self.prevclick = False
        self.currclick = True

        self.rendered =consts.FONT.render(self.text, False, consts.colors.black)


    def create_bounds_from_text(self):
        w, h = consts.FONT.size(self.text)     
        self.bounds = Rect(
            self.position[0] - w / 2,
            self.position[1] - h / 2,
            w, h)


    def update(self, events):
        self.prevclick = self.currclick

        x, y = mouse.get_pos()
        
        click = mouse.get_pressed()

        if click[0] and self.bounds.collidepoint(x, y):
            if not self.prevclick:
                self.currclick = True

                if self.onclick:
                    self.onclick()
        else: 
            self.currclick = False


    def draw(self, surface:Surface):
        if consts.DEBUG_MENU:
            draw.rect(surface, consts.colors.blue, self.bounds)
        surface.blit(self.rendered, self.bounds.topleft)