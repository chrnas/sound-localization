import json
import os

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, "methods.json")
methods_file = open(filename, "r")
methods_data = json.loads(methods_file.read())


class PosMethodData:
    def __init__(self, file, method) -> None:
        self.file = file
        self.method = method
        self.settings = {}


pos_methods_data = {}
for method_data in methods_data:
    method_file = open(os.path.join(dirname, method_data["filename"]), "r")
    exec(method_file.read())
    method_object = None
    exec("method_object = " + method_data["method"])
    pos_methods_data[method_data["name"]] = PosMethodData(
        method_data["filename"], method_object
    )

# for method_data in methods_data:
#    method_file = open(os.path.join(dirname, method_data["filename"]), "r")
#    exec(method_file.read())
#    print(method_data["name"])
#    pos_methods_data[method_data["name"]] = PosMethodData(
#        method_data["filename"], MethodClass(), False, 1)
