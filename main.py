import pygame as pg
from pygame import freetype
from search_bar import SearchBar
from graph import Graph
from element import Element
from opt_selector import OptSelector
from node_info import NodeInfo
from receipt import Receipt
from update_quantity import UpdateQuantity
from helpers import *

load_from_file()

width, height = (1800, 1000)
screen = pg.display.set_mode((width, height))


freetype.init(resolution=150)

font = freetype.SysFont(freetype.get_default_font(), 25)

done = False

Graph(screen, font)
SearchBar(screen, font)
OptSelector(screen, font)
Receipt(screen, font)
NodeInfo(screen, font)
UpdateQuantity(screen, font)

clock = pg.time.Clock()

while not done:
    screen.fill((255, 255, 255))
    for event in pg.event.get():
        for item in Element.element_dict.values():
            item.event(event)
        if event.type == pg.QUIT:
            done = True

    for item in Element.element_dict.values():
        item.draw()

    pg.display.flip()
    clock.tick(60)


