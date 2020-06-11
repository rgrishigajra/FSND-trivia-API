import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import setup_db, Question, Category
import sys
from werkzeug.exceptions import HTTPException, NotFound, PreconditionFailed
from sqlalchemy.sql import func

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
        '''
        Create an endpoint to handle GET requests
        for all available categories.
            '''
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
        '''
        Create a GET endpoint to get questions based on category.
        TEST: In the "List" tab / main screen, clicking on one of the
        categories in the left column will cause only questions of that
        category to be shown.
            '''
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_catergory_questions(category_id):
        print("\n\nGET questions by category hit", category_id)
        try:
            questions = Question.query.filter(
                Question.category == category_id).all()
            selection = [question.format() for question in questions]
            if not len(questions):
                abort(404)
            return jsonify({
                "success": True,
                "current_category": category_id,
                "questions": selection,
                "total_questions": len(questions)})
        except NotFound as e:
            print(sys.exc_info(), e)
            abort(404)
        except:
            print(sys.exc_info())
            abort(422)

    # routes for questions
        '''
        Create an endpoint to handle GET requests for questions,
        including pagination (every 10 questions).
        This endpoint should return a list of questions,
        number of total questions, current category, categories.
        TEST: At this point, when you start the application
        you should see questions and categories generated,
        ten questions per page and pagination at the bottom of the screen for three pages.
        Clicking on the page numbers should update the questions.
            '''
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

        '''
        Create an endpoint to DELETE question using a question ID.
        TEST: When you click the trash icon next to a question, the question will be removed.
        This removal will persist in the database and when you refresh the page.
            '''
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
        '''
        Create an endpoint to POST a new question,
        which will require the question and answer text,
        category, and difficulty score.
        TEST: When you submit a question on the "Add" tab,
        the form will clear and the question will appear at the end of the last page
        of the questions list in the "List" tab.

        Create a POST endpoint to get questions based on a search term.
        It should return any questions for whom the search term
        is a substring of the question.
        TEST: Search by any phrase. The questions list will update to include
        only question that include that string within their question.
        Try using the word "title" to start.
        '''
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
                    return jsonify(
                                    {"success": True,
                                    "questions": questions,
                                    "total_questions": len(search),
                                    "current_category": "ALL"
                                    }
                                    )
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

    # routes for quizzes

        '''
        Create a POST endpoint to get questions to play the quiz.
        This endpoint should take category and previous question parameters
        and return a random questions within the given category,
        if provided, and that is not one of the previous questions.
        TEST: In the "Play" tab, after a user selects "All" or a category,
        one question at a time is displayed, the user is allowed to answer
        and shown whether they were correct or not.
            '''
    @app.route('/quizzes', methods=['POST'])
    def get_quiz_question():
        print('\n\nGET quiz hit:')
        data = request.get_json()
        print(data)
        try:
            if data['quiz_category']['id']:
                questions = Question.query.filter(~(Question.id.in_(data['previous_questions']))).filter(
                    Question.category == data['quiz_category']['id']).order_by(func.random()).first()
            else:
                questions = Question.query.filter(
                    ~(Question.id.in_(data['previous_questions']))).order_by(func.random()).first()
            if questions is not None:
                selected_ques = questions.format()
            else:
                selected_ques = False
                # abort(412) #this doesnt work on front end but i think it should have
            print(selected_ques)
            return jsonify({
                "success": True,
                'question': selected_ques})
        except PreconditionFailed as e:
            print(sys.exc_info(), e)
            abort(412)
        except e:
            print(sys.exc_info(), e)
            abort(500)


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
            "message": "Request cant be processed"
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

    @app.errorhandler(412)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 412,
            "message": "Precondition for resouce failed",
            "question": False
        }), 412
    return app
