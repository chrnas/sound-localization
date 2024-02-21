import json


methods_file = open("Positioning/Methods.json", "r")
methods_data = json.loads(methods_file.read())


class PosMethodData:
    def __init__(self, file, method, active, weight) -> None:
        self.file = file
        self.method = method
        self.active = active
        self.weight = weight


pos_methods_data = {}

for method_data in methods_data:
    method_file = open("Positioning/" + method_data["filename"], "r")
    exec(method_file.read())
    print(method_data["name"])
    pos_methods_data[method_data["name"]] = PosMethodData(
        method_data["filename"], method_main, False, 1)
