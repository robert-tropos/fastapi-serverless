import os
from fastapi import FastAPI
from mangum import Mangum
import boto3
from uuid import uuid4

# USERS_TABLE = os.environ['USERS_TABLE']
USERS_TABLE = "test"
client = boto3.client('dynamodb')

stage = os.environ.get('STAGE', None)
openapi_prefix = f"/{stage}" if stage else "/"

# app = FastAPI(title="MyAwesomeApp") # Here is the magic
app = FastAPI(title="MyAwesomeApp", openapi_prefix=openapi_prefix) # Here is the magic

@app.get("/status")
def root():
    return {"status": "I am alive CICD!"}

@app.post("/add_quote/{password}/{quote_msg}")
def add_new_quote(quote_msg, password):

    if password == "troposiscool":

        quote_id = str(uuid4())

        client.put_item(TableName=USERS_TABLE,
            Item={
                'userId': {'S': quote_id},
                'quote': {'S': quote_msg},
            })

        return {'msg':"quote added",
                "quote_id":quote_id,
                "quote":quote_msg}
    else:
        return {"error": "no access for you!"}

@app.get("/")
def get_random_quote():
    db = boto3.resource('dynamodb')
    table = db.Table('test')
    response = table.scan(
        Limit=1,
        ExclusiveStartKey={
            'userId': str(uuid4())
        },
        ReturnConsumedCapacity='TOTAL'
    )
    print(response)
    if response["Items"]:
        return {"quote":response["Items"][0]["quote"]}

    else:
        return {"quote":"I'm having trouble finding random quotes - AWS lambda"}


handler = Mangum(app)