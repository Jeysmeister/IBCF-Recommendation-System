# import modules
import time
from tkinter import *
import os
from tkinter import ttk
from tkinter import messagebox, Menu
import csv

filepath = 'games.csv'
title = ""
username1 = ""

# Register User
def register_user():
    username_info = username.get()
    password_info = password.get()
    fr = open('users.txt', 'r')
    fa = open('users.txt', 'a')
    users = fr.readlines()
    user_lists = []

    def register_status(status, color):
        register_status_label.config(text=status, fg=color)

    for x in users:
        user = x.split("||")
        user_lists.append(user[0])

    if username_info in user_lists:
        register_status("Username already exists", "red")
    else:
        fa.write(username_info + "||")
        fa.write(password_info + "\n")
        fa.close()
        username_entry.delete(0, END)
        password_entry.delete(0, END)
        register_status("Registration Complete", "green")

    register_status_label = Label(register_screen, text="", fg="red", font=("calibri", 10))
    register_status_label.pack()

# Register
def register():
    global register_screen
    global username
    global password
    global username_entry
    global password_entry

    register_screen = Toplevel(main_screen)
    register_screen.title("RECOMMENDER SYSTEM")
    screen_width = register_screen.winfo_screenwidth()
    screen_height = register_screen.winfo_screenheight()
    window_width = 300
    window_height = 250
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    register_screen.geometry(f'{window_width}x{window_height}+{center_x + 200}+{center_y + 10}')
    register_screen.resizable(False, False)
    register_screen.iconbitmap('./rslogo.ico')

    username = StringVar()
    password = StringVar()

    Label(register_screen, text="REGISTRATION", bg="black", fg="white", width="300", height="2", font=("Calibri", 13)).pack()
    Label(register_screen, text="").pack()

    # username
    username_label = Label(register_screen, text="Username").pack(padx=40, side=TOP, anchor="w")
    username_entry = Entry(register_screen, textvariable=username, width=35)
    username_entry.pack()

    # password
    password_label = Label(register_screen, text="Password").pack(padx=40, side=TOP, anchor="w")
    password_entry = Entry(register_screen, textvariable=password, show='*', width=35)
    password_entry.pack()

    # showpass
    def show_pass():
        if password_entry.cget('show') == '*':
            password_entry.config(show='')
        else:
            password_entry.config(show='*')

    check_button = Checkbutton(register_screen, text="show password", command=show_pass)
    check_button.place(x=40, y=150)
    Label(register_screen, text="").pack()

    # register
    Label(register_screen, text="").pack()
    Button(register_screen, text="Register", width=30, height=1, bg="light gray", command=register_user).pack()

def login_verify():
    global username1
    username1 = username_verify.get()
    password1 = password_verify.get()
    username_login_entry.delete(0, END)
    password_login_entry.delete(0, END)

def main_account_screen():
    global main_screen
    global username_verify
    global password_verify
    global username_login_entry
    global password_login_entry

    # screen info
    main_screen = Tk()
    screen_width = main_screen.winfo_screenwidth()
    screen_height = main_screen.winfo_screenheight()
    window_width = 300
    window_height = 280
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    main_screen.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    main_screen.resizable(False, False)
    main_screen.iconbitmap('./rslogo.ico')
    main_screen.title("RECOMMENDER SYSTEM")

    username_verify = StringVar()
    password_verify = StringVar()

    # please enter details below
    Label(text="RECOMMENDER SYSTEM", bg="black", fg="white", width="300", height="2", font=("Calibri", 13)).pack()
    Label(text="").pack()

    # username
    Label(main_screen, text="Username").pack(padx=40, side=TOP, anchor="w")
    username_login_entry = Entry(main_screen, textvariable=username_verify, width=35)
    username_login_entry.pack()

    # password
    Label(main_screen, text="Password").pack(padx=40, side=TOP, anchor="w")
    password_login_entry = Entry(main_screen, textvariable=password_verify, show='*', width=35)
    password_login_entry.pack()
    Label(main_screen, text="").pack()

    def show_password():
        if password_login_entry.cget('show') == '*':
            password_login_entry.config(show='')
        else:
            password_login_entry.config(show='*')

    # showpassword
    check_button = Checkbutton(main_screen, text="show password", command=show_password)
    check_button.place(x=40, y=150)
    Label(main_screen, text="").pack()

    # login
    Button(main_screen, text="Login", bg="light gray", width=30, height=1, command=login_verify).pack()
    Label(text="").pack()

    # register
    Button(text="Not registered yet? Click here.", bg="white", height="1", width="25", command=register).pack()
    main_screen.bind('<Return>', lambda event: login_verify())
    main_screen.mainloop()

    main_screen.mainloop()

main_account_screen()