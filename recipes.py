class Ingredient:
    def __init__(self, name, quantity, unit):
        self.name = name
        self.quantity = quantity
        self.unit = unit

    @property
    def quantity(self):
        return self._quantity
    
    @quantity.setter
    def quantity(self, value):
        if value <= 0:
            raise ValueError("Количество должно быть положительным")
        self._quantity=float(value)

    def __str__(self):
        return f"{self.name}: {self.quantity} {self.unit}"
    
    def __repr__(self):
        return f"Ingredient({self.name!r}, {self.quantity}, {self.unit!r})"
    
    def __eq__(self, other):
        if not isinstance(other,Ingredient):
            return NotImplemented
        return self.name==other.name and self.unit==other.unit


class Recipe:
    def __init__(self, title, ingredients):
        self.title=title
        self.ingredients=ingredients

    def add_ingredient(self, ingredient):
        for existing in self.ingredients:
            if existing==ingredient:
                existing.quantity = existing.quantity+ingredient.quantity
                return
        self.ingredients.append(ingredient)

    @staticmethod
    def is_valid_ratio(ratio):
        return isinstance(ratio, (int, float)) and ratio > 0
    
    def scale(self, ratio):
        if not self.is_valid_ratio(ratio):
            raise ValueError("Коэффициент должен быть положительным числом")
        new_ingredients=[]
        for ing in self.ingredients:
            new_ing=Ingredient(ing.name, ing.quantity * ratio, ing.unit)
            new_ingredients.append(new_ing)
        return Recipe(self.title, new_ingredients)
    
    def __len__(self):
        return len(self.ingredients)
    def __str__(self):
        lines = [f"Рецепт: {self.title}"]
        for ing in self.ingredients:
            lines.append(f"  - {ing}")
        return "\n".join(lines)
    

class DietaryRecipe(Recipe):
    def __init__(self, title, diet_type, ingredients=None):
        if ingredients is None:
            ingredients=[]
        super().__init__(title, ingredients)
        self.diet_type=diet_type

    def scale(self, ratio):
        scaled = super().scale(ratio)
        return DietaryRecipe(scaled.title, self.diet_type, scaled.ingredients)
    
    def __str__(self):
        return f"[{self.diet_type}] {super().__str__()}"
        

class ShoppingList:
    def __init__(self):
        self._items = []

    def add_recipe(self, recipe, portions):
        if portions <= 0:
            raise ValueError("Количество порций должно быть положительным")
        scaled = recipe.scale(portions)
        for ingredient in scaled.ingredients:
            self._items.append((ingredient, recipe.title))

    def remove_recipe(self, title):
        self._items = [
            (ingredient,recipe_title)
            for ingredient, recipe_title in self._items
            if recipe_title!=title
        ]

    def get_list(self):
        aggregated = {}
        for ingredient, _ in self._items:
            key = (ingredient.name, ingredient.unit)
            if key in aggregated:
                aggregated[key]+=ingredient.quantity
            else:
                aggregated[key]=ingredient.quantity

        result = [
            Ingredient(name, quantity, unit)
            for (name, unit), quantity in aggregated.items()
        ]
        result.sort(key=lambda ing: ing.name)
        return result
    
    def __add__(self, other):
        new_list = ShoppingList()
        new_list._items = self._items+other._items
        return new_list


if __name__ == "__main__":
    pizza = Recipe("Пицца", [Ingredient("Мука", 500, "г")])
    pasta = Recipe("Паста", [Ingredient("Мука", 300, "г")])
    salad = Recipe("Салат", [Ingredient("Огурец", 2, "шт")])

    list1 = ShoppingList()
    list1.add_recipe(pizza, 1)

    list2 = ShoppingList()
    list2.add_recipe(pasta, 1)
    list2.add_recipe(salad, 1)

    combined = list1 + list2

    print("Объединённый список:")
    for ing in combined.get_list():
        print(f"  {ing}")

    print("\nИсходный list1 не изменился:")
    for ing in list1.get_list():
        print(f"  {ing}")

    print("\nИсходный list2 не изменился:")
    for ing in list2.get_list():
        print(f"  {ing}")