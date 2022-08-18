import pygame as pg
from element import Element
from factory import Factory
from node import Node
from helpers import *
import random

LEVEL_HEIGHT = 100
SPACE_BETWEEN_LEVELS = 200
SIZE_OF_MACHINE = 80
SPACE_BETWEEN_MACHINES = 100

COLORS = [(230, 25, 75), (60, 180, 75), (67, 99, 216), (145, 30, 180), (70, 240, 240), (240, 50, 230), (250, 190, 190), (0, 128, 128), (230, 190, 255), (154, 99, 36), (128, 0, 0), (255, 255, 195), (128, 128, 0), (255, 216, 177), (0, 0, 117), (128, 128, 128), (0, 0, 0)]


class Graph(Element):
    def __init__(self, surf, font):
        super().__init__("graph")
        self.factory = None
        self.nodes = []
        self.surf = surf
        self.font = font
        self.drag = False
        self.mouse_pos = 0
        self.x_offset = 0
        self.opt = 1
        self.name = ""

    def update_opt(self, opt):
        self.opt = opt
        if self.factory is not None:
            self.update_list(self.name)

    def update_list(self, name, quantity=0):
        self.name = name
        self.factory = Factory.create_factory(name, quantity=quantity, opt=self.opt)
        self.nodes = []
        self.x_offset = 0
        self.create_factory()

    def create_factory(self):
        factory_levels = self.factory.get_factory()

        cur_y = SPACE_BETWEEN_LEVELS
        for level_ind in range(len(factory_levels)):
            level = factory_levels[level_ind]
            level_width = sum([factory.get_width() * (SIZE_OF_MACHINE + SPACE_BETWEEN_MACHINES) for factory in level])
            cur_x = self.surf.get_width() / 2 - level_width / 2
            for factory in level:
                for machine in factory.head:
                    self.nodes.append(Node(self.surf, machine, cur_y, cur_x, SIZE_OF_MACHINE, self.font, level_ind))
                    cur_x += SIZE_OF_MACHINE + SPACE_BETWEEN_MACHINES
            cur_y += SPACE_BETWEEN_LEVELS + SIZE_OF_MACHINE

    def draw(self):
        new_mouse_pos = pg.mouse.get_pos()
        if self.drag:
            self.x_offset += new_mouse_pos[0] - self.mouse_pos[0]
            for node in self.nodes:
                node.rect.x += new_mouse_pos[0] - self.mouse_pos[0]
                node.rect.y += new_mouse_pos[1] - self.mouse_pos[1]
        self.mouse_pos = new_mouse_pos

        levels = max([node.level + 1 for node in self.nodes] + [0])
        tiered_nodes = [[] for _ in range(levels)]

        for node in self.nodes:
            tiered_nodes[node.level].append(node)

        level_material_dict = {}
        dist_between_dict = {}
        mats_outside = set()

        selected_node = list(filter(lambda n: n.selected, self.nodes))
        if selected_node:
            Element.element_dict["node_info"].update_node(selected_node[0])
            Element.element_dict["node_info"].shown = True
            to_color = list(filter(lambda n: any([prod in map(lambda x: x[0], n.machine.inputs) for prod in map(lambda x: x[0], selected_node[0].machine.product)]), self.nodes))
            to_color += list(filter(lambda n: any([inp in map(lambda x: x[0], n.machine.product) for inp in map(lambda x: x[0], selected_node[0].machine.inputs)]), self.nodes))
            to_color.append(selected_node[0])
        else:
            Element.element_dict["node_info"].shown = False
            to_color = self.nodes

        for level in range(levels-1):
            materials = set()
            for node in tiered_nodes[level]:
                for inp in node.machine.inputs:
                    materials.add(inp[0])
            for node in tiered_nodes[level + 1]:
                for prod in node.machine.product:
                    materials.add(prod[0])
            num_materials = len(materials)
            dist_between_lines = (SPACE_BETWEEN_LEVELS - 100) / num_materials if num_materials != 0 else 1
            materials = list(materials)
            level_material_dict[level] = materials
            dist_between_dict[level] = dist_between_lines

            for node_ind in range(len(tiered_nodes[level + 1])):
                node = tiered_nodes[level + 1][node_ind]
                colors = []
                for prod_ind in range(len(node.machine.product)):
                    prod = node.machine.product[prod_ind]
                    start_x = node.rect.x + ((node.rect.width / (len(node.machine.product) + 1)) * (prod_ind + 1))
                    line_height = node.rect.y - 60 - dist_between_lines * materials.index(prod[0])
                    color = COLORS[materials.index(prod[0])] if node in to_color else (100, 100, 100)
                    pg.draw.line(self.surf, color, (start_x, node.rect.y), (start_x, line_height), width=3)
                    dest_nodes = list(filter(lambda x: x.level <= level and prod[0] in [p[0] for p in x.machine.inputs] and isinstance(get_best_energy_recipe(prod[0]), list), self.nodes))
                    if dest_nodes:
                        for dest_node in dest_nodes:

                            dest_x = dest_node.rect.x + ([p[0] for p in dest_node.machine.inputs].index(
                                prod[0]) + 1) * SIZE_OF_MACHINE / (len(dest_node.machine.inputs) + 1) - 5
                            if dest_node.level == level:

                                pg.draw.line(self.surf, color, (start_x, line_height), (dest_x, line_height), width=3)
                                pg.draw.line(self.surf, color, (dest_x, line_height), (dest_x, dest_node.rect.y + SIZE_OF_MACHINE + 40), width=3)
                            else:
                                mats_outside.add(prod[0])
                                factory_levels = self.factory.get_factory()
                                width_above = max([sum([factory.get_width() * (SIZE_OF_MACHINE + (SPACE_BETWEEN_MACHINES - 1)) for factory in l]) for l in factory_levels[dest_node.level+1:level+1]])
                                dest_x1 = (self.surf.get_width() / 2 + width_above / 2 + 10 + (10 * (len(mats_outside) - 1))) + self.x_offset
                                height_of_prev = dest_node.rect.y + SIZE_OF_MACHINE + SPACE_BETWEEN_LEVELS
                                dest_y = height_of_prev - 60 - dist_between_dict[dest_node.level] * level_material_dict[dest_node.level].index(prod[0])
                                pg.draw.line(self.surf, color, (start_x, line_height), (dest_x1, line_height), width=3)
                                pg.draw.line(self.surf, color, (dest_x1, line_height), (dest_x1, dest_y), width=3)
                                pg.draw.line(self.surf, color, (dest_x1, dest_y), (dest_x, dest_y), width=3)
                                pg.draw.line(self.surf, color, (dest_x, dest_y), (dest_x, dest_node.rect.y + SIZE_OF_MACHINE + 40), width=3)
                    else:
                        prod_text = self.font.render(prod[0] + " x " + str(prod[1]), color, size=7)
                        mats_outside.add(prod[0])
                        factory_levels = self.factory.get_factory()
                        width = max([sum([factory.get_width() * (SIZE_OF_MACHINE + (SPACE_BETWEEN_MACHINES - 1)) for factory in l]) for l in factory_levels])
                        dest_x1 = (self.surf.get_width() / 2 + width / 2 + 10 + (
                                    10 * (len(mats_outside) - 1))) + self.x_offset
                        pg.draw.line(self.surf, color, (start_x, line_height), (dest_x1, line_height), width=3)
                        self.surf.blit(prod_text[0], (dest_x1 + 20, line_height))

                    colors.append(color)
                node.colors = colors

            for node in tiered_nodes[0]:
                des_x = node.rect.x + node.rect.width / 2
                pg.draw.line(self.surf, (0, 0, 0) if node in to_color else (100, 100, 100), (des_x, node.rect.y), (des_x, node.rect.y - 50), width=3)
        materials = list(set([inp[0] for node in tiered_nodes[-1] for inp in node.machine.inputs])) if len(tiered_nodes) else None
        for level in range(levels):
            for node in tiered_nodes[level]:
                raw_inputs = filter(lambda inp: not isinstance(get_best_material_recipe(inp[0]), list), node.machine.inputs)
                for inp in raw_inputs:
                    factory_levels = self.factory.get_factory()
                    start_x = node.rect.x + ([p[0] for p in node.machine.inputs].index(
                        inp[0]) + 1) * SIZE_OF_MACHINE / (len(node.machine.inputs) + 1) - 5
                    height_of_prev = node.rect.y + SIZE_OF_MACHINE + SPACE_BETWEEN_LEVELS
                    width = max([sum([factory.get_width() * (SIZE_OF_MACHINE + (SPACE_BETWEEN_MACHINES - 1)) for factory in l]) for l in factory_levels[level:level+2]])
                    if level != levels - 1:
                        dest_y = height_of_prev - 60 - dist_between_dict[level] * level_material_dict[level].index(inp[0])
                        dest_x = self.surf.get_width() / 2 - width / 2 - 50 + self.x_offset
                        color = COLORS[level_material_dict[level].index(inp[0])] if node in to_color else (100, 100, 100)
                    else:
                        dest_y = node.rect.y + SIZE_OF_MACHINE + 40 + 20 * (materials.index(inp[0]) + 1)
                        dest_x = self.surf.get_width() / 2 - width / 2 - 50 - 30 * materials.index(
                            inp[0]) + self.x_offset
                        color = COLORS[materials.index(inp[0])]
                    nodes_with_inp = filter(lambda x: inp[0] in [i[0] for i in x.machine.inputs], tiered_nodes[level])
                    total_amt = 0
                    for n in nodes_with_inp:
                        for i in n.machine.inputs:
                            if i[0] == inp[0]:
                                total_amt += i[1] * n.machine.clock_speed / 100
                                break
                    total_amt = round(total_amt, 2)
                    input_text = self.font.render(f"{inp[0]} x {total_amt}", color, size=7)
                    pg.draw.line(self.surf, color, (start_x, node.rect.y + SIZE_OF_MACHINE + 40), (start_x, dest_y), width=3)
                    pg.draw.line(self.surf, color, (start_x, dest_y), (dest_x, dest_y), width=3)
                    self.surf.blit(input_text[0], (dest_x - input_text[1].width, dest_y))

            for node in self.nodes:
                if node not in to_color:
                    node.gray = True
                else:
                    node.gray = False
                node.draw()

    def event(self, event):
        nodes_pressed = any([node.event(event) for node in self.nodes])
        if event.type == pg.MOUSEBUTTONDOWN and not nodes_pressed:
            self.drag = True
        if event.type == pg.MOUSEBUTTONUP:
            self.drag = False



