import json
import boto3
from boto3.dynamodb.conditions import Key
from random import shuffle

kong = boto3.client('lambda')

def lambda_handler(event, context):
    output = ran_name()
    
    dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
    table = dynamodb.Table('prizedraw')
    
    while True:
        temp = table.query(
            KeyConditionExpression=Key('account').eq(output))
        if temp['Items'] == output:
            output = ran_name()
        else:
            return output
    return output
    
    
def ran_name():
    output = ""
    
    in1 = kong.invoke(FunctionName='LetterGen',
                            InvocationType='RequestResponse')
    in2 = kong.invoke(FunctionName='NumGen',
                            InvocationType='RequestResponse')
    
    letter = json.loads(in1['Payload'].read().decode("utf-8"))
    number = json.loads(in2['Payload'].read().decode("utf-8"))
    
    temp = list(letter + str(number))
    shuffle(temp)
    output = ''.join(temp)
    return output
