import pytest
from recipes import Ingredient, Recipe, DietaryRecipe, ShoppingList


def test_ingredient_creation():
    flour = Ingredient("Мука", 500, "г")
    assert flour.name=="Мука"
    assert flour.quantity==500.0
    assert flour.unit=="г"


def test_ingredient_str():
    flour = Ingredient("Мука", 500, "г")
    assert str(flour)=="Мука: 500.0 г"


def test_ingredient_eq_same_name_and_unit():
    flour1 = Ingredient("Мука", 500, "г")
    flour2 = Ingredient("Мука", 200, "г")   
    assert flour1==flour2


def test_ingredient_eq_different_name():
    flour = Ingredient("Мука", 500, "г")
    sugar = Ingredient("Сахар", 500, "г")
    assert flour!=sugar


def test_ingredient_eq_different_unit():
    flour_g = Ingredient("Мука", 500, "г")
    flour_kg = Ingredient("Мука", 1, "кг")
    assert flour_g!=flour_kg


def test_recipe_creation():
    flour = Ingredient("Мука", 500, "г")
    pizza = Recipe("Пицца", [flour])
    assert pizza.title == "Пицца"
    assert pizza.ingredients == [flour]


def test_recipe_add_new_ingredient():
    pizza = Recipe("Пицца", [])
    pizza.add_ingredient(Ingredient("Мука", 500, "г"))
    assert len(pizza.ingredients)==1
    assert pizza.ingredients[0].name=="Мука"


def test_recipe_add_duplicate_ingredient_sums_quantity():
    pizza = Recipe("Пицца", [Ingredient("Мука", 500, "г")])
    pizza.add_ingredient(Ingredient("Мука", 200, "г"))
    assert len(pizza.ingredients)==1            
    assert pizza.ingredients[0].quantity == 700.0  


def test_recipe_scale_returns_new_object():
    original = Recipe("Пицца", [Ingredient("Мука", 500, "г")])
    scaled = original.scale(2)
    assert scaled is not original                        
    assert original.ingredients[0].quantity == 500.0      


def test_recipe_scale_multiplies_quantity():
    pizza = Recipe("Пицца", [
        Ingredient("Мука", 500, "г"),
        Ingredient("Сыр", 100, "г"),
    ])
    scaled = pizza.scale(3)
    assert scaled.ingredients[0].quantity==1500.0
    assert scaled.ingredients[1].quantity==300.0


def test_recipe_scale_invalid_ratio_raises():
    pizza = Recipe("Пицца", [Ingredient("Мука", 500, "г")])
    with pytest.raises(ValueError):
        pizza.scale(0)
    with pytest.raises(ValueError):
        pizza.scale(-1)


def test_recipe_len():
    pizza = Recipe("Пицца", [
        Ingredient("Мука", 500, "г"),
        Ingredient("Сыр", 100, "г"),
        Ingredient("Помидоры", 200, "г"),
    ])
    assert len(pizza)==3


def test_shopping_list_add_recipe():
    pizza = Recipe("Пицца", [Ingredient("Мука", 500, "г")])
    shopping = ShoppingList()
    shopping.add_recipe(pizza, 1)
    assert len(shopping._items) == 1


def test_shopping_list_add_recipe_invalid_portions_raises():
    pizza = Recipe("Пицца", [Ingredient("Мука", 500, "г")])
    shopping = ShoppingList()
    with pytest.raises(ValueError):
        shopping.add_recipe(pizza, 0)
    with pytest.raises(ValueError):
        shopping.add_recipe(pizza, -2)


def test_shopping_list_remove_recipe():
    pizza = Recipe("Пицца", [Ingredient("Мука", 500, "г")])
    pasta = Recipe("Паста", [Ingredient("Бекон", 200, "г")])
    shopping = ShoppingList()
    shopping.add_recipe(pizza, 1)
    shopping.add_recipe(pasta, 1)
    shopping.remove_recipe("Пицца")
    assert len(shopping._items) == 1
    assert shopping._items[0][0].name == "Бекон"


def test_shopping_list_remove_nonexistent_recipe():
    pizza = Recipe("Пицца", [Ingredient("Мука", 500, "г")])
    shopping = ShoppingList()
    shopping.add_recipe(pizza, 1)
    # удаление несуществующего рецепта не должно вызывать ошибку
    shopping.remove_recipe("Несуществующий")
    assert len(shopping._items) == 1


def test_shopping_list_get_list_aggregates_same_ingredients():
    pizza = Recipe("Пицца", [Ingredient("Мука", 500, "г")])
    pasta = Recipe("Паста", [Ingredient("Мука", 300, "г")])
    shopping = ShoppingList()
    shopping.add_recipe(pizza, 1)
    shopping.add_recipe(pasta, 1)
    result = shopping.get_list()
    assert len(result) == 1
    assert result[0].quantity == 800.0


def test_shopping_list_get_list_sorted_by_name():
    recipe = Recipe("Микс", [
        Ingredient("Сыр", 100, "г"),
        Ingredient("Бекон", 200, "г"),
        Ingredient("Мука", 500, "г"),
    ])
    shopping = ShoppingList()
    shopping.add_recipe(recipe, 1)
    result = shopping.get_list()
    names = [ing.name for ing in result]
    assert names == ["Бекон", "Мука", "Сыр"]


def test_shopping_list_add_combines_lists():
    pizza = Recipe("Пицца", [Ingredient("Мука", 500, "г")])
    pasta = Recipe("Паста", [Ingredient("Бекон", 200, "г")])
    list1 = ShoppingList()
    list1.add_recipe(pizza, 1)
    list2 = ShoppingList()
    list2.add_recipe(pasta, 1)
    combined = list1 + list2
    assert len(combined._items)==2


def test_shopping_list_add_does_not_mutate_originals():
    pizza = Recipe("Пицца", [Ingredient("Мука", 500, "г")])
    pasta = Recipe("Паста", [Ingredient("Бекон", 200, "г")])
    list1 = ShoppingList()
    list1.add_recipe(pizza, 1)
    list2 = ShoppingList()
    list2.add_recipe(pasta, 1)
    _ = list1+list2
    assert len(list1._items) == 1
    assert len(list2._items) == 1