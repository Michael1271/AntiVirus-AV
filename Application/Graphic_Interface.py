import os
import sys
import threading
import time
import webbrowser
from ntpath import basename
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Combobox
from tksheet import Sheet
import Handle_User
import Identity
import Security

# A Graphic User Interface (GUI) Program
__author__ = 'Michael Khoshahang'

# Global Variables
color1 = "#%02x%02x%02x" % (255, 255, 255)
color2 = "#%02x%02x%02x" % (252, 252, 252)
color3 = "#%02x%02x%02x" % (244, 247, 250)
color4 = "#%02x%02x%02x" % (22, 113, 238)
color5 = "#%02x%02x%02x" % (62, 81, 101)
color6 = "#%02x%02x%02x" % (240, 240, 240)

SERVER_IP = None
SERVER_PORT = None
new_notification = list()
welcome_window = None
root = None
login_window = None
screen = None
progress_window = None
main = None
frame0 = None
security_screen = None
identity_screen = None
info_screen = None
details_screen = None

remember_me = None
blank_notification_icon = None
current_notification_icon = None
new_notification_icon = None
notifications_button = None

protected_lbl = None
unprotected_lbl1 = None
unprotected_lbl2 = None
security_protected_lbl1 = None
security_protected_lbl2 = None
security_unprotected_lbl1 = None
security_unprotected_lbl2 = None
identity_protected_lbl1 = None
identity_protected_lbl2 = None
identity_unprotected_lbl1 = None
identity_unprotected_lbl2 = None
info_protected_lbl1 = None
info_protected_lbl2 = None
info_unprotected_lbl1 = None
info_unprotected_lbl2 = None

main_frame1 = None
main_frame2 = None
security_frame1 = None
security_frame2 = None
identity_frame1 = None
identity_frame2 = None
info_frame1 = None
info_frame2 = None


class Screen(object):
    """
    Class of an Screen instance.
    """

    def __init__(self):
        """
        The function is a constructor of the Screen object.
        :return: None
        """
        self._screen = Toplevel()
        self._screen.geometry('875x585')
        self._screen.resizable(False, False)
        self._screen["background"] = color3
        self._screen.title('AntiVirus-AV')
        self._screen.iconbitmap('Gui_Photos/logo.ico')

        windowWidth = self._screen.winfo_reqwidth()
        windowHeight = self._screen.winfo_reqheight()
        # Gets both half the screen width/height and window width/height
        positionRight = int(
            self._screen.winfo_screenwidth() / 4.7 - windowWidth / 2)
        positionDown = int(
            self._screen.winfo_screenheight() / 5.5 - windowHeight / 2)
        # Positions the window in the center of the page.
        self._screen.geometry("+{}+{}".format(positionRight, positionDown))

    def get_screen(self):
        """
        The function returns the Screen object.
        :return: the Screen object
        :rtype: object
        """
        return self._screen


class Redirector(object):
    """
    Class of an output redirection mechanism instance.
    """

    def __init__(self, text_widget):
        """
        The function is a constructor of the Redirector class.
        :param text_widget: the output redirection widget
        :return: None
        """
        self._output = text_widget
        self._output.config(state=DISABLED)

    def write(self, text):
        """
        The function adds text to the end and scroll to the end. In addition, it logs the given text.
        :param text: the text to be added
        :return: None
        """
        from Security import logger_object, logger
        self._output.config(state=NORMAL)

        if '\r' in text:  # replacing the inserted line with a new one
            if 'last' not in text:  # last line
                # inserting output to the output text widget
                self._output.insert(END, text)
                time.sleep(0.00000005)  # delay time
                self._output.delete(self._output.index(
                    "end-1c linestart"), "end-1c")
            else:
                self._output.insert(END, text[:-4])
        else:
            self._output.insert(END, text)
        self._output.see(END)
        if text != '\n' and '\r' not in text and logger_object.get_service_status() == 'ON':
            logger.info(text)
        self._output.config(state=DISABLED)

    def flush(self):
        """
        Auxiliary function
        :return: None
        """
        pass


def get_server_details_screen():
    """
    The function displays a screen in which the user inputs the server's ip address and port.
    :return: None
    """

    global SERVER_IP, SERVER_PORT
    screen = Tk()
    screen.geometry('875x585')
    screen.resizable(False, False)
    screen["background"] = color3
    screen.title('AntiVirus-AV')
    screen.iconbitmap('Gui_Photos/logo.ico')

    windowWidth = screen.winfo_reqwidth()
    windowHeight = screen.winfo_reqheight()
    # Gets both half the screen width/height and window width/height
    positionRight = int(screen.winfo_screenwidth() / 4.7 - windowWidth / 2)
    positionDown = int(screen.winfo_screenheight() / 5.5 - windowHeight / 2)
    # Positions the window in the center of the page.
    screen.geometry("+{}+{}".format(positionRight, positionDown))

    # Photos
    exit_button = PhotoImage(file='Gui_Photos/exit_button.png')

    # Frames
    frame1 = Frame(screen, width=875, height=35, bg=color1)
    frame1.place(x=0, y=0)
    frame1.config(bd=0, relief=GROOVE)

    frame2 = Frame(screen, width=840, height=180, bg=color2)
    frame2.place(x=20, y=80)
    frame2.config(bd=0, relief=GROOVE)

    # Labels
    Label(frame1, text='Server Details required', font=(
        'Open Sans', 15), bg=color1).place(x=350, y=0)
    Label(frame2, text="""Please enter the AntiVirus-AV server's IP Address and PORT""", font=('Open San', 13),
          bg=color1).place(x=205, y=0)
    Label(frame2, text="IP Address", font=(
        'Open San', 13), bg=color1).place(x=370, y=50)
    Label(frame2, text="PORT", font=('Open San', 13),
          bg=color1).place(x=370, y=100)

    # Entrys
    ip = StringVar()
    port = StringVar()
    ip_entry = Entry(frame2, textvariable=ip)
    ip_entry.place(x=370, y=70)
    ip_entry.focus()
    port_entry = Entry(frame2, textvariable=port)
    port_entry.place(x=370, y=120)

    Button(frame2, text='Establish connection', bg=color4, borderwidth=1, width=25, height=2,
           command=lambda: [set_global_variables(), screen.destroy()]).place(x=630, y=130)
    Button(frame1, image=exit_button, bg=color4, width=20, height=20, borderwidth=0,
           command=lambda: [screen.destroy(), sys.exit(0)]).place(x=1, y=5)

    def set_global_variables():
        """
        An auxiliary function that sets the global variables SERVER_IP and SERVER_PORT.
        :return: None
        """
        try:
            global SERVER_IP, SERVER_PORT
            nonlocal ip_entry, port_entry
            SERVER_IP = ip_entry.get()
            SERVER_PORT = port_entry.get()
        except:
            pass

    screen.bind('<Return>', lambda _: [
                set_global_variables(), screen.destroy()])
    screen.mainloop()


def welcome_screen():
    """
    The function displays a welcome screen which contains instructions to access the AntiVirus AV software.
    The function is displayed only for new users.
    :return: None
    """
    global welcome_window
    welcome_window = Tk()
    welcome_window.geometry('875x585')
    welcome_window.resizable(False, False)
    welcome_window["background"] = color3
    welcome_window.title('AntiVirus-AV')
    welcome_window.iconbitmap('Gui_Photos/logo.ico')

    windowWidth = welcome_window.winfo_reqwidth()
    windowHeight = welcome_window.winfo_reqheight()
    # Gets both half the screen width/height and window width/height
    positionRight = int(
        welcome_window.winfo_screenwidth() / 4.7 - windowWidth / 2)
    positionDown = int(welcome_window.winfo_screenheight() /
                       5.5 - windowHeight / 2)
    # Positions the window in the center of the page.
    welcome_window.geometry("+{}+{}".format(positionRight, positionDown))

    # Photos
    exit_button = PhotoImage(file='Gui_Photos/exit_button.png')

    # Frames
    frame1 = Frame(welcome_window, width=875, height=35, bg=color1)
    frame1.place(x=0, y=0)
    frame1.config(bd=0, relief=GROOVE)

    # Labels
    Label(frame1, text='Joining AntiVirus-AV', font=('Open Sans', 15),
          bg=color1).place(x=350, y=0)

    output_box1 = Text(progress_window, bg=color3, height=35, width=108)
    output_box1.place(x=0, y=35)

    output_box1.insert(END, """Hello There new User!\nPlease follow the instructions in order to access your AntiVirus AV and read the terms of service.\n
Instructions:
   1) Please make a registration in the next page.\n
   2) In the registration, you may enter your Name, username, mail and password for your antivirus service.\n
   3) You can Change your details whenever you want.\n
   4) You can see our details security policy here.\n\n
About Us:
    AntiVirus AV Organization is a non profit organization.\n
    Our goal is to make sure that everyone will have the ability to protect themselves.\n
    Therefore, We have created a software that can protect you. All the included services are free!\n
Privacy policy:
     We commit for never sharing any given mails, names, usernames and passwords with anyone else.\n
     Every single detail that is given is encrypted and stored as encrypted data in our databases\n
     You can enable the logging option down below in order to log all actions while using the software\n
     If you agree, You shall proceed.\n\n""")
    from Security import logger_object
    # Buttons
    logger_status = IntVar()
    Button(welcome_window, text='I accept the terms of service and privacy policy', bg=color4, borderwidth=1, width=35,
           height=2, command=lambda: [welcome_window.destroy(), logger_object.set_service_status(logger_status.get()),
                                      access_screen('', '', True)]).place(x=595, y=470)

    Radiobutton(login_window, text='Enable logging', pady=8, bg=color4, borderwidth=0, width=19, height=1,
                variable=logger_status, value=1).place(x=655, y=520)

    Button(frame1, image=exit_button, bg=color4, width=20, height=20, borderwidth=0,
           command=lambda: [print('Terminating Connection to Server'), welcome_window.destroy(), sys.exit(0)]).place(
        x=1, y=5)

    welcome_window.bind('<Return>',
                        lambda _: [welcome_window.destroy(), logger_object.set_service_status(logger_status.get()),
                                   access_screen('', '', True)])
    welcome_window.mainloop()


def access_screen(username, password, required):
    """
    The function displays an access screen where the user can log in or register to the antivirus software.
    :param username: the username of the user
    param password: the password of the user
    param required: if displaying access screen is required
    :return: None
    """
    global root
    root = Tk()
    root.geometry('875x585')
    root.resizable(False, False)
    root["background"] = color3
    root.title('AntiVirus-AV')
    root.iconbitmap('Gui_Photos/logo.ico')

    if not required:
        root.withdraw()

    windowWidth = root.winfo_reqwidth()
    windowHeight = root.winfo_reqheight()
    # Gets both half the screen width/height and window width/height
    positionRight = int(root.winfo_screenwidth() / 4.7 - windowWidth / 2)
    positionDown = int(root.winfo_screenheight() / 5.5 - windowHeight / 2)
    # Positions the window in the center of the page.
    root.geometry("+{}+{}".format(positionRight, positionDown))

    # Photos
    exit_button = PhotoImage(file='Gui_Photos/exit_button.png')

    # Frames
    frame1 = Frame(root, width=875, height=35, bg=color1)
    frame1.place(x=0, y=0)
    frame1.config(bd=0, relief=GROOVE)

    # Labels
    Label(frame1, text='Access Required', font=(
        'Open Sans', 15), bg=color1).place(x=350, y=0)
    Label(root, text='Access is required- Please Make a Login or Sign up', font=('Open Sans', 13), bg=color3).pack(
        pady=50)

    # Buttons
    if not required:
        Button(root, text='Login', bg=color4, borderwidth=1, width=21, height=2,
               command=login_screen(username, password)).pack(pady=8)
    else:
        Button(root, text='Login', bg=color4, borderwidth=1, width=21, height=2,
               command=lambda: login_screen('', '')).pack(pady=8)

    Button(root, text='Sign Up', bg=color4, borderwidth=1, width=21, height=2, command=lambda: register_screen()).pack(
        pady=8)
    Button(frame1, image=exit_button, bg=color4, width=20, height=20, borderwidth=0,
           command=lambda: [print('Terminating Connection to Server'), root.destroy(), sys.exit(0)]).place(x=1, y=5)

    root.mainloop()


def login_screen(username='', password=''):
    """
    the function displays a login window.
    :param username: the username of the user
    :param password: the password of the user
    :return: None
    """
    global root, login_window, remember_me

    login_window = Toplevel(root)
    login_window.title("Login Screen")
    login_window.geometry("300x250")
    login_window.resizable(False, False)
    login_window['background'] = color3
    login_window.title('AntiVirus-AV')
    login_window.iconbitmap('Gui_Photos/logo.ico')

    windowWidth = login_window.winfo_reqwidth()
    windowHeight = login_window.winfo_reqheight()
    # Gets both half the screen width/height and window width/height
    positionRight = int(login_window.winfo_screenwidth() /
                        2.5 - windowWidth / 2)
    positionDown = int(login_window.winfo_screenheight() /
                       3.5 - windowHeight / 2)
    # Positions the window in the center of the page.
    login_window.geometry("+{}+{}".format(positionRight, positionDown))

    if username == '' and password == '':
        # Labels & Entrys-
        username = StringVar()
        password = StringVar()
        Label(login_window, text='Please enter your details below', font=('OpenSans', 11),
              bg=color3).pack()
        Label(login_window, text='Username', font=(
            'OpenSans', 13), bg=color3).pack()
        username_entry = Entry(login_window, textvariable=username)
        username_entry.pack()
        username_entry.focus()
        Label(login_window, text='Password', font=(
            'OpenSans', 13), bg=color3).pack()
        password_entry = Entry(login_window, show='*', textvariable=password)
        password_entry.pack()
        Label(login_window, text="", bg=color3).pack()
        # Buttons
        Button(login_window, text='Login', font=('OpenSans', 12), bg=color4, borderwidth=1, width=9, height=1,
               command=lambda: Handle_User.login_user(username_entry, password_entry)).pack()
        global remember_me
        remember_me = IntVar()
        Radiobutton(login_window, text='Remember Me', pady=8,
                    bg=color3, variable=remember_me, value=1).pack()
    else:
        login_window.withdraw()
        # Buttons
        Button(login_window, text='Login', font=('OpenSans', 12), bg=color4, borderwidth=1, width=9, height=1,
               command=Handle_User.login_user(username, password)).pack()

    Button(login_window, text='Back', bg=color4, borderwidth=1, width=4, height=1,
           command=lambda: login_window.destroy()).place(x=4, y=1)

    login_window.bind('<Return>', lambda _: [
                      Handle_User.login_user(username_entry, password_entry)])
    login_window.mainloop()


def register_screen():
    """
    The function displays a Registration window.
    :return: None
    """
    global root, screen

    screen = Toplevel(root)
    screen.geometry("300x400")
    screen.resizable(False, False)
    screen['background'] = color3
    screen.title('AntiVirus-AV')
    screen.iconbitmap('Gui_Photos/logo.ico')

    windowWidth = screen.winfo_reqwidth()
    windowHeight = screen.winfo_reqheight()
    # Gets both half the screen width/height and window width/height
    positionRight = int(screen.winfo_screenwidth() / 2.5 - windowWidth / 2)
    positionDown = int(screen.winfo_screenheight() / 3.5 - windowHeight / 2)
    # Positions the window in the center of the page.
    screen.geometry("+{}+{}".format(positionRight, positionDown))

    # Labels & Entrys-
    name = StringVar()
    mail = StringVar()
    username = StringVar()
    password = StringVar()
    Label(screen, text='Please enter your details below', font=('Open Sans', 11),
          bg=color3).pack()
    Label(screen, text="", bg=color3).pack()
    Label(screen, text='First Name', font=('OpenSans', 13),
          bg=color3).pack()
    name_entry = Entry(screen, textvariable=name)
    name_entry.pack()
    name_entry.focus()
    Label(screen, text="", bg=color3).pack()
    Label(screen, text='Mail', font=('OpenSans', 13), bg=color3).pack()
    mail_entry = Entry(screen, textvariable=mail)
    mail_entry.pack()
    Label(screen, text="", bg=color3).pack()
    Label(screen, text='Username', font=('OpenSans', 13),
          bg=color3).pack()
    username_entry = Entry(screen, textvariable=username)
    username_entry.pack()
    Label(screen, text="", bg=color3).pack()
    Label(screen, text='Password', font=('OpenSans', 13),
          bg=color3).pack()
    password_entry = Entry(screen, show='*',
                           textvariable=password)
    password_entry.pack()
    Label(screen, text="", bg=color3).pack()

    # Buttons
    Button(screen, text='Sign Up', font=('OpenSans', 12), bg=color4, borderwidth=1, width=9, height=1,
           command=lambda: Handle_User.register_user(name_entry, username_entry, mail_entry, password_entry)).pack()

    Button(screen, text='Back', bg=color4, borderwidth=0, width=4, height=1,
           command=lambda: screen.destroy()).place(x=4, y=1)

    screen.bind('<Return>', lambda _: [
                Handle_User.login_user(username_entry, password_entry)])
    screen.mainloop()


def main_screen():
    """
    The function displays the Main AntiVirus AV Screen.
    :return: None
    """
    from Security import virus_scanner, updates_scanner, network_scanner_object
    from Identity import shredder, firewall, password_manager, file_locker

    global main, root, progress_window
    global new_notification_icon, current_notification_icon, blank_notification_icon, new_notification, notifications_button
    root.withdraw()

    main = Toplevel(root)
    main.geometry('875x585')
    main.resizable(False, False)
    main.configure(background=color3)
    main.title('AntiVirus-AV')
    main.iconbitmap('Gui_Photos/logo.ico')

    windowWidth = main.winfo_reqwidth()
    windowHeight = main.winfo_reqheight()
    # Gets both half the screen width/height and window width/height
    positionRight = int(main.winfo_screenwidth() / 4.7 - windowWidth / 2)
    positionDown = int(main.winfo_screenheight() / 5.5 - windowHeight / 2)
    # Positions the window in the center of the page.
    main.geometry("+{}+{}".format(positionRight, positionDown))

    firewall_status = firewall.get_service_status()
    if firewall_status:
        firewall_status = 'ON'
    else:
        firewall_status = 'OFF'

    # Photos
    fully_secured = PhotoImage(file='Gui_Photos/fully_secured.png')
    security_logo = PhotoImage(file='Gui_Photos/security_logo.png')
    identity_logo = PhotoImage(file='Gui_Photos/identity_logo.png')
    information_logo = PhotoImage(file='Gui_Photos/information_logo.png')
    unprotected_security = PhotoImage(
        file='Gui_Photos/unprotected_security.png')
    unprotected_identity = PhotoImage(
        file='Gui_Photos/unprotected_identity.png')
    new_notification_icon = PhotoImage(
        file='Gui_Photos/new_notification_icon.png')
    blank_notification_icon = PhotoImage(
        file='Gui_Photos/blank_notification_icon.png')
    current_notification_icon = blank_notification_icon
    settings_icon = PhotoImage(file='Gui_Photos/settings_icon.png')
    exit_button = PhotoImage(file='Gui_Photos/exit_button.png')

    # Frames
    global frame0, main_frame1, main_frame2
    frame0 = Frame(main, width=875, height=35, bg=color1)
    frame0.place(x=0, y=0)
    frame0.config(bd=0, relief=GROOVE)

    main_frame1 = Frame(main, width=750, height=200, bg=color1)
    main_frame1.place(x=120, y=100)
    main_frame1.config(bd=0, relief=GROOVE)

    main_frame2 = Frame(main, width=400, height=200, bg=color1)

    frame3 = Frame(main, width=150, height=170, bg=color1)
    frame3.place(x=120, y=385)
    frame3.config(bd=0, relief=GROOVE)

    frame4 = Frame(main, width=150, height=170, bg=color1)
    frame4.place(x=355, y=385)
    frame4.config(bd=0, relief=GROOVE)

    frame5 = Frame(main, width=150, height=170, bg=color1)
    frame5.place(x=590, y=385)
    frame5.config(bd=0, relief=GROOVE)

    # Labels
    global protected_lbl, unprotected_lbl1, unprotected_lbl2
    if virus_scanner.get_service_status() == 'ON' and updates_scanner.get_service_status() == 'ON' and network_scanner_object.get_service_status() == 'ON' and firewall_status == 'ON' and shredder.get_service_status() == 'ON' and password_manager.get_service_status() == 'ON' and file_locker.get_service_status() == 'ON':
        protected_lbl = Label(main_frame1, image=fully_secured,
                              borderwidth=0, font=('Open Sans', 15), bg=color1)
        protected_lbl.pack(padx=[90, 70])
    else:
        main_frame2.place(x=400, y=110)
        main_frame2.config(bd=0, relief=GROOVE)
        if virus_scanner.get_service_status() == 'OFF' or updates_scanner.get_service_status() == 'OFF' or network_scanner_object.get_service_status() == 'OFF':
            unprotected_lbl1 = Label(
                main_frame1, image=unprotected_security, borderwidth=0)
            unprotected_lbl1.pack()
            unprotected_lbl2 = Label(main_frame2,
                                     text='Check out your security protection\nto find out how you can\n protect your PC',
                                     borderwidth=0, font=('Open Sans', 15), bg=color1)
            unprotected_lbl2.place(x=45, y=75)
        else:
            unprotected_lbl1 = Label(
                main_frame1, image=unprotected_identity, borderwidth=0)
            unprotected_lbl1.pack()
            unprotected_lbl2 = Label(main_frame2,
                                     text='Check your identity protection\nto find out how you can\nprotect your identity',
                                     borderwidth=0, font=('Open Sans', 15), bg=color1)
            unprotected_lbl2.place(x=45, y=75)

    # Buttons
    Button(frame0, image=settings_icon, bg=color2, borderwidth=0,
           command=lambda: settings_screen()).place(x=720, y=1)

    if new_notification:
        current_notification_icon = blank_notification_icon
        new_notification.remove(new_notification[len(new_notification) - 1])
    try:
        with open('App_Files/Notifications.txt', 'x'):
            print("Creating Notifications file")
            pass
    except:
        pass
    with open('App_Files/Notifications.txt', 'r') as file:
        content = file.read()

    if content:
        import re
        display_notifications(re.sub(r'\n\s*\n', '\n', content, re.MULTILINE))
    else:
        notifications_button = Button(frame0, image=current_notification_icon, bg=color2, borderwidth=0,
                                      command=lambda: notification_screen())
        notifications_button.update()
        notifications_button.place(x=670, y=0)

    Button(frame0, image=exit_button, bg=color4, width=20, height=20, borderwidth=0,
           command=lambda: [print('Terminating Connection to Server'), root.destroy(), sys.exit(0)]).place(x=1, y=5)
    Button(frame0, text='Progress bar', bg=color4, borderwidth=0,
           command=lambda: [main.withdraw(), progress_window.deiconify()]).place(x=560, y=5)
    Button(frame3, text='\nProtect your PC from\nlatest viruses and threats', image=security_logo, compound='top',
           bg=color1, borderwidth=0, command=lambda: [main.withdraw(), security()]).pack(padx=[10, 10], pady=[15, 15])
    Button(frame4, text='\nKeeps your personal info\nsafe from hackers', image=identity_logo, compound='top', bg=color1,
           borderwidth=0, command=lambda: [main.withdraw(), identity()]).pack(padx=[10, 10], pady=[15, 15])
    Button(frame5, text='\nYour information', image=information_logo, compound='top', bg=color1, borderwidth=0,
           command=lambda: [main.withdraw(), information()]).pack(padx=[25, 25], pady=[10, 10])

    if Handle_User.user_instance.get_user_type():
        Button(frame0, text="""Admin's Panel""", bg=color4, borderwidth=0, command=lambda: admin_screen()).place(x=440,
                                                                                                                 y=5)

    progress_screen()
    main.mainloop()


def security():
    """
    The function displays a pc security screen.
    :return: None
    """
    from Security import virus_scanner, updates_scanner, network_scanner_object
    global security_screen
    security_screen = Screen().get_screen()

    # Photos
    home = PhotoImage(file='Gui_Photos/home_button.png')
    protected_security = PhotoImage(file='Gui_Photos/protected_security.png')
    unprotected_security = PhotoImage(
        file='Gui_Photos/unprotected_security.png')
    virus_scan_logo = PhotoImage(file='Gui_Photos/virus_scan_logo.png')
    secured_apps = PhotoImage(file='Gui_Photos/updates_button.png')
    network_scan_logo = PhotoImage(file='Gui_Photos/network_scan_logo.png')
    settings_icon = PhotoImage(file='Gui_Photos/settings_icon.png')
    go_home = PhotoImage(file='Gui_Photos/go_home.png')
    current_security = PhotoImage(file='Gui_Photos/current_security.png')

    # Frames
    global security_frame1, security_frame2
    frame0 = Frame(security_screen, width=875, height=35, bg=color1)
    frame0.place(x=0, y=0)
    frame0.config(bd=0, relief=GROOVE)

    security_frame1 = Frame(security_screen, width=200, height=200, bg=color1)
    security_frame1.place(x=120, y=110)
    security_frame1.config(bd=0, relief=GROOVE)

    security_frame2 = Frame(security_screen, width=400, height=200, bg=color1)
    security_frame2.place(x=400, y=110)
    security_frame2.config(bd=0, relief=GROOVE)

    frame3 = Frame(security_screen, width=150, height=170, bg=color1)
    frame3.place(x=120, y=385)
    frame3.config(bd=0, relief=GROOVE)

    frame4 = Frame(security_screen, width=150, height=170, bg=color1)
    frame4.place(x=297, y=385)
    frame4.config(bd=0, relief=GROOVE)

    frame5 = Frame(security_screen, width=150, height=170, bg=color1)
    frame5.place(x=475, y=385)
    frame5.config(bd=0, relief=GROOVE)

    frame6 = Frame(security_screen, width=150, height=170, bg=color1)
    frame6.place(x=650, y=385)
    frame6.config(bd=0, relief=GROOVE)

    # Labels
    Label(frame0, image=current_security, borderwidth=0).place(x=70, y=2)

    global security_protected_lbl1, security_protected_lbl2, security_unprotected_lbl1, security_unprotected_lbl2
    if virus_scanner.get_service_status() == 'ON' and updates_scanner.get_service_status() == 'ON' and network_scanner_object.get_service_status() == 'ON':
        security_protected_lbl1 = Label(
            security_frame1, image=protected_security, borderwidth=0)
        security_protected_lbl1.pack()
        security_protected_lbl2 = Label(security_frame2, text='Your PC is secured', borderwidth=0,
                                        font=('Open Sans', 13), bg=color1)
        security_protected_lbl2.place(x=130, y=85)
    else:
        security_unprotected_lbl1 = Label(
            security_frame1, image=unprotected_security, borderwidth=0)
        security_unprotected_lbl1.pack()
        security_unprotected_lbl2 = Label(security_frame2, text='Your PC is unprotected', borderwidth=0,
                                          font=('Open Sans', 13), bg=color1)
        security_unprotected_lbl2.place(x=125, y=85)

    # Buttons
    Button(frame0, image=settings_icon, bg=color2, borderwidth=0,
           command=lambda: settings_screen()).place(x=720, y=1)
    Button(frame0, image=home, borderwidth=0, command=lambda: [security_screen.destroy(), main.deiconify()]).place(
        x=600, y=2)
    Button(frame0, image=go_home, borderwidth=0, command=lambda: [security_screen.destroy(), main.deiconify()]).place(
        x=0, y=2)
    Button(frame3, text='\nScans your PC for\n threats', image=virus_scan_logo, compound='top', borderwidth=0,
           font=('Open Sans', 12), bg=color1, command=lambda: [security_screen.withdraw(),
                                                               virus_scanner_screen() if virus_scanner.get_service_status() == 'ON' else unactive_service_screen(
                                                                   'Security')]).place(x=13, y=0)
    Button(frame4, text='\nUpdate my PC', image=secured_apps, compound='top', borderwidth=0, font=('Open Sans', 12),
           bg=color1, command=lambda: [security_screen.withdraw(),
                                       update_pc_screen() if updates_scanner.get_service_status() == 'ON' else unactive_service_screen(
                                           'Security')]).place(x=13, y=0)
    Button(frame5, text='\nUpdate this App', image=secured_apps, compound='top', borderwidth=0, font=('Open Sans', 12),
           bg=color1, command=lambda: [security_screen.withdraw(),
                                       update_screen() if updates_scanner.get_service_status() == 'ON' else unactive_service_screen(
                                           'Security')]).place(x=13, y=0)
    Button(frame6, text='\nScan Your\nConnections', image=network_scan_logo, compound='top', borderwidth=0,
           font=('Open Sans', 12), bg=color1, command=lambda: [security_screen.withdraw(),
                                                               network_scanner_screen() if network_scanner_object.get_service_status() == 'ON' else unactive_service_screen(
                                                                   'Security')]).place(x=16, y=0)

    security_screen.mainloop()


def identity():
    """
    The function displays an identity window.
    :return: None
    """
    from Identity import shredder, firewall, password_manager, file_locker
    global identity_screen
    identity_screen = Screen().get_screen()

    firewall_status = firewall.get_service_status()
    if firewall_status:
        firewall_status = 'ON'
    else:
        firewall_status = 'OFF'

    # Photos
    home = PhotoImage(file='Gui_Photos/home_button.png')
    protected_identity = PhotoImage(file='Gui_Photos/protected_identity.png')
    unprotected_identity = PhotoImage(
        file='Gui_Photos/unprotected_identity.png')
    shredder_new_logo = PhotoImage(file='Gui_Photos/shredder_button.png')
    firewall_new_logo = PhotoImage(file='Gui_Photos/firewall_button.png')
    password_manager_new_logo = PhotoImage(
        file='Gui_Photos/password_manager_button.png')
    file_lock_new_logo = PhotoImage(file='Gui_Photos/file_locker_button.png')
    settings_icon = PhotoImage(file='Gui_Photos/settings_icon.png')
    go_home = PhotoImage(file='Gui_Photos/go_home.png')
    current_identity = PhotoImage(file='Gui_Photos/current_identity.png')

    # Frames
    global identity_frame1, identity_frame2
    frame0 = Frame(identity_screen, width=875, height=35, bg=color1)
    frame0.place(x=0, y=0)
    frame0.config(bd=0, relief=GROOVE)

    identity_frame1 = Frame(identity_screen, width=200, height=200, bg=color1)
    identity_frame1.place(x=120, y=110)
    identity_frame1.config(bd=0, relief=GROOVE)

    identity_frame2 = Frame(identity_screen, width=400, height=200, bg=color1)
    identity_frame2.place(x=400, y=110)
    identity_frame2.config(bd=0, relief=GROOVE)

    frame3 = Frame(identity_screen, width=150, height=170, bg=color1)
    frame3.place(x=120, y=385)
    frame3.config(bd=0, relief=GROOVE)

    frame4 = Frame(identity_screen, width=150, height=170, bg=color1)
    frame4.place(x=297, y=385)
    frame4.config(bd=0, relief=GROOVE)

    frame5 = Frame(identity_screen, width=150, height=170, bg=color1)
    frame5.place(x=475, y=385)
    frame5.config(bd=0, relief=GROOVE)

    frame6 = Frame(identity_screen, width=150, height=170, bg=color1)
    frame6.place(x=650, y=385)
    frame6.config(bd=0, relief=GROOVE)

    # Labels
    Label(frame0, image=current_identity, borderwidth=0).place(x=70, y=2)

    global identity_protected_lbl1, identity_protected_lbl2, identity_unprotected_lbl1, identity_unprotected_lbl2
    if firewall_status == 'ON' and shredder.get_service_status() == 'ON' and password_manager.get_service_status() == 'ON' and file_locker.get_service_status() == 'ON':
        identity_protected_lbl1 = Label(
            identity_frame1, image=protected_identity, borderwidth=0)
        identity_protected_lbl1.pack()
        identity_protected_lbl2 = Label(identity_frame2, text='Your identity is secured', borderwidth=0,
                                        font=('Open Sans', 13), bg=color1)
        identity_protected_lbl2.place(x=121, y=85)
    else:
        identity_unprotected_lbl1 = Label(
            identity_frame1, image=unprotected_identity, borderwidth=0)
        identity_unprotected_lbl1.pack()
        identity_unprotected_lbl2 = Label(identity_frame2, text='Your identity is unsecured', borderwidth=0,
                                          font=('Open Sans', 13), bg=color1)
        identity_unprotected_lbl2.place(x=121, y=85)

    # Buttons
    Button(frame0, image=settings_icon, bg=color2, borderwidth=0,
           command=lambda: settings_screen()).place(x=720, y=1)
    Button(frame0, image=home, borderwidth=0, command=lambda: [identity_screen.destroy(), main.deiconify()]).place(
        x=600, y=2)
    Button(frame0, image=go_home, borderwidth=0, command=lambda: [identity_screen.destroy(), main.deiconify()]).place(
        x=0, y=2)
    Button(frame3, text="""\nMakes sure\nyour deleted info\ncan't be recovered""", image=shredder_new_logo,
           compound='top', borderwidth=0, font=('Open Sans', 12), bg=color1,
           command=lambda: [identity_screen.withdraw(),
                            shredder_screen() if shredder.get_service_status() == 'ON' else unactive_service_screen(
                                'Identity')]).place(x=10, y=0)
    Button(frame4, text='\nManage your\nfirewall', image=firewall_new_logo, compound='top', borderwidth=0,
           font=('Open Sans', 12), bg=color1, command=lambda: [identity_screen.withdraw(),
                                                               firewall_screen() if firewall_status == 'ON' else unactive_service_screen(
                                                                   'Identity')]).place(x=22, y=0)
    Button(frame5, text='\nManage your\npassword', image=password_manager_new_logo, compound='top', borderwidth=0,
           font=('Open Sans', 12), bg=color1, command=lambda: [identity_screen.withdraw(), password_manager_screen(
               False) if password_manager.get_service_status() == 'ON' else unactive_service_screen('Identity')]).place(
        x=0, y=0)
    Button(frame6, text='\nLock your private\nfiles', image=file_lock_new_logo, compound='top', borderwidth=0,
           font=('Open Sans', 12), bg=color1, command=lambda: [identity_screen.withdraw(),
                                                               file_locker_screen() if file_locker.get_service_status() == 'ON' else unactive_service_screen(
                                                                   'Identity')]).place(x=15, y=0)

    identity_screen.mainloop()


def information():
    """
    The function displays an information screen.
    :return: None
    """
    from Security import virus_scanner, updates_scanner, network_scanner_object
    from Identity import shredder, firewall, password_manager, file_locker
    global info_screen
    info_screen = Screen().get_screen()

    # Photos
    home = PhotoImage(file='Gui_Photos/home_button.png')
    my_account = PhotoImage(file='Gui_Photos/my_account_button.png')
    security_policy = PhotoImage(file='Gui_Photos/security_policy.png')
    about = PhotoImage(file='Gui_Photos/about_button.png')
    help = PhotoImage(file='Gui_Photos/help_button.png')
    settings_icon = PhotoImage(file='Gui_Photos/settings_icon.png')
    fully_protected = PhotoImage(file='Gui_Photos/fully_protected.png')
    fully_unprotected = PhotoImage(file='Gui_Photos/fully_unprotected.png')
    go_home = PhotoImage(file='Gui_Photos/go_home.png')
    current_information = PhotoImage(file='Gui_Photos/current_information.png')

    firewall_status = firewall.get_service_status()
    if firewall_status:
        firewall_status = 'ON'
    else:
        firewall_status = 'OFF'

    # Frames
    global info_frame1, info_frame2
    frame0 = Frame(info_screen, width=875, height=35, bg=color1)
    frame0.place(x=0, y=0)
    frame0.config(bd=0, relief=GROOVE)

    info_frame1 = Frame(info_screen, width=200, height=200, bg=color1)
    info_frame1.place(x=120, y=110)
    info_frame1.config(bd=0, relief=GROOVE)

    info_frame2 = Frame(info_screen, width=400, height=200, bg=color1)
    info_frame2.place(x=400, y=110)
    info_frame2.config(bd=0, relief=GROOVE)

    frame3 = Frame(info_screen, width=150, height=170, bg=color1)
    frame3.place(x=120, y=385)
    frame3.config(bd=0, relief=GROOVE)

    frame4 = Frame(info_screen, width=150, height=170, bg=color1)
    frame4.place(x=297, y=385)
    frame4.config(bd=0, relief=GROOVE)

    frame5 = Frame(info_screen, width=150, height=170, bg=color1)
    frame5.place(x=475, y=385)
    frame5.config(bd=0, relief=GROOVE)

    frame6 = Frame(info_screen, width=150, height=170, bg=color1)
    frame6.place(x=650, y=385)
    frame6.config(bd=0, relief=GROOVE)

    # Labels
    Label(frame0, image=current_information, borderwidth=0).place(x=70, y=2)

    global info_protected_lbl1, info_protected_lbl2, info_unprotected_lb1, info_unprotected_lbl2
    if virus_scanner.get_service_status() == 'ON' and updates_scanner.get_service_status() == 'ON' and network_scanner_object.get_service_status() == 'ON' and firewall_status == 'ON' and shredder.get_service_status() == 'ON' and password_manager.get_service_status() == 'ON' and file_locker.get_service_status() == 'ON':
        info_protected_lbl1 = Label(
            info_frame1, image=fully_protected, borderwidth=0)
        info_protected_lbl1.pack()
        info_protected_lbl2 = Label(info_frame2, text="""You'r PC and Identity are fully protected""", borderwidth=0,
                                    font=('Open Sans', 13), bg=color1)
        info_protected_lbl2.place(x=61, y=85)
    else:
        info_unprotected_lb1 = Label(
            info_frame1, image=fully_unprotected, borderwidth=0)
        info_unprotected_lb1.pack()
        info_unprotected_lbl2 = Label(info_frame2, text='You are unprotected', borderwidth=0, font=('Open Sans', 13),
                                      bg=color1)
        info_unprotected_lbl2.place(x=125, y=85)

    # Buttons
    Button(frame0, image=settings_icon, bg=color2, borderwidth=0,
           command=lambda: settings_screen()).place(x=720, y=1)
    Button(frame0, image=home, borderwidth=0, command=lambda: [info_screen.destroy(), main.deiconify()]).place(x=600,
                                                                                                               y=2)
    Button(frame0, image=go_home, borderwidth=0, command=lambda: [info_screen.destroy(), main.deiconify()]).place(x=0,
                                                                                                                  y=2)
    Button(frame3, text='\nView My Account', image=my_account, compound='top', borderwidth=0, font=('Open Sans', 12),
           bg=color1,
           command=lambda: [info_screen.withdraw(), view_account(False)]).place(x=6, y=0)
    Button(frame4, text='\nCheck out our\nsecurity policy', image=security_policy, compound='top', borderwidth=0,
           font=('Open Sans', 12), bg=color1,
           command=lambda: webbrowser.open_new('https://antivirus-av-website.micha1245.repl.co/About')).place(x=6, y=0)
    Button(frame5, text='\nAbout us', image=about, compound='top', borderwidth=0, font=('Open Sans', 12), bg=color1,
           command=lambda: webbrowser.open_new('https://antivirus-av-website.micha1245.repl.co/About')).place(x=6, y=0)
    Button(frame6, text='\nGet help and support', image=help, compound='top', borderwidth=0, font=('Open Sans', 12),
           bg=color1,
           command=lambda: webbrowser.open_new('https://antivirus-av-website.micha1245.repl.co/Contact-Us')).place(x=0,
                                                                                                                   y=0)

    info_screen.mainloop()


def virus_scanner_screen():
    """
    The function displays a virus scan screen where the user can run virus scans.
    :return: None
    """
    global main, security_screen, progress_window
    if main:
        main.withdraw()
    screen = Screen().get_screen()

    # Photos
    scan_icon = PhotoImage(file='Gui_Photos/scan_picture.png')
    get_help = PhotoImage(file='Gui_Photos/get_help_icon.png')
    go_home = PhotoImage(file='Gui_Photos/go_home.png')
    go_security = PhotoImage(file='Gui_Photos/go_security.png')
    current_virus_scanner = PhotoImage(
        file='Gui_Photos/current_virus_scanner.png')

    # Frames
    frame1 = Frame(screen, width=875, height=35, bg=color1)
    frame1.place(x=0, y=0)
    frame1.config(bd=0, relief=GROOVE)

    frame2 = Frame(screen, width=635, height=80, bg=color2)
    frame2.place(x=220, y=110)
    frame2.config(bd=0, relief=GROOVE)

    frame3 = Frame(screen, width=635, height=80, bg=color2)
    frame3.place(x=220, y=205)
    frame3.config(bd=0, relief=GROOVE)

    frame4 = Frame(screen, width=635, height=130, bg=color2)
    frame4.place(x=220, y=300)
    frame4.config(bd=0, relief=GROOVE)

    # Labels & Entry-
    path = """''"""
    Label(frame1, image=current_virus_scanner, borderwidth=0).place(x=130, y=2)
    Label(frame1, text='Scan your device', font=(
        'Open Sans', 15), bg=color1).place(x=350, y=0)
    Label(screen, image=scan_icon, bg=color3).place(x=25, y=150)
    Label(frame2, text='Quick Scan (Recommended)', font=(
        'Open Sans', 13), bg=color2).place(x=10, y=10)
    Label(frame2, text='Checks the areas viruses target.',
          font=('Open Sans', 12), bg=color2).place(x=10, y=40)
    Label(frame3, text='Full Scan', font=(
        'Open Sans', 13), bg=color2).place(x=10, y=10)
    Label(frame3, text='Checks all your drives and folders - this will take some time.', font=('Open Sans', 12),
          bg=color2).place(x=10, y=43)
    Label(frame4, text='Custom Scan', font=(
        'Open Sans', 13), bg=color2).place(x=10, y=10)
    lbl = Label(frame4, text=f'Browse and Choose your directory for a scan', font=(
        'Open Sans', 12), bg=color2)
    lbl.place(x=10, y=40)

    def browse_folders():
        """
        The function browses files.
        :return: None
        """
        nonlocal path, lbl
        path = filedialog.askdirectory(initialdir="/", title="Choose a folder")
        lbl.configure(
            text=f"""The Chosen Directory to be scanned: {os.path.basename(path)}""")

    # Buttons
    Button(frame1, image=go_home, borderwidth=0, command=lambda: [
           screen.destroy(), main.deiconify()]).place(x=0, y=2)
    Button(frame1, image=go_security, borderwidth=0,
           command=lambda: [screen.destroy(), security_screen.deiconify()]).place(x=70, y=2)
    text = """This is the Virus Scanner Service.\n\nHere you can run quick, full or customed scans\nin order to find viruses or threats in your PC."""
    Button(frame1, image=get_help, bg=color2, borderwidth=0,
           command=lambda: help_screen(text)).place(x=820, y=0)

    Button(frame2, text='Run', bg=color4, borderwidth=1, width=21, height=2,
           command=lambda: [screen.destroy(), threading.Thread(target=progress_window.deiconify).start(),
                            threading.Thread(target=Security.virus_scan, args=('quick',)).start()]).place(x=465, y=15)
    Button(frame3, text='Run', bg=color4, borderwidth=1, width=21, height=2,
           command=lambda: [screen.destroy(), threading.Thread(target=progress_window.deiconify()).start(),
                            threading.Thread(target=Security.virus_scan, args=('full',)).start()]).place(x=465, y=15)
    Button(frame4, text='Browse', bg=color4, borderwidth=0, width=21, height=2, command=lambda: browse_folders()).place(
        x=465, y=25)
    Button(frame4, text='Run', bg=color4, borderwidth=0, width=21, height=2,
           command=lambda: [screen.destroy(), threading.Thread(target=progress_window.deiconify()).start(),
                            threading.Thread(target=Security.virus_scan, args=('full', path,)).start()]).place(x=465,
                                                                                                               y=80)

    screen.mainloop()


def found_virus_screen(infected_files):
    """
    The function displays a virus scan screen where the user can see the infected files that were found during the scan.
    :param infected_files: The list of the found infected files
    :return: None
    """
    global main, security_screen, progress_window
    if main:
        main.withdraw()
    screen = Screen().get_screen()

    # Frames
    frame1 = Frame(screen, width=875, height=35, bg=color1)
    frame1.place(x=0, y=0)
    frame1.config(bd=0, relief=GROOVE)

    frame2 = Frame(screen, width=840, height=240, bg=color2)
    frame2.place(x=20, y=80)
    frame2.config(bd=0, relief=GROOVE)

    # Labels
    Label(frame1, text='Alert Screen', font=(
        'Open Sans', 15), bg=color1).place(x=355, y=0)
    Label(frame2, text='Infected files that were found during the scan', font=('Open Sans', 14), bg=color2).pack(
        padx=237, pady=5)
    text = ''
    for index, infected_file in enumerate(infected_files):
        text += basename(infected_file)
        if (index + 1) % 6 == 0:
            text += '\n'
        elif index != (len(infected_files) - 1):
            text += ', '
    Label(frame2, text=text, font=('Open Sans', 13),
          bg=color2, justify=LEFT, anchor='w').pack()

    # Buttons
    if len(infected_files) > 1:
        txt = 'Remove all threats'
        Button(screen, text=txt, borderwidth=0, width=14, height=2,
               command=lambda: [Security.remove_files(infected_files), screen.destroy()]).place(x=745, y=440)
    else:
        txt = 'Remove threat'
        Button(screen, text=txt, borderwidth=0, width=14, height=2,
               command=lambda: [Security.remove_files(infected_files), screen.destroy()]).place(x=745, y=440)


def update_pc_screen():
    """
    The function displays an update screen where the user can check for windows updates.
    :return: None
    """
    global main, security_screen, progress_window
    if main:
        main.withdraw()
    screen = Screen().get_screen()

    # Photos
    get_help = PhotoImage(file='Gui_Photos/get_help_icon.png')
    go_home = PhotoImage(file='Gui_Photos/go_home.png')
    go_security = PhotoImage(file='Gui_Photos/go_security.png')
    current_updates_scanner = PhotoImage(
        file='Gui_Photos/current_updates_scanner.png')

    # Frames
    frame1 = Frame(screen, width=875, height=35, bg=color1)
    frame1.place(x=0, y=0)
    frame1.config(bd=0, relief=GROOVE)

    frame2 = Frame(screen, width=840, height=180, bg=color2)
    frame2.place(x=20, y=80)
    frame2.config(bd=0, relief=GROOVE)

    # Labels
    Label(frame1, image=current_updates_scanner,
          borderwidth=0).place(x=130, y=2)
    Label(frame1, text='Windows Update', font=(
        'Open Sans', 15), bg=color1).place(x=350, y=0)
    Label(frame2, text='Update Your PC', font=(
        'Open Sans', 13), bg=color1).place(x=10, y=10)
    Label(frame2, text='Finds and installs the latest updates for your Windows - so your pc stay safe and up to date',
          font=('Open Sans', 12), bg=color2).place(x=10, y=60)

    # Buttons
    Button(frame1, image=go_home, borderwidth=0, command=lambda: [
           screen.destroy(), main.deiconify()]).place(x=0, y=2)
    Button(frame1, image=go_security, borderwidth=0,
           command=lambda: [screen.destroy(), security_screen.deiconify()]).place(x=70, y=2)
    text = """This is the Updates Service.\n\nHere you can Check for updates\nfor your PC for keeping it up to date."""
    Button(frame1, image=get_help, bg=color2, borderwidth=0,
           command=lambda: help_screen(text)).place(x=820, y=0)
    Button(frame2, text='Check for updates', bg=color4, borderwidth=1, width=21, height=2,
           command=lambda: [screen.destroy(), threading.Thread(target=progress_window.deiconify()).start(),
                            threading.Thread(target=Security.check_for_updates).start()]).place(x=660, y=120)

    screen.bind('<Return>', lambda _: [screen.destroy(), threading.Thread(target=progress_window.deiconify()).start(),
                                       threading.Thread(target=Security.check_for_updates).start()])
    screen.mainloop()


def update_screen():
    """
    The function displays an update screen where the user can check for Software's updates.
    :return: None
    """
    global main, security_screen, progress_window
    if main:
        main.withdraw()
    screen = Screen().get_screen()

    # Photos
    get_help = PhotoImage(file='Gui_Photos/get_help_icon.png')
    go_home = PhotoImage(file='Gui_Photos/go_home.png')
    go_security = PhotoImage(file='Gui_Photos/go_security.png')
    current_updates_scanner = PhotoImage(
        file='Gui_Photos/current_updates_scanner.png')

    # Frames
    frame1 = Frame(screen, width=875, height=35, bg=color1)
    frame1.place(x=0, y=0)
    frame1.config(bd=0, relief=GROOVE)

    frame2 = Frame(screen, width=840, height=180, bg=color2)
    frame2.place(x=20, y=80)
    frame2.config(bd=0, relief=GROOVE)

    # Labels
    Label(frame1, image=current_updates_scanner,
          borderwidth=0).place(x=130, y=2)
    Label(frame1, text='Software Updates', font=(
        'Open Sans', 15), bg=color1).place(x=350, y=0)
    Label(frame2, text='Check for an update for AntiVirus-AV Software', font=('Open Sans', 13), bg=color2).place(x=10,
                                                                                                                 y=10)

    # Buttons
    Button(frame1, image=go_home, borderwidth=0, command=lambda: [
           screen.destroy(), main.deiconify()]).place(x=0, y=2)
    Button(frame1, image=go_security, borderwidth=0,
           command=lambda: [screen.destroy(), security_screen.deiconify()]).place(x=70, y=2)
    text = """This is the Updates Service.\n\nHere you can Check for AntiVirus AV Software\nfor keeping it up to date."""
    Button(frame1, image=get_help, bg=color2, borderwidth=0,
           command=lambda: help_screen(text)).place(x=820, y=0)
    Button(frame2, text='Check for updates', bg=color4, borderwidth=1, width=21, height=2,
           command=lambda: [screen.destroy(), threading.Thread(target=progress_window.deiconify).start(),
                            threading.Thread(target=Security.update_software_version).start()]).place(x=660, y=120)

    screen.bind('<Return>', lambda _: [screen.destroy(), threading.Thread(target=progress_window.deiconify).start(),
                                       threading.Thread(target=Security.update_software_version).start()])
    screen.mainloop()


def network_scanner_screen():
    """
    The function displays a network scan screen where the user can run network scans.
    :return: None
    """
    global main, security_screen, progress_window
    if main:
        main.withdraw()
    screen = Screen().get_screen()

    # Photos
    get_help = PhotoImage(file='Gui_Photos/get_help_icon.png')
    go_home = PhotoImage(file='Gui_Photos/go_home.png')
    go_security = PhotoImage(file='Gui_Photos/go_security.png')
    current_virus_scanner = PhotoImage(
        file='Gui_Photos/current_virus_scanner.png')

    # Frames
    frame1 = Frame(screen, width=875, height=35, bg=color1)
    frame1.place(x=0, y=0)
    frame1.config(bd=0, relief=GROOVE)

    frame2 = Frame(screen, width=840, height=180, bg=color2)
    frame2.place(x=20, y=80)
    frame2.config(bd=0, relief=GROOVE)

    # Labels
    Label(frame1, image=current_virus_scanner, borderwidth=0).place(x=130, y=2)
    Label(frame1, text='Network Scanning', font=(
        'Open Sans', 15), bg=color1).place(x=350, y=0)
    Label(frame2, text='Network Scanner', font=(
        'Open Sans', 13), bg=color2).place(x=10, y=10)
    Label(frame2, text='Scans for suspicious connections in your network', font=('Open Sans', 12), bg=color2).place(
        x=10, y=70)

    # Buttons
    Button(frame1, image=go_home, borderwidth=0, command=lambda: [
           screen.destroy(), main.deiconify()]).place(x=0, y=2)
    Button(frame1, image=go_security, borderwidth=0,
           command=lambda: [screen.destroy(), security_screen.deiconify()]).place(x=70, y=2)
    text = """This is the Network Scanner Service.\n\nHere you can search for suspicious connections\n in your network. if any found they'll\nbe removed."""
    Button(frame1, image=get_help, bg=color2, borderwidth=0,
           command=lambda: help_screen(text)).place(x=820, y=0)
    Button(frame2, text='Run', bg=color4, borderwidth=1, width=21, height=2,
           command=lambda: [screen.destroy(), threading.Thread(target=progress_window.deiconify).start(),
                            threading.Thread(target=Security.network_scanner).start()]).place(x=660, y=120)

    screen.bind('<Return>', lambda _: [screen.destroy(), threading.Thread(target=progress_window.deiconify).start(),
                                       threading.Thread(target=Security.network_scanner).start()])
    screen.mainloop()


def shredder_screen():
    """
    The function displays a shredder screen where the user can shred files..
    :return: None
    """
    global main, identity_screen, progress_window
    if main:
        main.withdraw()
    screen = Screen().get_screen()

    # Photos
    shredder_icon = PhotoImage(file='Gui_Photos/shredder_picture.png')
    get_help = PhotoImage(file='Gui_Photos/get_help_icon.png')
    go_home = PhotoImage(file='Gui_Photos/go_home.png')
    go_identity = PhotoImage(file='Gui_Photos/go_identity.png')
    current_shredder = PhotoImage(file='Gui_Photos/current_shredder.png')

    # Frames
    frame1 = Frame(screen, width=875, height=35, bg=color1)
    frame1.place(x=0, y=0)
    frame1.config(bd=0, relief=GROOVE)

    frame2 = Frame(screen, width=840, height=230, bg=color2)
    frame2.place(x=20, y=80)
    frame2.config(bd=0, relief=GROOVE)

    # Labels
    Label(frame1, image=current_shredder, borderwidth=0).place(x=172, y=0)
    Label(frame1, text='Shredder', font=(
        'Open Sans', 15), bg=color1).place(x=350, y=0)
    Label(screen, image=shredder_icon, bg=color3).place(x=650, y=360)
    Label(frame2, text='Shredder', font=(
        'Open Sans', 13), bg=color2).place(x=10, y=10)
    Label(frame2,
          text='Shredder Protects your identity by permanently deleting files, making sure sensitive information',
          font=('Open Sans', 12), bg=color2).place(x=5, y=45)
    Label(frame2, text="""can't be recovered""", font=(
        'Open Sans', 12), bg=color2).place(x=5, y=67)
    Label(frame2, text='Choose a folder to shred', font=(
        'Open Sans', 12), bg=color2).place(x=50, y=120)
    Label(frame2, text='Choose a shredding type', font=(
        'Open Sans', 12), bg=color2).place(x=325, y=120)

    # ComboBoxes-
    combo_box1 = Combobox(frame2, values=(
        'Recycle Bin', 'Temporary Files', 'Let Me Choose'))
    combo_box1.set('Recycle Bin')
    lbl1 = Label(frame2, text='Recycle Bin will be shred',
                 font=('Open Sans', 12), bg=color2)
    lbl1.place(x=50, y=170)

    def update_label1(event):
        nonlocal lbl1, path
        if combo_box1.get() == 'Recycle Bin':
            lbl1.config(text='Recycle Bin will be shred')

        elif combo_box1.get() == 'Temporary Files':
            lbl1.config(text='Windows temp files will be shred')

        else:  # combo_box1.get() == 'Let Me Choose':
            lbl1.config(text='Let me choose what to shred')
        path = combo_box1.get()
        lbl1.place(x=50, y=170)

    combo_box1.bind("<<ComboboxSelected>>", update_label1)
    combo_box1.place(x=50, y=145)

    combo_box2 = Combobox(frame2, values=('Basic', 'Safe', 'Complete'))
    combo_box2.set('Basic')  # Setting the Default Value
    lbl2 = Label(frame2, text='It shreds twice so its quick',
                 font=('Open Sans', 12), bg=color2)
    lbl2.place(x=325, y=170)

    def update_label2(event):
        nonlocal lbl2, mode
        if combo_box2.get() == 'Basic':
            lbl2.config(text='It shreds twice so its quick')

        elif combo_box2.get() == 'Safe':
            lbl2.config(text='It shreds five times so its secure')

        else:  # combo_box2.get() == 'Complete':
            lbl2.config(text='It shreds ten times for extra security')
        mode = combo_box2.get()
        lbl2.place(x=325, y=170)

    combo_box2.bind("<<ComboboxSelected>>", update_label2)
    combo_box2.place(x=325, y=145)
    mode = combo_box2.get()
    path = combo_box1.get()

    # Buttons
    Button(frame1, image=go_home, borderwidth=0, command=lambda: [
           screen.destroy(), main.deiconify()]).place(x=0, y=2)
    Button(frame1, image=go_identity, borderwidth=0,
           command=lambda: [screen.destroy(), identity_screen.deiconify()]).place(x=70, y=2)
    text = """This is the Shredder Service.\n\nHere your can shred sensitive inforamtion or\ntemporary files in order to protect your privacy."""
    Button(frame1, image=get_help, bg=color2, borderwidth=0,
           command=lambda: help_screen(text)).place(x=820, y=0)
    Button(frame2, text='Shred', bg=color4, borderwidth=1, width=21, height=2,
           command=lambda: [screen.destroy(), threading.Thread(target=progress_window.deiconify).start(),
                            threading.Thread(target=Identity.shred, args=(mode, path,)).start()]).place(x=660, y=120)

    screen.bind('<Return>', lambda _: [screen.destroy(), threading.Thread(target=progress_window.deiconify).start(),
                                       threading.Thread(target=Identity.shred, args=(mode, path,)).start()])
    screen.mainloop()


def firewall_screen():
    """
    The function displays a firewall screen where the user can manage the firewall.
    :return: None
    """
    global main, identity_screen, progress_window
    if main:
        main.withdraw()
    screen = Screen().get_screen()

    # Photos
    firewall_icon = PhotoImage(file='Gui_Photos/firewall_icon.png')
    get_help = PhotoImage(file='Gui_Photos/get_help_icon.png')
    go_home = PhotoImage(file='Gui_Photos/go_home.png')
    go_identity = PhotoImage(file='Gui_Photos/go_identity.png')
    current_firewall = PhotoImage(file='Gui_Photos/current_firewall.png')

    # Frames
    frame1 = Frame(screen, width=875, height=35, bg=color1)
    frame1.place(x=0, y=0)
    frame1.config(bd=0, relief=GROOVE)

    frame2 = Frame(screen, width=615, height=135,
                   bg=color2)
    frame2.place(x=245, y=95)
    frame2.config(bd=0, relief=GROOVE)

    frame3 = Frame(screen, width=615, height=135,
                   bg=color2)
    frame3.place(x=245, y=255)
    frame3.config(bd=0, relief=GROOVE)

    frame4 = Frame(screen, width=615, height=135,
                   bg=color2)
    frame4.place(x=245, y=415)
    frame4.config(bd=0, relief=GROOVE)

    # Labels
    Label(frame1, image=current_firewall, borderwidth=0).place(x=172, y=0)
    Label(frame1, text='FireWall Management', font=(
        'Open Sans', 15), bg=color1).place(x=320, y=0)
    Label(screen, image=firewall_icon, borderwidth=0,
          bg=color2).place(x=45, y=180)

    Label(frame2, text='Add Rule to Windows FireWall', font=('Open Sans', 13),
          bg=color1).place(x=20, y=5)
    Label(frame2, text='Rule Name', font=('Open Sans', 12),
          bg=color1).place(x=20, y=45)
    file_lbl = Label(frame2, text='Allow through firewall your program', font=('Open Sans', 12), borderwidth=0,
                     bg=color1)
    file_lbl.place(x=20, y=95)

    Label(frame3, text='Modify Rule', font=('Open Sans', 13),
          bg=color1).place(x=20, y=5)
    Label(frame3, text='Rule Name', font=('Open Sans', 12),
          bg=color1).place(x=20, y=45)
    Label(frame3, text='Rule Status (0/1)', font=('Open Sans', 11),
          bg=color1).place(x=200, y=45)

    Label(frame4, text='Allow/Block Port through Windows FireWall', font=('Open Sans', 13),
          bg=color1).place(x=20, y=5)
    Label(frame4, text='Port', font=('Open Sans', 12),
          bg=color1).place(x=20, y=45)
    Label(frame4, text='Port Type (TCP/UDP)', font=('Open Sans', 12),
          bg=color2).place(x=200, y=45)
    Label(frame4, text='Port Status (0/1)', font=('Open Sans', 12),
          bg=color2).place(x=380, y=45)
    lbl = Label(screen, text='FireWall Status: \nActive',
                font=('Open Sans', 11), borderwidth=0, bg=color3)
    lbl.place(x=45, y=80)

    # Entrys-
    rule_name1 = StringVar()
    file = None
    rule_name2 = StringVar()
    rule_status = StringVar()
    port = StringVar()
    protocol = StringVar()
    port_status = StringVar()

    rule_name_entry1 = Entry(frame2, textvariable=rule_name1)
    rule_name_entry1.place(x=20, y=70)

    rule_name_entry2 = Entry(frame3, textvariable=rule_name2)
    rule_name_entry2.place(x=20, y=70)

    rule_status_entry = Entry(frame3, textvariable=rule_status)
    rule_status_entry.place(x=200, y=70)

    port_entry = Entry(frame4, textvariable=port)
    port_entry.place(x=20, y=70)

    protocol_entry = Entry(frame4, textvariable=protocol)
    protocol_entry.place(x=200, y=70)

    port_status_entry = Entry(frame4, textvariable=port_status)
    port_status_entry.place(x=380, y=70)

    def clicked():
        from Identity import firewall
        if btn['text'] == "Active":
            success = firewall.activate_firewall()
            if success:
                btn.configure(text='Deactive')
                lbl.configure(text='FireWall Status: \nActive')
        else:
            success = firewall.deactivate_firewall()
            if success:
                btn.configure(text='Active')
                lbl.configure(text='FireWall Status: \nDeactive')

    def browse_files():
        """
        The function browses files.
        :return: None
        """
        nonlocal file, file_lbl
        file = filedialog.askopenfilename(
            initialdir="/", title="Select a File")
        file_lbl.configure(
            text=f"""Chosen File to be allowed through firewall : {os.path.basename(file)}""")

    # Buttons
    Button(frame1, image=go_home, borderwidth=0, command=lambda: [
           screen.destroy(), main.deiconify()]).place(x=0, y=2)
    Button(frame1, image=go_identity, borderwidth=0,
           command=lambda: [screen.destroy(), identity_screen.deiconify()]).place(x=70, y=2)
    text = """This is the Firewall Service.\n\nHere your can modify rules or\nadd ports to be allowed thorugh the firewall."""
    Button(frame1, image=get_help, bg=color2, borderwidth=0,
           command=lambda: help_screen(text)).place(x=820, y=0)
    Button(frame2, text='Browse files', bg=color4, borderwidth=1, width=14, height=1,
           command=lambda: browse_files()).place(x=495, y=100)
    Button(frame2, text='Add Rule', bg=color4, borderwidth=1, width=14, height=1,
           command=lambda: [Identity.add_rule(rule_name_entry1.get(), file), screen.destroy(),
                            progress_window.deiconify()]).place(x=495, y=50)
    Button(frame3, text='Modify Rule', bg=color4, borderwidth=1, width=14, height=1,
           command=lambda: [Identity.modify_rule(rule_name_entry2.get(), rule_status_entry.get(), screen.destroy(),
                                                 progress_window.deiconify())]).place(x=495, y=100)
    Button(frame4, text='Add/Modify Port', bg=color4, borderwidth=1, width=14, height=1,
           command=lambda: [Identity.modify_port(port_entry.get(), protocol_entry.get(), port_status_entry.get()),
                            screen.destroy(), progress_window.deiconify()]).place(x=495, y=100)
    Button(screen, text='Display FireWall Rules', bg=color4, borderwidth=1, width=20, height=1,
           command=lambda: [screen.destroy(), progress_window.deiconify(),
                            print(os.popen('powershell.exe get-netfirewallrule -all').read())]).place(x=30, y=315)
    Button(screen, text='Open Windows Defender Firewall ', bg=color4, borderwidth=1, width=25, height=1,
           command=lambda: [os.system('wf.msc')]).place(x=15, y=365)
    from Identity import firewall
    if firewall.get_firewall_status():
        btn = Button(screen, text='Deactive', bg=color4,
                     borderwidth=1, width=14, height=1, command=clicked)
    else:
        btn = Button(screen, text='Active', bg=color4,
                     borderwidth=1, width=14, height=1, command=clicked)
    btn.place(x=52, y=140)

    screen.mainloop()


def password_manager_screen(authenticated):
    """
    The function displays a password manager screen where the user can store and manage passwords.
    :param authenticated: a boolean value indicating whether the user was authenticated
    :return: None
    """
    global main, identity_screen, progress_window

    if main:
        main.withdraw()

    screen = Screen().get_screen()

    if not authenticated:
        screen.withdraw()
        authentication_screen(screen, 'password_manager')

    # Photos
    get_help = PhotoImage(file='Gui_Photos/get_help_icon.png')
    go_home = PhotoImage(file='Gui_Photos/go_home.png')
    go_identity = PhotoImage(file='Gui_Photos/go_identity.png')
    current_password_manager = PhotoImage(
        file='Gui_Photos/current_password_manager.png')

    # Frames
    frame1 = Frame(screen, width=875, height=35, bg=color1)
    frame1.place(x=0, y=0)
    frame1.config(bd=0, relief=GROOVE)

    # Creating Table-
    table = Sheet(screen)
    table.place(x=220, y=110)
    table.set_sheet_data([["" for j in range(2)] for j in range(20)])

    # table enable choices listed below:
    table.enable_bindings(("single_select", "row_select", "column_width_resize", "arrowkeys", "right_click_popup_menu",
                           "rc_select", "rc_insert_row", "rc_delete_row", "copy", "cut", "paste", "delete", "undo",
                           "edit_cell"))
    # Labels
    Label(frame1, image=current_password_manager,
          borderwidth=0).place(x=172, y=0)
    Label(frame1, text='Password Manager', font=(
        'Open Sans', 15), bg=color1).place(x=350, y=0)

    # Buttons
    Button(frame1, image=go_home, borderwidth=0, command=lambda: [
           screen.destroy(), main.deiconify()]).place(x=0, y=2)
    Button(frame1, image=go_identity, borderwidth=0,
           command=lambda: [screen.destroy(), identity_screen.deiconify()]).place(x=70, y=2)
    text = """This is the Password Manager Service.\n\nHere you can save your passwords with notes.\nIn order to use correctly please do not\npress any of the keys while selecting a cell.\n\n Please enter your password and notes for it\n and than press add. you can reveal or hide it\nby pressing the show/hide button.\n\n if you want to add more passwords,\nplease unhide your passwords and enter\nthe new one to the next empty slot."""
    Button(frame1, image=get_help, bg=color2, borderwidth=0,
           command=lambda: help_screen(text)).place(x=820, y=0)
    Button(screen, text='Add', bg=color4, borderwidth=1, width=21, height=2,
           command=lambda: Identity.add_password(table)).place(x=680, y=170)
    button = Button(screen, text='Show', bg=color4, borderwidth=1, width=21, height=2,
                    command=lambda: Identity.display(table, button))
    button.place(x=680, y=230)
    Button(screen, text='Clear', bg=color4, borderwidth=1, width=21, height=2,
           command=lambda: Identity.clear_data(table)).place(x=680, y=290)

    screen.mainloop()


def file_locker_screen():
    """
    The function displays a file locker screen where the user can lock files in the App_Locker.
    :return: None
    """
    global main, identity_screen, progress_window
    if main:
        main.withdraw()

    screen = Screen().get_screen()

    # Photos
    get_help = PhotoImage(file='Gui_Photos/get_help_icon.png')
    go_home = PhotoImage(file='Gui_Photos/go_home.png')
    go_identity = PhotoImage(file='Gui_Photos/go_identity.png')
    current_file_locker = PhotoImage(file='Gui_Photos/current_file_locker.png')

    # Frames
    frame1 = Frame(screen, width=875, height=35, bg=color1)
    frame1.place(x=0, y=0)
    frame1.config(bd=0, relief=GROOVE)

    frame2 = Frame(screen, width=840, height=200, bg=color2)
    frame2.place(x=20, y=80)
    frame2.config(bd=0, relief=GROOVE)

    # Labels
    path = ''
    Label(frame1, image=current_file_locker, borderwidth=0).place(x=172, y=0)
    Label(frame1, text='File App_Locker', font=(
        'Open Sans', 15), bg=color1).place(x=350, y=0)
    Label(frame2, text='File Locking', font=(
        'Open Sans', 13), bg=color2).place(x=10, y=10)
    Label(frame2, text='Lock your files in your locker',
          font=('Open Sans', 12), bg=color2).place(x=10, y=60)
    dir_lbl = Label(frame2, text=f'Browse and Choose your Directory to be locked', font=(
        'Open Sans', 12), bg=color2)
    dir_lbl.place(x=10, y=125)

    def browse_folders():
        """
        The function browses folders.
        :return: None
        """
        nonlocal path, dir_lbl
        path = filedialog.askopenfilename(initialdir="", title="Choose a file")
        dir_lbl.configure(
            text=f"""The Chosen file to be locked: {os.path.basename(path)}""")

    # Buttons
    Button(frame1, image=go_home, borderwidth=0, command=lambda: [
           screen.destroy(), main.deiconify()]).place(x=0, y=2)
    Button(frame1, image=go_identity, borderwidth=0,
           command=lambda: [screen.destroy(), identity_screen.deiconify()]).place(x=70, y=2)
    text = """This is the File App_Locker Service.\n\nHere your can lock yourfiles\nfor the purpose of keeping your privacy.\nin order to lock a directory please browse\nthe directory's path and\nthen select lock/unlock\nNote that all the files from the given directory\n will be deleted automatically."""
    Button(frame1, image=get_help, bg=color2, borderwidth=0,
           command=lambda: help_screen(text)).place(x=820, y=0)
    Button(frame2, text='Browse', bg=color4, borderwidth=1, width=21, height=2, command=lambda: browse_folders()).place(
        x=650, y=60)
    btn = Button(frame2, text='Lock', bg=color4, borderwidth=1, width=21, height=2, command=lambda: [
        Identity.locker('lock', path) if btn['text'] == 'lock' else Identity.locker(
            'unlock', path),
        btn.config(text='Unlock') if btn['text'] == 'Lock' else btn.config(text='Lock')])
    btn.place(x=650, y=125)

    screen.mainloop()


def unactive_service_screen(parent):
    """
    The function displays an unactive service screen.
    :param parent: the parent screen of the unactive service screen
    :return: None
    """
    global main, security_screen, identity_screen
    if main:
        main.withdraw()
    screen = Screen().get_screen()

    # Photos
    go_home = PhotoImage(file='Gui_Photos/go_home.png')
    go_security = PhotoImage(file='Gui_Photos/go_security.png')
    go_identity = PhotoImage(file='Gui_Photos/go_identity.png')
    current_unactive_service = PhotoImage(
        file='Gui_Photos/current_unactive_service.png')

    # Frames
    frame1 = Frame(screen, width=875, height=35, bg=color1)
    frame1.place(x=0, y=0)
    frame1.config(bd=0, relief=GROOVE)

    # Labels
    if parent == 'Identity':
        Label(frame1, image=current_unactive_service,
              borderwidth=0).place(x=168, y=2)
    else:
        Label(frame1, image=current_unactive_service,
              borderwidth=0).place(x=130, y=2)
    Label(screen,
          text="""This service is unactive. Active it in order to use it's features.\nYou can active this service by accessing the settings screen.""",
          font=('Open Sans', 13), bg=color3).place(x=200, y=260)

    # Buttons
    Button(frame1, image=go_home, borderwidth=0, command=lambda: [
           screen.destroy(), main.deiconify()]).place(x=0, y=2)
    if parent == 'Security':
        Button(frame1, image=go_security, borderwidth=0,
               command=lambda: [screen.destroy(), security_screen.deiconify()]).place(x=70, y=2)
    else:  # parent == 'Identity':
        Button(frame1, image=go_identity, borderwidth=0,
               command=lambda: [screen.destroy(), identity_screen.deiconify()]).place(x=70, y=2)

    screen.mainloop()


def progress_screen():
    """
    The function displays a progress window where the user can see the results of his actions.
    :return: None
    """

    global progress_window
    progress_window = Screen().get_screen()
    progress_window.withdraw()

    # Photos
    home = PhotoImage(file='Gui_Photos/home_button.png')

    # Frames
    frame1 = Frame(progress_window, width=875, height=35, bg=color1)
    frame1.place(x=0, y=0)
    frame1.config(bd=0, relief=GROOVE)

    # Labels
    Label(frame1, text='Progress bar', font=(
        'Open Sans', 15), bg=color1).place(x=350, y=0)

    # Output Handling
    output_box = Text(progress_window, bg=color3, height=35, width=108)
    output_box.place(x=0, y=35)

    # Displaying a scroll bar
    scroll_bar = Scrollbar(progress_window, command=output_box.yview)
    scroll_bar.place(x=855, y=36, height=550)

    # Buttons
    Button(frame1, image=home, borderwidth=0, command=lambda: [progress_window.withdraw(), main.deiconify()]).place(
        x=10, y=0)

    # keep original stdout and assigning RedirectText as stdout
    old_stdout = sys.stdout
    sys.stdout = Redirector(output_box)

    progress_window.bind('<Return>', lambda _: [
                         progress_window.withdraw(), main.deiconify()])
    progress_window.mainloop()
    sys.stdout = old_stdout  # assign back original stdout


def admin_screen():
    """
    The function displays the admin's screen.
    :return: None
    """
    global main, progress_window
    from Client import get_active_clients

    if main:
        main.withdraw()
    screen = Screen().get_screen()

    # Photos
    home = PhotoImage(file='Gui_Photos/home_button.png')

    # Frames
    frame1 = Frame(screen, width=875, height=35, bg=color1)
    frame1.place(x=0, y=0)
    frame1.config(bd=0, relief=GROOVE)

    frame2 = Frame(screen, width=840, height=230, bg=color2)
    frame2.place(x=20, y=80)
    frame2.config(bd=0, relief=GROOVE)

    # Labels
    Label(frame1, text="""Admin's Panel""", bg=color1,
          font=('Open Sans', 15)).place(x=350, y=0)
    Label(frame2, text='Active Client Connections', font=(
        'Open Sans', 15), bg=color1).place(x=0, y=5)
    Label(frame2, text=get_active_clients(), font=(
        'Open Sans', 12), bg=color1).place(x=0, y=80)
    # Buttons
    Button(frame1, image=home, borderwidth=0, command=lambda: [
           screen.destroy(), main.deiconify()]).place(x=10, y=0)

    screen.bind('<Return>', lambda _: [screen.destroy(), main.deiconify()])
    screen.mainloop()


def notification_screen():
    """
    The function displays a small notification screen where the
    user can see his/her notification.
    :return: None
    """
    global main, new_notification
    screen = Toplevel()
    screen.geometry('320x330')
    screen.resizable(False, False)
    screen["background"] = color3
    screen.title('AntiVirus-AV')
    screen.iconbitmap('Gui_Photos/logo.ico')

    windowWidth = screen.winfo_reqwidth()
    windowHeight = screen.winfo_reqheight()
    # Gets both half the screen width/height and window width/height
    positionRight = int(screen.winfo_screenwidth() / 1.72 - windowWidth / 5)
    positionDown = int(screen.winfo_screenheight() / 1.46 - windowHeight / 0.5)
    # Positions the window in the center of the page.
    screen.geometry("+{}+{}".format(positionRight, positionDown))

    # Photos
    back_button = PhotoImage(file='Gui_Photos/back_button.png')

    # Frames
    frame1 = Frame(screen, width=320, height=35, bg=color1)
    frame1.place(x=0, y=0)
    frame1.config(bd=0, relief=GROOVE)

    # Labels
    Label(frame1, text='Notifications', font=(
        'Open Sans', 14), bg=color1).place(x=100, y=0)

    if not new_notification:
        Label(screen, text=f"""{Handle_User.user_instance.get_username()}'s Notifications List is empty""",
              font=('Open Sans', 12), bg=color3).pack(pady=45)
    else:
        Label(screen,
              text=f"""{Handle_User.user_instance.get_username()}'s Notifications List:\n\n {f"".join(new_notification[len(new_notification) - 1])}""",
              font=('Open Sans', 12), bg=color3).pack(pady=45)
        new_notification.remove(new_notification[len(new_notification) - 1])
        with open('App_Files/Notifications.txt', "w+"):
            pass
        screen.after(5500, screen.destroy)

    # Buttons
    Button(frame1, text='Back', image=back_button, compound='left', bg=color1, fg=color4, width=65, height=28,
           borderwidth=0, command=lambda: screen.destroy()).place(x=0, y=0)

    if not new_notification:
        global notifications_button, blank_notification_icon, current_notification_icon
        current_notification_icon = blank_notification_icon
        global frame0
        if notifications_button:
            notifications_button.destroy()
        notifications_button = Button(frame0, image=current_notification_icon, bg=color2, borderwidth=0,
                                      command=lambda: notification_screen())
        notifications_button.place(x=670, y=0)

    screen.mainloop()


def display_notifications(notification):
    """
    The function displays new notifications for the user.
    :return: None
    """
    global new_notification_icon, current_notification_icon, notifications_button, new_notification
    new_notification.append(notification)
    with open('App_Files/Notifications.txt', 'a') as file:
        file.write(new_notification[len(new_notification) - 1])
        file.write('\n')
    current_notification_icon = new_notification_icon
    notifications_button = Button(frame0, image=current_notification_icon, bg=color2, borderwidth=0,
                                  command=lambda: notification_screen())
    notifications_button.place(x=670, y=0)


def settings_screen():
    """
    The function displays a services screen where the user can manage the running services of the software.
    :return: None
    """
    from Security import virus_scanner, updates_scanner, network_scanner_object
    from Identity import shredder, firewall, password_manager, file_locker
    global main

    screen = Toplevel()
    screen.geometry('300x330')
    screen.resizable(False, False)
    screen["background"] = color3
    screen.title('AntiVirus-AV')
    screen.iconbitmap('Gui_Photos/logo.ico')

    windowWidth = screen.winfo_reqwidth()
    windowHeight = screen.winfo_reqheight()
    # Gets both half the screen width/height and window width/height
    positionRight = int(screen.winfo_screenwidth() / 1.42 - windowWidth / 1.9)
    positionDown = int(screen.winfo_screenheight() / 3.2 - windowHeight / 1.5)
    # Positions the window in the center of the page.
    screen.geometry("+{}+{}".format(positionRight, positionDown))

    # Photos
    back_button = PhotoImage(file='Gui_Photos/back_button.png')
    fully_secured = PhotoImage(file='Gui_Photos/fully_secured.png')
    protected_security = PhotoImage(file='Gui_Photos/protected_security.png')
    protected_identity = PhotoImage(file='Gui_Photos/protected_identity.png')
    unprotected_security = PhotoImage(
        file='Gui_Photos/unprotected_security.png')
    unprotected_identity = PhotoImage(
        file='Gui_Photos/unprotected_identity.png')
    fully_protected = PhotoImage(file='Gui_Photos/fully_protected.png')
    fully_unprotected = PhotoImage(file='Gui_Photos/fully_unprotected.png')
    settings_virus_scanner_on = PhotoImage(
        file='Gui_Photos/settings_virus_scanner_on.png')
    settings_virus_scanner_off = PhotoImage(
        file='Gui_Photos/settings_virus_scanner_off.png')
    settings_updates_scanner_on = PhotoImage(
        file='Gui_Photos/settings_updates_scanner_on.png')
    settings_updates_scanner_off = PhotoImage(
        file='Gui_Photos/settings_updates_scanner_off.png')
    settings_shredder_on = PhotoImage(
        file='Gui_Photos/settings_shredder_on.png')
    settings_shredder_off = PhotoImage(
        file='Gui_Photos/settings_shredder_off.png')
    settings_firewall_on = PhotoImage(
        file='Gui_Photos/settings_firewall_on.png')
    settings_firewall_off = PhotoImage(
        file='Gui_Photos/settings_firewall_off.png')
    settings_password_manager_on = PhotoImage(
        file='Gui_Photos/settings_password_manager_on.png')
    settings_password_manager_off = PhotoImage(
        file='Gui_Photos/settings_password_manager_off.png')
    settings_file_locker_on = PhotoImage(
        file='Gui_Photos/settings_file_locker_on.png')
    settings_file_locker_off = PhotoImage(
        file='Gui_Photos/settings_file_locker_off.png')

    # Frames
    firstframe = Frame(screen, width=300, height=35, bg=color1)
    firstframe.place(x=0, y=0)
    firstframe.config(bd=0, relief=GROOVE)

    # Labels
    Label(firstframe, text='Services', font=(
        'Open Sans', 14), bg=color1).place(x=110, y=0)
    Label(screen, text='Security', font=(
        'Open Sans', 13), bg=color1).pack(pady=40)
    Label(screen, text='Identity', font=(
        'Open Sans', 13), bg=color1).pack(pady=40)

    firewall_status = firewall.get_service_status()
    if firewall_status:
        firewall_status = 'ON'
    else:
        firewall_status = 'OFF'

    def active_or_deactive_service(service):
        """
        The function actives/deactivate the given service.
        :return: None
        """
        global main, security_screen, identity_screen, info_screen, main_frame1, main_frame2, security_frame1, security_frame2, identity_frame1, identity_frame2, info_frame1, info_frame2
        global protected_lbl, unprotected_lbl1, unprotected_lbl2
        global security_protected_lbl1, security_protected_lbl2, security_unprotected_lbl1, security_unprotected_lbl2
        global identity_protected_lbl1, identity_protected_lbl2, identity_unprotected_lbl1, identity_unprotected_lbl2
        global info_protected_lbl1, info_protected_lbl2, info_unprotected_lbl1, info_unprotected_lbl2
        nonlocal firewall_status

        if service == 'Scanners':
            nonlocal scanner_btn
            if scanner_btn['text'] == 'OFF':
                scanner_btn.config(text='ON')
                scanner_btn.config(image=settings_virus_scanner_on)
                virus_scanner.set_service_status('ON')
                network_scanner_object.set_service_status('ON')
                print('Virus Scanner Service is now activated')
                try:
                    security_frame1.destroy()
                    security_frame2.destroy()

                    security_frame1 = Frame(
                        security_screen, width=200, height=200, bg=color1)
                    security_frame1.place(x=120, y=110)
                    security_frame1.config(bd=0, relief=GROOVE)

                    security_frame2 = Frame(
                        security_screen, width=400, height=200, bg=color1)
                    security_frame2.place(x=400, y=110)
                    security_frame2.config(bd=0, relief=GROOVE)

                    security_protected_lbl1 = Label(
                        security_frame1, image=protected_security, borderwidth=0)
                    security_protected_lbl1.pack()
                    security_protected_lbl2 = Label(security_frame2, text='Your PC is secured', borderwidth=0,
                                                    font=('Open Sans', 13), bg=color1)
                    security_protected_lbl2.place(x=130, y=85)
                except:
                    pass
            else:
                scanner_btn.config(text='OFF')
                scanner_btn.config(image=settings_virus_scanner_off)
                virus_scanner.set_service_status('OFF')
                network_scanner_object.set_service_status('OFF')
                print('Virus Scanner Service is now deactivated')
                try:
                    security_frame1.destroy()
                    security_frame2.destroy()

                    security_frame1 = Frame(
                        security_screen, width=200, height=200, bg=color1)
                    security_frame1.place(x=120, y=110)
                    security_frame1.config(bd=0, relief=GROOVE)

                    security_frame2 = Frame(
                        security_screen, width=400, height=200, bg=color1)
                    security_frame2.place(x=400, y=110)
                    security_frame2.config(bd=0, relief=GROOVE)

                    security_unprotected_lbl1 = Label(
                        security_frame1, image=unprotected_security, borderwidth=0)
                    security_unprotected_lbl1.pack()
                    security_unprotected_lbl2 = Label(security_frame2, text='Your PC is unprotected', borderwidth=0,
                                                      font=('Open Sans', 13), bg=color1)
                    security_unprotected_lbl2.place(x=125, y=85)
                except:
                    pass

        elif service == 'Updates Scanner':
            nonlocal updates_scanner_btn
            if updates_scanner_btn['text'] == 'OFF':
                updates_scanner_btn.config(text='ON')
                updates_scanner_btn.config(image=settings_updates_scanner_on)
                updates_scanner.set_service_status('ON')
                print('Updates Scanner Service is now activated')
                try:
                    security_frame1.destroy()
                    security_frame2.destroy()

                    security_frame1 = Frame(
                        security_screen, width=200, height=200, bg=color1)
                    security_frame1.place(x=120, y=110)
                    security_frame1.config(bd=0, relief=GROOVE)

                    security_frame2 = Frame(
                        security_screen, width=400, height=200, bg=color1)
                    security_frame2.place(x=400, y=110)
                    security_frame2.config(bd=0, relief=GROOVE)

                    security_protected_lbl1 = Label(
                        security_frame1, image=protected_security, borderwidth=0)
                    security_protected_lbl1.pack()
                    security_protected_lbl2 = Label(security_frame2, text='Your PC is secured', borderwidth=0,
                                                    font=('Open Sans', 13), bg=color1)
                    security_protected_lbl2.place(x=130, y=85)
                except:
                    pass
            else:
                updates_scanner_btn.config(text='OFF')
                updates_scanner_btn.config(image=settings_updates_scanner_off)
                updates_scanner.set_service_status('OFF')
                print('Updates Scanner Service is now deactivated')
                try:
                    security_frame1.destroy()
                    security_frame2.destroy()

                    security_frame1 = Frame(
                        security_screen, width=200, height=200, bg=color1)
                    security_frame1.place(x=120, y=110)
                    security_frame1.config(bd=0, relief=GROOVE)

                    security_frame2 = Frame(
                        security_screen, width=400, height=200, bg=color1)
                    security_frame2.place(x=400, y=110)
                    security_frame2.config(bd=0, relief=GROOVE)

                    security_unprotected_lbl1 = Label(
                        security_frame1, image=unprotected_security, borderwidth=0)
                    security_unprotected_lbl1.pack()
                    security_unprotected_lbl2 = Label(security_frame2, text='Your PC is unprotected', borderwidth=0,
                                                      font=('Open Sans', 13), bg=color1)
                    security_unprotected_lbl2.place(x=125, y=85)
                except:
                    pass

        elif service == 'Shredder':
            from Identity import firewall
            nonlocal shredder_btn
            firewall_status = firewall.get_service_status()
            if firewall_status:
                firewall_status = 'ON'
            else:
                firewall_status = 'OFF'

            if shredder_btn['text'] == 'OFF':
                shredder_btn.config(text='ON')
                shredder_btn.config(image=settings_shredder_on)
                shredder.set_service_status('ON')
                print('Shredder Service is now activated')
                try:
                    identity_frame1.destroy()
                    identity_frame2.destroy()

                    identity_frame1 = Frame(
                        identity_screen, width=200, height=200, bg=color1)
                    identity_frame1.place(x=120, y=110)
                    identity_frame1.config(bd=0, relief=GROOVE)

                    identity_frame2 = Frame(
                        identity_screen, width=400, height=200, bg=color1)
                    identity_frame2.place(x=400, y=110)
                    identity_frame2.config(bd=0, relief=GROOVE)

                    identity_protected_lbl1 = Label(
                        identity_frame1, image=protected_identity, borderwidth=0)
                    identity_protected_lbl1.pack()
                    identity_protected_lbl2 = Label(identity_frame2, text='Your identity is secured', borderwidth=0,
                                                    font=('Open Sans', 13), bg=color1)
                    identity_protected_lbl2.place(x=121, y=85)
                except:
                    pass
            else:
                shredder_btn.config(text='OFF')
                shredder_btn.config(image=settings_shredder_off)
                shredder.set_service_status('OFF')
                print('Shredder Service is now deactivated')
                try:
                    identity_frame1.destroy()
                    identity_frame2.destroy()

                    identity_frame1 = Frame(
                        identity_screen, width=200, height=200, bg=color1)
                    identity_frame1.place(x=120, y=110)
                    identity_frame1.config(bd=0, relief=GROOVE)

                    identity_frame2 = Frame(
                        identity_screen, width=400, height=200, bg=color1)
                    identity_frame2.place(x=400, y=110)
                    identity_frame2.config(bd=0, relief=GROOVE)

                    identity_unprotected_lbl1 = Label(
                        identity_frame1, image=unprotected_identity, borderwidth=0)
                    identity_unprotected_lbl1.pack()
                    identity_unprotected_lbl2 = Label(identity_frame2, text='Your identity is unsecured', borderwidth=0,
                                                      font=('Open Sans', 13), bg=color1)
                    identity_unprotected_lbl2.place(x=121, y=85)
                except:
                    pass

        elif service == 'Firewall':
            from Identity import firewall
            nonlocal firewall_btn
            firewall_status = firewall.get_service_status()
            if firewall_status:
                firewall_status = 'ON'
            else:
                firewall_status = 'OFF'

            if firewall_btn['text'] == 'OFF':
                firewall_btn.config(text='ON')
                firewall.activate_firewall()
                try:
                    identity_frame1.destroy()
                    identity_frame2.destroy()

                    identity_frame1 = Frame(
                        identity_screen, width=200, height=200, bg=color1)
                    identity_frame1.place(x=120, y=110)
                    identity_frame1.config(bd=0, relief=GROOVE)

                    identity_frame2 = Frame(
                        identity_screen, width=400, height=200, bg=color1)
                    identity_frame2.place(x=400, y=110)
                    identity_frame2.config(bd=0, relief=GROOVE)

                    identity_protected_lbl1 = Label(
                        identity_frame1, image=protected_identity, borderwidth=0)
                    identity_protected_lbl1.pack()
                    identity_protected_lbl2 = Label(identity_frame2, text='Your identity is secured', borderwidth=0,
                                                    font=('Open Sans', 13), bg=color1)
                    identity_protected_lbl2.place(x=121, y=85)
                except:
                    pass
            else:
                firewall_btn.config(text='OFF')
                firewall.deactivate_firewall()
                try:
                    identity_frame1.destroy()
                    identity_frame2.destroy()

                    identity_frame1 = Frame(
                        identity_screen, width=200, height=200, bg=color1)
                    identity_frame1.place(x=120, y=110)
                    identity_frame1.config(bd=0, relief=GROOVE)

                    identity_frame2 = Frame(
                        identity_screen, width=400, height=200, bg=color1)
                    identity_frame2.place(x=400, y=110)
                    identity_frame2.config(bd=0, relief=GROOVE)

                    identity_unprotected_lbl1 = Label(
                        identity_frame1, image=unprotected_identity, borderwidth=0)
                    identity_unprotected_lbl1.pack()
                    identity_unprotected_lbl2 = Label(identity_frame2, text='Your identity is unsecured', borderwidth=0,
                                                      font=('Open Sans', 13), bg=color1)
                    identity_unprotected_lbl2.place(x=121, y=85)
                except:
                    pass

        elif service == 'Password Manager':
            from Identity import firewall
            nonlocal password_manager_btn
            firewall_status = firewall.get_service_status()
            if firewall_status:
                firewall_status = 'ON'
            else:
                firewall_status = 'OFF'
            if password_manager_btn['text'] == 'OFF':
                password_manager_btn.config(text='ON')
                password_manager_btn.config(image=settings_password_manager_on)
                password_manager.set_service_status('ON')
                print('Password Manager Service is now activated')
            else:
                password_manager_btn.config(text='OFF')
                password_manager_btn.config(
                    image=settings_password_manager_off)
                password_manager.set_service_status('OFF')
                print('Password Manager Service is now deactivated')

        elif service == 'File App_Locker':
            from Identity import firewall
            nonlocal file_locker_btn
            firewall_status = firewall.get_service_status()
            if firewall_status:
                firewall_status = 'ON'
            else:
                firewall_status = 'OFF'

            if file_locker_btn['text'] == 'OFF':
                file_locker_btn.config(text='ON')
                file_locker_btn.config(image=settings_file_locker_on)
                file_locker.set_service_status('ON')
                print('File App_Locker Service is now activated')
            else:
                file_locker_btn.config(text='OFF')
                file_locker_btn.config(image=settings_file_locker_off)
                file_locker.set_service_status('OFF')
                print('File App_Locker Service is now deactivated')
        try:
            main_frame1.destroy()
            main_frame2.destroy()
            info_frame1.destroy()
            info_frame2.destroy()

            info_frame1 = Frame(info_screen, width=200, height=200, bg=color1)
            info_frame1.place(x=120, y=110)
            info_frame1.config(bd=0, relief=GROOVE)

            info_frame2 = Frame(info_screen, width=400, height=200, bg=color1)
            info_frame2.place(x=400, y=110)
            info_frame2.config(bd=0, relief=GROOVE)
        except:
            pass
        main_frame1 = Frame(main, width=650, height=200, bg=color1)
        main_frame1.place(x=120, y=100)
        main_frame1.config(bd=0, relief=GROOVE)

        if virus_scanner.get_service_status() == 'ON' and updates_scanner.get_service_status() == 'ON' and network_scanner_object.get_service_status() == 'ON' and firewall_status == 'ON' and shredder.get_service_status() == 'ON':
            protected_lbl = Label(main_frame1, image=fully_secured, borderwidth=0, font=(
                'Open Sans', 15), bg=color1)
            protected_lbl.pack(padx=[90, 30])
            try:
                info_protected_lbl1 = Label(
                    info_frame1, image=fully_protected, borderwidth=0)
                info_protected_lbl1.pack()
                info_protected_lbl2 = Label(info_frame2, text="""You'r PC and Identity are fully protected""",
                                            borderwidth=0, font=('Open Sans', 13), bg=color1)
                info_protected_lbl2.place(x=61, y=85)
            except:
                pass
        else:
            main_frame2 = Frame(main, width=400, height=200, bg=color1)
            main_frame2.place(x=400, y=110)
            main_frame2.config(bd=0, relief=GROOVE)
            try:
                info_unprotected_lb1 = Label(
                    info_frame1, image=fully_unprotected, borderwidth=0)
                info_unprotected_lb1.pack()
                info_unprotected_lbl2 = Label(info_frame2, text='You are unprotected', borderwidth=0,
                                              font=('Open Sans', 13), bg=color1)
                info_unprotected_lbl2.place(x=125, y=85)
            except:
                pass

            if virus_scanner.get_service_status() == 'OFF' or updates_scanner.get_service_status() == 'OFF' or network_scanner_object.get_service_status() == 'OFF':
                unprotected_lbl1 = Label(
                    main_frame1, image=unprotected_security, borderwidth=0)
                unprotected_lbl1.pack()
                unprotected_lbl2 = Label(main_frame2,
                                         text='Check out your security protection\nto find out how you can\n protect your PC',
                                         borderwidth=0, font=('Open Sans', 15), bg=color1)
                unprotected_lbl2.place(x=45, y=75)
            else:
                unprotected_lbl1 = Label(
                    main_frame1, image=unprotected_identity, borderwidth=0)
                unprotected_lbl1.pack()
                unprotected_lbl2 = Label(main_frame2,
                                         text='Check your identity protection\nto find out how you can\nprotect your identity',
                                         borderwidth=0, font=('Open Sans', 15), bg=color1)
                unprotected_lbl2.place(x=45, y=75)

    # Buttons
    scanner_btn = Button(screen, text=virus_scanner.get_service_status(), image=[
        settings_virus_scanner_on if virus_scanner.get_service_status().capitalize() == 'On' else settings_virus_scanner_off],
        borderwidth=0, font=('Open Sans', 11), bg=color3,
        command=lambda: active_or_deactive_service('Scanners'))
    scanner_btn.place(x=0, y=70)
    updates_scanner_btn = Button(screen, text=updates_scanner.get_service_status(), image=[
        settings_updates_scanner_on if updates_scanner.get_service_status().capitalize() == 'On' else settings_updates_scanner_off],
        borderwidth=0, font=('Open Sans', 11), bg=color3,
        command=lambda: active_or_deactive_service('Updates Scanner'))
    updates_scanner_btn.place(x=0, y=105)
    shredder_btn = Button(screen, text=shredder.get_service_status(), image=[
        settings_shredder_on if shredder.get_service_status().capitalize() == 'On' else settings_shredder_off],
        borderwidth=0, font=('Open Sans', 11), bg=color3,
        command=lambda: active_or_deactive_service('Shredder'))
    shredder_btn.place(x=0, y=175)
    firewall_btn = Button(screen, text=firewall_status, image=[
        settings_firewall_on if firewall_status.capitalize() == 'On' else settings_firewall_off], borderwidth=0,
        font=('Open Sans', 11), bg=color3, command=lambda: active_or_deactive_service('Firewall'))
    firewall_btn.place(x=0, y=210)
    password_manager_btn = Button(screen, text=password_manager.get_service_status(), image=[
        settings_password_manager_on if password_manager.get_service_status().capitalize() == 'On' else settings_password_manager_off],
        borderwidth=0, font=('Open Sans', 11), bg=color3,
        command=lambda: active_or_deactive_service('Password Manager'))
    password_manager_btn.place(x=0, y=245)
    file_locker_btn = Button(screen, text=file_locker.get_service_status(), image=[
        settings_file_locker_on if file_locker.get_service_status().capitalize() == 'On' else settings_file_locker_off],
        borderwidth=0, font=('Open Sans', 11), bg=color3,
        command=lambda: active_or_deactive_service('File App_Locker'))
    file_locker_btn.place(x=0, y=280)
    Button(firstframe, text='Back', image=back_button, compound='left', bg=color1, fg=color4, width=65, height=28,
           borderwidth=0, command=lambda: screen.destroy()).place(x=0, y=0)

    screen.mainloop()


def help_screen(instructions):
    """
    The function displays a small help screen that guides the user what to do.
    :param instructions: the instructions that sholud be displayed on the help screen
    :return: None
    """
    screen = Toplevel()
    screen.geometry('340x340')
    screen.resizable(False, False)
    screen["background"] = color3
    screen.title('AntiVirus-AV')
    screen.iconbitmap('Gui_Photos/logo.ico')

    windowWidth = screen.winfo_reqwidth()
    windowHeight = screen.winfo_reqheight()
    # Gets both half the screen width/height and window width/height
    positionRight = int(screen.winfo_screenwidth() / 1.5 - windowWidth / 1.9)
    positionDown = int(screen.winfo_screenheight() / 3 - windowHeight / 1.5)
    # Positions the window in the center of the page.
    screen.geometry("+{}+{}".format(positionRight, positionDown))

    # Photos
    back_button = PhotoImage(file='Gui_Photos/back_button.png')

    # Frames
    frame1 = Frame(screen, width=340, height=35, bg=color1)
    frame1.place(x=0, y=0)
    frame1.config(bd=0, relief=GROOVE)

    # Labels
    Button(frame1, text='Back', image=back_button, compound='left', bg=color1, fg=color4, width=65, height=28,
           borderwidth=0, command=lambda: screen.destroy()).place(x=0, y=0)
    Label(frame1, text='Help', font=('Open Sans', 14),
          bg=color1).place(x=144, y=0)
    Label(screen, text=instructions, font=(
        'Open Sans', 11), bg=color3).pack(pady=40)

    screen.mainloop()


def view_account(authenticated):
    """
    The function displays a small account details screen.
    :param authenticated: a boolean value indicating whether the user was authenticated
    :return: None
    """
    global main, info_screen, progress_window
    screen = Screen().get_screen()

    if not authenticated:
        screen.withdraw()
        authentication_screen(screen, 'view_account')

    if main:
        main.withdraw()

    # Photos
    go_home = PhotoImage(file='Gui_Photos/go_home.png')
    go_info = PhotoImage(file='Gui_Photos/go_info.png')

    # Frames
    frame1 = Frame(screen, width=875, height=35, bg=color1)
    frame1.place(x=0, y=0)
    frame1.config(bd=0, relief=GROOVE)

    frame2 = Frame(screen, width=840, height=180, bg=color2)
    frame2.place(x=20, y=80)
    frame2.config(bd=0, relief=GROOVE)

    # Labels
    if Handle_User.user_instance.get_user_type():
        is_admin = 'Administrator'
    else:
        is_admin = 'Premium User'

    Label(frame1, text='My Account', font=(
        'Open Sans', 15), bg=color1).place(x=350, y=0)
    lbl = Label(frame2,
                text=f'Username: {Handle_User.user_instance.get_username()}\n\nMail: {Handle_User.user_instance.get_mail()}\n\nPassword: ' + "".join(
                    ['*' for _ in range(len(Handle_User.user_instance.get_password()))]) + f'\n\nUser type: {is_admin}',
                font=('Open Sans', 14), bg=color2)
    lbl.place(x=310, y=10)

    # Buttons
    Button(frame1, image=go_home, borderwidth=0, command=lambda: [
           screen.destroy(), main.deiconify()]).place(x=0, y=2)
    Button(frame1, image=go_info, borderwidth=0, command=lambda: [screen.destroy(), info_screen.deiconify()]).place(
        x=70, y=2)
    Button(frame2, text='Change Details', font=('Open Sans', 12), background=color2, borderwidth=0,
           command=lambda: change_details_screen()).place(x=700, y=5)
    btn = Button(frame2, text='Show', font=('Open Sans', 12), background=color2, borderwidth=0,
                 command=lambda: [change_btn_text(), lbl.config(
                     text=f'Username: {Handle_User.user_instance.get_username()}\n\nMail: {Handle_User.user_instance.get_mail()}\n\nPassword: {Handle_User.user_instance.get_password()}\n\nUser type: {is_admin}') if '*' in
                                                                                                                                                                                                                       lbl[
                                                                                                                                                                                                                           'text'] else lbl.config(
                     text=f'Username: {Handle_User.user_instance.get_username()}\n\nMail: {Handle_User.user_instance.get_mail()}\n\nPassword: ' + "".join(
                         ['*' for _ in
                          range(len(Handle_User.user_instance.get_password()))]) + f'\n\nUser type: {is_admin}')])
    btn.place(x=521, y=97)

    def change_btn_text():
        nonlocal btn
        if btn['text'] == 'Show':
            btn.config(text='Hide')
        else:
            btn.config(text='Show')

    screen.mainloop()


def authentication_screen(parent, next_function):
    """
    the function displays a user validation window.
    :param parent: the previous window
    :param next_function: the function to be displayed after authentication
    :return: None
    """
    screen = Toplevel()
    if main:
        main.withdraw()
    screen.title("Authentication Screen")
    screen.geometry("300x250")
    screen.resizable(False, False)
    screen['background'] = color3
    screen.title('AntiVirus-AV')
    screen.iconbitmap('Gui_Photos/logo.ico')

    windowWidth = screen.winfo_reqwidth()
    windowHeight = screen.winfo_reqheight()
    # Gets both half the screen width/height and window width/height
    positionRight = int(screen.winfo_screenwidth() / 2.5 - windowWidth / 2)
    positionDown = int(screen.winfo_screenheight() / 3.5 - windowHeight / 2)
    # Positions the window in the center of the page.
    screen.geometry("+{}+{}".format(positionRight, positionDown))

    # Photos
    exit_button = PhotoImage(file='Gui_Photos/exit_button.png')

    # Labels
    Label(screen, text='Password', font=('OpenSans', 13), bg=color3).pack()
    lbl = Label(screen, text="Authentication Failed - invalid password",
                bg=color3, fg="red", font=('Open Sans', 8))

    # Entrys
    password = StringVar()
    password_entry = Entry(screen, show='*', textvariable=password)
    password_entry.pack(pady=5)
    password_entry.focus()

    # Buttons
    Button(screen, text='Check', font=('OpenSans', 12), bg=color4, borderwidth=1, width=9, height=1,
           command=lambda: [
               continue_button.pack() if Handle_User.authenticate_user(password_entry.get()) else [lbl.pack(pady=5),
                                                                                                   screen.after(2000,
                                                                                                                lbl.destroy)]]).pack(
        pady=5)

    if next_function == 'view_account':
        continue_button = Button(screen, text='Continue', font=('OpenSans', 12), bg=color4, borderwidth=1, width=9,
                                 height=1,
                                 command=lambda: [screen.destroy(), parent.destroy(), view_account(True)])
    elif next_function == 'password_manager':
        continue_button = Button(screen, text='Continue', font=('OpenSans', 12), bg=color4, borderwidth=1, width=9,
                                 height=1,
                                 command=lambda: [screen.destroy(), parent.destroy(), password_manager_screen(True)])
    Button(screen, image=exit_button, bg=color4, width=20, height=20, borderwidth=0,
           command=lambda: [main.deiconify(), parent.destroy(), screen.destroy()]).place(x=1, y=5)

    screen.mainloop()


def change_details_screen():
    """
    The function displays a Registration window.
    :return: None
    """

    global details_screen
    details_screen = Toplevel()
    details_screen.geometry("300x400")
    details_screen.resizable(False, False)
    details_screen['background'] = color3
    details_screen.title('AntiVirus-AV')
    details_screen.iconbitmap('Gui_Photos/logo.ico')

    windowWidth = details_screen.winfo_reqwidth()
    windowHeight = details_screen.winfo_reqheight()
    # Gets both half the screen width/height and window width/height
    positionRight = int(
        details_screen.winfo_screenwidth() / 2.5 - windowWidth / 2)
    positionDown = int(details_screen.winfo_screenheight() /
                       3.5 - windowHeight / 2)
    # Positions the window in the center of the page.
    details_screen.geometry("+{}+{}".format(positionRight, positionDown))

    # Labels & Entrys-
    name = StringVar()
    mail = StringVar()
    username = StringVar()
    password = StringVar()
    Label(details_screen, text='Please enter your new details below.\nFill only the filed you are willing to change.',
          font=('Open Sans', 11),
          bg=color3).pack(pady=17)
    Label(details_screen, text="", bg=color3).pack()
    Label(details_screen, text='Mail', font=('OpenSans', 13), bg=color3).pack()
    mail_entry = Entry(details_screen, textvariable=mail)
    mail_entry.pack()
    Label(details_screen, text="", bg=color3).pack()
    Label(details_screen, text='Username', font=('OpenSans', 13),
          bg=color3).pack()
    username_entry = Entry(details_screen, textvariable=username)
    username_entry.pack()
    Label(details_screen, text="", bg=color3).pack()
    Label(details_screen, text='Password', font=('OpenSans', 13),
          bg=color3).pack()
    password_entry = Entry(details_screen, show='*',
                           textvariable=password)
    password_entry.pack()
    Label(details_screen, text="", bg=color3).pack()

    # Buttons
    Button(details_screen, text='Update', font=('OpenSans', 12), bg=color4, borderwidth=1, width=9, height=1,
           command=lambda: [Handle_User.change_details(mail_entry.get(), username_entry.get(), password_entry.get()),
                            details_screen.destroy()]).pack()
    Button(details_screen, text='Back', bg=color4, borderwidth=0, width=4, height=1,
           command=lambda: details_screen.destroy()).place(x=4, y=1)

    details_screen.mainloop()
