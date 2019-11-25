import json
import boto3
import os
from botocore.exceptions import ClientError

AWS_REGION = "eu-west-1"
SENDER = "James Ford <jamestaylor034@gmail.com>"

CONFIGURATION_SET = "Group_Project-SJ"
SUBJECT = "Amazon Pinpoint Test (SDK for Python)"

CHARSET = "UTF-8"

pinpoint = boto3.client('pinpoint')
client = boto3.client('ses', region_name=AWS_REGION)


def lambda_handler(event, context):

    sqs = boto3.client('sqs')

    queue_url = 'https://sqs.eu-west-1.amazonaws.com/402060165867/StandardQueue'
    
    prize = event['prize']
    
    if event['mobile'] == '':
        a ="None"
    else:
        a = event['mobile']
        text(prize,a)
        
    if event['email'] == '':
        b ="None"
    else:
        b = event['email']
        email(prize,b)

    response = sqs.send_message(
        
        MessageBody="Test drive",
        
        QueueUrl=queue_url,
        
        DelaySeconds=10,
        
        MessageAttributes={
            
            'account': {
                'DataType': 'String',
                'StringValue': event['account']
            },
            
            'email': {
                'DataType': 'String',
                'StringValue': b
            },
            
            'mobile_number': {
                'DataType': 'String',
                'StringValue': a
            },
            
            'name': {
                'DataType': 'String',
                'StringValue': event['name']
            },
            
            'prize': {
               'DataType': 'String',
                'StringValue': event['prize']
            }
            
        }
    )
    return response
    
    
def text(prize, num):
    message = 'You have won ' + prize + '. Well played'
    temp = str(num[0:])
    number = '+44' + temp
    
    pinpoint.send_messages(
        ApplicationId='87832a40b77b44139eb9bcbfebeb7585',
        MessageRequest={
            'Addresses': {
                number: {'ChannelType': 'SMS'}
            },
            'MessageConfiguration': {
                'SMSMessage': {
                    'Body': message ,
                    'MessageType': 'PROMOTIONAL'
                }
            }
        }
    )
    
def email(prize, email):
    TOADDRESSES = [email]
    
    BODY_TEXT = """
    """ + prize + """"""
    
    BODY_HTML = """
        <html>
        <head></head>
        <body>
          <h1>Prize Draw - Group Project</h1>
          <p>You have won """ + prize + """. Well played.</p>
        </body>
        </html>
    """
    
    
    try:
        response = client.send_email(
            Source=SENDER,
            Destination={
                'ToAddresses': TOADDRESSES,
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    }
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            ConfigurationSetName=CONFIGURATION_SET,
        )
    except ClientError as e:
        print(e)
    else:
        print("Email sent!")
        print("Message ID: " + response['MessageId'])
