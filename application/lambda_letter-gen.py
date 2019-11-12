import json
from random import randrange

letters=['a', 'b', 'c', 'd', 'e', 'f', 'g', 
         'h', 'i', 'j', 'k', 'l', 'n', 'm', 
         'o', 'p', 'q', 'r', 's', 't', 'u', 
         'v', 'w', 'x', 'y', 'z',]

def lambda_handler(event, context):
    output=""
    num = (int(randrange(10)) + 5)
    
    for i in range(num):
        output += letters[randrange(26)]
    
    return output
