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
        

if __name__ == "__main__":
    vegan_pizza = DietaryRecipe(
        "Пицца Маргарита",
        "веган",
        [Ingredient("Тесто", 300, "г"), Ingredient("Соус", 100, "г")]
    )

    print(vegan_pizza)
    print()

    big = vegan_pizza.scale(2)
    print(big)
    print()

    # Проверяем, что scale вернул именно DietaryRecipe
    print(type(big).__name__)        # DietaryRecipe
    print(big.diet_type)             # веган