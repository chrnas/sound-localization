import json
import cli
import ecohandling

eco_file = open("EcoHandling/Methods.json", "r")
eco_data = json.loads(eco_file.read())

class EcoHandlingMethod:
    def __init__(self, filename, method) -> None:
        self.filename = filename
        self. method = method

eco_methods_data = {}

for eco_method in eco_data:
    eco_file = open("EcoHandling/" + eco_method["filename"], "r")
    exec(eco_file.read)
    eco_methods_data[eco_method["name"]] = EcoHandlingMethod(eco_method["filename"], cli.method_main)