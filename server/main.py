import ujson
import ssl
import commands
import server

from datetime import datetime
from time import sleep
from threading import Thread
from sys import stdout

log = commands.Log("command_parser")
def parser():
    """
        CLI parser
        TODO: beautify code xD
    """
    command = input(f"{commands.colorama.Fore.CYAN}> {commands.colorama.Fore.WHITE}")
    if command is None:
        pass
    
    function = command.split(" ")[0]
    
    if function not in commands.COMMANDS:
        log.Error("Invalid command."); return
    arguments = command.replace(function + " ", "").split(" ")
    if arguments[0] != function:
        for k, v in enumerate(arguments):
            arguments[k] = "\"%s\"" % v
        arguments = ",".join(arguments)
        execute = f"commands.{function}({arguments})"
    else:
        execute = f"commands.{function}()"
    try:
        eval(execute)
    except(SyntaxError, TypeError):
        usage = commands.COMMANDS[function]["usage"]
        log.Error(f"Invalid usage. Usage: {usage}");


def main():
    colors = commands.colorama
    stdout.write(f"""
                {colors.Fore.CYAN}Welcome to WeTalk {colors.Fore.GREEN}1{colors.Fore.WHITE}.{colors.Fore.GREEN}0{colors.Fore.CYAN}
                  Made by {colors.Fore.GREEN}0xD{colors.Fore.WHITE}#{colors.Fore.MAGENTA}1337

                {colors.Fore.CYAN}Type {colors.Fore.WHITE}help {colors.Fore.CYAN}to see all commands

        \n""")
    while True:
        try:
            parser()
        except KeyboardInterrupt:
            stdout.write("Goodbye!\n")
            exit(0)


if __name__ == "__main__":
    main()