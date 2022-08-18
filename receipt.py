import pygame as pg
from element import Element
import math


class Receipt(Element):
    def __init__(self, surf, font):
        super().__init__("receipt")
        self.open = False
        self.opening = False
        self.closing = False
        self.surf = surf
        self.font = font
        self.size = 8
        self.body_height = 10
        self.tab = pg.Rect(155, 0, 100, 40)

    def draw_tab(self):
        pg.draw.rect(self.surf, (255, 255, 255), self.tab, border_bottom_left_radius=10, border_bottom_right_radius=10)
        pg.draw.rect(self.surf, (0, 0, 0), self.tab, width=3, border_bottom_left_radius=10,
                     border_bottom_right_radius=10)
        cover_rect = pg.Rect(self.tab.x + 3, self.tab.y - 4, self.tab.width - 6, 10)
        pg.draw.rect(self.surf, (255, 255, 255), cover_rect)
        if self.open:
            pg.draw.line(self.surf, (0, 0, 0), (self.tab.x + 30, self.tab.y + 10),
                         (self.tab.x + self.tab.width / 2, self.tab.y + 5), width=3)
            pg.draw.line(self.surf, (0, 0, 0), (self.tab.x + self.tab.width / 2, self.tab.y + 5),
                         (self.tab.x + self.tab.width - 30, self.tab.y + 10), width=3)
            pg.draw.line(self.surf, (0, 0, 0), (self.tab.x + 30, self.tab.y + 20),
                         (self.tab.x + self.tab.width / 2, self.tab.y + 15), width=3)
            pg.draw.line(self.surf, (0, 0, 0), (self.tab.x + self.tab.width / 2, self.tab.y + 15),
                         (self.tab.x + self.tab.width - 30, self.tab.y + 20), width=3)
        else:
            pg.draw.line(self.surf, (0, 0, 0), (self.tab.x + 30, self.tab.y + 10),
                         (self.tab.x + self.tab.width / 2, self.tab.y + 15), width=3)
            pg.draw.line(self.surf, (0, 0, 0), (self.tab.x + self.tab.width / 2, self.tab.y + 15),
                         (self.tab.x + self.tab.width - 30, self.tab.y + 10), width=3)
            pg.draw.line(self.surf, (0, 0, 0), (self.tab.x + 30, self.tab.y + 20),
                         (self.tab.x + self.tab.width / 2, self.tab.y + 25), width=3)
            pg.draw.line(self.surf, (0, 0, 0), (self.tab.x + self.tab.width / 2, self.tab.y + 25),
                         (self.tab.x + self.tab.width - 30, self.tab.y + 20), width=3)
    def draw(self):
        if not self.open:
            self.draw_tab()
            return
        graph = Element.element_dict["graph"]
        body = pg.Rect(30, -40, 350, self.body_height)
        pg.draw.rect(self.surf, (255, 255, 255), body, border_radius=10)
        pg.draw.rect(self.surf, (0, 0, 0), body, width=3, border_radius=10)
        if not graph.factory:
            none_text = self.font.render("Nothing to see here!", (0, 0, 0), size=self.size)
            self.surf.blit(none_text[0], (body.x + 20, body.y + 60))
            self.body_height = body.y + 140
            self.tab.y = self.body_height - 40
            self.draw_tab()
        else:
            x = body.x + 20
            cur_y = body.y + 60
            diff = 10

            factory = graph.factory
            energy_label_text = self.font.render("Energy: ", (0, 0, 0), size=self.size)
            self.surf.blit(energy_label_text[0], (x, cur_y))

            cur_y += energy_label_text[1].height + diff

            energy = int(math.ceil(factory.get_energy()))
            energy_text = self.font.render(f"{energy} MW / min", (0, 0, 0), size=self.size)
            self.surf.blit(energy_text[0], (x + 40, cur_y))

            cur_y += energy_text[1].height + diff

            materials = factory.get_materials()
            material_label_text = self.font.render("Materials: ", (0, 0, 0), size=self.size)
            self.surf.blit(material_label_text[0], (x, cur_y))

            cur_y += material_label_text[1].height + diff

            for material in materials:
                material_text = self.font.render(f"{material} x {materials[material]} / min", (0, 0, 0), size=self.size)
                self.surf.blit(material_text[0], (x + 40, cur_y))
                cur_y += material_text[1].height + diff

            byproducts = factory.get_byproducts()
            byproducts_label_text = self.font.render("Byproducts: ", (0, 0, 0), size=self.size)
            self.surf.blit(byproducts_label_text[0], (x, cur_y))

            cur_y += byproducts_label_text[1].height + diff

            for byproduct in byproducts:
                byproduct_text = self.font.render(f"{byproduct} x {byproducts[byproduct]} / min", (0, 0, 0), size=self.size)
                self.surf.blit(byproduct_text[0], (x + 40, cur_y))
                cur_y += byproduct_text[1].height + diff

            machine_label_text = self.font.render("Machines: ", (0, 0, 0), size=self.size)
            self.surf.blit(machine_label_text[0], (x, cur_y))

            cur_y += machine_label_text[1].height + diff

            machines = factory.get_machines()
            for machine in machines:
                machine_text = self.font.render(f"{machine} x {machines[machine]}", (0, 0, 0), size=self.size)
                self.surf.blit(machine_text[0], (x + 40, cur_y))
                cur_y += machine_text[1].height + diff

            product_label_text = self.font.render("Product: ", (0, 0, 0), size=self.size)
            self.surf.blit(product_label_text[0], (x, cur_y))

            cur_y += product_label_text[1].height + diff

            product = factory.product[0]
            product_amount = factory.product[1]
            product_text = self.font.render(f"{product} x {product_amount} / min", (0, 0, 0), size=self.size)
            self.surf.blit(product_text[0], (x + 40, cur_y))

            cur_y += product_text[1].height + diff

            self.body_height = cur_y + 60
            self.tab.y = self.body_height - 40
            self.draw_tab()

    def event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and self.tab.collidepoint(event.pos):
            if self.open:
                self.closing = True
            else:
                self.opening = True
            self.open = not self.open
            if not self.open:
                self.tab.y = 0
