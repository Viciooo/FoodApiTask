import string
from typing import List

import requests
from requests import Response
from src.main.utils.sercrets import FOOD_API_KEY as API_KEY
from src.main.classes.meal import Meal
from src.main.api.dbService import insert_meal, try_fetch_from_db


def list_to_string(l: List):
    result = l[0]
    for i in range(1, len(l)):
        result += ',' + l[i]
    return result


def build_ingredients_list(ingredients: List[dict]):
    result: List[string] = []
    for ingredient in ingredients:
        result.append(ingredient['name'])
    return result


def find_food(included_ingredients: List, excluded_ingredients: List):
    results_of_db_search: List[Meal] = try_fetch_from_db(included_ingredients, excluded_ingredients)
    if len(results_of_db_search) > 0:
        return results_of_db_search
    URL: string = 'https://api.spoonacular.com/recipes/complexSearch?apiKey=' + API_KEY
    headers: dict = {'Content-Type': 'application/json'}
    params: dict = {'addRecipeNutrition': True, 'fillIngredients': True,
                    'includeIngredients': list_to_string(included_ingredients),
                    'excludeIngredients': list_to_string(excluded_ingredients)}

    resp: Response = requests.get(URL, headers=headers, params=params)
    data: dict = resp.json()

    results: dict = data['results']

    meal_list: List[Meal] = []
    for meal in results:
        new_meal = Meal(meal['title'],
                        meal['image'],
                        build_ingredients_list(meal['usedIngredients']),
                        build_ingredients_list(meal['missedIngredients']),
                        {'amount': meal['nutrition']['nutrients'][3]['amount'],
                         'unit': meal['nutrition']['nutrients'][3]['unit']},
                        {'amount': meal['nutrition']['nutrients'][9]['amount'],
                         'unit': meal['nutrition']['nutrients'][9]['unit']},
                        {'amount': meal['nutrition']['nutrients'][0]['amount'],
                         'unit': meal['nutrition']['nutrients'][0]['unit']})
        meal_list.append(new_meal)
        insert_meal(new_meal, included_ingredients, excluded_ingredients)
    return meal_list


if __name__ == "__main__":
    included = ['tomatoes', 'eggs', 'pasta']
    excluded = ['plums']
    meals= find_food(included, excluded)
    for meal in meals:
        print(meal)
