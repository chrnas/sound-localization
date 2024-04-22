
from .commands import pos_list, pos_activate, \
    pos_deactivate, pos_weight, run_once, run_cont, \
    stop, mic_list, mic_add, mic_remove


def print_startup():
    print("Startup complete")
    print("Welcome to the program")


def get_command_input():
    command_string = input()

    command_data = command_string.split(" ")

    return command_data


def handle_command(command_data, pos_data, eco_data):
    command = command_data[0]
    args = []
    if len(command_data) > 1:
        args = command_data[1:]

    match command:
        case "test":
            print("Args are:")
            for i in args:
                print(i)
            print("testcommand executed")
        case "PosList":
            pos_list(pos_data)
        case "PosActivate":
            pos_activate(pos_data, args)
        case "PosDeactivate":
            pos_deactivate(pos_data, args)
        case "PosWeight":
            pos_weight(pos_data, args)
        case "PosActivate":
            pos_activate(pos_data, args)
        case "PosDeactivate":
            pos_deactivate(pos_data, args)
        case "PosWeight":
            pos_weight(pos_data, args)
        case "RunOnce":
            run_once(args[0])
        case "RunCont":
            run_cont(args[0])
        case "Stop":
            stop()
        case "MicList":
            mic_list()
        case "MicAdd":
            mic_add(args)
        case "MicRemove":
            mic_remove(args[0])
        case "exit":
            exit(0)
        case _:
            print("Unknown command")


print_startup()


def run_cli(positioning_data, eco_data):
    running = True
    while running:
        command = get_command_input()

        handle_command(command, positioning_data, eco_data)
