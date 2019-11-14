import json
from random import randrange

prizes = ['1', '2', '3', '4', '5']

def lambda_handler(event, context): 
    return prizes[randrange(len(prizes))]
