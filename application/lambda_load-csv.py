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
        csv_reader = csv.reader(recList)#, delimiter=',', quotechar='"')
        for row in csv_reader:
            #print(row)
            if (firstrecord):
                firstrecord=False
                continue
            id = row[0]
            name = row[1].replace(',','').replace('$','') if row[1] else '-'
            account = row[2].replace(',','').replace('$','') if row[2] else 0
            email = row[3].replace(',','').replace('$','') if row[3] else 0
            mobile_number = row[4].replace(',','').replace('$','') if row[4] else 0
            prize = row[5].replace(',','').replace('$','') if row[5] else 0
            response = dyndb.put_item(
                TableName='winners',
                Item={
                'id' : {'N':str(id)},
                'name': {'S':name},
                'account': {'S':str(account)},
                'email': {'S':str(account)},
                'mobile number': {'S':str(mobile_number)},
                'prize': {'S': prize}
                }
            )
        print('Put succeeded:')
        return "abcdefg"
    except Exception, e:
        print (str(e))
        return "Probs an error" + ' ' + str(e) + ' ' + str(recList)
