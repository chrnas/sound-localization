import json
import os

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'methods.json')


methods_file = open(filename, "r")
methods_data = json.loads(methods_file.read())


class PosMethodData:
    def __init__(self, file, method, active, weight) -> None:
        self.file = file
        self.method = method
        self.active = active
        self.weight = weight


pos_methods_data = {}

# for method_data in methods_data:
#    method_file = open(os.path.join(dirname, method_data["filename"]), "r")
#    exec(method_file.read())
#    print(method_data["name"])
#    pos_methods_data[method_data["name"]] = PosMethodData(
#        method_data["filename"], MethodClass(), False, 1)
