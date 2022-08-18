import requests
from bs4 import BeautifulSoup

BASE_URL = "https://satisfactory.fandom.com/wiki/"
BASE_MATERIALS = ["Ores"]

recipes_dict = {"Water": 0, "Copper Powder": [[[("Copper Ingot", 300.0)], "Constructor", [("Copper Powder", 50.0, 4.8)]], [[("Copper Ingot", 300.0)], "Constructor", [("Copper Powder", 50.0, 4.8)]], [[("Copper Ingot", 300.0)], "Constructor", [("Copper Powder", 50.0, 4.8)]]]}

banned_ingredients = ["Petroleum Coke", "Polymer Resin", "Heavy Oil Residue"]
special_energy = {"Encased Plutonium Cell": 375.0, "Nuclear Pasta": 1000.0, "Plutonium Pellet": 500}


def load_from_file():
    with open("recipes.txt") as f:
        for line in f.readlines():
            split_line = line.split(":")
            recipes_dict[split_line[0]] = eval(split_line[1])


def save_to_file():
    with open("recipes.txt", "w") as f:
        for key in recipes_dict:
            f.write(f"{key}: {recipes_dict[key]}\n")


def save_to_file_append(item):
    with open("recipes.txt", "a+") as f:
        f.write(f"{item}: {recipes_dict[item]}\n")


def get_best_energy_recipe(item):
    """Returns the best recipe optimized for energy for a given item"""
    if item in recipes_dict:
        return recipes_dict[item] if not isinstance(recipes_dict[item], list) else recipes_dict[item][0]
    else:
        res = get_recipes(item)
        return res if not isinstance(res, list) else res[0]


def get_best_material_recipe(item):
    """Returns best recipe optimized for raw materials for a given item"""
    if item in recipes_dict:
        return recipes_dict[item] if not isinstance(recipes_dict[item], list) else recipes_dict[item][1]
    else:
        res = get_recipes(item)
        return res if not isinstance(res, list) else res[1]


def get_best_space_recipe(item):
    """Returns the best recipe optimized for the number of machines for a given item"""
    if item in recipes_dict:
        return recipes_dict[item] if not isinstance(recipes_dict[item], list) else recipes_dict[item][2]
    else:
        res = get_recipes(item)
        return res if not isinstance(res, list) else res[2]


def get_recipes(item):
    """Returns a list of recipes for a given item"""
    global recipes_dict

    if item in recipes_dict:
        return recipes_dict[item]
    recipes = []

    print(item)

    url = BASE_URL + "_".join(item.split())
    response = requests.get(url)
    soup = BeautifulSoup(
        response.text,
        "html.parser",
    )

    categories = soup.find(id="catlinks")

    if "Crafting" not in soup.text:
        Exception(f"WAS NOT ABLE TO FIND RECIPES FOR {item}")

    if "Ores" in categories.text or item in ["Water", "Crude Oil", "Nitrogen Gas"]:
        value = 1 if item != "Water" else 0
        recipes_dict[item] = value
        save_to_file_append(item)
        return value

    recipe_table = soup.find(class_="wikitable")
    all_recipes = recipe_table.findAll("tr")[1:]

    for recipe_ind in range(len(all_recipes)):
        recipe = all_recipes[recipe_ind]
        firstRow = recipe.get("class") == ["firstRow"]
        rows = recipe.findAll("td")
        if firstRow and rows[0].contents[0] != item:
            Exception("The desired item and recipe did not match!")

        ingredients = []
        ing_ind = 1 if firstRow else 0
        col = rows[ing_ind]
        while "sec" not in col.text:
            col_lines = col.findAll("div", recursive=False)
            if len(col_lines) == 0:
                ing_ind += 1
                break
            link = col_lines[0].find("a")
            amount_span = col_lines[1].contents[0]
            amount = float(amount_span.contents[0].split()[0])

            if firstRow:
                ingredients.append((link["title"], amount))
            else:
                recipes[-1][0].append((link["title"], amount))

            ing_ind += 1
            if ing_ind == len(rows):
                break
            col = rows[ing_ind]
        if any([ing[0] in banned_ingredients for ing in ingredients]):
            if not firstRow:
                recipes = recipes[:-1]
            continue

        if not firstRow and any([item == ing[0] for ing in recipes[-1][0]]):
            recipes = recipes[:-1]

        if not firstRow: continue

        machine_span = rows[ing_ind].contents[0]
        machine = machine_span.find("a")["title"]

        product = []

        for prod_ind in range(ing_ind + 1, len(rows) - 1):
            col_lines = rows[prod_ind].findAll("div", recursive=False)
            link = col_lines[0].find("a")
            amount_span = col_lines[1].contents[0]
            amount = float(amount_span.contents[0].split()[0])

            if len(col_lines) < 3 and item in special_energy:
                energy = special_energy[item]
            else:
                energy_span = col_lines[2].contents[0]
                energy = float(energy_span.contents[0].split()[0])

            product.append((link["title"], amount, energy))

        if all([i in [ingredients[0][0], product[0][0]] for i in ["Plastic", "Rubber"]]) or \
           any(["Packaged" in ing[0] or item == ing[0] for ing in ingredients]):
            continue
        recipes.append([ingredients, machine, product])
    best_energy = min(recipes, key=lambda x: sum([x[2][0][2] + get_energy_value(get_best_energy_recipe(ing[0]), [item])*(ing[1]/x[2][0][1]) for ing in x[0]]))
    best_material = min(recipes, key=lambda x: sum([get_material_value(get_best_material_recipe(ing[0]), [item])*(ing[1]/x[2][0][1]) for ing in x[0]]))
    best_space = min(recipes, key=lambda x: sum([get_space_value(get_best_space_recipe(ing[0]), [item]) for ing in x[0]]))
    recipes_dict[item] = [best_energy, best_material, best_space]
    save_to_file_append(item)
    return [best_energy, best_material, best_space]


def get_energy_value(recipe, acc):
    """Returns energy required to produce 1 item in the given recipe"""
    if not isinstance(recipe, list):
        return 0
    return recipe[2][0][2] + sum([get_energy_value(get_best_energy_recipe(ing[0]), acc + [recipe[2][0][0]])*(ing[1]/recipe[2][0][1]) for ing in recipe[0] if ing[0] not in acc])


def get_material_value(recipe, acc):
    """Returns the number of raw materials required to produce 1 item in the given recipe"""
    if not isinstance(recipe, list):
        return recipe
    return sum([get_material_value(get_best_material_recipe(ing[0]), acc + [recipe[2][0][0]])*(ing[1]/recipe[2][0][1]) for ing in recipe[0] if ing[0] not in acc])


def get_space_value(recipe, acc):
    """Returns the number of machines required to produce 1 item in the given recipe"""
    if not isinstance(recipe, list):
        return 0
    return (1 / recipe[2][0][1]) + sum([get_space_value(get_best_space_recipe(ing[0]), acc + [recipe[2][0][0]]) * (ing[1]/recipe[2][0][1]) for ing in recipe[0] if ing[0] not in acc])