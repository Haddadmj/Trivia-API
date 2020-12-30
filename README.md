# Udacitrivia

Udacitrivia is website backed by restful API, allow the user to do the list below 

1) Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category. 

All backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/).

## Getting Started
To Use this project, clone it first, then follow the guide for each end, [backend](./backend) then [frontend](./frontend)

### Backend

The `./backend` directory contains a completed Flask and SQLAlchemy server.
[View the README.md within ./backend for more details.](./backend/README.md)</br>
[View the API within ./backend](./backend/API_Docs.md)

### Frontend

The `./frontend` directory contains a complete React frontend to consume the data from the Flask server 

[View the README.md within ./frontend for more details.](./frontend/README.md)

## API Reference

### Getting Started

* Base URL: Currently this application is only hosted locally. The backend is hosted at `http://localhost:5000/`
* Authentication: No Authentication Needed.

### Error Handling

Errors are returned as JSON in the following format:<br>

    {
        "success": False,
        "error": 404,
        "message": "resource not found"
    }

The API will return three types of errors:

* 400 – bad request
* 404 – resource not found
* 422 – unprocessable
* 405 - method not allowed

### Endpoints

#### GET /categories

* General: Returns a list categories.
* Sample: `curl localhost:5000/categories`<br>

        {
        "categories": {
            "1": "Science", 
            "2": "Art", 
            "3": "Geography", 
            "4": "History", 
            "5": "Entertainment", 
            "6": "Sports"
        }, 
        "success": true
        }


#### GET /questions

* General:
  * Returns a list questions.
  * Results are paginated in groups of 10.
  * Also returns list of categories and total number of questions.
* Sample: `curl localhost:5000/questions`<br>

        {
        "categories": {
            "1": "Science", 
            "2": "Art", 
            "3": "Geography", 
            "4": "History", 
            "5": "Entertainment", 
            "6": "Sports"
        }, 
        "current_catagory": null, 
        "questions": [
            {
            "answer": "Maya Angelou", 
            "category": 4, 
            "difficulty": 2, 
            "id": 1, 
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
            }, 
            {
            "answer": "Muhammad Ali", 
            "category": 4, 
            "difficulty": 1, 
            "id": 2, 
            "question": "What boxer's original name is Cassius Clay?"
            }, 
            {
            "answer": "Apollo 13", 
            "category": 5, 
            "difficulty": 4, 
            "id": 3, 
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
            }, 
            {
            "answer": "Tom Cruise", 
            "category": 5, 
            "difficulty": 4, 
            "id": 4, 
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
            }, 
            {
            "answer": "Edward Scissorhands", 
            "category": 5, 
            "difficulty": 3, 
            "id": 5, 
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
            }, 
            {
            "answer": "Brazil", 
            "category": 6, 
            "difficulty": 3, 
            "id": 6, 
            "question": "Which is the only team to play in every soccer World Cup tournament?"
            }, 
            {
            "answer": "Uruguay", 
            "category": 6, 
            "difficulty": 4, 
            "id": 7, 
            "question": "Which country won the first ever soccer World Cup in 1930?"
            }, 
            {
            "answer": "George Washington Carver", 
            "category": 4, 
            "difficulty": 2, 
            "id": 8, 
            "question": "Who invented Peanut Butter?"
            }, 
            {
            "answer": "Lake Victoria", 
            "category": 3, 
            "difficulty": 2, 
            "id": 9, 
            "question": "What is the largest lake in Africa?"
            }, 
            {
            "answer": "The Palace of Versailles", 
            "category": 3, 
            "difficulty": 3, 
            "id": 10, 
            "question": "In which royal palace would you find the Hall of Mirrors?"
            }
        ], 
        "success": true, 
        "total_questions": 19
        }

#### DELETE /questions/<question_id>

* General:
  * Deletes a question by id using url parameters.
  * Returns id of deleted question upon success.
* Sample: `curl -X DELETE localhost:5000/questions/19`<br>
        {
        "deleted": "19", 
        "success": true
        }


#### POST /questions

* General:
  * Creates a new question using JSON request parameters.
  * Returns JSON object with newly created question id.
* Sample: `curl -X POST localhost:5000/questions/create -H 'Content-Type: application/json' -d '{"question":"What is the dev name?","answer":"Mohammad","category":4,"difficulty":5}'`<br>
        {
        "question_id": 23,
        "success": true
        }


#### POST /questions/search

* General:
  * Searches for questions using search term in JSON request parameters.
  * Returns JSON object with matching questions.
* Sample: `curl -X POST localhost:5000/questions/search -H "Content-Type: application/json" -d '{"search": "which"}'`<br>

        {
        "questions": [
            {
            "answer": "Muhammad Ali", 
            "category": 4, 
            "difficulty": 1, 
            "id": 2, 
            "question": "What boxer's original name is Cassius Clay?"
            }
        ], 
        "success": true
        }

#### GET /categories/<category_id>/questions

* General:
  * Gets questions by category id using url parameters.
  * Returns JSON object with paginated matching questions.
* Sample: `curl localhost:5000/categories/4/questions`<br>

        {
        "current_category": "History", 
        "questions": [
            {
            "answer": "Maya Angelou", 
            "category": 4, 
            "difficulty": 2, 
            "id": 1, 
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
            }, 
            {
            "answer": "Muhammad Ali", 
            "category": 4, 
            "difficulty": 1, 
            "id": 2, 
            "question": "What boxer's original name is Cassius Clay?"
            }, 
            {
            "answer": "George Washington Carver", 
            "category": 4, 
            "difficulty": 2, 
            "id": 8, 
            "question": "Who invented Peanut Butter?"
            }, 
            {
            "answer": "Mohammad", 
            "category": 4, 
            "difficulty": 3, 
            "id": 20, 
            "question": "What is the dev name?"
            }
        ], 
        "success": true, 
        "total_questions": 4
        }

#### POST /quizzes

* General:
  * Allows users to play the quiz game.
  * Uses JSON request parameters of category and previous questions.
  * Returns JSON object with random question not among previous questions.
* Sample: `curl -X POST localhost:5000/quizzes -H "Content-Type: application/json" -d '{"previous_questions": [1, 2],"quiz_category": {"type": "click", "id": 0}}'`<br>

{
  "question": {
    "answer": "Mona Lisa",
    "category": 2,
    "difficulty": 3,
    "id": 13,
    "question": "La Giaconda is better known as what?"
  },
  "success": true
}

## Authors
Mohammad Al-Haddad 

## Acknowledgements
Uadcity for providing the starter code