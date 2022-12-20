import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, data):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in data]
    current_questions = questions[start:end]

    return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @DONE: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    """
    @DONE: Use the after_request decorator to set Access-Control-Allow
    """

    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Autorization, true")
        response.headers.add("Access-Control-Allow-Methods", "GET, POST, PATCH, DELETE, PUT, OPTIONS") 
        response.headers.add("Access-Control-Allow-Credentials", "true")
        return response
    """
    @DONE:
    Create an endpoint to handle GET requests
    for all available categories.
    """

    @app.route('/api/v1/categories')
    def all_categories():
        categories = Category.query.all()
        formated_cats = [category.format() for category in categories]

        return jsonify({
            "success" : True,
            "categories": formated_cats
        })

    """
    @DONE:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/api/v1/questions')
    def get_questions():
        questions = Question.query.all()
        categories = Category.query.all()
        paginated_questions = paginate_questions(request, questions)
        formated_cats = [category.format() for category in categories]
        
        return jsonify({
            "success": True,
            "questions": paginated_questions,
            "categories": formated_cats,
            "total_questions": len(questions),
            "currentCategory": 1
        })


    """
    @DONE:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.route('/api/v1/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id==question_id).one_or_none()

            if not question:
                abort(404)

            question.delete()
            return jsonify({ "success": True })
        except:
            abort(422)

     
    """
    @DONE:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/api/v1/questions', methods=['POST'])
    def add_question():
        body = request.get_json('question')
        question = body.get('question', None)
        answer = body.get('answer', None)
        difficulty = body.get('difficulty', None)
        category = body.get('category', None)
        
        try:
            question = Question(
                question=question, 
                answer=answer, 
                difficulty=difficulty, 
                category=category
                )

            question.insert()

        except:
            abort(422)

        return jsonify({
            "success": True,
        })



    """
    @DONE:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/api/v1/questions', methods=['GET'])
    def search_questions():
        body = request.get_json()
        search = body.get('search')
        try:
            if search:
                questions = Question.query.filter( 
                    Question.question.ilike("%{}%".format(search))
                    )
            
            formated_results = paginate_questions(request, questions)

            return jsonify({
                "success": True,
                "questions": formated_results,
                "total_questions": len(questions),
                "current_category": 1
            })

        except:
            abort(422)

    """
    @DONE:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    @app.route('/api/v1/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):

        try:
            questions = Question.query.filter(Question.category == category_id).all()
            if not questions:
                abort(404)

            return jsonify({
                "success": True,
                "questions": paginate_questions(request, questions)
                })
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

    @app.route('/api/v1/quizzes', methods=['POST'])
    def quiz():
        body = request.get_json()
        selectedCategory = body.get('quiz_category', None).get('id')
        prevQuestions = body.get('previous_questions')

        try:
            if selectedCategory == 0:
                questions_by_category = Question.query.all() # Get All if category == 0
            else:
                questions_by_category = Question.query.filter(Question.category == selectedCategory).all()

            new_questions = [question.format() for question in questions_by_category if question.id not in prevQuestions]

            if len(new_questions) == 0:
                next_question = None
            else:
                next_question = random.choice(new_questions)

            return jsonify({
                        "prevQuestions": prevQuestions,
                        "question": next_question
                    })

        except:
            abort(422)

      
    """
    @DONE:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

    @app.errorhandler(401)
    def unauthorised(error):
        return jsonify({"success": False, "error": 401, "message": "unauthorised"}), 401

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}), 404
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),  422
        ) 

    return app

