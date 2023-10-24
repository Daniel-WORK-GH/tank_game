class Menu:
    def __init__(self, objects:list):
        self.objects = objects

    
    def update(self, events):
        for o in self.objects:
            o.update(events)


    def draw(self, surface):
        for o in self.objects:
            o.draw(surface)