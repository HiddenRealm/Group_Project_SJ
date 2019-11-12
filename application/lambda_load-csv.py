import boto3
import csv

def lambda_handler(event, context):
    region='eu-west-1'
    recList=[]
    try:            
        s3=boto3.client('s3')            
        dyndb = boto3.client('dynamodb', region_name=region)
        confile= s3.get_object(Bucket='testbucket123212321', Key='winners.csv')
        recList = confile['Body'].read().split('\n')
        firstrecord=True
        csv_reader = csv.reader(recList)
        
        for row in csv_reader:
            
            try:
                print(row[1])
                temp == row[1]
            except:
                break
            
            
            if (firstrecord):
                firstrecord=False
                continue
            
            
            id = row[0]
            name = row[1].replace(',','').replace('$','') 
            account = row[2].replace(',','').replace('$','')
            email = row[3].replace(',','').replace('$','') if row[3] else 'NULL'
            mobile_number = row[4].replace(',','').replace('$','') if row[4] else 'NULL'
            prize = row[5].replace(',','').replace('$','')
            
            print(id, name, account, email, mobile_number, prize)
            
            response = dyndb.put_item(
                TableName='prizedraw',
                Item={
                'id' : {'N':str(id)},
                'name': {'S':name},
                'account': {'S':str(account)},
                'email': {'S':str(email)},
                'mobile number': {'S':str(mobile_number)},
                'prize': {'S': prize}
                }
            )
    except Exception, e:
        print (str(e))
