import string
from typing import List
from src.main.classes.meal import Meal
from src.main.utils.normalizer import prepare_html_name
from src.main.utils.translation import translate_to_polish


class HTML_builder:
    @classmethod
    def build(cls, meals: List[Meal]):
        html_page: string = ''
        html_page += cls.__gen_html_head()
        for meal in meals:
            html_page += cls.__gen_html_header(meal.name)
            html_page += cls.__gen_table_with_meal(meal)
            html_page += cls.__gen_table_with_ingredients(meal.list_of_missing_ingredients,
                                                          meal.list_of_present_ingredients)
            html_page += cls.__gen_html_sep()
        html_page += cls.__gen_html_end()
        return html_page

    @classmethod
    def __gen_html_head(cls):
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

    @classmethod
    def __gen_table_with_meal(cls, meal: Meal):
        return f"""
            <table>
            <tr>
            <th>Name</th>
            <th>Nazwa</th>
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

    @classmethod
    def __gen_table_with_ingredients(cls, missing_ingredients: List, present_ingredients: List):
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

    @classmethod
    def __gen_html_sep(cls):
        return """<br><hr><br>"""

    @classmethod
    def __gen_html_end(cls):
        return """
        </body>
        </html>
        """

    @classmethod
    def __gen_html_header(cls, text: string):
        return f"""
        <h1>{text}</h1>
        """


def generate_html_document(included_ingredients: List, meals: List[Meal]):
    file_name = prepare_html_name(included_ingredients)
    with open(file_name, 'w') as f:
        f.write(HTML_builder.build(meals))
