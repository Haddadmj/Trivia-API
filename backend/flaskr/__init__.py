import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    # GET request to get all categories
    @app.route('/categories')
    def get_categories():
        categories = Category.query.order_by('id').all()
        formatted_categories = {
            category.id: category.type for category in categories}
        if len(formatted_categories) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'categories': formatted_categories
        })

    # GET request to get all questions
    @app.route('/questions')
    def get_questions():
        questions = Question.query.all()
        current_questions = paginate_questions(request, questions)
        categories = Category.query.order_by(Category.id).all()

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'categories': {category.id: category.type for category in categories},
            'total_questions': len(questions),
            'current_catagory': None
        })

    # DELETE request to delete question given id

    @app.route('/questions/<question_id>', methods=['DELETE'])
    def delete_question(question_id):

        question = Question.query.get(question_id)

        if question is None:
            abort(404)

        question.delete()

        return jsonify({
            'success': True,
            'deleted': question_id
        })

    # POST request to create question given question,answer,category id,difficulty

    @app.route('/questions/create', methods=['POST'])
    def create_question():
        body = request.get_json()

        if len(body) == 0:
            abort(422)
        
        question = body['question']
        answer = body['answer']
        category = int(body['category'])
        difficulty = int(body['difficulty'])

        if (question is None) or (answer is None) or (category is None) or (difficulty is None):
            abort(422)

        question = Question(question, answer, category, difficulty)
        question.insert()

        return jsonify({
            'success': True,
            'question_id': question.id
        })

    # GET request to search for question given search term
    @app.route('/questions/search', methods=['POST'])
    def get_questions_start_with():
        body = request.get_json()
        search = body.get('search')

        if body is None:
            abort(422)

        search_query = Question.query.order_by('id').filter(
            Question.question.ilike(f'%{search}%'))

        formatted_search = [question.format() for question in search_query]

        if len(formatted_search) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': formatted_search
        })

    @app.route('/categories/<category_id>/questions')
    def get_questions_in_category(category_id):
        questions = Question.query.filter(
            Question.category == category_id).all()
        formatted_questions = [question.format() for question in questions]

        if len(formatted_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': formatted_questions,
            'total_questions': len(formatted_questions),
            'current_category': Category.query.get(category_id).type
        })

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():

        body = request.get_json()

        if body is None:
            abort(422)

        prev = body.get('previous_questions')
        quiz_category = int(body.get('quiz_category')['id'])

        if (prev is None) or (quiz_category is None):
            abort(400)

        if quiz_category == 0:
            questions = Question.query.all()
            question = questions[random.randrange(0, len(questions))]
            if question.id in prev:
                question = questions[random.randrange(0, len(questions))]
            if len(prev) == len(questions):
                question = None
        else:
            questions = Question.query.filter(
                Question.category == quiz_category).all()
            question = questions[random.randrange(0, len(questions))]
            if question.id in prev:
                question = questions[random.randrange(0, len(questions))]
            if len(prev) == len(questions):
                question = None

        return jsonify({
            'success': True,
            'question': question.format()
        })

    '''
    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    '''

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource Not Found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method Not Allowed"
        }), 405

    @app.errorhandler(500)
    def internal_server(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500

    return app
