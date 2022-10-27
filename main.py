import os
from fastapi import FastAPI
from mangum import Mangum
import boto3

# USERS_TABLE = os.environ['USERS_TABLE']
USERS_TABLE = "test"
client = boto3.client('dynamodb')

stage = os.environ.get('STAGE', None)
openapi_prefix = f"/{stage}" if stage else "/"

# app = FastAPI(title="MyAwesomeApp") # Here is the magic
app = FastAPI(title="MyAwesomeApp", openapi_prefix=openapi_prefix) # Here is the magic

@app.get("/")
def root():
    return {"API is running":"aw yeah CICD"}

@app.get("/hello")
def hello_world():
    return {"message": "Hello World"}

@app.post("/post/{quote_id}")
def post_quote(quote_id):
    client.put_item(TableName=USERS_TABLE,
        Item={
            'userId': {'S': quote_id},
            'quote': {'S': 'test_quote'}
        })

    return {'msg':"quote added"}

@app.post("/add_quote/{quote_id}/{quote_msg}")
def add_new_quote(quote_id, quote_msg):
    client.put_item(TableName=USERS_TABLE,
        Item={
            'userId': {'S': quote_id},
            'quote': {'S': quote_msg}
        })

    return {'msg':"quote added",
            "userId":quote_id,
            "quote":quote_msg}


@app.get("/get/{quote_id}")
def post_quote(quote_id):
    resp = client.get_item(TableName=USERS_TABLE,
        Key={
            'userId': {'S': quote_id},
        })

    item = resp.get("Item")
    if not item:
        return {"error":"quote doesn't exist"}
    
    return {
        "quote_id_retrieved": item.get('userId').get('S'),
        "quote_retrieved": item.get('quote').get('S'),
        }


handler = Mangum(app)