# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 



## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## API Reference
### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Request cant be processed
- 405: Method Not allowed
- 500: Internal server error

### Endpoints 

GET '/categories' 
GET '/categories/<int:category_id>/questions'
GET '/questions'
POST '/questions'
POST '/quizzes'
DELETE '/questions/<int:question_id>'


GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
```
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}
```
GET '/categories/<int:category_id>/questions'
-  Gets questions based on category.
-  Request Arguments: None
-  Returns: Category requested, an array of questions, each a dictionary with 4 keys as given below
```
{
'current_category': 6, 
'questions': [
                {
                'answer': 'Brazil', 
                'category': 6, 
                'difficulty': 3, 
                'id': 10, 
                'question': 'Which is the only team to play in every soccer World Cup tournament?
                },
                {'answer': 'Uruguay', 
                'category': 6, 
                'difficulty': 4, 
                'id': 11, 
                'question': 'Which country won the first ever soccer World Cup in 1930?'}
            ], 
'success': True, 
'total_questions': 6
    
}
```

GET '/questions?page=<int:page_no>'
-  Gets all questions
-  Request Arguments: page number, pased in url
-  Returns: questions, including pagination (every 10 questions).This endpoint returns a list of questions,number of total questions, current category, categories.
```
{
    'categories': 
        {'1': 'Science', '2': 'Art', '3': 'Geography', '4': 'History', '5': 'Entertainment', '6': 'Sports'}, 
        'current_category': 'ALL',
        'total_questions': 19,
        'questions': [
                {
                'answer': 'Brazil', 
                'category': 6, 
                'difficulty': 3, 
                'id': 10, 
                'question': 'Which is the only team to play in every soccer World Cup tournament?
                },
                {'answer': 'Uruguay', 
                'category': 6, 
                'difficulty': 4, 
                'id': 11, 
                'question': 'Which country won the first ever soccer World Cup in 1930?'}
                ]
    }
```
POST '/questions'
- Performs search on all questions and Adding a question based on what args are passed.
- Request Arguments: A json in data with key 'searchTerm' OR keys: 'question','answer','difficulty''category'
- Returns: An array of questions like in the example aboce if theres a search happening or confirmation of the new question created by sending its ID
```
Either:
    {'created': 29, 'success': True}
Or: Same response as the GET Questions API response
```
POST '/quizzes'
- Returns a question from the particular category thats asked, or a question in general if no category is defined, the question doesnt appear in the previous questions array that was passed in arguments.
- Request Arguments: {'quiz_category': {'type': , 'id': },"previous_questions":[An array of question Ids that have been used already]} 
- Returns a question, same structure as above. Returns False in question field instead of a json when theres no question left, this turns the game off on front end.
- 
```
{
'question': {
    'answer': 'Real Madrid', 
    'category': 6, 
    'difficulty': 4, 
    'id': 26, 
    'question': 'Who won the UEFA champions league in 2018?'
    }, 
'success': True
}
```

DELETE '/questions/<int:question_id>'
- Delete the question for which id is specified
- Request Args: The question ID
- Returns the id of the question deleted as confirmation
```
{'deleted': 10, 'success': True}
```
## Authors
Rishabh Gajra and The udacity team that made the starter code and Project tasks.



