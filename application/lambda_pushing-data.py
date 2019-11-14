import json
import boto3
from boto3.dynamodb.conditions import Key
import random

def lambda_handler(event, context):
    region='eu-west-1'
    dyndb = boto3.client('dynamodb', region_name=region)
    dyndb.put_item(TableName='prizedraw', 
    Item={'account':{'S':'Banana'},
    'name':{'S':'value2'},
    'email':{'S':'value2'},
    'mobile number':{'S':'value2'},
    'prize':{'S':'value2'}})
