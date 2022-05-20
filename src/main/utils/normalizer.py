from pathlib import Path
from typing import List


def normalize_list(list_to_normalize):
    for i in range(len(list_to_normalize)):
        for c in list_to_normalize[i]:
            if not c.isalnum():
                list_to_normalize[i] = list_to_normalize[i].translate({ord(c): None})

        list_to_normalize[i] = list_to_normalize[i].lower()

    return list_to_normalize


def prepare_html_name(included_ingredients: List):
    included_ingredients = normalize_list(included_ingredients)

    if len(included_ingredients) > 0:
        result = included_ingredients[0]
        for i in range(1, len(included_ingredients)):
            result += '_' + included_ingredients[i]
    else:
        result = 'no_ingredients'

    result += '.html'
    dir_path = str(Path(__file__).parent.parent.parent.parent.resolve()) + r'\docs\examples'+'\\'

    return dir_path+result

