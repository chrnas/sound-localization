import CLI.commands

def printStartup():
    print("Startup complete")
    print("Welcome to the program")

def getCommandInput():
    print("Write a command:")
    commandString = input()

    commandData = commandString.split(" ")

    return commandData

def handleCommand(commandData):
    command = commandData[0]
    args = commandData[1:]

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
        print("Unkown command")

printStartup()

def runCLI(positioningData, ecoData):
    running = True
    while running:
        command = getCommandInput()

        handleCommand(command)
        
