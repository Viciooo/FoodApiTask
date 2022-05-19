from src.main.api.food_search import find_food
from src.main.utils.html_generator import generate_html_document

if __name__ == "__main__":
    included = ['tomatoes', 'eggs', 'pasta']
    excluded = ['plums']
    generate_html_document(included, find_food(included, excluded))
