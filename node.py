import pygame as pg
import math
from element import Element

class Node:
    def __init__(self, surf, machine, top, left, size, font, level, gray=False):
        self.machine = machine
        self.surf = surf
        self.rect = pg.Rect(left, top, size, size)
        self.font = font
        self.level = level
        self.colors = [(0, 0, 0) for _ in self.machine.product]
        self.last_pos = [0, 0]
        self.mouse_pos = [0, 0]
        self.selected = False
        self.drag = False
        self.gray = gray
        self.was_shift = False

    def draw(self):
        new_mouse_pos = pg.mouse.get_pos()
        if self.drag:
            self.rect.x += new_mouse_pos[0] - self.mouse_pos[0]
            self.rect.y += new_mouse_pos[1] - self.mouse_pos[1]
            if pg.key.get_pressed()[pg.K_LSHIFT]:
                self.rect.y = self.last_pos[1]
                self.was_shift = True
            elif self.was_shift:
                self.was_shift = False
                self.rect.y = new_mouse_pos[1] - (self.rect.height/2)
        self.mouse_pos = new_mouse_pos
        name = self.machine.product[0][0]
        name = name if len(name.split()) < 3 else "".join(map(lambda x: x[0].upper(), name.split()))
        name = name + " x " + str(self.machine.product[0][1])
        machine_text = self.font.render(self.machine.name, (0, 0, 0), size=10)
        product_text = self.font.render(name, self.colors[0], size=6)
        clock_text = self.font.render(str(int(math.ceil(self.machine.clock_speed))) + "%", (0, 0, 0), size=10)
        energy_text = self.font.render(str(int(math.ceil(self.machine.energy))) + " MW", (0, 0, 0), size=7)
        pg.draw.rect(self.surf, ((30, 255, 30) if not self.selected else (255, 30, 30)) if not self.gray else (100, 100, 100), self.rect, 0)
        pg.draw.rect(self.surf, (0, 0, 0) if not self.gray else (100, 100, 100), self.rect, 3)
        self.surf.blit(machine_text[0], (self.rect.x - (machine_text[1].width - self.rect.width) / 2, self.rect.y + 90))
        self.surf.blit(product_text[0], (self.rect.x - product_text[1].width + (self.rect.width / 2) - 20, self.rect.y - 45))
        self.surf.blit(clock_text[0], (self.rect.x + (self.rect.width / 2) - (clock_text[1].width / 2), self.rect.y + (self.rect.height / 2) - (clock_text[1].height / 2)))
        self.surf.blit(energy_text[0], (self.rect.x + (self.rect.width / 2) - (energy_text[1].width / 2),
                                       self.rect.y + (self.rect.height / 2) + (clock_text[1].height / 2) + 10))
        if len(self.machine.product) > 1:
            second_name = self.machine.product[1][0]
            second_name = second_name if len(second_name.split()) < 3 else "".join(map(lambda x: x[0].upper(), second_name.split()))
            second_name = f"{second_name}  x {self.machine.product[1][1]}"
            second_product_text = self.font.render(second_name, self.colors[1], size=6)
            self.surf.blit(second_product_text[0], (self.rect.x + (self.rect.width / 2) + 25, self.rect.y - 25))

    def event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            self.last_pos = (self.rect.x, self.rect.y)
            if self.rect.collidepoint(event.pos):
                self.mouse_pos = pg.mouse.get_pos()
                self.drag = True
                return True

        if event.type == pg.MOUSEBUTTONUP:
            if math.sqrt((self.rect.x - self.last_pos[0])**2 + (self.rect.y - self.last_pos[1])**2) < 5 and self.rect.collidepoint(event.pos):
                self.selected = True
            elif self.selected and math.sqrt((self.rect.x - self.last_pos[0])**2 + (self.rect.y - self.last_pos[1])**2) < 5:
                self.selected = False

            self.drag = False
