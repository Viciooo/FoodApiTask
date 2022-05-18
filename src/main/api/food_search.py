import string
from typing import List
import requests
from requests import Response
from src.main.utils.sercrets import FOOD_API_KEY as API_KEY


def list_to_string(l: List):
    result = l[0]
    for i in range(1, len(l)):
        result += ',' + l[i]
    return result


def find_food(included_ingredients: List, excluded_ingredients: List):
    URL: string = 'https://api.spoonacular.com/recipes/complexSearch?apiKey=' + API_KEY
    headers: dict = {'Content-Type': 'application/json'}
    params: dict = {'addRecipeNutrition': True, 'addRecipeInformation': True,
                    'includeIngredients': list_to_string(included_ingredients),
                    'excludeIngredients': list_to_string(excluded_ingredients)}

    resp: Response = requests.get(URL, headers=headers)
    print(resp.status_code)
    print(resp.json())


if __name__ == "__main__":
    included = ['tomatoes', 'eggs', 'pasta']
    excluded = ['plums']
    find_food(included, excluded)
