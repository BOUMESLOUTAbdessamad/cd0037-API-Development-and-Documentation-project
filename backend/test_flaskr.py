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

        self.new_question = {
            "question": "What is the best FIFA world cup ever?", 
            "answer": "Qatar 2022",
            "category": 6,
            "difficulty": 1
            }

        self.quiz_data = {
            "previous_questions": [99],
            "quiz_category": {"type": "Other", "id": 7}, 
        }

        self.quiz_data2 = {
            "previous_questions": [],
            "quiz_category": {"type": "Sports", "id": 6}, 
        }



    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    DONE
    Write at least one test for each test for successful operation and for expected errors.
    """

    # Test GET /api/v1/questions
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

    # Test POST /api/v1/questions/search
    def test_search_questions_with_results(self):
        res = self.client().post('/api/v1/questions/search', json={"searchTerm": "What"})
        data = json.loads(res.data)

        self.assertEqual(data['total_questions'], 19)
        self.assertEqual(res.status_code, 200)

    def test_search_questions_without_results(self):
        res = self.client().post('/api/v1/questions/search', json={"searchTerm": "2026"})
        data = json.loads(res.data)

        self.assertEqual(data['total_questions'], 0)
        self.assertEqual(res.status_code, 404)

    # Test GET /api/v1/categories
    def test_get_categories_with_results(self):
        res = self.client().get('/api/v1/categories')
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data['categories']), 6)


    def test_get_categories_without_results(self):
        res = self.client().get('/api/v1/categories')
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(len(data['categories']), 0)

    # Test DELETE /api/v1/questions
    def test_delete_question_with_success(self):
        res = self.client().delete('/api/v1/questions/10')
        data = json.loads(res.data)
        with self.app.app_context():
            question = Question.query.filter(Question.id == 10).one_or_none()
        
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(question, None)

    def test_422_for_delete_question_failure(self):
        res = self.client().delete('/api/v1/questions/999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    # Test POST /api/v1/questions/{id}
    def test_create_new_question(self):
        res = self.client().post("/api/v1/questions", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_405_on_question_creation_not_allowed(self):
        res = self.client().post("/api/v1/questions/20", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")

    # Test GET /api/v1/categories/{id}/questions
    def test_get_questions_by_category(self):
        res = self.client().get('/api/v1/categories/1/questions')
        data = json.loads(res.data)
    
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 4)
        self.assertEqual(res.status_code, 200)

    def test_404_sent_requesting_questions_by_category(self):
        res = self.client().get('/api/v1/categories/99/questions')
        data = json.loads(res.data)
    
        self.assertEqual(data['success'], False)
        self.assertEqual(len(data['question']), 0)
        self.assertEqual(res.status_code, 404)

    #Test Test POST /api/v1/quizzes
    def test_quiz_get_random_question(self):
        res = self.client().post('/api/v1/quizzes', json=self.quiz_data2)
        data = json.loads(res.data)
        self.assertTrue(data['question'])
        self.assertEqual(len(data['prevQuestions']), 0)
        self.assertEqual(res.status_code, 200)

    def test_400_on_quiz_bad_request(self):
        res = self.client().post('/api/v1/quizzes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,  400)
        self.assertEqual(data["message"], "bad request")

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()