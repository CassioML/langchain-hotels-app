from fastapi import FastAPI, Depends

from utils.ai import capitalize, get_answer
from utils.db import get_keyspace, get_session
from utils.models import QuestionRequest, Answer

# helpers
def fa_db():
    yield get_session()

def fa_ks():
    yield get_keyspace()

# app

app = FastAPI()


@app.get('/')
def index():
    return {'data': 'Here it is.'}


@app.get('/capitalize/{input}')
def cap(input):
    return {'data': capitalize(input)}


@app.get('/people/{n}')
def people(n: int, db=Depends(fa_db), ks=Depends(fa_ks)):
    rows = db.execute(f'SELECT * FROM {ks}.people LIMIT %s', (n, ))

    returned = [
        {
            'city': row.city,
            'name': row.name,
        }
        for row in rows
    ]

    return {'data': returned}


@app.post('/qa')
def qa(question_request: QuestionRequest) -> Answer:
    answer = get_answer(question_request.question)
    return Answer(
        question=question_request.question,
        answer=answer,
    )
