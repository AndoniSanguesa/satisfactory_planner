import pygame as pg
from element import Element


class SearchBar(Element):
    def __init__(self, surf, font):
        super().__init__("search_bar")
        width, height = (200, 60)
        self.search = pg.Rect(10, surf.get_height()-10-height, width, height)
        self.go = pg.Rect(10+width, surf.get_height()-10-height, height+20, height)

        self.text = ""
        self.active = False
        self.surf = surf
        self.font = font

    def event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.search.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
            if self.go.collidepoint(event.pos):
                Element.element_dict["graph"].update_list(self.text)
                self.text = ""
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == pg.K_RETURN:
                    Element.element_dict["graph"].update_list(self.text)
                    self.text = ""
                else:
                    self.text += event.unicode

    def draw(self):
        txt_surface = self.font.render(self.text, (0, 0, 0))
        go_txt_surface = self.font.render("go", (0, 0, 0))
        self.search.w = max(200, txt_surface[0].get_width() + 10)
        self.go.x = max(210, txt_surface[0].get_width() + 20)
        pg.draw.rect(self.surf, (255, 255, 255), self.search, 0)
        pg.draw.rect(self.surf, (0, 0, 0), self.search, 3)
        pg.draw.rect(self.surf, (30, 255, 30), self.go, 0)
        pg.draw.rect(self.surf, (0, 0, 0), self.go, 3)
        self.surf.blit(txt_surface[0], (self.search.x + 5, self.search.y + 10))
        self.surf.blit(go_txt_surface[0], (self.go.x + 10, self.go.y + 10))
