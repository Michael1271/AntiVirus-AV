import base64
import json
import os
import random
import subprocess
import sys
import time
from ntpath import basename
import winshell
from Cryptography import encrypt

# A program that deals with Privacy Services.
# The program includes Shredding Services, Firewall management Services and File locking Services.
__author__ = "Michael Khoshahang"


class Shredder(object):
    """
    Class of a Shredder object.
    """

    def __init__(self):
        """
        The function is a constructor of the Shredder object.
        """
        self.status = None

    def get_service_status(self):
        """
        The function returns the shredder's service status.
        :return: the shredder status
        :rtype: str
        """
        return self.status

    def set_service_status(self, status):
        """
        The function sets the shredder's service status to be the given status.
        :return: None
        """
        self.status = status
        if status == 'ON':
            with open('App_Files/Services.txt', 'r+') as file:
                lines_list = file.readlines()
                lines_list[3] = json.dumps(
                    {encrypt('Shredder'): encrypt('ON')})
                lines_list[3] += '\n'
                file.seek(0)
                file.truncate(0)
                file.write("".join(lines_list))
        elif status == 'OFF':
            with open('App_Files/Services.txt', 'r+') as file:
                lines_list = file.readlines()
                lines_list[3] = json.dumps(
                    {encrypt('Shredder'): encrypt('OFF')})
                lines_list[3] += '\n'
                file.seek(0)
                file.truncate(0)
                file.write("".join(lines_list))


class Firewall(object):
    """
    Class of a Firewall object.
    """

    def __init__(self):
        """
        The function is a constructor of the Firewall object.
        """
        self.status = self.get_firewall_status()

    def get_firewall_status(self):
        """
        The function returns the firewall's status- active/deactive.
        :return: the firewall's status- ON/OFF
        :rtype: str
        """
        try:
            status = os.popen(
                'netsh advfirewall show allprofiles state').read()
            if status.count('ON') == 3:
                return 'ON'
            return 'OFF'
        except:
            pass

    def get_service_status(self):
        """
        The function returns the firewall's service status.
        :return: the firewall's service status
        :rtype: str
        """
        return self.status

    def activate_firewall(self):
        """
        The function deactivates Windows Firewall
        :return: if the Windows FireWall's activation was successful
        :rtype: bool
        """
        try:
            os.popen('netsh advfirewall set privateprofile state off')
            print('Windows Firewall is now Activated.\n')
            self.set_service_status('ON')
            return True
        except Exception as e:
            print(
                f'Could not Active Windows Firewall. The error {e} occurred.\n')
            return False

    def deactivate_firewall(self):
        """
        The function deactivates Windows Firewall
        :return: if the Windows FireWall's deactivation was successful
        :rtype: bool
        """
        try:
            os.popen('netsh advfirewall set privateprofile state off')
            print('Windows Firewall is now Deactivated.\n')
            self.set_service_status('Off')
            return True
        except Exception as e:
            print(
                f'Could not Deactive Windows Firewall. The error {e} occurred.\n')
            return False

    def set_service_status(self, status):
        """
        The function sets the firewall's service status to be the given status.
        :return: None
        """
        self.status = status
        if status == 'ON':
            self.deactivate_firewall()
        else:
            self.activate_firewall()


class Password_Manager(object):
    """
    Class of a Password_Manager object.
    """

    def __init__(self):
        """
        The function is a constructor of the Pasword Manager object.
        """
        self.status = None

    def get_service_status(self):
        """
        The function returns the password manager's service status.
        :return: the password manager's service status
        :rtype: str
        """
        return self.status

    def set_service_status(self, status):
        """
        The function sets the password manager's service status to be the given status.
        :return: None
        """
        self.status = status
        if status == 'ON':
            with open('App_Files/Services.txt', 'r+') as file:
                lines_list = file.readlines()
                lines_list[4] = json.dumps(
                    {encrypt('Password Manager'): encrypt('ON')})
                lines_list[4] += '\n'
                file.seek(0)
                file.truncate(0)
                file.write("".join(lines_list))
        elif status == 'OFF':
            with open('App_Files/Services.txt', 'r+') as file:
                lines_list = file.readlines()
                lines_list[4] = json.dumps(
                    {encrypt('Password Manager'): encrypt('OFF')})
                lines_list[4] += '\n'
                file.seek(0)
                file.truncate(0)
                file.write("".join(lines_list))


class File_Locker(object):
    """
    Class of a File App_Locker object.
    """

    def __init__(self):
        """
        The function is a constructor of the File App_Locker object.
        """
        self.status = None

    def get_service_status(self):
        """
        The function returns the file locker's service status.
        :return: the file locker's service status
        :rtype: str
        """
        return self.status

    def set_service_status(self, status):
        """
        The function sets the file locker's service status to be the given status.
        :return: None
        """
        self.status = status
        if status == 'ON':
            with open('App_Files/Services.txt', 'r+') as file:
                lines_list = file.readlines()
                lines_list[5] = json.dumps(
                    {encrypt('File App_Locker'): encrypt('ON')})
                lines_list[5] += '\n'
                file.seek(0)
                file.truncate(0)
                file.write("".join(lines_list))
        elif status == 'OFF':
            with open('App_Files/Services.txt', 'r+') as file:
                lines_list = file.readlines()
                lines_list[5] = json.dumps(
                    {encrypt('File App_Locker'): encrypt('OFF')})
                lines_list[5] += '\n'
                file.seek(0)
                file.truncate(0)
                file.write("".join(lines_list))


# Global Varaibles
shredder = Shredder()
firewall = Firewall()
password_manager = Password_Manager()
file_locker = File_Locker()


def progress_duration(seconds):
    """
    the function gets the seconds of scanning and turns them to
    HOURS:MINUTES:SECONDS syntax
    :param seconds: the given seconds of the scan
    :return: string with the time of the scan
    :rtype: str
    """
    hours = str(seconds // 3600)
    minutes = str((seconds % 3600) // 60)
    seconds = str((seconds % 3600) % 60)

    if float(hours) != 0:
        return f'{hours[:-2]} Hours, {minutes[:-2]} Minutes and {"%.2f" % float(seconds)} Seconds.\n'
    elif float(minutes) != 0:
        return f'{minutes[:-2]} Minutes and {"%.2f" % float(seconds)} Seconds.\n'
    elif float(seconds) != 0:
        return f'{"%.2f" % float(seconds)} Seconds.\n'


def shred(mode='Basic', path=''):
    """
    The Function shreds files in order to protect the user's identity.
    :param mode: the shredding mode: Basic, Safe, Complete
    :param path: the path to be shredded: Recycle Bin or Temporary files
    :return: None
    """
    start_time = time.perf_counter()
    failed_shredding = list()
    if mode == 'Basic':
        repeat = 1
    elif mode == 'Safe':
        repeat = 5
    else:  # mode == 'Complete':
        repeat = 10

    if path == 'Let Me Choose':
        path = random.choice(['Recycle Bin', 'Temporary Files'])

    executed = False  # An auxiliary boolean variable
    if path == 'Recycle Bin':
        object_list = list(winshell.recycle_bin())
        if object_list:  # if list is not empty
            print(f'Starting Shredding process at {path}\n')
            executed = True
            print(f'We are getting ready to shred {len(object_list)} files')
            time.sleep(1)
            for index, file_path in enumerate(object_list):
                for _ in range(repeat):
                    try:
                        success = False
                        file_path = '\\'.join(
                            file_path.original_filename().split('\\'))  # adding double slash (\\) in the file_path
                        # undeleting the selected file
                        winshell.undelete(file_path.original_filename())
                        if not os.path.isdir(file_path):  # is file
                            success = shred_file(file_path)
                            if not success:  # if didn't succeed shredding the file
                                failed_shredding.append(file_path)
                        # deleting the selected file again
                        winshell.delete_file(file_path.original_filename())
                    except:
                        pass
                if (index + 1) == (len(object_list)):  # last file
                    sys.stdout.write(
                        f'\rShredding ({int(((index + 1) / len(object_list)) * 100)}%): {basename(file_path)}last')
                else:
                    sys.stdout.write(
                        f'\rShredding ({int(((index + 1) / len(object_list)) * 100)}%): {basename(file_path)}')

            # Emptying recycle bin.
            winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=False)
            print('\nShredding Report:')
            print(f'Successfully shred: {len(object_list) - len(failed_shredding)} '
                  f'out of {len(object_list)} Files || Failed to shred : '
                  f'{len(failed_shredding)} files')
            finish_time = time.perf_counter()
        else:
            print('There are no items in the Recycle Bin to be shredded\n')

    elif path == 'Temporary Files':
        directory_path = r'c:\windows\temp'
        object_list = os.listdir(directory_path)
        if object_list:
            print(f'Starting Shredding process at {path}\n')
            executed = True
            print(f'We are getting ready to shred {len(object_list)} files')
            time.sleep(1)
            for index, file_path in enumerate(object_list):
                if index == (len(object_list) - 1):  # last file
                    sys.stdout.write(
                        f'\rShredding ({int((index / len(object_list) - 1) * 100)}%): {basename(file_path)}last')
                else:
                    sys.stdout.write(
                        f'\rShredding ({int((index / len(object_list) - 1) * 100)}%): {basename(file_path)}')
                for _ in range(repeat):
                    try:
                        if not os.path.isdir(file_path):  # is file
                            success = shred_file(file_path)
                            if not success:  # if didn't succeed shredding the file
                                failed_shredding.append(file_path)
                    except:
                        pass
            process = subprocess.Popen('del /S /Q /F %s\\*.*' % directory_path, shell=True, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)  # deleting all temporary files
            process.communicate()
            for file in object_list:
                os.remove(file)

            finish_time = time.perf_counter()
            print('\n\nShredding Report:')
            print(f'Successfully shredded: {len(object_list) - len(failed_shredding)} '
                  f'out of {len(object_list)} Files || Failed to shred : '
                  f'{len(failed_shredding)} files. Deleted: {len(object_list)}')

    if executed:
        print(
            f'Shredding has been finished in {progress_duration(finish_time - start_time)}')
        from Graphic_Interface import display_notifications
        display_notifications('Shredding process has finished.')
    else:
        print(
            f"""We didn't shred any files since we couldn't find any in {path} """)


def shred_file(file):
    """
    An auxiliary function that shreds the given file.
    :param file: the given file's path to be shred
    :return: True/False if the process was successful
    :rtype: bool
    """
    try:
        with open(file, 'wb') as file:
            file.truncate(0)
            for i in range(random.randint(99999, 999999)):
                file.write(base64.b64encode(bytes(f'{i} \n',
                                                  'ascii')))  # writing random bytes on the file in order to make it harder to recover it
        return True
    except Exception as e:
        print(f'Cannot open the file {file}. The error {e} occurred')
        return False


def add_rule(rule_name, file_path):
    """
    The Function adds the given rule to Windows Firewall.
    :param rule_name: the name of the rule
    :param file_path: the path of the file
    :return: None
    """
    try:
        if rule_name is not None and file_path is not None:
            subprocess.call(
                f"netsh advfirewall firewall add rule name={rule_name} dir=out action=block enable=no program={file_path}",
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print(
                f'Rule {rule_name} for {file_path} was added successfully to Windows Firewall.\n')
        else:
            pass
    except:
        pass


def modify_rule(rule_name, status):
    """
    The Function Enables or Disables a specific rule, 0 = Disable / 1 = Enable.
    :param rule_name: the name of the rule to be modified
    :param status: the rule's modified status- 0 = Disable / 1 = Enable.
    :return: None
    """
    try:
        if rule_name is not None and status is not None:
            status, message = ("yes", "Enabled") if status else (
                "no", "Disabled")
            subprocess.call(
                f"netsh advfirewall firewall set rule name={rule_name} new enable={status}",
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print(f'Rule {rule_name} {message}')
        else:
            pass
    except:
        pass


def modify_port(port, protocol, status):
    """
    The Function Allows or Blocks a specific Port through Windows Firewall.
    :param port: the port to be allowed through windows firewall
    :param protocol: the type of the port (TCP/UDP)
    :param status: The status of the port - 0 = Block / 1 = Allow.
    :return: None
    """
    if port != '' and protocol != '' and status != '':
        if str(status) == '0':
            status = 'block'
        else:  # str(status) == '1':
            status = 'allow'
        try:
            subprocess.call(
                f"""netsh advfirewall firewall add rule name="{status.capitalize()} Port {port}" protocol={protocol} dir=out localport={port} action={status}""",
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print(
                f'Port: {port} Protocol: {protocol} is now {status}ed through Windows Firewall.')
        except:
            print(
                f'Port: {port} Protocol: {protocol} could not be {status}ed through Windows Firewall.')
    else:
        print('The given port or protocol or status was empty.')


def add_password(table):
    """
    The function gets a password and notes for the password and adds a new_data password to the password's file.
    :param table: the table of the data
    :return: None
    """
    try:
        with open('App_Files/Passwords.txt', 'x'):  # creating saved_passwords file
            pass
    except:
        pass

    new_data = table.get_sheet_data()
    new_data = [lst for lst in new_data if
                ['', ''] not in lst]  # takes the new data from the table- prevents adding empty rows

    if new_data:  # prevent adding empty rows
        try:
            with open('App_Files/Passwords.txt', 'r') as file:
                saved_data = eval(file.read())
        except:
            saved_data = list()
        if saved_data:
            with open('App_Files/Passwords.txt', 'w+') as file:
                saved_data[saved_data.index(['', ''])] = new_data
                file.write(f'{str(saved_data)}')
        else:  # adding new data for the first time
            with open('App_Files/Passwords.txt', 'w+') as file:
                file.write(f'{str(table.get_sheet_data())}')
        table.update()
        with open('App_Files/Passwords.txt', 'w') as file:
            file.write(str(table.get_sheet_data()))


def display(table, button):
    """
    The function dispalys or hides the passwords and notes of the table.
    :param table: the table of the data
    :param button: the show/hide data button
    :return: None
    """
    table.selection_clear()
    table.deselect(table.get_currently_selected())
    data = table.get_sheet_data()
    if data.count(['', '']) != 20:  # There is new data in the table
        with open('App_Files/Passwords.txt', 'w') as file:
            file.write(str(data))
        button.config(text='Show')
        table.set_sheet_data([["" for j in range(2)] for j in range(20)])

    else:  # There isn't new data in the table
        try:
            with open('App_Files/Passwords.txt', 'r') as file:
                data = eval(file.read())
            button.config(text='Hide')
            table.set_sheet_data(data)
        except:
            pass
    table.update()


def clear_data(table):
    """
    The function clears all the saved data from the table and from the file App_Files/Passwords.txt
    param table: the table of the data
    :return: None
    """
    try:
        with open('App_Files/Passwords.txt', 'w+'):
            pass
    except:
        pass
    table.set_sheet_data([["" for j in range(2)] for j in range(20)])


def locker(command, file_path):
    """
    The function locks/unlocks in the the given file path according to the command
    :param command: the command to be executed: lock/unlock
    :param file_path: the file's path to be locked/unlocked
    :return: None
    """
    try:
        file_path = rf'{file_path}'
        if command == 'lock':
            # denys access to the file
            print(os.popen(f'echo Y|cacls {file_path} /P everyone:n').read())
        else:  # command = 'unlock'
            # allows access to the file
            print(os.popen(f'echo Y|cacls {file_path} /P everyone:f').read())
    except Exception as e:
        print(
            f'Could not lock/unlock file: {basename(file_path)}. The error {e} occured.')
