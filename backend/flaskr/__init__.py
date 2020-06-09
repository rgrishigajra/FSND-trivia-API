import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import setup_db, Question, Category
import sys
from werkzeug.exceptions import HTTPException, NotFound

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
  # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

  # cors headers allow
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             "Content-Tpe,Authorization,true")
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,PATCH,DELETE,OPTIONS')
        return response

  # helper functions
    def paginate_questions(questions, request):
        page = request.args.get('page', 1, type=int)
        start = (page-1)*QUESTIONS_PER_PAGE
        end = start+QUESTIONS_PER_PAGE
        selection = [question.format() for question in questions[start:end]]
        return selection
  # app routes
    # routes for categories
    @app.route('/categories', methods=['GET'])
    def list_categories():
        print("\n\nGET categories hit:")
        try:
            categories_query = Category.query.all()
            categories = {}
            for cat in categories_query:
                categories[cat.id] = cat.type
            print(categories, "\n\n")
            if len(categories_query) == 0:
                abort(404)
            return jsonify({
                "success": True,
                "categories": categories
            })
        except NotFound as e:
            print(sys.exc_info(), e)
            abort(404)
        except:
            print(sys.exc_info())
            abort(500)

    # routes for questions
    @app.route('/questions', methods=['GET'])
    def get_questions():
        print("\n\nGET questions hit:")
        try:
            categories_query = Category.query.all()
            categories = {}
            for cat in categories_query:
                categories[cat.id] = cat.type
            if len(categories_query) == 0:
                abort(404)
            questions_query = Question.query.all()
            selection = paginate_questions(questions_query, request)
            if not selection:
                abort(404)
            print(selection, "\n\n")
            return jsonify({
                "success": True,
                "categories": categories,
                "current_category": 'ALL',
                "questions": selection,
                "total_questions": len(questions_query)
            })
        except NotFound as e:
            print(sys.exc_info(), e)
            abort(404)
        except e:
            print(sys.exc_info(), e)
            abort(500)

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_questions(question_id):
        print('\n\nDELETE questions hit:', question_id)
        ques = Question.query.get(question_id)
        if ques is None:
            abort(404)
        ques.delete()
        print(ques.format())
        return jsonify({
            'success': True,
            'deleted': ques.id
        })

    '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

    '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

    '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

    '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
    '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

    '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  # error handlers :
    @app.errorhandler(404)
    def error_resource_not_found(error):
        return jsonify({
            "success": False,
            "message": "Resource not found",
            "error": 404
        }), 404

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "message": "Internal server error",
            "error": 500
        }), 500

    @app.errorhandler(422)
    def not_processable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "request cant be processed"
        }), 422

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405
    return app
