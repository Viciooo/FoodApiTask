from src.main.api.dbService import check_if_search_id_in_db, delete_from_db_meals_from_search_with_search_id
from src.main.api.food_search import find_food
from src.main.utils.html_generator import generate_html_document

if __name__ == "__main__":
    generate_html_document(['tomatoes', 'eggs', 'pasta'], find_food(['tomatoes', 'eggs', 'pasta'], ['plums']))
    generate_html_document([], find_food([], []))