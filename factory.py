from helpers import *
from machine import Machine


class Factory:
    def __init__(self, head, sub_factories, opt):
        self.materials = {}
        self.head = head
        self.energy = 0
        self.machines = {}
        self.sub_factories = sub_factories
        self.product = (self.head[0].product[0][0], sum([machine.product[0][1] for machine in self.head]))
        self.inputs = list(map(lambda inp: inp[0], self.head[0].inputs))
        self.opt = opt
        self.levels = []
        self.byproducts = {}

    @staticmethod
    def create_factory(item, quantity=0, opt=1):
        """Creates a factory for an item optimized for chosen feature : 0 => energy, 1 => materials, 2 => space"""
        if opt == 0:
            recipe = get_best_energy_recipe(item)
        elif opt == 1:
            recipe = get_best_material_recipe(item)
        else:
            recipe = get_best_space_recipe(item)
        if not isinstance(recipe, list):
            return []

        if quantity == 0:
           quantity = recipe[2][0][1]

        head = []
        sub_factories = []

        while quantity > 0:
            if quantity >= recipe[2][0][1]:
                product = [(prod[0], prod[1]) for prod in recipe[2]]
                head.append(Machine(recipe[1], product, 100.0, recipe[0], recipe[2][0][2]))
                quantity -= recipe[2][0][1]
            else:
                clock_speed = round(quantity / recipe[2][0][1] * 100, 2)
                new_inputs = list(map(lambda x: (x[0], round(x[1] * (quantity / recipe[2][0][1]), 2)), recipe[0]))
                product = [(prod[0], round(prod[1] * clock_speed / 100.0, 2)) for prod in recipe[2]]
                head.append(Machine(recipe[1], product, clock_speed, new_inputs, recipe[2][0][2]))
                break

        consolidated_ingredients = [(recipe[0][ing][0], sum([machine.inputs[ing][1] for machine in head])) for ing in
                                    range(len(recipe[0]))]
        for ing in consolidated_ingredients:
            sub_factories.append(Factory.create_factory(ing[0], ing[1], opt=opt))

        return Factory(head, list(filter(lambda x: x != [], sub_factories)), opt)

    def get_factory(self):
        # maps materials to the level they should be represented at
        if self.levels:
            return self.levels
        level_dictionary = {}

        all_factories = [[self]]

        to_process = []
        lvl = 0
        for factory in all_factories[lvl]:
            to_process.extend(factory.sub_factories)
        lvl += 1
        while to_process:
            all_factories.append(to_process)
            to_process = []
            for factory in all_factories[lvl]:
                to_process.extend(factory.sub_factories)
            lvl += 1

        for level in range(len(all_factories)):
            for factory in all_factories[level]:
                material = factory.product[0]
                level_dictionary[material] = level

        mid_levels = [[] for _ in range(len(all_factories))]
        for level in range(len(all_factories)):
            for factory in all_factories[level]:
                mid_levels[level_dictionary[factory.product[0]]].append(factory)

        final_levels = [[] for _ in range(len(all_factories))]
        for level in range(len(mid_levels)):
            materials_in_level = set([factory.product[0] for factory in mid_levels[level]])
            for material in materials_in_level:
                to_combine = list(filter(lambda x: x.product[0] == material, mid_levels[level]))
                total_output = sum([factory.product[1] for factory in to_combine])
                recipe = get_recipes(material)[self.opt]
                one_output = recipe[2][0][1]
                head = []
                while total_output > 0:
                    if total_output >= one_output:
                        product = [(prod[0], prod[1]) for prod in recipe[2]]
                        head.append(Machine(recipe[1], product, 100.0, recipe[0], recipe[2][0][2]))
                        total_output -= one_output
                    else:
                        new_inputs = list(map(lambda x: (x[0], round(x[1] * (one_output / recipe[2][0][1]), 2)), recipe[0]))
                        clock_speed = round(total_output / recipe[2][0][1] * 100, 2)
                        product = [(prod[0], round(prod[1] * clock_speed / 100.0, 2)) for prod in recipe[2]]
                        head.append(Machine(recipe[1], product, clock_speed, new_inputs, recipe[2][0][2]))
                        break
                final_levels[level].append(Factory(head, [], self.opt))
            final_levels[level].sort(key=lambda x: x.head[0].name)
        self.levels = final_levels
        return final_levels

    def get_energy(self):
        if self.energy == 0:
            self.calculate_energy()
        return self.energy

    def get_materials(self):
        if len(self.materials) == 0:
            self.calculate_materials()
        return self.materials

    def get_machines(self):
        if len(self.machines) == 0:
            self.calculate_machines()
        return self.machines

    def get_byproducts(self):
        if len(self.byproducts) == 0:
            self.calculate_byproducts()
        return self.byproducts

    def calculate_byproducts(self):
        for sub_fact in self.sub_factories:
            for byprod in sub_fact.get_byproducts():
                if byprod not in self.byproducts:
                    self.byproducts[byprod] = 0
                self.byproducts[byprod] += sub_fact.get_byproducts()[byprod]
        for machine in self.head:
            if len(machine.product) > 1:
                if machine.product[1][0] not in self.byproducts:
                    self.byproducts[machine.product[1][0]] = 0
                self.byproducts[machine.product[1][0]] += machine.product[1][1]

    def calculate_energy(self):
        for machine in self.head:
            self.energy += machine.energy * machine.product[0][1]
        for factory in self.sub_factories:
            self.energy += factory.get_energy()
        self.energy = round(self.energy, 3)

    def calculate_materials(self):
        for sub_fact in self.sub_factories:
            for material in sub_fact.get_materials():
                if material not in self.materials:
                    self.materials[material] = 0
                self.materials[material] += sub_fact.get_materials()[material]
        for machine in self.head:
            for inp in machine.inputs:
                if not isinstance(get_recipes(inp[0]), list):
                    if inp[0] not in self.materials:
                        self.materials[inp[0]] = 0
                    self.materials[inp[0]] += round(inp[1], 3)
        for material in self.materials:
            self.materials[material] = round(self.materials[material], 3)

    def calculate_machines(self):
        all_machines = [machine.name for j in self.get_factory() for i in j for machine in i.head]
        machines_set = set(all_machines)
        for machine in machines_set:
            self.machines[machine] = all_machines.count(machine)

    def get_width(self):
        return len(self.head)
