from typing import List

from tabulate import tabulate

from src.main.classes.meal import Meal
from src.main.utils.normalizer import prepare_html_name


def generate_html_document(included_ingredients:List,meals:List[Meal]):
    file_name = prepare_html_name(included_ingredients)
    f = open(file_name,'w')
    # table = []
    # for meal in meals:

    table = [['one', 'two', 'three'], ['four', 'five', 'six'], ['seven', 'eight', 'nine']]
    f.write(tabulate(table, tablefmt='html'))

included = ['tomatoes', 'eggs', 'pasta']

generate_html_document(included,[])



# print(tabulate(table, tablefmt='html'))