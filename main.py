import json
import positioning as pos
import cli


if __name__ == "__main__":
    startup_file = open("launch_settings.json", "r")
    startup_settings = json.loads(startup_file.read())

    if startup_settings["UIMode"] == "CLI":
        cli.run_cli(pos.PosMethodData, 1)
    elif startup_settings["UIMode"] == "GUI":
        pass
    else:
        print("Launch setting for \"UIMode\" is incorrect. Shutting down")
        exit(-1)
