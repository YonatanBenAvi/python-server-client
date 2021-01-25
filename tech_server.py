"""
made by Yonatan Ben Avi
the server makes a connection with the client
and gets from the client what to do
"""
#   Heights sockets Ex. 2.7 template - server side
#   Author: Barak Gonen, 2017

from PIL import ImageGrab
import socket
import time
import random
import shutil
import subprocess
from constants import *


def receive_client_request(client_socket):
    """Receives the full message sent by the client

    Works with the protocol defined in the client's
    "send_request_to_server" function

    Returns:
        command: such as DIR, EXIT, SCREENSHOT etc
        params: the parameters of the command

    Example: 12DIR c:\cyber as input will result in
    command = 'DIR', params = 'c:\cyber'
    """
    buffer = int(client_socket.recv(BUFFER_SIZE).decode('utf-8'))
    data = client_socket.recv(buffer).decode('utf-8').split()
    if len(data) == 1:
        return data[0], None
    elif len(data) == 0:
        return None, None
    else:
        return data[0], ' '.join(data[1:])


def check_client_request(command, params):
    """Check if the params are good.

    For example, the filename to be copied actually exists

    Returns:
        valid: True/False
        error_msg: None if all is OK, otherwise some error message
    """
    if command in command_list:
        if command in no_parameter_command_list:
            if params is None:
                return True, None
            else:
                return False, "command shouldn't accept parameter's"
        else:
            if params is None:
                return False, 'params are none type'
            elif command == 'EXECUTE':
                if os.path.exists(params):
                    return True, None
                else:
                    return False, 'params are not valid'
            elif os.path.exists(params):
                return True, None
            elif command == 'COPY':
                if os.path.exists(params.split()[0]) and \
                        os.path.exists(params.split()[1]):
                    return True, None
                else:
                    return False, 'params are not valid'
            else:
                return False, 'params are not valid'
    else:
        return False, 'command is not recognized by server'


def handle_client_request(command, params):
    """Create the response to the client,
    given the command is legal and params are OK

    For example, return the list of filenames in a directory

    Returns:
        response: the requested data
    """
    if command == 'TIME':
        return 'local time: ' + time.ctime(time.time())
    elif command == 'NAME':
        return "My name is Yonatan's server"
    elif command == 'RAND':
        return 'Random number is: ' + str(random.randint(0, 1000))
    elif command in ('EXIT', 'QUIT'):
        return 'you have requested to disconnect from the server'
    elif command == 'TAKE_SCREENSHOT':
        im = ImageGrab.grab()
        try:
            im.save(IMAGE_PATH)
            return 'the image has been saved successfully to: ' + IMAGE_PATH
        except FileNotFoundError:
            print('the image path is invalid')
            return 'there was a problem saving the image to the folder'
    elif command == 'SEND_FILE':
        with open(params, 'rb') as file:
            done = False
            array_file = []
            while not done:
                data = file.read(PACKET_SIZE)
                if data == b'':
                    break
                array_file.append(data)
            return array_file
    elif command == 'DIR':
        return '\n'.join(os.listdir(params))
    elif command == 'DELETE':
        os.remove(params)
        return params + ' has been deleted successfully'
    elif command == 'COPY':
        shutil.copy(params.split()[0], params.split()[1])
        return f'{params.split()[0]}\nhas been successfully ' \
               f'copied to:\n{params.split()[1]}\n'
    elif command == 'EXECUTE':
        if platform.system() == 'Darwin':
            subprocess.call(["/usr/bin/open", "-W", "-n", "-a", params])
            return f'{params} has been opened successfully'
        else:
            subprocess.call(params)
            return f'{params} has been opened successfully'
    else:
        return 'command has not been recognized by server'


def send_response_to_client(response, client_socket, error_message=b'0'):
    """Create a protocol which sends the response to the client

    The protocol should be able to handle short responses as well as files
    (for example when needed to send the screenshot to the client)
    """
    client_socket.send(error_message)
    if isinstance(response, str):
        # protocol to send string messages
        client_socket.send(str(len(response.encode('utf-8')))
                           .zfill(BUFFER_SIZE).encode('utf-8'))
        client_socket.send(response.encode('utf-8'))
    elif isinstance(response, list):
        # protocol to send files messages
        len_message = str(sum([len(bytes(x)) for x in response])) \
            .zfill(BUFFER_SIZE)
        client_socket.send(len_message.encode('utf-8'))
        for i in response:
            client_socket.send(i)


def handle_single_client(client_socket):
    """
    program receives the command and parameters from the client
    checks if command and params are valid and handles the request
    accordingly. if not valid the program sends an error message
    back to the client.
    the program returns whether the server should exit or not.

    :param client_socket:
    :return: True/False
    """
    client_done = False
    while not client_done:
        # handle requests until user asks to exit
        try:
            command, params = receive_client_request(client_socket)
        except (ValueError, ConnectionResetError):
            print("the client isn't responding correctly"
                  " therefore the server is disconnecting"
                  " from the client")
            return False
        command = command.upper()
        valid, error_msg = check_client_request(command, params)
        if valid:
            response = handle_client_request(command, params)
            send_response_to_client(response, client_socket)
        else:
            send_response_to_client(error_msg, client_socket, b'1')

        if command == 'EXIT':
            client_socket.close()
            print('you have requested to disconnect the server')
            return True
        elif command == 'QUIT':
            client_socket.close()
            return False


def handle_clients(server_socket):
    """
    makes a connection with a client until a client disconnects
    the server
    :param server_socket:
    :return:
    """
    server_done = False
    while not server_done:
        client_socket, address = server_socket.accept()
        # handle requests until user asks to exit
        server_done = handle_single_client(client_socket)
    server_socket.close()


def main():
    """
    accepts a connection from the client and communicates with it
    """
    # open socket with client
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVERS_IP, PORT))
    server_socket.listen(1)
    handle_clients(server_socket)


if __name__ == '__main__':
    main()
