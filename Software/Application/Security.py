from __future__ import print_function
import concurrent.futures
import hashlib
import json
import logging
import os
import platform
import socket
import subprocess
import sys
import threading
import time
from ntpath import basename
from pathlib import Path
from virus_total_apis import ApiError
from virus_total_apis import PrivateApi
from virus_total_apis import PublicApi
import Web_Scrapper
from Cryptography import encrypt
# Data for Virus Total scanner service
from Secret_Variables import Virus_Total_Service_Secret_API

# A program that deals with Security Services.
# The program includes Virus Scanning Services, Updating services and Network
# Scanning Services.

__author__ = "Michael Khoshahang"


class Virus_Scanner(object):
    """
    A class of A Virus Scanner instance.
    """

    def __init__(self):
        """
        The function is a constructor of the Virus Scanner object.
        """
        self._status = None
        try:
            self._virus_total_service = PublicApi(
                Virus_Total_Service_Secret_API)
        except:
            try:
                self._virus_total_service = PrivateApi(
                    Virus_Total_Service_Secret_API)
            except ApiError as e:
                print(f'Could not active Virus Total Virus Scanner Service.'
                      f'The error {e} occured.')
                sys.exit(0)  # Stopping the function

    def get_virus_total_service(self):
        """
        The function returns the virus total service object.
        :return: the virus total service object
        :rtype: object
        """
        return self._virus_total_service

    def get_service_status(self):
        """
        The function returns the virus scanner's service status.
        :return: the virus total service scanner's service status
        :rtype: str
        """
        return self._status

    def set_service_status(self, status):
        """
        The function sets the virus scanner's service status to be the
        given status.
        :return: None
        """
        self._status = status
        if status == 'ON':
            with open('App_Files/Services.txt', 'r+') as file:
                lines_list = file.readlines()
                lines_list[0] = json.dumps({encrypt('Virus Scanner'):
                                            encrypt('ON')})
                lines_list[0] += '\n'
                file.seek(0)
                file.truncate(0)
                file.write("".join(lines_list))
        elif status == 'OFF':
            with open('App_Files/Services.txt', 'r+') as file:
                lines_list = file.readlines()
                lines_list[0] = json.dumps(
                    {encrypt('Virus Scanner'): encrypt('OFF')})
                lines_list[0] += '\n'
                file.seek(0)
                file.truncate(0)
                file.write("".join(lines_list))


class Updates_Scanner(object):
    """
    Class of a Updates Scanner instance.
    """

    def __init__(self):
        """
        The function is a constructor of the Updates Scanner object.
        """
        self._status = None

    def get_service_status(self):
        """
        The function returns the updates scanner's service status.
        :return: the updates scanner's service status
        :rtype: str
        """
        return self._status

    def set_service_status(self, status):
        """
        The function sets the updates scanner's service status to be the
        given status.
        :return: None
        """
        self._status = status
        if status == 'ON':
            with open('App_Files/Services.txt', 'r+') as file:
                lines_list = file.readlines()
                lines_list[1] = json.dumps(
                    {encrypt('Updates Scanner'): encrypt('ON')})
                lines_list[1] += '\n'
                file.seek(0)
                file.truncate(0)
                file.write("".join(lines_list))
        elif status == 'OFF':
            with open('App_Files/Services.txt', 'r+') as file:
                lines_list = file.readlines()
                lines_list[1] = json.dumps(
                    {encrypt('Updates Scanner'): encrypt('OFF')})
                lines_list[1] += '\n'
                file.seek(0)
                file.truncate(0)
                file.write("".join(lines_list))


class Network_Scanner(object):
    """
    Class of a Network Scanner instance.
    """

    def __init__(self):
        """
        The function is a constructor of the Network Scanner object.
        """
        self._status = None

    def get_service_status(self):
        """
        The function returns the network scanner's service status.
        :return: the network scanner's service status
        :rtype: str
        """
        return self._status

    def set_service_status(self, status):
        """
        The function sets the network scanner's service status to be the
        given status.
        :return: None
        """
        self._status = status
        if status == 'ON':
            with open('App_Files/Services.txt', 'r+') as file:
                lines_list = file.readlines()
                lines_list[2] = json.dumps(
                    {encrypt('Network Scanner'): encrypt('ON')})
                lines_list[2] += '\n'
                file.seek(0)
                file.truncate(0)
                file.write("".join(lines_list))
        elif status == 'OFF':
            with open('App_Files/Services.txt', 'r+') as file:
                lines_list = file.readlines()
                lines_list[2] = json.dumps(
                    {encrypt('Network Scanner'): encrypt('OFF')})
                lines_list[2] += '\n'
                file.seek(0)
                file.truncate(0)
                file.write("".join(lines_list))


class Logger(object):
    """
    Class of a logger instance
    """

    def __init__(self):
        """
        The function initializing the logger instance.
        :return: None
        """
        self._status = None
        self._logger = logging.getLogger()

    def start_logging(self):
        """
        The function starts the logger
        :return: None
        """
        self._logger.setLevel(logging.INFO)
        if not os.path.exists('app_logs'):
            os.mkdir('app_logs')
        os.chdir('app_logs')
        for i in range(1, 10000):
            if os.path.exists(f'logs{i}.log'):
                with open(f'logs{i}.log', 'r') as file:
                    if file.read():  # log file is already writen
                        try:
                            # next log file is not already created
                            with open(f'logs{i + 1}.log', 'x'):
                                pass
                            self.file_handler = logging.FileHandler(filename=f'logs{i + 1}.log', encoding='utf-8',
                                                                    mode='w')
                            break
                        except:
                            pass
                    else:
                        self.file_handler = logging.FileHandler(
                            filename=f'logs{i}.log', encoding='utf-8', mode='w')
                        break
            else:
                with open(f'logs{i}.log', 'x'):
                    pass
                self.file_handler = logging.FileHandler(
                    filename=f'logs{i}.log', encoding='utf-8', mode='w')
                break
        os.chdir('..')
        self.console_handler = logging.StreamHandler()
        self.file_handler.setFormatter(logging.Formatter(
            '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        self._logger.addHandler(self.file_handler)
        self._logger.addHandler(self.console_handler)

    def get_logger(self):
        """
        The function returns the logger instance
        :return: the logger instance
        :rtype: Object
        """
        return self._logger

    def set_service_status(self, status):
        """
        The function sets the logger's service status to be the
        given status.
        :return: None
        """
        if status == 1:
            status = 'ON'
        else:
            status = 'OFF'

        self._status = status
        if status == 'ON':
            with open('App_Files/Services.txt', 'r+') as file:
                lines_list = file.readlines()
                lines_list[6] = json.dumps({encrypt('Logger'): encrypt('ON')})
                lines_list[6] += '\n'
                file.seek(0)
                file.truncate(0)
                file.write("".join(lines_list))
            self.start_logging()

        elif status == 'OFF':
            with open('App_Files/Services.txt', 'r+') as file:
                lines_list = file.readlines()
                lines_list[6] = json.dumps({encrypt('Logger'): encrypt('OFF')})
                lines_list[6] += '\n'
                file.seek(0)
                file.truncate(0)
                file.write("".join(lines_list))

    def get_service_status(self):
        """
        The function returns the logger's service status.
        :return: the virus logger's service status
        :rtype: str
        """
        return self._status


virus_scanner = Virus_Scanner()
updates_scanner = Updates_Scanner()
network_scanner_object = Network_Scanner()
logger_object = Logger()
logger = logger_object.get_logger()

# Global Variables for virus scanning
failed_scanning = list()
infected_files = list()
ROOT = r'C:\\'


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


def get_suspicious_files(scan_type, path=ROOT):
    """
    the function checks if there are suspicious files that need to be checked
    and returns the suspicious file list.
    :param scan_type: the type of the scan.quick or full
    :param path: the requested path to be scanned; default path ---> ROOT
    :return: a list of suspicious files that need to be deep scanned.
    :rtype: list
    """
    files_list = list()
    if scan_type == 'quick':  # quick scanning- getting specific types of files
        extensions_list = ['.exe', '.dll', '.DLL', '.bat', '.jar']
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = root + os.sep + file
                if Path(file_path).suffix in extensions_list:
                    files_list.append(file_path)

    elif scan_type == 'full':  # full scanning- getting all types of files
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = root + os.sep + file
                files_list.append(file_path)
    return files_list


def virus_scan(scan_type, path=ROOT):
    """
    the function runs a the scan on the suspicious files that were founded if they were founded.
    :param scan_type: the type of the scan: quick or full
    :param path: the requested path to be quick scanned; default path ---> ROOT
    :return: None
    """
    from Graphic_Interface import found_virus_screen
    global infected_files, failed_scanning
    scanned_extensions = dict()

    if not os.path.exists(path):  # if the given path is not valid
        if path:
            print(
                f"""The given path: '{path}' is not valid. Please enter a new Path \n""")
        else:
            print('The given path was empty. Please enter a new Path \n')
        print("""Virus scan wasn't successfully completed.\n""")
        return  # stopping the function

    print('Hold on. We are getting your files to be scanned.\n')
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(get_suspicious_files, scan_type, path)
        suspicious_files = future.result()

    start_time = time.perf_counter()  # time counter starting
    if suspicious_files:  # there are suspicious files to be scanned
        print(f'Starting to virus scan {path}')
        print(f'We are getting ready to scan {len(suspicious_files)} files\n')
        time.sleep(0.1)
        for index, file_path in enumerate(suspicious_files):
            # sending the file to deep scan
            threading.Thread(target=deep_scan, args=(file_path,)).start()
            if (index + 1) == len(suspicious_files):  # printing for last file
                finish_time = time.perf_counter()  # time counter finished
                sys.stdout.write(
                    f'\rScanning ({index + 1} files || {int(((index + 1) / len(suspicious_files)) * 100)}%): {basename(file_path)} || {(progress_duration(finish_time - start_time))[:-2]}): {basename(file_path)}last')
            else:
                sys.stdout.write(
                    f'\rScanning ({index + 1} files || {int(((index + 1) / len(suspicious_files)) * 100)}% || {(progress_duration(time.perf_counter() - start_time))[:-2]}): {basename(file_path)}')
        if infected_files:
            result = f'We found {len(infected_files)} infected files in Directory {path}.'
        else:
            result = f'Directory {path} is clean'

        for file_path in suspicious_files:  # getting scanned file's extensions statistics
            file_extension = Path(file_path).suffix
            if file_path not in failed_scanning:
                if file_extension not in scanned_extensions:
                    scanned_extensions[file_extension] = 1
                else:
                    scanned_extensions[file_extension] += 1

        print('\n\nVirus Scan Report:')
        print(result)
        print(f'Successfully scanned: {len(suspicious_files) - len(failed_scanning)} '
              f'out of {len(suspicious_files)} Files || Failed to scan : '
              f'{len(failed_scanning)} files')
        [print(
            f'{"%.2f" % float((value / (len(suspicious_files) - len(failed_scanning))) * 100)}% ({value}) {extension} files')
            for extension, value in scanned_extensions.items()]  # printing scanned file's extensions statistics
        print(f'Virus Scan has finished in '
              f'{progress_duration(finish_time - start_time)}')

        if infected_files:
            # displaying found viruses screen
            found_virus_screen(infected_files)

        from Graphic_Interface import display_notifications
        display_notifications('Virus Scanning process has finished.')
    else:
        print(
            f'We did not ran virus scan in {path} since there are not suspicious files there.\n')


def deep_scan(file_path):
    """
    The function is used in order to read the file's Hash and send it to
    Virus Total Scanner in order to determine if the file is infected.
    :param file_path: the path of the file to be scanned
    :return: None
    """
    global infected_files
    try:
        with open(file_path, "rb") as file:
            file_content = file.read()
            hashed_content = hashlib.md5(file_content).hexdigest()
            is_infected = virus_total_scanner(file_path, hashed_content)
            if is_infected:  # if more than 20 AntiViruses determined that the file is infected
                infected_files.append(file_path)
    except:
        pass


def virus_total_scanner(file_path, hashed_content):
    """
    The function scans the file's hash content with
    Virus Total scanning services and returns if the given hashed content is infected.
    :param file_path: the file's path
    :param hashed_content: the file's hash
    :return: True/False according to whether the file is infected or not.
    :rtype: bool
    """
    global failed_scanning
    response = virus_scanner.get_virus_total_service().get_file_report(
        hashed_content)  # getting the file report from virus total services
    response = (json.dumps(response, sort_keys=False, indent=4))
    if '"response_code": 1' in response:
        positive = response[response.find(
            '"positives":'):response.find('"positives":') + 20]
        found = True  # Boolean auxiliary variable
        for i in range(20):
            if i in positive:
                found = False
        return found
    elif '"response_code": 0' in response:  # failed to scan
        failed_scanning.append(file_path)
        return False


def remove_files(files_list):
    """
    The function  gets a files list and deletes them.
    :param files_list: a list of the wanted files to be deleted.
    :return: None
    """
    from Identity import shred_file

    for infected_file in files_list:
        try:
            shred_file(infected_file)  # trying to shred the file
            os.unlink(infected_file)
            print(f'infected file {infected_file} has deleted\n')
        except Exception as e:
            print(f'Could not delete the infected file {infected_file}. '
                  f'The error {e} occurred.\n')


def check_for_updates():
    """
    The Function checks for updates by comparing the PC's version and build number to the latest ones.
    :return: None
    """
    start_time = time.perf_counter()
    try:
        # Getting the current version and build usign platform module
        current_version = platform.release()
        current_build = platform.version(
        )[platform.version().find('.', 4) + 1:]

        # Getting the newest version
        # checking for windows insider program build update
        latest_version, latest_build = Web_Scrapper.get_latest_windows_version()
        print(latest_version, latest_build)
        print(current_version, current_build)
        if current_version != latest_version or current_build != latest_build:
            print(
                f'There is new version of Windows that you can upgrade to. Version: {latest_version}:{latest_build} \n')
            update('Windows')
        else:
            print(
                f'Your Windows version is up to date. Version: Windows {latest_version}')
        print(f'Searching for drivers updates')
        update('Drivers')

        finish_time = time.perf_counter()
        print(
            f'Updating has finished in {progress_duration(finish_time - start_time)}')

        from Graphic_Interface import display_notifications
        display_notifications('Updating process has finished.')

    except Exception as e:
        print('Could not update')


def update(update_type):
    """
    The Function updates the Windows version/Build according to the requested update to be executed.
    :param update_type: the type of the requested update to be executed
    :return: None
    """
    if update_type == 'Windows':  # if there is an update for the operating system/build version
        # opening MediaCreationTool for updating windows
        os.system('MediaCreationTool20H2.exe')

    else:  # update_type == 'Drivers':
        try:  # checking for Microsoft apps/drivers updates
            subprocess.Popen(
                ["powershell", "(echo y& echo y) | powershell Install-Module -Name PSWindowsUpdate"])
            subprocess.Popen(
                ["powershell", "Set-ExecutionPolicy RemoteSigned"])
            subprocess.Popen(["powershell", "Import-Module PSWindowsUpdate"])
            subprocess.Popen(
                ["powershell", "Get-Command -module PSWindowsUpdate"])
            subprocess.Popen(["powershell", "Get-WUInstall -MicrosoftUpdate"])
            subprocess.Popen(
                ["powershell", "Install-WindowsUpdate -MicrosoftUpdate -AcceptAll -AutoReboot"])
            print(
                """Windows driver's and Microsoft apps updates have been completed. Please restart your PC\n""")
        except Exception as e:
            print(
                f'Could not update Windows drivers, the error {e} occurred.\n')


def update_software_version():
    """
    The Function updates the AntiVirus AV Software version.
    :return: None
    """
    from AntiVirus_AV import latest_stored_version
    from Web_Scrapper import get_latest_software_version

    latest_version = get_latest_software_version()
    if latest_version != latest_stored_version:
        print(
            f'AntiVirus AV Update is available. Current Version: {latest_stored_version}. Latest Version: {latest_version}')
        print('Please visit https://AntiVirus-AV-Website.micha1245.repl.co and download the latest version.')
    else:
        print(f'You are up to date. Version: {latest_version}')

    from Graphic_Interface import display_notifications
    display_notifications('Updating process has finished.')


def get_ip_address():
    """
    The function returns the computer's Subnet mask.
    :return: the Subnet mask
    :rtype: str
    """
    contentList = os.popen("ipconfig").read().split()
    # Getting the start_index of the ip address=
    start_index = (contentList.index('IPv4') + 13)
    # Getting the finish_index ip address
    finish_index = contentList.index('Subnet')
    return "".join(contentList[start_index:finish_index])


def get_running_ports(ip, port, udp_tcp_list):
    """
    An auxiliary function that returns a list of running ports.
    :param ip: the ip address
    :param port: the checked port
    :param udp_tcp_list: the list of ip's and ports in tcp/udp form.
    :return: None
    """
    # creating a socket with TCP protocol
    s_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # creating a socket with UDP protocol
    s_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    location = (ip, port)
    result_tcp = s_tcp.connect_ex(location)  # create connection
    result_udp = s_udp.connect_ex(location)  # create connection
    if result_tcp == 0:  # checking if TCP port is open
        udp_tcp_list.append(('TCP', port))
    if result_udp == 0:  # checking if UDP port is open
        udp_tcp_list.append(('UDP', port))
    s_tcp.close()
    s_udp.close()


def scan_suspicious_ports():
    """
    The Function prints the open suspicious ports in the network for the PC's ip.
    :return: None
    """
    # well known ports list
    ports_list = [1, 5, 7, 18, 20, 21, 22, 23, 25, 29, 37, 42, 43, 49, 53,
                  69, 70, 79, 80, 103, 108, 109, 110, 115, 118, 119, 137,
                  139, 143, 150, 156, 161, 179, 190, 194, 197, 389, 396,
                  443, 444, 445, 458, 546, 547, 563, 569, 1080]
    # suspicious ports list
    suspicious_ports = [('TCP', 31), ('TCP', 1170), ('TCP', 1234),
                        ('TCP', 1243), ('TCP', 1981), ('TCP', 2001),
                        ('TCP', 2023), ('UDP', 2140), ('TCP', 2989),
                        ('TCP', 3024), ('TCP', 3150), ('TCP', 3700),
                        ('TCP', 4950), ('TCP', 6346), ('TCP', 6400),
                        ('TCP', 6667), ('TCP', 6670), ('TCP', 12345),
                        ('TCP', 12346), ('TCP', 16660), ('UDP', 18753),
                        ('TCP', 20034), ('TCP', 20432), ('UDP', 20433),
                        ('TCP', 27374), ('UDP', 27444), ('TCP', 27665),
                        ('TCP', 30100), ('UDP', 31335), ('TCP', 31337),
                        ('TCP', 33270), ('TCP', 33567), ('TCP', 33568),
                        ('TCP', 40421), ('TCP', 60008), ('TCP', 65000)]

    threading_list = []  # list with all the threads
    ip_dict = {}  # dict with all the ports, types and the PC's ip

    ip = get_ip_address()
    udp_tcp_list = []  # reset the ports list
    for port in ports_list:
        # create thread
        thread = threading.Thread(target=get_running_ports,
                                  args=(ip, port, udp_tcp_list))
        # adding the thread to the list of threads
        threading_list.append(thread)
        thread.start()  # start thread
    ip_dict[ip] = udp_tcp_list  # set the value for key ip to be ports list
    for thread in threading_list:  # run on the list of threads
        thread.join()  # using join method

    found = False
    suspicious_ports_found = list()
    for key, value in ip_dict.items():
        for index, port_tuple in enumerate(value):
            if port_tuple in suspicious_ports:
                suspicious_ports_found.append((port_tuple[0], port_tuple[1]))
                found = True
            if index == (len(ip_dict) - 1):  # last file
                sys.stdout.write(
                    f'\rScanning ports ({int((index / len(list(ip_dict.values())[0])) * 100)}%): {port_tuple[1]} Type: {port_tuple[0]}last')
            else:
                sys.stdout.write(
                    f'\rScanning ports ({int((index / len(list(ip_dict.values())[0])) * 100)}%): {port_tuple[1]} Type: {port_tuple[0]}')
    if not found:  # No risky ports open on the network
        print('There are no Suspicious Ports that running on your network.\n')
    else:
        for suspicious_port in suspicious_ports_found:
            print(
                f'Found Suspicious Open Port On {suspicious_port[1]}, The Port type is: {suspicious_port[0]}')
        for suspicious_port in suspicious_ports_found:
            print(f'\rClosing Port: {suspicious_port[1]}')
            close_port(suspicious_port)


def close_port(port):
    """
    The Function gets a requested port and closes it.
    :param port: the port to be closed
    :return: None
    """
    command = f'netstat -a -o -n | find "{port}"'
    pids = list()
    output = os.popen(command).read()

    for line in output.split("\n"):
        pids.append(line.split(" ")[-1])
    print(pids)
    for pid in pids:
        try:
            print(os.popen(f'TASKKILL /F /PID {pid}').read())
        except Exception as e:
            print(
                f'Could not terminate port {port} by pid {pid}. The error {e} occurred.')


def network_scanner():
    """
    The Function scans the network using the auxiliary functions above.
    :return: None
    """
    start_time = time.perf_counter()
    print('Scanning your connections...\n')
    scan_suspicious_ports()
    finish_time = time.perf_counter()
    print(
        f'Network Scanning has finished in {progress_duration(finish_time - start_time)}')

    from Graphic_Interface import display_notifications
    display_notifications('Network Scanning process has finished.\n')
