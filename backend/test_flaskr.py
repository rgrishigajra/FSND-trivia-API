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

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_list_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        if res.status_code == 200:
            self.assertTrue(data['success'])
            self.assertTrue(len(data['categories']))

    def test_404_error_list_categories_failure(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        if res.status_code == 404:
            self.assertFalse(data['success'])
            self.assertEqual(data['message'], 'Resource not found')

    def test_get_questions(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)
        # print(data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)
        self.assertIsInstance(data['questions'], list)
        self.assertTrue(len(data['questions']))
        self.assertIsInstance(data['total_questions'], int)
        self.assertIsInstance(data['current_category'], str)
        self.assertIsInstance(data['categories'], dict)
        self.assertTrue(len(data['categories']))

    def test_404_error_get_questions(self):
        res = self.client().get('/questions?page=1000')
        self.assertEqual(res.status_code, 404)
        data = json.loads(res.data)
        # print(data)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Resource not found')

    def test_delete_questions(self):
        ques = Question.query.order_by(Question.id).first()
        res = self.client().delete('/questions/'+str(ques.id))
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        # print(dat)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], ques.id)
        test = Question.query.get(ques.id)
        self.assertEqual(test, None)

    def test_404_error_delete_questions(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Resource not found')

    def test_create_question(self):
        res = self.client().post('/questions',
                                 json={'question': 'Who won the UEFA champions league in 2018?', 'answer': 'Real Madrid', 'difficulty': '4', 'category': '6'})
        data = json.loads(res.data)
        # print(data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsInstance(data['created'], int)

    def test_400_error_create_question(self):
        res = self.client().post('/questions',
                                 json={'question': 'Who won the UEFA champions league in 2018?', 'answer': 'Real Madrid', 'difficulty': '4'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Bad request')
    def test_successful_search_questions(self):
        res=self.client().post('/questions',json={'searchTerm': 'a'})
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsInstance(data['total_questions'],int)
        self.assertIsInstance(data['questions'],list)
        self.assertIsInstance(data['current_category'],str)

    def test_unsuccessful_search_questions(self):
        res=self.client().post('/questions',json={'searchTerm': 'jakfjkahfjkahfjkdahfjkhksdjfhksj'})
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertFalse(data['success'])
        self.assertEqual(data['total_questions'],0)
        self.assertIsInstance(data['questions'],list)
        self.assertIsInstance(data['current_category'],str)

    def test_get_category_questions(self):
        res = self.client().get('/categories/6/questions')
        data = json.loads(res.data)
        # print(data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsInstance(data['questions'], list)
        self.assertTrue(len(data['questions']))
        self.assertIsInstance(data['total_questions'], int)
        self.assertIsInstance(data['current_category'], int)

    def test_404_error_get_category_questions(self):
        res = self.client().get('/categories/600/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Resource not found')

    def test_quiz(self):
        jsonobj={'quiz_category': {'type': 'Sports', 'id': '6'},"previous_questions":[24,11]}
        res = self.client().post('/quizzes', json=jsonobj)
        data = json.loads(res.data)
        # print(data)
        self.assertIsInstance(data['question'],dict)
        self.assertTrue(bool(data['question']))
        self.assertNotIn(data['question']['id'],jsonobj['previous_questions'])

    def test_error_quiz_out_of_questions(self):
        questions = Question.query.filter(
                Question.category == 6).all()
        selection = [question.format()['id'] for question in questions]
        jsonobj={'quiz_category':  {'type': 'Sports', 'id': '6'},"previous_questions":selection}
        res = self.client().post('/quizzes', json=jsonobj)
        data = json.loads(res.data)
        # print(data)
        self.assertEqual(res.status_code, 200)
        self.assertFalse(data['question'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
