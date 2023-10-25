from pygame import *
import consts

class Textbox:
    def __init__(self, text:str, position:Vector2=None, minwidth:int=None):
        self.text = text
        self.position = position
        self.minwidth = minwidth

        self.bounds:Rect

        self.selected = False
        self.firstclick = True

        self.prevclick = False
        self.currclick = True

        if not self.position:
            self.position = Vector2(0, 0)

        self.create_bounds_from_text(self.text)

        self.rendered = consts.FONT.render(self.text, False, consts.colors.black)


    def create_bounds_from_text(self, text:str):
        w, h = consts.FONT.size(text)     

        if w > self.minwidth:
            self.bounds = Rect(self.position[0] - w / 2, self.position[1] - h / 2, w, h)
        else:
            self.position[0] = self.position[0]
            self.bounds = Rect(
                self.position[0] - self.minwidth / 2,
                self.position[1] - h / 2,
                self.minwidth, h)


    def update(self, events):
        self.prevclick = self.currclick

        x, y = mouse.get_pos()
        
        click = mouse.get_pressed()

        if click[0]:
            if self.bounds.collidepoint(x, y):
                self.selected = True

                if self.firstclick and not self.prevclick:
                    self.text = ""
                    self.firstclick = False
                    self.rendered = consts.FONT.render(self.text, False, consts.colors.black)
                    self.create_bounds_from_text(self.text)
                    self.currclick = True
            else: 
                self.selected = False
        
        if not(click[0] and self.bounds.collidepoint(x, y)):
            self.currclick = False

        try:
            if self.selected:
                for event in events: 
                    if event.type == KEYDOWN:
                        key = event.key

                        if key != K_BACKSPACE:
                            if key == K_KP_0: self.text += '0'
                            elif key == K_KP_1: self.text += '1'
                            elif key == K_KP_2: self.text += '2'
                            elif key == K_KP_3: self.text += '3'
                            elif key == K_KP_4: self.text += '4'
                            elif key == K_KP_5: self.text += '5'
                            elif key == K_KP_6: self.text += '6'
                            elif key == K_KP_7: self.text += '7'
                            elif key == K_KP_8: self.text += '8'
                            elif key == K_KP_9: self.text += '9'
                            elif key == K_KP_PERIOD: self.text += '.'
                            elif key == K_KP_ENTER: pass
                            elif key == K_RETURN: pass
                            elif key == K_TAB: pass
                            elif key == KMOD_CTRL: pass
                            elif key == K_ESCAPE: pass
                            elif event.mod & event.mod & KMOD_CTRL and event.key == K_v:
                                print(scrap.get(SCRAP_TEXT).decode("utf-8"))
                                self.text += str(scrap.get(SCRAP_TEXT).decode("utf-8"))
                                self.text = self.text.replace(chr(0), "")
                            else: self.text += chr(event.key)
                        else:
                            self.text = self.text[:-1]
                        
                        self.rendered = consts.FONT.render(self.text, False, consts.colors.black)
                        self.create_bounds_from_text(self.text)
                        
        except Exception as e:
            print(e)


    def draw(self, surface:Surface):
        if consts.DEBUG_MENU:
            draw.rect(surface, consts.colors.blue, self.bounds)
        surface.blit(self.rendered, self.bounds.topleft)