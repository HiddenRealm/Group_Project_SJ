import json
import boto3
from boto3.dynamodb.conditions import Key
import random

def lambda_handler(event, context):
    region='eu-west-1'
    dyndb = boto3.client('dynamodb', region_name=region)
    
    if event['mobile'] == '':
        a ="None"
    else:
        a = event['mobile']
        
    if event['email'] == '':
        b ="None"
    else:
        b = event['email']    
        
    dyndb.put_item(TableName='prizedraw', 
    Item={'account':{'S':event['account']},
    'name':{'S':event['name']},
    'email':{'S':b},
    'mobile number':{'S':a},
    'prize':{'S':event['prize']}})
