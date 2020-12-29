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

    return questions[start:end]


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app, resources={r"*/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    '''
    Get request to get categories
    Request Response : 'success','categories' formatted as key:value pair
    '''
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

    '''
    Get request to get questions
    Request Response : 'success','questions'
    '''
    @app.route('/questions')
    def get_questions():
        questions = Question.query.all()
        current_questions = paginate_questions(request, questions)
        categories = Category.query.order_by(Category.id).all()
        formatted_categories = {
            category.id: category.type for category in categories}

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'categories': formatted_categories,
            'total_questions': len(questions),
            'current_catagory': None
        })
    '''
    DELETE request to delete question given ID
    Request Response : 'success','deleted_id'
    '''
    @app.route('/questions/<question_id>', methods=['DELETE'])
    def delete_question(question_id):

        question = Question.query.get(question_id)

        if question is None:
            abort(404)

        question.delete()

        return jsonify({
            'success': True,
            'deleted_id': question_id
        })
    '''
    POST request to create question
    Request Body: question,answer,category id,difficulty
    Request Response : 'success','question_id'
    '''
    @app.route('/questions/create', methods=['POST'])
    def create_question():
        body = request.get_json()

        if body is None:
            abort(422)

        try:
            question = body['question']
            answer = body['answer']
            category = body['category']
            difficulty = body['difficulty']

            for x in body:
                print(type(body[x]))

            newQuestion = Question(question, answer, category, difficulty)

            newQuestion.insert()

            return jsonify({
                'success': True,
                'question_id': newQuestion.id
            })

        except Exception:
            abort(422)
    '''
    POST request to search question
    Request Body: search
    Request Response : 'success','questions'
    '''
    @app.route('/questions/search', methods=['POST'])
    def get_questions_start_with():
        body = request.get_json()

        if body is None:
            abort(422)

        try:
            search = body.get('search')
            search_query = Question.query.order_by('id').filter(
                Question.question.ilike(f'%{search}%'))

            formatted_search = [question.format() for question in search_query]

            if len(formatted_search) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'questions': formatted_search
            })
        except Exception:
            abort(422)
    '''
    Get request to get questions in certin category
    Request Response : 'success','questions'
    '''
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
    '''
    POST request get questions to play the quiz
    Request Body: previous_questions, quiz_category
    Request Response : 'success','questions'
    where question is not repeated
    '''
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():

        body = request.get_json()

        if body is None:
            abort(422)

        try:
            prev = body['previous_questions']
            quiz_category = body['quiz_category']['id']

            print(prev)

            if quiz_category == 0:
                questions = Question.query.all()
                question = questions[random.randrange(0, len(questions))]
                if question.id in prev:
                    question = questions[random.randrange(0, len(questions))]
            else:
                questions = Question.query.filter(
                    Question.category == quiz_category).all()
                question = questions[random.randrange(0, len(questions))]
                if question.id in prev:
                    question = questions[random.randrange(0, len(questions))]

            return jsonify({
                'success': True,
                'question': question.format()
            })

        except Exception:
            abort(422)

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
