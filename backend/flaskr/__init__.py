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
            questions_query = Question.query.order_by(Question.id).all()
            selection = paginate_questions(questions_query, request)
            if not selection:
                abort(404)
            print(questions_query, len(selection), "\n\n")
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
        print('\n\nDELETE questions hit:', question_id, "\n\n")
        ques = Question.query.get(question_id)
        if ques is None:
            abort(404)
        ques.delete()
        print(ques.format())
        return jsonify({
            'success': True,
            'deleted': ques.id
        })

    @app.route('/questions', methods=['POST'])
    def create_questions():
        print("\n\nPOST questions hit:",)
        try:
            data = request.get_json()
            print(data, '\n\n')
            if 'searchTerm' in data:
                print('searching')
                search = Question.query.order_by(Question.id).filter(
                    Question.question.ilike("%"+data['searchTerm']+'%')).all()
                # questions = paginate_questions(search, request) #to paginate search results, fromt end doesnt support paginating search results
                questions = [query.format() for query in search]
                print(len(search), "questions found, showing", len(questions))
                if len(search) == 0:
                    return jsonify({"success": False,
                                    "questions": questions,
                                    "total_questions": len(search),
                                    "current_category": "ALL"
                                    })
                else:
                    return jsonify({"success": True,
                                    "questions": questions,
                                    "total_questions": len(search),
                                    "current_category": "ALL"
                                    })
            question = Question(question=data['question'], answer=data['answer'],
                                category=data['category'], difficulty=data['difficulty'])
            question.insert()
            return jsonify({
                "success": True,
                "created":  question.id
            })
        except KeyError as e:
            print(sys.exc_info(), e)
            abort(400)
        except:
            print(sys.exc_info())
            abort(422)

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

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request"
        }), 400
    return app
