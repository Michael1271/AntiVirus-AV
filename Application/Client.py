import os
import socket
import sys
from getmac import get_mac_address
from Cryptography import encrypt_to_hash
from Graphic_Interface import get_server_details_screen
from Secret_Variables import Software_Activation_Key

# A client socket program
__author__ = 'Michael Khoshahang'

# Global Variables-
MSG_LENGTH = 2048
get_server_details_screen()
from Graphic_Interface import SERVER_IP, SERVER_PORT

try:
    ADDRESS = (SERVER_IP, int(SERVER_PORT))
except Exception as e:
    print(
        f'[Client] Could not connect to the server on {SERVER_IP}:{SERVER_PORT}. The error {e} occurred.')
    os.system("pause")
    sys.exit(1)

ENCODING_FORMAT = 'utf-8'
DISCONNECT_MESSAGE = 'disconnect'
is_active = False

try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Creating a client socket object
    client.connect(ADDRESS)
    print(f'[Client] Connecting to {ADDRESS[0]}:{ADDRESS[1]}')
    print(f'[Client] Connected to {SERVER_IP}:{SERVER_PORT}')
except Exception as e:
    print(
        f'[Client] Could not connect to the server on {SERVER_IP}:{SERVER_PORT}. The error {e} occurred.')
    os.system("pause")
    sys.exit(1)


def send_request_to_server(client_socket, request):
    """
    The function sends the request to the server.
    :param client_socket : the client
    :param request : the request
    :return: None
    """
    client_socket.send(request)


def receive_server_response(client_socket):
    """
    The function receives the response from the server and returns it.
    :param client_socket : the Client
    :return: the client's request
    :rtype: str
    """
    return client_socket.recv(MSG_LENGTH)


def main():
    """
    The main function of the client module which handles the initial connection
    to the server and starts the software if there is a permission to do so.
    :return: None
    """
    from AntiVirus_AV import start_antivirus
    global is_active, client
    try:
        send_request_to_server(
            client, f'{Software_Activation_Key}'.encode(ENCODING_FORMAT))
        permission = receive_server_response(client).decode(ENCODING_FORMAT)
        if permission == 'True':
            is_active = True
            start_antivirus()
        else:
            os.system("pause")
            sys.exit(1)
    except:
        os.system("pause")
        sys.exit(1)


def get_active_clients():
    """
    The function gets the active status of the all the connected clients.
    :return: A string of all the active clients details
    :rtype: str
    """
    global client
    send_request_to_server(
        client, 'get_active_clients'.encode(ENCODING_FORMAT))
    response = receive_server_response(client).decode(ENCODING_FORMAT)
    if response != '':
        string = ''
        sentence = ''
        connections_list = list()

        for letter in response:
            if letter != '~':
                sentence += letter
            else:
                connections_list.append(sentence)
                sentence = ''

        for connection_address in connections_list:
            if connection_address != '':
                string += f"""IP Address: {connection_address} || Mac Address: {encrypt_to_hash(get_mac_address(ip=str(connection_address[:connection_address.find(':')]), network_request=True))} || Status: Online\n"""
    else:
        string = f'Could not analyze active clients.'
    return string
