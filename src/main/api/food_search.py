import string
from typing import List

import requests
from requests import Response
from src.main.utils.sercrets import FOOD_API_KEY as API_KEY
from src.main.classes.meal import Meal
from src.main.api.dbService import insert_meal, try_fetch_from_db


def list_to_string(list_: List):
    if len(list_) == 0:
        return
    result = list_[0]
    for i in range(1, len(list_)):
        result += ',' + list_[i]
    return result


def build_ingredients_list(ingredients: List[dict]):
    result: List[string] = []
    for ingredient in ingredients:
        result.append(ingredient['name'])
    return result


def get_data_from_api(included_ingredients: List, excluded_ingredients: List):
    URL: string = 'https://api.spoonacular.com/recipes/complexSearch?apiKey=' + API_KEY
    headers: dict = {'Content-Type': 'application/json'}
    included_ingredients_string = list_to_string(included_ingredients)
    excluded_ingredients_string = list_to_string(excluded_ingredients)
    if included_ingredients_string is None:
        if excluded_ingredients_string is None:
            params: dict = {'addRecipeNutrition': True, 'fillIngredients': True,
                            'sort': 'min-missing-ingredients',
                            'number': 5,
                            }
        params: dict = {'addRecipeNutrition': True, 'fillIngredients': True,
                        'sort': 'min-missing-ingredients',
                        'excludeIngredients': excluded_ingredients_string,
                        'number': 5,
                        }
    elif excluded_ingredients_string is None:
        params: dict = {'addRecipeNutrition': True, 'fillIngredients': True,
                        'sort': 'min-missing-ingredients',
                        'includeIngredients': included_ingredients_string,
                        'number': 5,
                        }
    else:
        params: dict = {'addRecipeNutrition': True, 'fillIngredients': True,
                        'includeIngredients': included_ingredients_string,
                        'excludeIngredients': excluded_ingredients_string,
                        'sort': 'min-missing-ingredients',
                        'number': 5,
                        }

    resp: Response = requests.get(URL, headers=headers, params=params)
    data: dict = resp.json()

    return data['results']


def find_food(included_ingredients: List, excluded_ingredients: List):
    results_of_db_search: List[Meal] = try_fetch_from_db(included_ingredients, excluded_ingredients)
    if len(results_of_db_search) > 0:
        return results_of_db_search
    results = get_data_from_api(included_ingredients, excluded_ingredients)
    meal_list: List[Meal] = []
    for m in results:
        new_meal = Meal(m['title'],
                        m['image'],
                        build_ingredients_list(m['usedIngredients']),
                        build_ingredients_list(m['missedIngredients']),
                        {'amount': m['nutrition']['nutrients'][3]['amount'],
                         'unit': m['nutrition']['nutrients'][3]['unit']},
                        {'amount': m['nutrition']['nutrients'][9]['amount'],
                         'unit': m['nutrition']['nutrients'][9]['unit']},
                        {'amount': m['nutrition']['nutrients'][0]['amount'],
                         'unit': m['nutrition']['nutrients'][0]['unit']})
        meal_list.append(new_meal)
        insert_meal(new_meal, included_ingredients, excluded_ingredients)
    return meal_list
