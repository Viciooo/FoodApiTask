class Meal:
    def __init__(self, name, picture, list_of_present_ingredients, list_of_missing_ingredients, carbs, proteins,
                 calories):
        self.name = name
        self.picture = picture
        self.list_of_present_ingredients = list_of_present_ingredients
        self.list_of_missing_ingredients = list_of_missing_ingredients
        self.carbs = carbs
        self.proteins = proteins
        self.calories = calories

    def __str__(self):
        return f'Name: {self.name}\n' \
               f'Picture: {self.picture}\n' \
               f'Carbs: {self.carbs}\n' \
               f'Proteins: {self.proteins}\n' \
               f'Calories: {self.calories}\n' \
               f'Used ingredients: {self.list_of_present_ingredients}\n' \
               f'Missing ingredients: {self.list_of_missing_ingredients}\n'
