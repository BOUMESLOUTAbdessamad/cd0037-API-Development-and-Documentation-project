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
        self.database_path = "postgresql://{}/{}".format('student:student@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    DONE
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_questions_with_results(self):
        res = self.client().get('/api/v1/questions')

        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data['questions']), 10)

    def test_get_questions_without_results(self):
        res = self.client().get('/api/v1/questions')

        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(len(data['questions']), 0)

    def test_search_questions_with_results(self):
        res = self.client().post('/api/v1/questions/search', json={"searchTerm": "What"})

        data = json.loads(res.data)
        self.assertEqual(data['total_questions'], 8)
        self.assertEqual(res.status_code, 200)

    def test_search_questions_without_results(self):
        res = self.client().post('/api/v1/questions/search', json={"searchTerm": "2026"})

        data = json.loads(res.data)
        self.assertEqual(data['total_questions'], 0)
        self.assertEqual(res.status_code, 404)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()