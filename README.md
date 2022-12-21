
# Trivia API Documentation  [![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)

Trivia API is a Quiz app. It allows you to add questions, update and delete them, also questions are classified by categories.

With Trivia API you can:

- Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
- Delete questions.
- Add questions and require that they include question and answer text.
- Search for questions based on a text query string.
- Play a quiz game, randomizing either all questions or within a specific category.



# Get started

## Installation

Clone the project repository to your machine.

### Backend
Install python requirements.

```bash
  $ cd backend
  $ pip install -r requirements.txt
```
### Frontend
Install npm Pacakges

Plugins or plugin presets will be loaded automatically from `package.json`
```bash
  $ cd frontend
  $ npm install
```



## Running Tests

To run tests, run the following commands

1 - Setup ENV variables

```bash
cd backend

$ export FLASK_APP=flaskr
$ export FLASK_ENV=developement
```

2 - Run the flask App

```bash
$ flask run
```

3 - Run the React App

```bash
cd frontend

$ npm start
```


## API Reference

### Get all questions

```http
GET /api/v1/questions
```
Example
```http
$ curl http://127.0.0.1:5000/api/v1/questions
```
Results (json)

```http
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }
  ],
```

### Delete a question

```http
DELETE /api/v1/questions/${id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `int` | **Required**. id of question to delete |

Example
```http
$ curl -X DELETE http://127.0.0.1:5000/api/v1/questions/8 
```
### Add a question

```http
POST /api/v1/questions
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `question`    | `string` | **Required**. The text question |
| `answer`      | `string` | **Required**. The Anwser of the question |
| `difficulty`  | `string` | **Required**. Difficulty level of the question  |
| `category`    |  `int`   | **Required**. In which category the question is classified|

Example

```http
$ curl -X POST  -H "Content-Type: application/json" -d '{"question":"What is the best E-learning Plateform?","answer":"Udacity", "category":"1", "difficulty":"1"}' http://127.0.0.1:5000/api/v1/questions

```

Results

```http
    {
        "success": true
    }
```

### Search

```http
POST /api/v1/questions/search
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `searchTerm`    | `string` | **Required**. Get questions based on a search term |

Example

```http
$ curl -X POST  -H "Content-Type: application/json" -d '{"searchTerm":"learning"}' http://127.0.0.1:5000/api/v1/questions/search

```

Results

```http
{
  "current_category": null,
  "questions": [
    {
      "answer": "Udacity",
      "category": 1,
      "difficulty": 1,
      "id": 33,
      "question": "What is the best E-learning Plateform?"
    },
  ],
  "total_questions": 1
}
```


### GET all categories

```http
GET /api/v1/categories
```
Example
```http
$ curl http://127.0.0.1:5000/api/v1/categories
```




### GET endpoint to get questions based on category

```http
GET /api/v1/categories/${id}/questions
```
Example
```http
$ curl http://127.0.0.1:5000/api/v1/categories/1/questions
```
## Response Codes
We use standard HTTP codes to denote successful execution or indicate when errors occur. For some errors, the response will include
additional information about the error, including an application error
code and human readable error description.

### On successful execution

| Operation | HTTP Response Code | Response body                       |
| :-------- | :------- | :-------------------------------- |
| `GET`      | `200` | The requested data (order, document, etc) as JSON |
| `POST`     | `201` | Sucess message as JSON |

### Error Handling

| Error Condition | HTTP Response Code | Response body|
| :-------- | :------- | :-------------------------------- |
| `If the submitted data was invalid or the request was bad.` | `400` | Error entity, in JSON |
| `The user/client was not authorised` | `401` | Error entity, in JSON  |
| `If the resource requested is not found`  | `404` | Error entity, in JSON  |
| `Unprocessable Entity`| `422` | Error entity, in JSON  |

## Authors

- [@AbdessamadB](https://github.com/BOUMESLOUTAbdessamad)


## License

[MIT](https://choosealicense.com/licenses/mit/)

