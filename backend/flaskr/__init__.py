import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def pagination(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(db_URI="", test_config=None):
    # create and configure the app
    app = Flask(__name__)
    if db_URI:
        setup_db(app, db_URI)
    else:
        setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs (done)
    """
    cors = CORS(app, resources={r"/*": {"origins": "*"}})
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow(done)
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.(done)
    """
    @app.route('/categories', methods=['GET'])
    def get_categories():
        categories = Category.query.all()

        dict_categories = {
            category.id: category.type for category in categories}

        if len(dict_categories) == 0:
            abort(404)

        return jsonify(
            {
                'success': True,
                'categories': dict_categories
            }
        )

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.(done)

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions', methods=['GET'])
    def get_questions():
        # get  all questions and number of total questions
        questions = Question.query.order_by(Question.id).all()
        total_questions = len(questions)

        # pagination of the questions list
        current_questions = pagination(request, questions)

        categories = Category.query.all()
        dict_categories = {
            category.id: category.type for category in categories}

        if (len(current_questions) == 0):
            abort(404)

        return jsonify(
            {
                'success': True,
                'questions': current_questions,
                'total_questions': total_questions,
                'categories': dict_categories
            }
        )

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.(done)

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()

            if question is None:
                abort(404)
            else:
                question.delete()

                return jsonify(
                    {
                        'success': True,
                        'deleted': question_id,
                        'total_questions': len(Question.query.all())
                    }
                )

        except:
            abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.(done)

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def new_question():
        body = request.get_json()
        new_question = body.get("question", None)
        new_answer = body.get("answer", None)
        new_category = body.get("category", None)
        new_difficulty = body.get("difficulty", None)

        try:
            question = Question(question=new_question, answer=new_answer,
                                category=new_category, difficulty=new_difficulty)
            question.insert()

            return jsonify(
                {
                    'success': True,
                    'created': question.id,
                    'total_questions': len(Question.query.all())
                }
            )
        except:
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.(done)

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions/search', methods=['POST'])
    def search():
        search = request.json.get('search')

        questions = Question.query.filter(
            Question.question.ilike(
                "%" + search + "%")).all()
        
        if (len(questions) == 0):
            abort(404)

        current_question = pagination(request, questions)

        return jsonify({
            'success': True,
            'questions': current_question,
            'total_questions': len(questions),
            'current_category': None
        })


    """
    @TODO:
    Create a GET endpoint to get questions based on category.(done)

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        try:
            questions = Question.query.filter(
                category_id == Question.category).all()
            current_questions = pagination(request, questions)
            category = Category.query.filter(
                Category.id == category_id).one_or_none()

            if len(questions) == 0:
                abort(404)

            return jsonify(
                {
                    'success': True,
                    'questions': current_questions,
                    'category': category.type,
                    'total_questions': len(questions)
                }
            )
        except:
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def quiz():

        body = request.get_json()
        category = body.get('quiz_category', None)
        prev_questions = body.get('previous_questions', None)

        if category is None or prev_questions is None:
            abort(400)

        questions = Question.query.filter(
            Question.category == category['id']).all()

        if (category['id'] == 0):
            questions = Question.query.all()

        current_questions = [question.format(
        ) for question in questions if question.id not in prev_questions]

        random_question = None

        if current_questions:
            random_question = random.choice(current_questions)

        return jsonify({
            'success': True,
            'question': random_question
        })

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.(done)
    """
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(500)
    def Internal_Server_Error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500

    return app
