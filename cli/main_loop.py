def print_startup():
    print("Startup complete")
    print("Welcome to the program")


def get_command_input():
    print("Write a command:")
    command_string = input()

    command_data = command_string.split(" ")

    return command_data


def handle_command(command_data):
    command = command_data[0]
    args = command_data[1:]

    if command == "test":
        print("Args are:")
        for i in args:
            print(i)
        print("testcommand executed")
    elif command == "ECOList":
        pass
    elif command == "ECOSet":
        pass
    elif command == "PosList":
        pass
    elif command == "PosActivate":
        pass
    elif command == "PosDeactivate":
        pass
    elif command == "PosWeight":
        pass
    elif command == "RunOnce":
        pass
    elif command == "RunCont":
        pass
    elif command == "Stop":
        pass
    elif command == "MicList":
        pass
    elif command == "MicAdd":
        pass
    elif command == "MicRemove":
        pass
    elif command == "exit":
        exit(0)
    else:
        print("Unknown command")


print_startup()


def run_cli(positioning_data, eco_data):
    running = True
    while running:
        command = get_command_input()

        handle_command(command)
