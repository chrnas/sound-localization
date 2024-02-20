import json

startupfile = open("launchSettings.json", "r")
startupSettings = json.loads(startupfile.read())

import Positioning.PositioningHandler as Pos
import EcoHandling.EcoHandler as eco

if startupSettings["UIMode"] == "CLI":
    import CLI.mainLoop as UI
    UI.runCLI(Pos.pos_methods_data, eco.eco_methods_data)
elif startupSettings["UIMode"] == "GUI":
    pass
else:
    print("Launch setting for \"UIMode\" is incorrect. Shutting down")
    exit(-1)