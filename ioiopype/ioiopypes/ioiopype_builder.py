import json

class IOIOPypeBuilder:
    def __init__(self, filepath):
        with open(filepath, 'r') as file:
            data = json.load(file)
'''
READ JSON FILE
PARSE FILE
INITIALIZE NODES
CONNECT NODES
'''