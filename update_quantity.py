from element import Element
import pygame as pg


class UpdateQuantity(Element):
    def __init__(self, surf, font):
        super().__init__("update_quantity")
        go = Element.element_dict["search_bar"].go
        self.surf = surf
        self.font = font
        self.text = ""
        self.active = False
        self.search = pg.Rect(go.x + go.width + 40, go.y, 200, 60)
        self.button = pg.Rect(self.search.x + self.search.width, self.search.y, 180, 60)

    def draw(self):
        txt_surface = self.font.render(self.text, (0, 0, 0))
        button_txt_surface = self.font.render("Quant", (0, 0, 0))
        go = Element.element_dict["search_bar"].go
        self.search.x = go.x + go.width + 20
        self.search.w = max(200, txt_surface[0].get_width() + 10)
        self.button.x = self.search.x + self.search.width
        pg.draw.rect(self.surf, (255, 255, 255), self.search, 0)
        pg.draw.rect(self.surf, (0, 0, 0), self.search, 3)
        pg.draw.rect(self.surf, (30, 255, 30), self.button, 0)
        pg.draw.rect(self.surf, (0, 0, 0), self.button, 3)
        self.surf.blit(txt_surface[0], (self.search.x + 5, self.search.y + 10))
        self.surf.blit(button_txt_surface[0], (self.button.x + 10, self.button.y + 10))

    def event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.button.collidepoint(event.pos) and self.text.isnumeric():
                graph = Element.element_dict["graph"]
                if graph.factory is None:
                    return
                graph.update_list(graph.name, quantity=float(self.text))
                self.text = ""
            if self.search.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == pg.K_RETURN:
                    graph = Element.element_dict["graph"]
                    if graph.factory is None:
                        return
                    graph.update_list(graph.name, quantity=float(self.text))
                    self.text = ""
                else:
                    self.text += event.unicode
