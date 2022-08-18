from element import Element
import pygame as pg


class NodeInfo(Element):
    def __init__(self, surf, font):
        super().__init__("node_info")
        self.surf = surf
        self.font = font
        self.shown = False
        self.node = None

    def update_node(self, node):
        self.node = node

    def draw(self):
        if self.shown:
            machine_name = self.font.render(self.node.machine.name, (0, 0, 0), size=10)
            input_label = self.font.render("Inputs: ", (0, 0, 0), size=10)
            input_texts = [self.font.render(f"{inp[0]} : {inp[1]}/min", (0, 0, 0), size=10) for inp in self.node.machine.inputs]
            output_label = self.font.render("Outputs: ", (0, 0, 0), size=10)
            output_texts = [self.font.render(f"{prod[0]} : {prod[1]}/min", (0, 0, 0), size=10) for prod in self.node.machine.product]

            all_texts = [machine_name, input_label, output_label] + input_texts + output_texts
            max_width = max([text[1].width + 40 for text in all_texts])
            height = sum([text[1].height for text in all_texts]) + 20 * len(all_texts)

            rect = pg.Rect(self.surf.get_width()-max_width-20, -20, max_width + 40, height+60)

            pg.draw.rect(self.surf, (255, 255, 255), rect, border_radius=20)
            pg.draw.rect(self.surf, (0, 0, 0), rect, width=3, border_radius=20)

            cur_y = 20

            self.surf.blit(machine_name[0], (rect.x + 20, cur_y))

            cur_y += 20 + machine_name[1].height

            self.surf.blit(input_label[0], (rect.x + 20, cur_y))

            cur_y += 20 + input_label[1].height

            for text in input_texts:
                self.surf.blit(text[0], (rect.x + 40, cur_y))
                cur_y += 20 + text[1].height

            self.surf.blit(output_label[0], (rect.x + 20, cur_y))

            cur_y += 20 + output_label[1].height

            for text in output_texts:
                self.surf.blit(text[0], (rect.x + 40, cur_y))
                cur_y += 20 + text[1].height

