import sqlite3
import string
from typing import List

from src.main.classes.meal import Meal

conn = sqlite3.connect('mydb.db')
cursor = conn.cursor()


def generate_search_id(included_ingredients: List, excluded_ingredients: List):
    included_ingredients.sort()
    excluded_ingredients.sort()
    if len(included_ingredients) > 0:
        result = included_ingredients[0]
        for i in range(1, len(included_ingredients)):
            result += '_' + included_ingredients[i]
        for i in excluded_ingredients:
            result += '_n_' + i
    elif len(excluded_ingredients) > 0:
        result = 'n_' + excluded_ingredients[0]
        for i in range(1, len(excluded_ingredients)):
            result += '_n_' + excluded_ingredients[i]
    else:
        result = ''
    return result


def try_fetch_from_db(included_ingredients: List, excluded_ingredients: List):
    search_id: string = generate_search_id(included_ingredients, excluded_ingredients)
    meal_list: List[Meal] = []
    with conn:
        cursor.execute("""SELECT 
        present_ingredients_list_id,
        missing_ingredients_list_id,
        name,
        picture,
        carbs,
        carbs_unit,
        proteins,
        proteins_unit,
        calories,
        calories_unit
        FROM MEAL WHERE search_id = ?""",
                       (search_id,))

        results = cursor.fetchall()
        for meal_info in results:
            cursor.execute("""SELECT name from ingredient where present_ingredients_list_id = ?""",
                           (meal_info[0],))
            present_ingredients = cursor.fetchall()

            cursor.execute("""SELECT name from ingredient where missing_ingredients_list_id = ?""",
                           (meal_info[1],))
            missing_ingredients = cursor.fetchall()
            meal_list.append(Meal(meal_info[2],
                                  meal_info[3],
                                  present_ingredients,
                                  missing_ingredients,
                                  {'amount': meal_info[4], 'unit': meal_info[5]},
                                  {'amount': meal_info[6], 'unit': meal_info[7]},
                                  {'amount': meal_info[8], 'unit': meal_info[9]}
                                  ))
    return meal_list


def insert_meal(meal: Meal, included_ingredients: List, excluded_ingredients: List):
    with conn:
        cursor.execute('INSERT INTO MISSING_INGREDIENTS_LIST (meal_name) values (?)', (meal.name,))
        missing_ingredients_list_id: int = cursor.lastrowid

        cursor.execute('INSERT INTO PRESENT_INGREDIENTS_LIST (meal_name) values (?)', (meal.name,))
        present_ingredients_list_id: int = cursor.lastrowid

        cursor.execute(
            """INSERT INTO MEAL (search_id,present_ingredients_list_id,missing_ingredients_list_id,name,picture,carbs,carbs_unit,proteins,proteins_unit,calories,calories_unit)
             values (?,?,?,?,?,?,?,?,?,?,?)""",
            (generate_search_id(included_ingredients, excluded_ingredients)
             , present_ingredients_list_id,
             missing_ingredients_list_id,
             meal.name,
             meal.picture,
             meal.carbs['amount'],
             meal.carbs['unit'],
             meal.proteins['amount'],
             meal.proteins['unit'],
             meal.calories['amount'],
             meal.calories['unit']))

        for ingredient_name in meal.list_of_missing_ingredients:
            cursor.execute(
                'INSERT INTO INGREDIENT (present_ingredients_list_id,missing_ingredients_list_id,name) values (?,?,?)',
                (None, missing_ingredients_list_id, ingredient_name))

        for ingredient_name in meal.list_of_present_ingredients:
            cursor.execute(
                'INSERT INTO INGREDIENT (present_ingredients_list_id,missing_ingredients_list_id,name) values (?,?,?)',
                (present_ingredients_list_id, None, ingredient_name))
