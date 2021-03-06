# Group_Project_SJ
Group Project for QA, Prize Generator

## Intro
    The Generator need to be build in AWS as a minimum, it only needs minimal user input.
    The two most important parts of this project are to seperate the main elements and to have it hosted on AWS.
    These are both large steps from out individual projects.

    The rest of the read-me is the install & build instructions

## Contents:
Throughout this readme you are going to need to create a number of diffent AWS systems, this README should instruct you of how to do this.
These are all the things you should expect to find here.
    
    Single EC2 Instance for Jenkins
    Complete Usable EC2 Instance & It's AMI
    Load-Balancer
    Auto-Scaler
    All of the Lambda Functions needed to run the Application
    DynamoDB instance needed for Database
    SQS Configuration
    Pinpoint Configuration
    S3 Bucket

## EC2 Instances:
Before you start creating the actual instances you should make the IAM role & Security Groups.

###### IAM Role - Create Role:
1. Select type of trusted entity (AWS Service)
2. Choose the service thay will use this role (EC2)
3. Attach the following Permissions:
    1. AWSLambdaFullAccess
4. Name the Role 'EC2'
    
###### Security Group - Create Security Group:
1. Security Group Name 'Jenkins'
2. Inbound:
    1. Custom TCP Rule - TCP - 8080 - Custom - 0.0.0.0/0
    2. Custom TCP Rule - TCP - 8080 - Custom - ::/0
    3. SSH - TCP - 22 - Custom - 0.0.0.0/0
    4. SSH - TCP - 22 - Custom - ::/0
4. Outbound:
    1. All Traffic - All - All - 0.0.0.0/0

###### Security Group - Create Security Group:
1. Security Group Name 'Front-end Sec-Grp'
2. Inbound:
    1. HTTP - TCP - 80 - Custom - 0.0.0.0/0
    2. HTTP - TCP - 80 - Custom - ::/0
    3. SSH - TCP - 22 - Custom - 0.0.0.0/0
    4. SSH - TCP - 22 - Custom - ::/0
4. Outbound:
    1. All Traffic - All - All - 0.0.0.0/0

### Jenkins EC2 Instance:
            
###### For the Jenkins instance you need to launch a new EC2 Instance, for the settings i used:
1. Amazon Linux 2 AMI (Choose AMI)
2. t2.mirco (Choose Instance Type)
3. IAM Role - Drop down menu - Choose 'EC2' (Configure Instance)
4. Enable CloudWatch Detailed Monitoring (Configure Instance)
5. Select Existing security group (Configure Security Group)
6. Select 'Jenkins' (Configure Security Group)  
  
These are all of the changes you will need to make to the default settings  
Once you SSH into the instance you will need to install Jenkins.

    sudo yum install -y jenkins
    #you can check the status of the jenkins daemon with
    sudo systemctl status jenkins

Once thats done you can get your IPV4 from AWS and put that into a new tab, make sure the IPV4 is followed by ':8080'  
it will ask for a key, take the line of code in red and run the cat command on that path inside your jenkins instance,  
this should give you the key to access jenkins.  
  
Install the sugested addons and make an account.  
While you're waiting you can use the IPV4 to webhook to your forked version of this repo.

    http://52.18.231.98:8080/github-webhook/

It will look similar to that, but with your IPV4.  
Back to jenkins, create a new item & name it.  
Make sure its a 'Freestyle Project'  

Inside Jenkins Configure you need to:  
1. Paste your forked github link - Git - (Source Code Management)
2. Tick 'GitHub hook trigger for GITScm Polling (Build Triggers)
3. Paste the following commands inside the execute shell (Build):
        
        sudo docker login -u (dockerHub-Username) -p (dockerHub-Password)
        sudo docker build -t (dockerHub-Username)/prize-draw:latest .
        sudo docker push (dockerHub-Username)/prize-draw:latest
        sudo docker rmi -f (dockerHub-Username)/prize-draw

**You may need to disable CSRF Project in jenkins for the webhook to work**  
**This setting can be found by clicking 'Manage Jenkins'**  
**Then choosing 'Configure Global Security'**  
This should be the Jenkins EC2 Instance complete.

### EC2 AMI

###### For the Main instance you need to launch a new EC2 Instance, for the settings i used:
1. Amazon Linux 2 AMI (Choose AMI)
2. t2.mirco (Choose Instance Type)
3. IAM Role - Drop down menu - Choose 'EC2' (Configure Instance)
4. Enable CloudWatch Detailed Monitoring (Configure Instance)
5. Select Existing security group (Configure Security Group)
6. Select 'Front-end Sec-Grp' (Configure Security Group)

These are all of the changes you will need to make to the default settings  
Once you SSH into the instance you will need to install Docker:  

    sudo yum update -y
    sudo amazon-linux-extras install -y docker
    sudo service docker start
    #you can check the status of the docker daemon with
    sudo systemctl status docker
    
Next we are going to set up the crontab, to do this enter:  

    crontab -e

Inside this file enter:  

    * * * * * ./Scripts/Updating.sh
   
Now in the root directory type:  

     mkdir Scripts
     cd Scripts
     nano Updating.sh

Inside the Updating script paste in this code:  

    #!/bin/bash
    sudo docker pull (dockerHub-Username)/prize-draw
    sudo docker history --format "{{.CreatedAt}}" (dockerHub-Username)/prize-draw |head -n 1 > /tm
    p/temp.txt
    sudo docker rmi -f (dockerHub-Username)/prize-draw

    docker=$(head -n 1 /tmp/temp.txt)
    aws=$(head -n 1 /tmp/awsVersion.txt)

    if [ "$docker" != "$aws" ]
    then
    echo "$docker" > /tmp/awsVersion.txt
    sudo docker rm -f prize
    sudo docker rmi -f keep-this
    sudo docker pull (dockerHub-Username)/prize-draw
    sudo docker tag (dockerHub-Username)/prize-draw keep-this
    sudo docker run -d -p 80:5000 --name prize (dockerHub-Username)/prize-draw
    fi

Back on the AWS webpage select the EC2 instance, click Action -> Image -> Create Image  
Name it 'Prize-AMI'  

## Load-Balancer
Under 'Load Balancing' Select 'Load Balancers':  
1. Create Load Balancer
2. Application Load Balancer
3. Name it
4. Select any 2 Availability Zones
5. Select Existing Security Group - (Front-end Sec-Grp)
6. New Name
7. Create

## Auto-Scaler
Under 'Auto Scaling' Select 'Auto Scaling Groups':  
1. Create Auto Scaling group
2. Launch Configuration
3. My AMIs -> 'Prize-AMI'
4. t2.micro
5. Name it
6. IAM Role -> EC2
7. Tick Monitoring
8. Select Existing Security Group - (Front-end Sec-Grp)
9. Create Launch Configuration
10. Group Name
11. Choose any 2 Subnets
12. Advanced Details:
    1. Tick Load Balacing
    2. Target Groups -> Load Balancer #6 name
    3. Tick Monitoring
13. Create Auto Scaling Group


## Lambda's
Here you will find information on how to set up all of the Lambda's you will need to run this app.  
Before you start creating the actual lambdas you should make the IAM roles needed.

###### IAM Role - Create Roles:
DynamoFullAccess:  

    1. Select type of trusted entity (AWS Service)
    2. Choose the service thay will use this role (Lambda)
    3. Attach the following Permissions:
        1. AmazonDynamoDBFullAccess
    4. Name the Role 'DynamoFullAccess'

Dynamo+Lambda-Control:  

    1. Select type of trusted entity (AWS Service)
    2. Choose the service thay will use this role (Lambda)
    3. Attach the following Permissions:
        1. AWSLambdaFullAccess
        2. AmazonDynamoDBFullAccess
    4. Name the Role 'Dynamo+Lambda-Control'

S3-Admin-Access:

    1. Select type of trusted entity (AWS Service)
    2. Choose the service thay will use this role (Lambda)
    3. Attach the following Permissions:
        1. AmazonS3FullAccess
        2. AmazonDynamoDBFullAccess
    4. Name the Role 'S3-Admin-Access'

Lambda-SNS:

    1. Select type of trusted entity (AWS Service)
    2. Choose the service thay will use this role (Lambda)
    3. Attach the following Permissions:
        1. AWSLambdaFullAccess
        2. AdministratorAccess
    4. Name the Role 'Lambda-SNS'
    
LambdaToSQS:

    1. Select type of trusted entity (AWS Service)
    2. Choose the service thay will use this role (Lambda)
    3. Attach the following Permissions:
        1. AmazonSQSFullAccess
        2. AmazonDynamoDBFullAccess
        3. AdministratorAccess
    4. Name the Role 'LambdaToSQS'
    
Lambda:

    1. Select type of trusted entity (AWS Service)
    2. Choose the service thay will use this role (Lambda)
    3. Attach the following Permissions:
    4. Name the Role 'Lambda'

### LetterGen
1. Create function
2. Name 'LetterGen'
3. Runtime 'Python 3.7'
4. Choose an Execution role -> Use Existing -> Lambda
5. In the Fucntion code paste 'lambda_letter-gen.py' from the application folder of this repo.

### PrizeGen
1. Create function
2. Name 'PrizeGen'
3. Runtime 'Python 3.7'
4. Choose an Execution role -> Use Existing -> DynamoFullAccess
5. In the Fucntion code paste 'lambda_prize-gen.py' from the application folder of this repo.

### NumGen
1. Create function
2. Name 'NumGen'
3. Runtime 'Python 3.7'
4. Choose an Execution role -> Use Existing -> Lambda
5. In the Fucntion code paste 'lambda_num-gen.py' from the application folder of this repo.

### loadcsv
1. Create function
2. Name 'loadcsv'
3. Runtime 'Python 3.7'
4. Choose an Execution role -> Use Existing -> S3-Admin-Access
5. In the Fucntion code paste 'lambda_load-csv.py' from the application folder of this repo.
6. Change the S3 Bucket name to the name of the S3 bucket you create

### PushDataToQueue
1. Create function
2. Name 'PushDataToQueue'
3. Runtime 'Python 3.7'
4. Choose an Execution role -> Use Existing -> Lambda-SNS
5. In the Fucntion code paste 'lambda_pushing-data.py' from the application folder of this repo.

### ListenAndPush
1. Create function
2. Name 'ListenAndPush'
3. Runtime 'Python 3.7'
4. Choose an Execution role -> Use Existing -> LambdaToSQS
5. In the Fucntion code paste 'lambda_sqs-listen.py' from the application folder of this repo.
6. In the Designer hit '+ Add trigger':  
    1. Find SQS. 
    2. Select your SQS - StandardQueue
    3. Batch - 10
    4. Tick Enable Trigger

### AccountCreation
1. Create function
2. Name 'AccountCreation'
3. Runtime 'Python 3.7'
4. Choose an Execution role -> Use Existing -> Dynamo+Lambda-Control
5. In the Fucntion code paste 'lambda_account-creation.py' from the application folder of this repo.

## DynamoDB
### prizedraw
1. Create Table
2. Name - 'prizedraw'
3. Partition Key - 'account' (String)
4. Create

### prizes
1. Create Table
2. Name - 'prizes'
3. Partition Key - 'id' (Number)
4. Create

## SQS
1. Create New Queue
2. Name - 'StandardQueue'
3. Standard Queue
4. Quick-Create Queue

## Pinpoint (SES & SMS)
1. Create a Project
2. Name - 'SNS'
3. Click Configure on the email button:  
    1. Enter an email to get verified.
    2. Once verified you can send emails to this address.
    3. For the ability to send to any emails you need to open a ticket on the support center.
4. Click Configure on the SMS & Voice button:  
    1. Tick enable SMS channel for this project
    2. You start with a limit of $1 worth of texts
    3. To increase this you need to open a ticket on the support center.

## S3 Bucket
1. Create Bucket
2. Name it
3. Tick CloudWatch Request Metrics
4. Upload 'prizes.csv' into the bucket, its found in the application folder
