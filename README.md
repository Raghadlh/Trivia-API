# API Development and Documentation Final Project

## Trivia App
This App allows you to manage trivia questions, play games, and perform other operations such as:

1. Display questions—both all questions and by category. Questions should show the question, category, and difficulty rating by default and can show or hide the answer.
2. Delete questions.
3. Add questions.
4. Search for questions based on a text.
5. Play the quiz game.


### Getting Started

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Frontend 

> _tip_: this frontend is designed to work with [Flask-based Backend](../backend) so it will not load successfully if the backend is not working or not connected. We recommend that you **stand up the backend first**, test using Postman or curl, update the endpoints in the frontend, and then the frontend should integrate smoothly.

### Installing Dependencies

1. **Installing Node and NPM**
   This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

2. **Installing project dependencies**
   This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```

> _tip_: `npm i`is shorthand for `npm install``


### Running Your Frontend in Dev Mode

The frontend app was built using create-react-app. In order to run the app in development mode use `npm start`. You can change the script in the `package.json` file.

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.

```bash
npm start
```

## Testing

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 422,
    "message": "unprocessable"
}
```
The API will return four error types when requests fail:
- 400: Bad Request
- 404: Not Found
- 422: Not Processable 
- 500: Internal Server Error 
### Endpoints 
#### GET /categories
- General:
    - Returns a list of category, success value
- Sample: `curl http://127.0.0.1:5000/categories`

```
{
    "categories":{
        "1":"Science",
        "2":"Art",
        "3":"Geography",
        "4":"History",
        "5":"Entertainment",
        "6":"Sports"
    },
    "success":true
    }
```
#### GET /questions
- General:
    - Returns a list of questions,number of total questions, current category, categories.
- Sample: `curl http://127.0.0.1:5000/questions`
```
{
 "categories":{
   "1":"Science",
   "2":"Art",
   "3":"Geography",
   "4":"History",
   "5":"Entertainment",
   "6":"Sports"
 },
   "questions":[
    {
    "answer":"Apollo 13",
    "category":5,
    "difficulty":4,
    "id":2,
    "question":"What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
    "answer":"Tom Cruise",
    "category":5,
    "difficulty":4,
    "id":4,
    "question":"What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
    "answer":"Maya Angelou",
    "category":4,
    "difficulty":2,
    "id":5,
    "question":"Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {"answer":"Edward Scissorhands",
    "category":5,
    "difficulty":3,
    "id":6,
    "question":"What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
    "answer":"Muhammad Ali",
    "category":4,
    "difficulty":1,
    "id":9,
    "question":"What boxer's original name is Cassius Clay?"
    },
    {
    "answer":"Brazil",
    "category":6,
    "difficulty":3,
    "id":10,
    "question":"Which is the only team to play in every soccer World Cup tournament?"
    },
    {
    "answer":"Uruguay",
    "category":6,
    "difficulty":4,
    "id":11,
    "question":"Which country won the first ever soccer World Cup in 1930?"
    },
    {
    "answer":"George Washington Carver",
    "category":4,
    "difficulty":2,
    "id":12,
    "question":"Who invented Peanut Butter?"
    },
    {
    "answer":"Lake Victoria",
    "category":3,
    "difficulty":2,
    "id":13,
    "question":"What is the largest lake in Africa?"
    },
    {
    "answer":"The Palace of Versailles",
    "category":3,
    "difficulty":3,
    "id":14,
    "question":"In which royal palace would you find the Hall of Mirrors?"
    }
    ],
    "success":true,
    "total_questions":19
}
```
#### DELETE /questions/<int:question_id>
- General:
     - Delete question using a question ID.
     - Return success value,total of questions,question ID.
- Sample: `curl -X DELETE http://127.0.0.1:5000/questions/47`
```
{
 "deleted":47,
 "success":true,
 "total_questions":19
}
```
#### POST /questions
- General:
    - Add new question.
    - Return success value,total of questions,question ID.
- Sample: curl -X POST -H "Content-Type: application/json" -d "{"question":"Which planet is the hottest in the solar system?","answer":"Venus","category":1,"difficulty":"2"}" http://127.0.0.1:5000/questions
```
{
"created":48,
"success":true,
"total_questions":20
}
```
#### POST /questions/search
- General:
     - Get questions based on a search term.
     - Return success value,questions,total of questions,category.
- Sample: `curl -X POST -H "Content-Type: application/json" -d "{"search": "title"}" http://localhost:5000/questions/search`
```
{
 "current_category":null,
 "questions":[
  {
  "answer":"Maya Angelou",
  "category":4,
  "difficulty":2,
  "id":5,
  "question":"Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
  },
  {
  "answer":"Edward Scissorhands",
  "category":5,
  "difficulty":3,
  "id":6,
  "question":"What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
  }
  ],
  "success":true,
  "total_questions":2
}
```
### GET /categories/<int:category_id>/questions
- General:
     - Get questions based on category.
     - Return success value,questions,total of questions,category.
- Sample:`curl http://127.0.0.1:5000/categories/3/questions`
```
{
 "category":"Geography",
 "questions":[
  {
  "answer":"Lake Victoria",
  "category":3,
  "difficulty":2,
  "id":13,
  "question":"What is the largest lake in Africa?"
  },
  {
  "answer":"The Palace of Versailles",
  "category":3,
  "difficulty":3,
  "id":14,
  "question":"In which royal palace would you find the Hall of Mirrors?"
  },
  {"answer":"Agra",
  "category":3,
  "difficulty":2,
  "id":15,
  "question":"The Taj Mahal is located in which Indian city?"
  }
  ],
  "success":true,
  "total_questions":3
}
```
### POST /quizzes
- General:
     - Get questions to play the quiz.
     - Return a random questions within the given category.
- Sample:`curl -X POST -H "Content-Type: application/json" -d "{"quiz_category": {"type": "Geography", "id": "3"},"previous_questions": [13]}" http://localhost:5000/quizzes`
```
{
"question":{
"answer":"The Palace of Versailles",
"category":3,
"difficulty":3,
"id":14,
"question":"In which royal palace would you find the Hall of Mirrors?"
},
"success":true
}
```
