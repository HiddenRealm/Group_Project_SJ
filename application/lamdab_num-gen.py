import json
from random import randrange

def lambda_handler(event, context):
    output=""
    num = (int(randrange(5)) + 5)
    
    for i in range(num):
        output += str(randrange(10))
    
    return int(output)
