import json
import positioning as pos
import ecohandling as eco
import cli


if __name__ == "__main__":
    startup_file = open("launch_settings.json", "r")
    startup_settings = json.loads(startup_file.read())

    if startup_settings["UIMode"] == "CLI":
        cli.run_cli(pos.pos_methods_data, eco.eco_methods_data)
    elif startup_settings["UIMode"] == "GUI":
        pass
    else:
        print("Launch setting for \"UIMode\" is incorrect. Shutting down")
        exit(-1)
