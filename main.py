from internal_commands import INTERNAL_COMMANDS
import os
import subprocess
import sys
import time

# Define a simulated PATH for external Python scripts
MY_PATH = ["C:\\path\\scripts", "C:\\path\\scripts2"]

def execute_internal_command(command, args, stdin=None, stdout=None):
    """Executes internal shell commands."""
    if command in INTERNAL_COMMANDS:
        original_stdout = sys.stdout
        original_stdin = sys.stdin

        if stdout:
            sys.stdout = stdout
        if stdin:
            sys.stdin = stdin

        INTERNAL_COMMANDS[command](args)

        sys.stdout = original_stdout
        sys.stdin = original_stdin
    else:
        print(f"Command not found: {command}")

def execute_external_command(command, args, stdin=None, stdout=None):
    """Executes external Python scripts or system commands."""
    try:
        # Check if command exists in MY_PATH
        for directory in MY_PATH:
            full_path = os.path.join(directory, command)
            if os.path.exists(full_path):
                proc = subprocess.Popen(["python", full_path] + args, stdin=stdin, stdout=stdout)
                return proc

        # Fallback to system commands
        proc = subprocess.Popen(f'{command} ' + ' '.join(f'"{arg}"' if ' ' in arg else arg for arg in args), stdin=stdin, stdout=stdout, shell=True)

        return proc
    except FileNotFoundError:
        print(f"Command not found: {command}")

def handle_redirection_and_pipe(user_input):
    """Handles piping and redirection."""
    pipe_commands = user_input.split("|")
    num_commands = len(pipe_commands)
    previous_process = None

    for i, cmd in enumerate(pipe_commands):
        cmd_parts = cmd.strip().split()

        stdin = None
        stdout = None

        # Output redirection
        if ">" in cmd_parts:
            idx = cmd_parts.index(">")
            output_file = cmd_parts[idx + 1]
            stdout = open(output_file, "w")
            cmd_parts = cmd_parts[:idx]

        # Input redirection
        if "<" in cmd_parts:
            idx = cmd_parts.index("<")
            input_file = cmd_parts[idx + 1]
            stdin = open(input_file, "r")
            cmd_parts = cmd_parts[:idx]

        command = cmd_parts[0].lower()
        args = cmd_parts[1:]

        # For piping, we need to pass the output of one command to the next
        if i == 0:  # First command
            if command in INTERNAL_COMMANDS:
                execute_internal_command(command, args, stdin=stdin, stdout=stdout or subprocess.PIPE)
            else:
                if num_commands == 1:
                    previous_process = execute_external_command(command, args, stdin=stdin, stdout=stdout)
                else:
                    previous_process = execute_external_command(command, args, stdin=stdin,
                                                                stdout=stdout or subprocess.PIPE)
        elif i < num_commands - 1:  # Middle commands
            if command in INTERNAL_COMMANDS:
                execute_internal_command(command, args)
            else:
                previous_process = execute_external_command(command, args, stdin=previous_process.stdout, stdout=subprocess.PIPE)
        else:  # Last command in pipe
            if command in INTERNAL_COMMANDS:
                execute_internal_command(command, args, stdin=previous_process.stdout, stdout=stdout)
            else:
                previous_process = execute_external_command(command, args, stdin=previous_process.stdout, stdout=stdout)

    if stdout:
        stdout.close()
    if stdin:
        stdin.close()

def main():
    while True:
        time.sleep(0.5)
        try:
            # Custom prompt showing username, current directory, and "> "
            user_prompt = f"{os.getlogin()}@{os.getcwd()}> "
            user_input = input(user_prompt).strip()

            if not user_input:
                continue

            # Handle pipes and redirections
            if "|" in user_input or ">" in user_input or "<" in user_input:
                handle_redirection_and_pipe(user_input)
                continue

            # Split input into command and arguments
            parts = user_input.split()
            command = parts[0].lower()
            args = parts[1:]

            # Execute internal or external commands
            if command in INTERNAL_COMMANDS:
                execute_internal_command(command, args)
            else:
                execute_external_command(command, args)

        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
