from fastapi import FastAPI
from pydantic import BaseModel
from DB import database
app = FastAPI()

class regModel(BaseModel):
    first_name : str
    last_name : str
    user_name : str
    phone_no : int
    age : int
    gmail : str
    password : str







@app.get('/')
def get_data():
    response = database.table('new_user').select("*").execute()
    return response.data


@app.post('/register')

def post_data(data:regModel):
    user_data = data.dict()
    response = database.table('new_user').insert(user_data).execute()

    return {'message':'user has been registered','response':response.data}
