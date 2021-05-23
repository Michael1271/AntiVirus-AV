import json
import re
import time
from tkinter import *
from pymongo import MongoClient
import Graphic_Interface
import Web_Scrapper
from Cryptography import *
from Secret_Variables import Admin_Details, DataBaseAccess

# A Program that deals with Handling Users Registrations and logins
__author__ = 'Michael Khoshahang'


class User(object):
    """
    A class of a User object.
    """

    def __init__(self, name, mail, username, password, is_admin):
        """
        The function is a constructor of the User object.
        :param name: the user's name
        :param mail: the user's mail address'
        :param username: the user's username
        :param password: the user's password'
        :param is_admin: a boolean variable indicating if the user is admin or not
        :return: None
        """
        self._name = name
        self._username = username
        self._password = password
        self._mail = mail
        self._user_type = is_admin

    def get_name(self):
        """
        The function return the user's name.
        :return: the name of the user
        :rtype: str
        """
        return self._name

    def get_username(self):
        """
        The function return the user's username.
        :return: the username of the user
        :rtype: str
        """
        return self._username

    def get_mail(self):
        """
        The function return the user's mail address.
        :return: the mail of the user
        :rtype: str
        """
        return self._mail

    def get_password(self):
        """
        The function return the user's password.
        :return: the mail of the user
        :rtype: str
        """
        return self._password

    def get_user_type(self):
        """
        The function returns a boolean that represents if the user is admin or not.
        :return: a boolean that represents if the user is admin or not
        :rtype: bool
        """
        return self._user_type

    def set_username(self, new_username):
        """
        The function gets a new username and sets it as the current username
        :param new_username: the new username
        :return: None
        """
        self._username = new_username

    def set_mail(self, new_mail):
        """
        The function gets a new mail and sets it as the current mail
        :param new_mail: the new mail
        :return: None
        """
        self._mail = new_mail

    def set_password(self, new_password):
        """
        The function gets a new password and sets it as the current password
        :param new_password: the new password
        :return: None
        """
        self._password = new_password


# Global & Auxiliary variables
user_instance = None
mail = None
mail_validation = False
is_admin = False
color3 = "#%02x%02x%02x" % (244, 247, 250)
# Valid email syntax regex
regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'


def connect_to_db():
    """
    The function creates a connection to the DataBase.
    :return: the connection
    :rtype: Object
    """

    print('Connecting to MongoDB DataBase...')
    return MongoClient(DataBaseAccess)


database = connect_to_db().Users.UsersDataBase  # Connecting to the database


def register_user(name, username, mail, password):
    """
    the function registers a user by adding his username and password
    to the database. all details are being added to the database after md5 hashing.
    :return: None
    """
    from Graphic_Interface import screen
    global regex, mail_validation, database
    name = name.get().capitalize()
    mail = mail.get()
    username = username.get()
    password = password.get()

    try:  # validating the given email address with a valid regex
        if re.search(regex, mail):
            mail_validation = True
    except:
        pass

    if name == '' and mail == '' and username == '' and password == '':
        lbl = Label(screen,
                    text="Registration did not succeed- Name, Mail, Username and Password are required to Register",
                    bg=color3, fg="red", font=('Open Sans', 8))
        lbl.pack()
        screen.after(3500, lbl.destroy)

    elif name == '':
        lbl = Label(screen, text="Registration did not succeed- Name is required to Register", bg=color3, fg="red",
                    font=('Open Sans', 8))
        lbl.pack()
        screen.after(3500, lbl.destroy)

    elif mail == '':
        lbl = Label(screen, text="Registration did not succeed- Mail is required to Register", bg=color3, fg="red",
                    font=('Open Sans', 8))
        lbl.pack()
        screen.after(3500, lbl.destroy)

    elif username == '':
        lbl = Label(screen, text="Registration did not succeed- Username is required to Register", bg=color3, fg="red",
                    font=('Open Sans', 8))
        lbl.pack()
        screen.after(3500, lbl.destroy)

    elif password == '':
        lbl = Label(screen, text="Registration did not succeed- Password is required to Register", bg=color3, fg="red",
                    font=('Open Sans', 8))
        lbl.pack()
        screen.after(3500, lbl.destroy)

    elif not mail_validation:
        lbl = Label(screen, text="Registration did not succeed- Mail is not valid", bg=color3, fg="red",
                    font=('Open Sans', 8))
        lbl.pack()
        screen.after(3500, lbl.destroy)

    elif len(password) < 5:
        lbl1 = Label(screen, text="Registration did not succeed- \npassword has to be at least \n5 characters long",
                     bg=color3, fg="red", font=('Open Sans', 8))
        lbl1.pack()
        screen.after(3500, lbl1.destroy)

    else:  # passed all initial errors
        user_details = {'Name': encrypt(name),
                        'Mail': encrypt(mail),
                        'Username': encrypt_to_hash(username),
                        'Password': encrypt_to_hash(password)}  # creating user_details json object

        partial_user_details = {'Username': encrypt(username),
                                'Password': encrypt(password)}  # auxiliary variable

        name = user_details['Name']
        mail = user_details['Mail']
        username = user_details['Username']
        found_error = False
        for user in database.find({}):
            stored_name = user['Name']
            stored_mail = user['Mail']
            stored_username = user['Username']
            if name == stored_name:  # name is already taken
                lbl = Label(screen, text="Registration did not succeed- Name is already taken", bg=color3,
                            fg="red", font=('Open Sans', 8))
                lbl.pack()
                screen.after(3500, lbl.destroy)
                found_error = True
            elif mail == stored_mail:
                lbl = Label(screen, text="Registration did not succeed- Mail is already taken", bg=color3,
                            fg="red", font=('Open Sans', 8))
                lbl.pack()
                screen.after(3500, lbl.destroy)
                found_error = True

            elif username == stored_username:
                lbl = Label(screen, text="Registration did not succeed- username is already taken", bg=color3,
                            fg="red", font=('Open Sans', 8))
                lbl.pack()
                screen.after(3500, lbl.destroy)
                found_error = True
            break
        if not found_error:
            try:
                insert_user_to_database(user_details)
                Web_Scrapper.send_welcome_mail(mail, name, partial_user_details['Username'],
                                               partial_user_details['Password'])
                print('\nSending mail... \n')
            except Exception as e:
                print(
                    f'Could not send mail to {mail}. The error {e} occurred.')

            lbl = Label(screen, text="Registration Success",
                        bg=color3, fg="green", font=("Open Sans", 11))
            lbl.pack()
            screen.after(3500, lbl.destroy)


def login_user(username, password):
    """
    the function tries to log in the user by comparing the data that is
    in the database and the given data - username and password.
    :param username: the username of the user
    :param password: the password of the user
    :return: None
    """
    from Graphic_Interface import login_window
    global user_instance, mail, is_admin, database

    try:
        username = username.get()
        password = password.get()
    except:
        username = username
        password = password

    found_user = False
    if username != '' and password != '':
        for user in database.find({}):
            stored_username = user['Username']
            stored_password = user['Password']
            if (encrypt_to_hash(username) == stored_username and
                    encrypt_to_hash(
                        password) == stored_password):  # if matching username and password to the stored ones
                found_user = True
                name = decrypt(user['Name'])  # getting user's name
                mail = decrypt(user['Mail'])  # getting user's mail
                break
        if found_user:
            from Graphic_Interface import remember_me
            try:
                if remember_me.get() == 1:  # writing in a file whether to remember the user or not
                    with open('App_Files/Instant_Login.txt', 'r+') as file:
                        if not file.read():
                            file.write(json.dumps(
                                {encrypt(username): encrypt(password)}))
            except:
                pass
            if encrypt_to_hash(username) == Admin_Details[0] and encrypt_to_hash(password) == Admin_Details[
                    1]:  # checking if user is admin
                is_admin = True
            user_instance = User(name, mail, username, password, is_admin)
            login_window.destroy()
            Graphic_Interface.main_screen()  # displaying home screen

        else:  # user was not found in the database
            found_user = False
            # searching for username in the database
            for user in database.find({}):
                stored_username = user['Username']
                # searching for the username in the database
                if encrypt_to_hash(username) == stored_username:
                    found_user = True
            if not found_user:
                lbl = Label(login_window, text="Login Failed - Username is not in the database", bg=color3, fg="red",
                            font=('Open Sans', 8))
                lbl.pack()
                login_window.after(3500, lbl.destroy)

            found_user = False
            # searching for matching password for the username in the database
            for user in database.find({}):
                stored_username = user['Username']
                stored_password = user['Password']
                if encrypt_to_hash(username) == stored_username and encrypt_to_hash(password) == stored_password:
                    found_user = True
            if not found_user:
                lbl = Label(login_window, text="Login Failed - invalid password", bg=color3, fg="red",
                            font=('Open Sans', 8))
                lbl.pack()
                login_window.after(3500, lbl.destroy)
    else:
        if username == '' and password == '':
            lbl = Label(login_window, text="Login Failed - Name and Password input are required", bg=color3, fg="red",
                        font=('Open Sans', 8))
            lbl.pack()
            login_window.after(3500, lbl.destroy)

        elif username == '':
            lbl = Label(login_window, text="Login Failed - Username input is required", bg=color3, fg="red",
                        font=('Open Sans', 8))
            lbl.pack()
            login_window.after(3500, lbl.destroy)

        elif password == '':
            lbl = Label(login_window, text="Login Failed - Password input is required",
                        bg=color3, fg="red", font=('Open Sans', 8))
            lbl.pack()
            login_window.after(3500, lbl.destroy)


def is_exist(param):
    """
    the function gets a parameter and checks if it's exist in the database.
    :param param: the parameter to be checked in the database
    :return: True/False according to whether the parameter is in the database or not
    :rtype: boolean
    """
    global database
    for user in database.find({}):
        if user['Username'] == param or user['Password'] == param:
            return True
    return False


def insert_user_to_database(user_details):
    """
    The function gets a list of the user's details and inserts it to the database
    and returns True/False according to the success or failure of the action.
    :param user_details: dictionary of the user's details
    :return: True/False according to the success or failure of the action
    :rtype: boolean
    """
    global database
    try:
        # inserting user's details to the database
        database.insert_one(user_details)
        return True
    except:
        return False


def authenticate_user(password):
    """
    The function authenticates the user by comparing the given password to the stored password
    :param password: the given password to be compared to the stored password
    :return: True/False according to the authentication of the user
    """
    global user_instance

    return user_instance.get_password() == password


def change_details(mail, username, password):
    """
    The function gets a mail, username and password and assigns the new values to the existing details.
    :param mail: the new/existing mail
    :param username: the new/existing username
    :param password: the new/existing password
    :return: None
    """
    global user_instance, regex, mail_validation, database
    from Graphic_Interface import details_screen, remember_me

    user_details = {'Name': encrypt(user_instance.get_name()),
                    'Mail': encrypt(user_instance.get_mail()),
                    'Username': encrypt_to_hash(user_instance.get_username()),
                    'Password': encrypt_to_hash(user_instance.get_password())}

    database.delete_one(user_details)  # deleting user from database

    if mail != '':
        mail_validation = False
    try:  # validating the given email address with a valid regex
        if re.search(regex, mail):
            mail_validation = True
    except:
        pass
        found_mail = False
        for user in database.find({}):
            if user['Mail'] == mail:
                found_mail = True
        if found_mail:
            lbl = Label(details_screen, text="Registration did not succeed- Mail is already taken", bg=color3,
                        fg="red", font=('Open Sans', 8))
            lbl.pack()
            details_screen.after(3500, lbl.destroy)
        if mail_validation and not found_mail:  # every input is  valid
            user_instance.set_mail(mail)
            try:
                # inserting the user with the new details
                insert_user_to_database(user_details)
                Web_Scrapper.send_welcome_mail(encrypt(mail),
                                               encrypt(user_details['Name']),
                                               encrypt(username),
                                               encrypt(password))
                print('\nSending mail... \n')
            except Exception as e:
                print(
                    f'Could not send mail to {mail}. The error {e} occurred.')
    if username != '' and username != user_details['Username']:
        user_instance.set_username(username)
    if password != '' and password != user_details['Password']:
        user_instance.set_password(password)

    new_user_details = {'Name': encrypt(user_instance.get_name()),
                        'Mail': encrypt(user_instance.get_mail()),
                        'Username': encrypt_to_hash(user_instance.get_username()),
                        'Password': encrypt_to_hash(user_instance.get_password())}  # user's details dictionary
    try:
        if remember_me.get() == 1:
            file = open('App_Files/Instant_Login.txt', 'r+')
            if file.read():
                file.close()
                with open('App_Files/Instant_Login.txt', 'w') as file:
                    file.write(
                        json.dumps({encrypt(user_instance.get_username()): encrypt(user_instance.get_password())}))

        # inserting user's details tp the database
        database.insert_one(new_user_details)
        lbl = Label(details_screen, text="Updating details succeded",
                    bg=color3, fg="green", font=("Open Sans", 11))
        lbl.pack()
        details_screen.after(3500, lbl.destroy)
        time.sleep(4)
    except:
        lbl = Label(details_screen, text="Updating details did not succeded",
                    bg=color3, fg="red", font=("Open Sans", 11))
        lbl.pack()
        details_screen.after(3500, lbl.destroy)
        time.sleep(4)
