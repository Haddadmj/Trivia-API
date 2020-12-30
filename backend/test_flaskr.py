import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.testQuestion = {
            'question': 'What is the dev name?',
            'answer': 'Mohammad',
            'category': '1',
            'difficulty': '5'
        }

        self.testQuiz = {"previous_questions": [
            1, 2], "quiz_category": {"type": "click", "id": 0}}

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_200_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['categories']))

    def test_405_get_categories(self):
        res = self.client().post('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['message'], 'Method Not Allowed')
        self.assertFalse(data['success'])

    def test_200_get_paginated_questions(self):
        res = self.client().get('/questions?page=2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['categories']))
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])

    def test_404_get_paginated_questions(self):
        res = self.client().get('/questions?page=200')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'Resource Not Found')
        self.assertFalse(data['success'])

    def test_200_delete_question(self):
        question_id_to_delete = 15
        res = self.client().delete(f'/questions/{question_id_to_delete}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted_id'], f'{question_id_to_delete}')

    def test_404_delete_question(self):
        res = self.client().delete('/questions/200')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'Resource Not Found')
        self.assertFalse(data['success'])

    def test_200_create_question(self):
        res = self.client().post('/questions/create', json=self.testQuestion)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['question_id'])

    def test_422_create_question(self):
        res = self.client().post('/questions/create', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['message'], 'Unprocessable')
        self.assertFalse(data['success'])

    def test_200_search_question(self):
        res = self.client().post('/questions/search', json={'search': 'box'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(data['questions'])

    def test_404_search_question(self):
        res = self.client().post('/questions/search',
                                 json={'search': 'nmdfjknjdfgj'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'Resource Not Found')
        self.assertFalse(data['success'])

    def test_200_get_category_questions(self):
        category_id = 5
        res = self.client().get(f'/categories/{category_id}/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(data['questions'])

    def test_404_get_category_questions(self):
        category_id = 500
        res = self.client().get(f'/categories/{category_id}/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'Resource Not Found')
        self.assertFalse(data['success'])

    def test_200_play_quiz(self):
        res = self.client().post('/quizzes', json=self.testQuiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(data['question'])
        self.assertTrue(data['success'])

    def test_422_play_quiz(self):
        res = self.client().post('/quizzes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['message'], 'Unprocessable')
        self.assertFalse(data['success'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
