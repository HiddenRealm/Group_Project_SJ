import boto3
import csv

def lambda_handler(event, context):
    region='eu-west-1'
    recList=[]
    try:            
        s3=boto3.client('s3')            
        dyndb = boto3.client('dynamodb', region_name=region)
        confile= s3.get_object(Bucket='testbucket123212321', Key='prizes.csv')
        recList = confile['Body'].read().split('\n')
        csv_reader = csv.reader(recList)
        count = 0

        for row in csv_reader2:
            if count == 199:
                break
            count += 1
            
            id = row[0]
            prize = row[1]
            
            response = dyndb.put_item(
                TableName='prizes',
                Item={
                'id' : {'N':str(id)},
                'prize': {'S':str(prize)}
                }
            )
        return "Worked"
        
    except Exception, e:
        print (str(e))
