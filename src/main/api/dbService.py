import sqlite3
import string
from typing import List
from pathlib import Path

from src.main.classes.meal import Meal


def open_db():
    db_path: string = str(Path(__file__).parent.resolve()) + r'\mydb.db'
    conn_ = sqlite3.connect(db_path)
    cursor_ = conn_.cursor()
    cursor_.execute("PRAGMA foreign_keys=ON");
    return conn_, cursor_


conn, cursor = open_db()


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
        meal_id,
        name,
        picture,
        carbs,
        carbs_unit,
        proteins,
        proteins_unit,
        calories,
        calories_unit
        FROM MEALS WHERE search_id = ?""",
                       (search_id,))

        results = cursor.fetchall()
        for meal_info in results:
            meal_id: int = meal_info[0]

            cursor.execute("""SELECT name from present_ingredients where meal_id = ?""",
                           (meal_id,))
            present_ingredients = cursor.fetchall()

            cursor.execute("""SELECT name from missing_ingredients where meal_id = ?""",
                           (meal_id,))
            missing_ingredients = cursor.fetchall()
            meal_list.append(Meal(meal_info[1],
                                  meal_info[2],
                                  present_ingredients,
                                  missing_ingredients,
                                  {'amount': meal_info[3], 'unit': meal_info[4]},
                                  {'amount': meal_info[5], 'unit': meal_info[6]},
                                  {'amount': meal_info[7], 'unit': meal_info[8]}
                                  ))
    return meal_list


def insert_meal(meal: Meal, included_ingredients: List, excluded_ingredients: List):
    with conn:
        cursor.execute(
            """INSERT INTO MEALS (search_id,name,picture,carbs,carbs_unit,proteins,proteins_unit,calories,calories_unit)
             values (?,?,?,?,?,?,?,?,?)""",
            (generate_search_id(included_ingredients, excluded_ingredients),
             meal.name,
             meal.picture,
             meal.carbs['amount'],
             meal.carbs['unit'],
             meal.proteins['amount'],
             meal.proteins['unit'],
             meal.calories['amount'],
             meal.calories['unit']))
        meal_id: int = cursor.lastrowid

        for ingredient_name in meal.list_of_missing_ingredients:
            cursor.execute(
                'INSERT INTO MISSING_INGREDIENTS (meal_id,name) values (?,?)',
                (meal_id, ingredient_name))

        for ingredient_name in meal.list_of_present_ingredients:
            cursor.execute(
                'INSERT INTO PRESENT_INGREDIENTS (meal_id,name) values (?,?)',
                (meal_id, ingredient_name))


def get_meals_count():
    with conn:
        cursor.execute("""SELECT COUNT(*) FROM MEALS;""")
        result: int = cursor.fetchone()
    return result


def check_if_search_id_in_db(search_id: string):
    with conn:
        cursor.execute("""SELECT search_id FROM MEALS where search_id=?;""", (search_id,))
        result: string = cursor.fetchone()
    return True if result is not None else False


def delete_from_db_meals_from_search_with_search_id(search_id: string):
    with conn:
        cursor.execute("""DELETE FROM MEALS where search_id=?;""", (search_id,))



