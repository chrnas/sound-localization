import argparse
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import InMemoryHistory
from .commands import pos_list, pos_set_setting, calculate_position, mic_list, mic_add, mic_remove, mic_add_soundfile


def print_startup():
    print("Startup complete")
    print("Welcome to the position estimation program based on sound files")


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="CLI for estimating positions based on sound files.")
    subparsers = parser.add_subparsers(dest='command')

    # Test command
    subparsers.add_parser(
        'test', help='Execute a test command to verify CLI functionality.')

    # PosList command
    subparsers.add_parser(
        'PosList', help='List all available positioning methods with their details.')

    # PosSetSetting command
    pos_set_setting_parser = subparsers.add_parser(
        'PosSetSetting', help='Set a specific setting for a specific positioning method.')
    pos_set_setting_parser.add_argument(
        'position', help='Name of the positioning method.')
    pos_set_setting_parser.add_argument(
        'setting_name', help='Name of the setting.')
    pos_set_setting_parser.add_argument(
        'setting_value', help='Value of the setting.')

    # CalculatePosition command
    calculate_position_parser = subparsers.add_parser(
        'CalculatePosition', help='Calculate the position using a specified positioning method.')
    calculate_position_parser.add_argument(
        'method', help='Name of the positioning method to use.')

    # MicList command
    subparsers.add_parser('MicList', help='List all configured microphones.')

    # MicAdd command
    mic_add_parser = subparsers.add_parser(
        'MicAdd', help='Add a new microphone configuration.')
    mic_add_parser.add_argument(
        'mic', nargs=3, help='Name, latitude, and longitude of the new microphone.')
    mic_add_parser.add_argument(
        '--soundfile', help='Path to the sound file recorded by the microphone.')

    # MicRemove command
    mic_remove_parser = subparsers.add_parser(
        'MicRemove', help='Remove a microphone configuration.')
    mic_remove_parser.add_argument(
        'mic', help='Name of the microphone to remove, or "all" to remove all microphones.')

    # MicAddSoundFile command
    mic_add_soundfile_parser = subparsers.add_parser(
        'MicAddSoundFile', help='Add a sound file to an existing microphone.')
    mic_add_soundfile_parser.add_argument(
        'mic', help='Name of the microphone.')
    mic_add_soundfile_parser.add_argument(
        'soundfile', help='Path to the sound file to add.')

    return parser


def handle_command(args, positioning_methods):
    match args.command:
        case "test":
            print("Args are:")
            for arg in vars(args):
                if arg != 'command':
                    print(f"{arg}: {getattr(args, arg)}")
            print("test command executed")
        case "PosList":
            pos_list(positioning_methods)
        case "PosSetSetting":
            pos_set_setting(positioning_methods, args.position,
                            args.setting_name, args.setting_value)
        case "CalculatePosition":
            calculate_position(positioning_methods, args.method)
        case "MicList":
            mic_list()
        case "MicAdd":
            mic_add(args.mic, args.soundfile)
        case "MicRemove":
            mic_remove(args.mic)
        case "MicAddSoundFile":
            mic_add_soundfile(args.mic, args.soundfile)
        case "exit":
            print("Exiting CLI.")
            exit(0)
        case _:
            print("Unknown command")


command_list = [
    "test", "PosList", "PosSetSetting", "CalculatePosition",
    "MicList", "MicAdd", "MicRemove", "MicAddSoundFile", "exit"
]


def run_cli(positioning_data):
    parser = create_parser()
    completer = WordCompleter(command_list, ignore_case=True)
    history = InMemoryHistory()

    while True:
        try:
            input_str = prompt("> ", completer=completer, history=history)
            if input_str.strip().lower() == 'exit':
                print("Exiting CLI.")
                break
            args = parser.parse_args(input_str.split())
            handle_command(args, positioning_data)
        except SystemExit:
            # argparse throws a SystemExit exception if parsing fails, we'll catch it to keep the loop running
            continue
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    print_startup()
    positioning_data = {}  # Replace with actual initialization
    run_cli(positioning_data)
