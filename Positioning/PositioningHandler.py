import json

methodsFile = open("Positioning/Methods.json", "r")
methodsData = json.loads(methodsFile.read())
class PositioningData:
    names = {}
    files = {}
    methods = {}
    active = {}
    weights = {}

    def addMethod(function, name):
        methods[name] = function
        active[name] = False
        weights[name] = 1.0

positioningData = PositioningData()

for methodData in methodsData:
    methodFile = open("Positioning/" + methodData["filename"], "r")
    exec(methodFile.read())
    print(methodData["name"])
    positioningData.addMethod(methodMain, methodData["name"])
    
