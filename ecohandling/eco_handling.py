import json

eco_file = open("EcoHandling/methods.json", "r")
eco_data = json.loads(eco_file.read())


class EcoHandlingMethod:
    def __init__(self, filename, method) -> None:
        self.filename = filename
        self. method = method


eco_methods_data = {}

for eco_method in eco_data:
    eco_file = open("ecohandling/" + eco_method["filename"], "r")
    exec(eco_file.read(100))
    eco_methods_data[eco_method["name"]] = EcoHandlingMethod(
        eco_method["filename"], method_main)
