import json
import boto3
from boto3.dynamodb.conditions import Key
import random

def lambda_handler(event, context):
    randomnum = random.randint(1,101)
    region='eu-west-1'
    recList=[]
    dyndb = boto3.resource('dynamodb', region_name=region)
    table = dyndb.Table('prizes')
    response = table.query(
        KeyConditionExpression=Key('id').eq(randomnum))
      
    for i in response['Items']:
        output = i['prize']
    return output
