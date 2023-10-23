from pygame import *
import consts

class Textbox:
    def __init__(self, position:Vector2=None, minwidth:int=None):
        self.text = ""
        self.startposition = (position[0], position[1])
        self.position = position
        self.minwidth = minwidth

        self.bounds:Rect

        self.selected = False

        if not self.position:
            self.position = Vector2(0, 0)

        self.create_bounds_from_text("")

        self.rendered = consts.FONT.render(self.text, False, consts.colors.red)


    def create_bounds_from_text(self, text:str):
        w, h = consts.FONT.size(text)     

        if w > self.minwidth:
            diff = (self.bounds.width - self.minwidth) / 2
            self.position[0] = self.startposition[0] - diff

            self.bounds = Rect(self.position[0], self.position[1], w, h)
        else:
            self.position[0] = self.startposition[0]
            self.bounds = Rect(*self.startposition, self.minwidth, h)


    def update(self, events):
        x, y = mouse.get_pos()
        
        click = mouse.get_pressed()

        if click[0]:
            if self.bounds.collidepoint(x, y):
                self.selected = True
            else: 
                self.selected = False

        try:
            if self.selected:
                for event in events: 
                    if event.type == KEYDOWN:
                        key = event.key

                        if key != K_BACKSPACE:
                            self.text += chr(event.key)
                        else:
                            self.text = self.text[:-1]
                        
                        self.rendered = consts.FONT.render(self.text, False, consts.colors.red)
                        self.create_bounds_from_text(self.text)
                        
        except Exception as e:
            print(e)


    def draw(self, surface:Surface):
        if consts.DEBUG_MENU:
            draw.rect(surface, consts.colors.blue, self.bounds)
        surface.blit(self.rendered, self.position)