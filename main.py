import json

startupfile = open("launchSettings.json", "r")
startupSettings = json.loads(startupfile.read())

import Positioning.PositioningHandler as Pos

if startupSettings["UIMode"] == "CLI":
    import CLI.mainLoop as UI
    UI.runCLI(Pos.positioningData, 1)
elif startupSettings["UIMode"] == "GUI":
    pass
else:
    print("Launch setting for \"UIMode\" is incorrect. Shutting down")
    exit(-1)