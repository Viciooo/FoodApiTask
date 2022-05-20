import unittest
from typing import List

from src.main.api.dbService import get_meals_count, check_if_search_id_in_db, \
    delete_from_db_meals_from_search_with_search_id, generate_search_id
from src.main.api.food_search import get_data_from_api, find_food
from src.main.classes.meal import Meal


class FoodSearchTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        find_food([], [])

    def test_get_data_from_api_should_return_data(self):
        result: dict = get_data_from_api([], [])

        self.assertTrue(result is not None)
        self.assertTrue(len(result) <= 5)

    def test_find_food_should_fetch_from_db(self):
        result_1: List[Meal] = find_food([], [])
        self.assertTrue(result_1 is not None)
        meals_count_1: int = get_meals_count()
        result_2: List[Meal] = find_food([], [])
        meals_count_2: int = get_meals_count()
        self.assertTrue(result_1 == result_2)
        self.assertEqual(meals_count_1, meals_count_2)

    def test_find_food_should_insert_to_db(self):
        if check_if_search_id_in_db(''):
            delete_from_db_meals_from_search_with_search_id('')
        find_food([], [])
        self.assertTrue(check_if_search_id_in_db(''))
        delete_from_db_meals_from_search_with_search_id('')

    def test_generate_search_id_should_work_for_no_ingredients(self):
        self.assertEqual('', generate_search_id([], []))

    def test_generate_search_id_of_mixed_data_should_work(self):
        self.assertEqual('eggs_pasta_tomatoes_n_plums', generate_search_id(['tomatoes', 'eggs', 'pasta'], ['plums']))

    def test_generate_search_id_of_only_excluded_elements_should_work(self):
        self.assertEqual('n_nuts_n_plums', generate_search_id([], ['plums', 'nuts']))

    @classmethod
    def tearDownClass(cls):
        delete_from_db_meals_from_search_with_search_id('')
