"""
made by Yonatan Ben Avi
the client makes a connection with the server
and tells the server what to do
"""
#   Heights sockets Ex. 2.7 template - client side
#   Author: Barak Gonen, 2017
import socket
import platform
import os
from constants import *


def valid_request(request):
    """Check if the request is valid (is included in the available commands)

    Return:
        True if valid, False if not
    """
    return False if request == ''\
        else request.split()[0].upper() in command_list


def send_request_to_server(my_socket, request):
    """Send the request to the server. First the length
     of the request (2 digits), then the request itself

    Example: '04EXIT'
    Example: '12DIR c:\\cyber'
    """
    my_socket.send((str(len(request.encode('utf-8'))).zfill(BUFFER_SIZE) +
                    request).encode('utf-8'))


def handle_server_response(my_socket, request):
    """Receive the response from the server and handle it, according to the request

    For example, DIR should result in printing the contents to the screen,
    while SEND_FILE should result in saving the received file
        and notifying the user
    """
    request_command = request.split()[0].upper()
    error_check = my_socket.recv(1).decode('utf-8')
    buffer = int(my_socket.recv(BUFFER_SIZE).decode('utf-8'))
    if not request_command == 'SEND_FILE':
        data = my_socket.recv(buffer).decode('utf-8')
        print(data)
    else:
        # reads 1024 bytes until message is fully read
        data = my_socket.recv(PACKET_SIZE)
        buffer_left = buffer - len(data)
        while buffer_left > 0:
            data += my_socket.recv(PACKET_SIZE)
            buffer_left = buffer - len(data)
        # checks if there was an error
        if error_check == '0':
            try:
                request_list = request.split(SPLIT_CHAR)
                with open(rf'{FILE_PATH}{request_list[-1]}', 'wb') as file:
                    file.write(data)
                print('file sent successfully')
            except FileNotFoundError:
                print('The file path is incorrect')
        else:
            # prints the error message
            print(data.decode('utf-8'))


def main():
    """
    creates a connection to the server and communicates with it
    """
    # open socket with the server
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((CLIENTS_IP, PORT))

    # print instructions
    print('Welcome to remote computer application. Available commands are:')
    print('\n'.join(command_list))

    done = False
    # loop until user requested to exit
    while not done:
        request = input("Please enter command:\n")
        if valid_request(request):
            try:
                send_request_to_server(my_socket, request)
                handle_server_response(my_socket, request)
            except (ValueError, ConnectionResetError):
                done = True
                print("the server isn't responding correctly therefore"
                      " the client is disconnecting")
            if request.upper() == 'EXIT' or request.upper() == 'QUIT':
                done = True
        else:
            print('the command is not valid')
    my_socket.close()


if __name__ == '__main__':
    main()
