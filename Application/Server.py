import socket
import threading
from Secret_Variables import Software_Activation_Key

# A Server Program that provides the antivirus service for it's clients
__author__ = 'Michael Khoshahang'

# Global Variables-
MSG_LENGTH = 2048
SERVER_IP = socket.gethostbyname(socket.gethostname())  # getting the Server IP
# Address that contains the Server ip and a random free port
ADDRESS = (SERVER_IP, 0)
ENCODING_FORMAT = 'utf-8'
clients = list()
latest_version = '3.1'

try:
    # AF_INET ---> working with IPv4 || SOCK_DGRAM ---> UDP
    # Creating a server socket object
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDRESS)  # Assign object to IP and PORT
    print('[Server] Initiating Server...')
    server.listen()  # waiting for clients || listening mode
    print(f'[Server] Running on {ADDRESS[0]}:{server.getsockname()[1]}')
except Exception as e:
    print(
        f'[Server] Could not run on {ADDRESS[0]}:{server.getsockname()[1]}. The error {e} occured.')


def receive_client_message(client_socket):
    """
    The function receives messages that are sent by the client.
    The function is working with the protocol defined in the client's program
    "send_request_to_server" function.
    :param client_socket: the client
    :return: the client's request
    :rtype: str
    """
    return client_socket.recv(MSG_LENGTH)


def send_message_to_client(response, client_socket):
    """
    The function creates a protocol which sends the response to the client.
    :param client_socket : the client
    :type: socket
    """
    if client_socket is not None:
        client_socket.send(response)
    else:
        print("[Server] Reference Error")


def handle_clients(client_object, address):
    """
    The function handles many clients.
    :param client_object: the client connection object
    :param address: the client's address
    :return: None
    """
    global clients
    while True:
        try:
            message = receive_client_message(
                client_object).decode(ENCODING_FORMAT)
            if message == 'get_active_clients':
                send_message_to_client(send_active_clients().encode(
                    ENCODING_FORMAT), client_object)
            elif message == 'getversion':
                send_message_to_client(latest_version.encode(
                    ENCODING_FORMAT), client_object)
            else:
                validation = 'False'
                if message == Software_Activation_Key:
                    validation = 'True'
                send_message_to_client(validation.encode(ENCODING_FORMAT),
                                       client_object)
        except:
            print(f"[Server] Disconnecting client {address[0]}:{address[1]}")
            clients.remove((client_object, address[0], address[1]))
            client_object.close()
            print(f'[Server] Active connections {len(clients)}')
            break


def main():
    """
    The main function of the Server module.
    :return: None
    """
    global server, clients

    while True:
        # enables connection and stores the connection object and IP of the client
        client_object, address = server.accept()
        # printing new connection address
        print(f'[Server] New connection from {address[0]}:{address[1]}')
        clients.append((client_object, address[0], address[1]))
        threading.Thread(target=handle_clients, args=(
            client_object, address)).start()
        print(f'[Server] Active connections {len(clients)}')


def send_active_clients():
    """
    The function sends to a specific client statuses of all the connected
    clients.
    :return: A string of the connected clients to the server
    :rtype: str
    """

    global clients
    if clients:
        response = ''
        for client in clients:
            response += f"{client[1]}:{str(client[2])}"
    else:
        response = 'There are no active clients right now.'
    return response


if __name__ == '__main__':
    main()
