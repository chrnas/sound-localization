from .commands import *

def print_startup():
    print("Startup complete")
    print("Welcome to the program")


def get_command_input():
    print("Write a command:")
    command_string = input()

    command_data = command_string.split(" ")

    return command_data


def handle_command(command_data, pos_data, eco_data):
    command = command_data[0]
    args = command_data[1:]
    print(command)
    if command == "test":
        print("Args are:")
        for i in args:
            print(i)
        print("testcommand executed")
    elif command == "ECOList":
        eco_list(eco_data, args)
    elif command == "ECOSet":
        eco_set(eco_data, args)
    elif command == "PosList":
        pos_list(args[0])
    elif command == "PosActivate":
        pos_activate(args[0])
    elif command == "PosDeactivate":
        pos_deactivate(args[0])
    elif command == "PosWeight":
        pos_weight(args[0])
    elif command == "PosActivate":
        pos_activate(pos_data, args)
    elif command == "PosDeactivate":
        pos_deactivate(pos_data, args)
    elif command == "PosWeight":
        pos_weight(pos_data, args)
    elif command == "RunOnce":
        run_once(args[0])
    elif command == "RunCont":
        run_cont(args[0])
    elif command == "Stop":
        stop()
    elif command == "MicList":
        mic_list(args[0])
    elif command == "MicAdd":
        mic_add(args[0])
    elif command == "MicRemove":
        mic_remove(args[0])
    elif command == "exit":
        exit(0)
    else:
        print("Unknown command")


print_startup()

def run_cli(positioning_data, eco_data):

    running = True
    while running:
        command = get_command_input()

        handle_command(command, positioning_data, eco_data)
