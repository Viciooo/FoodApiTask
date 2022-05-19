import string
from typing import List
from src.main.classes.meal import Meal
from src.main.utils.normalizer import prepare_html_name
from src.main.utils.translation import translate_to_polish


def gen_html_head():
    return """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    table, th, td {
    border: 1px solid black;
    border-collapse: collapse;
    padding: 1rem;
    font-size: 1.5rem;
    }
    </style>
    </head>
    <body>
    """


def gen_table_with_meal(meal: Meal):
    return f"""
        <table>
        <tr>
        <th>Name in english</th>
        <th>Name in polish</th>
        <th>Picture</th>
        <th>Carbs</th>
        <th>Proteins</th>
        <th>Calories</th>
        </tr>
        <tr>
        <td>{meal.name}</td>
        <td>{translate_to_polish(meal.name)}</td>
        <td>{meal.picture}</td>
        <td>{meal.carbs['amount']} {meal.carbs['unit']}</td>
        <td>{meal.proteins['amount']} {meal.proteins['unit']}</td>
        <td>{meal.calories['amount']} {meal.calories['unit']}</td>
        </tr>
        </table>
        <br><br>
        """


def gen_table_with_ingredients(missing_ingredients: List, present_ingredients: List):
    start = f"""
        <table>
        <tr>
        <th>Ingredient name</th>
        <th>Is missing?</th>
        </tr>"""
    end = """    
        </table>
        <br><br>
        """
    for ingredient in missing_ingredients:
        start += f"""
        <tr>
        <td>{ingredient[0]}</td>
        <td>{True}</td>
        </tr>
        """
    for ingredient in present_ingredients:
        start += f"""
        <tr>
        <td>{ingredient[0]}</td>
        <td>{False}</td>
        </tr>
        """
    start += end
    return start


def gen_html_sep():
    return """<br><hr><br>"""


def gen_html_end():
    return """
    </body>
    </html>
    """


def gen_html_header(text: string):
    return f"""
    <h1>{text}</h1>
    """


def generate_html_document(included_ingredients: List, meals: List[Meal]):
    file_name = prepare_html_name(included_ingredients)
    HTML_TABLE: string = """
    <table>
    <tr>
    <th>Month</th>
    <th>Savings</th>
    </tr>
    <tr>
    <td>January</td>
    <td>$100</td>
    </tr>
    <tr>
    <td>February</td>
    <td>$80</td>
    </tr>
    </table>
    """

    f = open(file_name, 'w')
    f.write(gen_html_head())
    for meal in meals:
        f.write(gen_html_header(meal.name))
        f.write(gen_table_with_meal(meal))
        f.write(gen_table_with_ingredients(meal.list_of_missing_ingredients, meal.list_of_present_ingredients))
        f.write(gen_html_sep())
    f.write(gen_html_end())
