"""
made by Yonatan Ben Avi
constants file
"""
import platform
import os
BUFFER_SIZE = 10
MAX_DATA_RECEIVE_SIZE = 1729
CLIENTS_IP = '127.0.0.1'
PORT = 43216
PACKET_SIZE = 1024

# checks if operating system is osx or windows and sets variables accordingly
if platform.system() == 'Darwin':
    FILE_PATH = rf'{os.environ["HOME"]}/Desktop/client_python/'
    SPLIT_CHAR = '/'
    IMAGE_PATH = rf'{os.environ["HOME"]}/Desktop/Server_python/screen.png'
else:
    IMAGE_PATH = rf'{os.environ["USERPROFILE"]}\Desktop\Server_python/screen.png'
    FILE_PATH = rf'{os.environ["USERPROFILE"]}\Desktop\client_python\\'
    SPLIT_CHAR = '\\'

command_list = ['TIME', 'NAME', 'RAND', 'EXIT', 'TAKE_SCREENSHOT', 'HISTORY',
                'SEND_FILE', 'DIR', 'DELETE', 'COPY', 'EXECUTE', 'QUIT']


SERVERS_IP = '0.0.0.0'
no_parameter_command_list = ['TIME', 'NAME', 'RAND', 'EXIT', 'TAKE_SCREENSHOT', 'QUIT', 'HISTORY']


