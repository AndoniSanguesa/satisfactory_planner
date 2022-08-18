class Machine:
    def __init__(self, name, product, clock_speed, inputs, energy):
        self.name = name
        self.product = product
        self.clock_speed = clock_speed
        self.inputs = inputs
        self.energy = round(energy * (clock_speed / 100)**0.6, 3)

    def __str__(self):
        return f"[Type: {self.name}, Product: {self.product}, Clock Speed: {self.clock_speed}, Energy/Item: {self.energy}]"

    def __repr__(self):
        return f"[Type: {self.name}, Product: {self.product}, Clock Speed: {self.clock_speed}, Energy/Item: {self.energy}]"