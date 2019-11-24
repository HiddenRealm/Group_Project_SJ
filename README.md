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
    Auto-Scaler
    Load-Balancer
    All of the Lambda Functions needed to run the Application
    DynamoDB instance needed for Database
    SQS Configuration
    Pinpoint Configuration
    S3 Bucket
    
## Jenkins EC2 Instance:
Before creating an instance you should make a IAM Role & Security Group:
    IAM Role - Create Role:
        * Select type of trusted entity (AWS Service)
        * Choose the service thay will use this role (EC2)
        * Attach the following Permissions:
            * AWSLambdaFullAccess
        * Name the Role 'EC2'
    Security Group - Create Security Group:
        * Security Group Name 'Jenkins'
        * Inbound:
            * Custom TCP Rule - TCP - 8080 - Custom - 0.0.0.0/0
            * Custom TCP Rule - TCP - 8080 - Custom - ::/0
            * SSH - TCP - 22 - Custom - 0.0.0.0/0
            * SSH - TCP - 22 - Custom - ::/0
        * Outbound:
            * All Traffic - All - All - 0.0.0.0/0
        
For the Jenkins instance you need to launch a new EC2 Instance, for the settings i used:
    * Amazon Linux 2 AMI (Choose AMI)
    * t2.mirco (Choose Instance Type)
    * IAM Role - Drop down menu - Choose 'EC2' (Configure Instance)
    * Enable CloudWatch Detailed Monitoring (Configure Instance)
    * Select Existing security group (Configure Security Group)
    * Select 'Jenkins' (Configure Security Group)
These are all of the changes you will need to make to the default settings
Once you SSH into the instance you will need to install Jenkins
  
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
    * Paste your forked github link - Git - (Source Code Management)
    * Tick 'GitHub hook trigger for GITScm Polling (Build Triggers)
    * Paste the following commands inside the execute shell (Build):
        
        sudo docker login -u (dockerHub-Username) -p (dockerHub-Password)
        sudo docker build -t (dockerHub-Username)/prize-draw:latest .
        sudo docker push (dockerHub-Username)/prize-draw:latest
        sudo docker rmi -f (dockerHub-Username)/prize-draw

--- You may need to disable CSRF Project in jenkins for the webhook to work ---
--- This setting can be found by clicking 'Manage Jenkins' ---
--- Then choosing 'Configure Global Security' ---
This should be the Jenkins EC2 Instance complete.

## EC2 AMI


## Auto-Scaler


## Load-Balancer


## Lambda's
Here you will find information on how to set up all of the Lambda's you will need to run this app.
### LetterGen

### PrizeGen

### NumGen

### loadcsv

### PushDataToQueue

### ListenAndPush

### AccountCreation

## DynamoDB


## SQS


## Pinpoint (SES & SMS)


## S3 Bucket

