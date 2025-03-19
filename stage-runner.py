import argparse
import subprocess
import time


def main():
    # Create a parser with the same arguments as needed
    parser = argparse.ArgumentParser(
        description="Run the executable from dist directory")
    parser.add_argument(
        'server_port', help='Port number to bind the server to')
    parser.add_argument(
        'client_port', help='Port number to bind the client to')
    args = parser.parse_args()

    # Run the executable in the background with all command line arguments
    cmd = ["./dist/server_runner"] + [args.server_port]

    # Start the process in the background
    server_process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE
    )

    print("Server started")

    # Run the executable in the background with all command line arguments
    cmd = ["./dist/client_runner"] + [args.client_port]

    # Start the process in the background
    client_process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE
    )

    print("Client started")

    # Wait for the server process to complete
    server_stdout, server_stderr = server_process.communicate()
    print("\nServer process finished")
    if server_stdout:
        print(f"Server Output:\n{server_stdout.decode()}")
    if server_stderr:
        print(f"Server Standard Error:\n{server_stderr.decode()}")

    # Wait for the client process to complete
    client_stdout, client_stderr = client_process.communicate()
    print(
        f"Client process finished")
    if client_stdout:
        print(f"Client Output:\n{client_stdout.decode()}")
    if client_stderr:
        print(f"Client Standard Error:\n{client_stderr.decode()}")


if __name__ == "__main__":
    main()
