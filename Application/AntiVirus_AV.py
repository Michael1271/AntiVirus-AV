import os
import json
import threading
from Cryptography import *

# An AntiVirus User Main Program
__author__ = 'Michael Khoshahang'

latest_stored_version = '3.1'


def handle_services():
    """
    The function handles the initialization and changes of the software's services.
    all software services are written as json objects and encrypted.
    :return: None
    """
    if not os.path.exists('App_Files'):
        os.mkdir('App_Files')
        print('Creating App Files Folder')
    try:
        with open('App_Files/Services.txt', 'x+') as file:  # creating the file for the first time
            print('Creating Services file')
            # creating a services statuses file
            file.write(json.dumps({encrypt('Virus Scanner'):
                                   encrypt('ON')}) + '\n')
            file.write(json.dumps({encrypt('Updates Scanner'):
                                   encrypt('ON')}) + '\n')
            file.write(json.dumps({encrypt('Network Scanner'):
                                   encrypt('ON')}) + '\n')
            file.write(json.dumps({encrypt('Shredder'):
                                   encrypt('ON')}) + '\n')
            file.write(json.dumps({encrypt('Password Manager'):
                                   encrypt('ON')}) + '\n')
            file.write(json.dumps({encrypt('File App_Locker'):
                                   encrypt('ON')}) + '\n')
            file.write(json.dumps({encrypt('Logger'):
                                   encrypt('None')}) + '\n')
    except:
        pass

    with open('App_Files/Services.txt',
              'r') as file:  # reading the file and assigning it's values to the matched classes
        from Security import virus_scanner, updates_scanner, \
            network_scanner_object, logger_object
        from Identity import shredder, password_manager, file_locker
        file.seek(0)
        virus_scanner.set_service_status(
            decrypt(list(json.loads(file.readline()).values())[0]))
        updates_scanner.set_service_status(
            decrypt(list(json.loads(file.readline()).values())[0]))
        network_scanner_object.set_service_status(
            decrypt(list(json.loads(file.readline()).values())[0]))
        shredder.set_service_status(
            decrypt(list(json.loads(file.readline()).values())[0]))
        password_manager.set_service_status(
            decrypt(list(json.loads(file.readline()).values())[0]))
        file_locker.set_service_status(
            decrypt(list(json.loads(file.readline()).values())[0]))
        logger_object.set_service_status(
            decrypt(list(json.loads(file.readline()).values())[0]))


def start_antivirus():
    """
    The function starts the AntiVirus AV software if there
    is a permission to do so from the server.
    :return: None
    """
    threading.Thread(target=handle_services, args=()).start()
    from Graphic_Interface import welcome_screen, access_screen
    print('AntiVirus AV is Starting...')

    if not os.path.exists('App_Files/Instant_Login.txt'):
        # if using the software for the first time
        f = open('App_Files/Instant_Login.txt', 'x')
        f.close()
        print('Creating Instant login file')
        welcome_screen()
    else:
        with open('App_Files/Instant_Login.txt', 'r+') as file:
            content = file.read()
            if content:  # fast login
                access_screen(decrypt("".join(list(json.loads(content).keys()))),
                              decrypt(
                                  "".join(list(json.loads(content).values()))),
                              False)  # automatically login
            else:
                access_screen('', '', True)  # need to log in manually


if __name__ == '__main__':
    import Client

    Client.main()
