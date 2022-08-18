from abc import ABC


class Element(ABC):
    element_dict = {}

    def __init__(self, name):
        Element.element_dict[name] = self

    def event(self, event):
        pass

    def draw(self):
        pass
