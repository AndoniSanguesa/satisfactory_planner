import pygame as pg
from element import Element


class OptSelector(Element):
    def __init__(self, surf, font):
        super().__init__("opt_selector")
        self.opt = 1
        self.surf = surf
        self.font = font
        self.y = Element.element_dict["search_bar"].search.y - 50
        self.opts = [(0, 0) for _ in range(3)]
        self.cur_opt = 1
        self.border = pg.Rect(10, self.y-10, 10, 40)

    def draw(self):
        cur_x = 20

        pg.draw.rect(self.surf, (255, 255, 255), self.border, border_radius=15)
        pg.draw.rect(self.surf, (0, 0, 0), self.border, width=3, border_radius=15)

        opt_text = self.font.render("Optimize For: Energy", (0, 0, 0), size=10)
        mat_text = self.font.render("Materials", (0, 0, 0), size=10)
        space_text = self.font.render("Space", (0, 0, 0), size=10)
        self.surf.blit(opt_text[0], (cur_x, self.y))
        cur_x += opt_text[1].width + 20
        circ_pos = (cur_x, self.y + 10)
        pg.draw.circle(self.surf, (0, 0, 0), circ_pos, 10, width=3)
        if self.cur_opt == 0:
            pg.draw.circle(self.surf, (0, 0, 0), circ_pos, 5)
        self.opts[0] = circ_pos
        cur_x += 20
        self.surf.blit(mat_text[0], (cur_x, self.y))
        cur_x += mat_text[1].width + 20
        circ_pos = (cur_x, self.y + 10)
        pg.draw.circle(self.surf, (0, 0, 0), circ_pos, 10, width=3)
        if self.cur_opt == 1:
            pg.draw.circle(self.surf, (0, 0, 0), circ_pos, 5)
        self.opts[1] = circ_pos
        cur_x += 20
        self.surf.blit(space_text[0], (cur_x, self.y))
        cur_x += space_text[1].width + 20
        circ_pos = (cur_x, self.y + 10)
        pg.draw.circle(self.surf, (0, 0, 0), circ_pos, 10, width=3)
        if self.cur_opt == 2:
            pg.draw.circle(self.surf, (0, 0, 0), circ_pos, 5)
        self.opts[2] = circ_pos
        self.border.width = cur_x + 20

    def event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            for ind in range(3):
                if ((event.pos[0] - self.opts[ind][0]) ** 2 + (event.pos[1] - self.opts[ind][1]) ** 2) ** 0.5 < 10:
                    if ind != self.cur_opt:
                        Element.element_dict["graph"].update_opt(ind)
                    self.cur_opt = ind
                    break



