#import json
import boto3

def lambda_handler(event, context):
    region='eu-west-1'
    dyndb = boto3.client('dynamodb', region_name=region)
    dyndb.put_item(TableName='prizedraw', 
    Item={'account':{'S':event["Records"][0]["messageAttributes"]['account']['stringValue']},
    'name':{'S':event["Records"][0]["messageAttributes"]['name']['stringValue']},
    'email':{'S':event["Records"][0]["messageAttributes"]['email']['stringValue']},
    'mobile number':{'S':event["Records"][0]["messageAttributes"]['mobile_number']['stringValue']},
    'prize':{'S':event["Records"][0]["messageAttributes"]['prize']['stringValue']}
    })
    return event["Records"][0]["messageAttributes"]["account"]["stringValue"]
