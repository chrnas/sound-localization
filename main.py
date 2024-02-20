import json

import Positioning.PositioningHandler as Pos

startup_file = open("launchSettings.json", "r")
startup_settings = json.loads(startup_file.read())

if startup_settings["UIMode"] == "CLI":
    import CLI.mainLoop as UI

    UI.run_cli(Pos.pos_methods_data, 1)
elif startup_settings["UIMode"] == "GUI":
    pass
else:
    print("Launch setting for \"UIMode\" is incorrect. Shutting down")
    exit(-1)
