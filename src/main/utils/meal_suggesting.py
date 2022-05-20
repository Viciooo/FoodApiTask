import string
from typing import List

from src.main.classes.meal import Meal


def get_amount_in_grams(nutrition: dict):
    return {'µg': float(nutrition['amount']) * (10 ** -6),
            'mg': float(nutrition['amount']) * 10 ** -3,
            'g': float(nutrition['amount'])}[nutrition['unit']]


def get_proteins_to_carbs_ratio(meal: Meal):
    return get_amount_in_grams(meal.proteins) / get_amount_in_grams(meal.carbs)


def get_names_of_best_and_worst_meals(meal_list: List[Meal]):
    best_ratio: float = 0.0
    worst_ratio: float = float("inf")
    best_meal_name: string = ''
    worst_meal_name: string = ''
    for meal in meal_list:
        curr_meal_ratio = get_proteins_to_carbs_ratio(meal)
        if best_ratio < curr_meal_ratio:
            best_ratio = curr_meal_ratio
            best_meal_name = meal.name
        elif worst_ratio > curr_meal_ratio:
            worst_ratio = curr_meal_ratio
            worst_meal_name = meal.name

    return best_meal_name, worst_meal_name
