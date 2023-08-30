import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import setup_db, Question, Category
from settings import  DB_USER, DB_PASSWORD,DB_HOST,DB_TEST


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""

        self.database_path = 'postgresql://{}:{}@{}/{}'.format(DB_USER,DB_PASSWORD,DB_HOST, DB_TEST)
        self.app = create_app(self.database_path)
        self.client = self.app.test_client

        self.new_question = {
            "answer": "Snow White",
            "category": 5,
            "difficulty": 3,
            "question": "Which Disney Princess talks to the most animals?"
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_paginated_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get("/questions?page=800", json={"categories": 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_get_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_422_if_question_does_not_exist(self):
        res = self.client().delete("/questions/5000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_new_question(self):

        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_search_question(self):
        res = self.client().post("/questions/search", json={'search': 'title'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
    
    def test_search_question_fails(self):
        res = self.client().post("/questions/search", json={'search': 'ababababa'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

    def test_422_delete_question_fails(self):
        res = self.client().delete("/questions/50000")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)

    def test_get_questions_by_category(self):
        res = self.client().get("/categories/4/questions")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["category"], "History")

    def test_422_get_questions_by_category_fails(self):
        res = self.client().get("/categories/50/questions")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)

    def test_play_quiz(self):
        res = self.client().post('/quizzes',
                                 json={"quiz_category": {"type": "Geography", "id": "3"}, "previous_questions": [13]})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_400_play_quiz_fails(self):
        res = self.client().post('/quizzes', json={})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
