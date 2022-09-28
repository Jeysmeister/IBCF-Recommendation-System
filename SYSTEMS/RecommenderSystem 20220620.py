# import modules
from tkinter import *
import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, Menu
import csv
from Enhanced import *

filepath = "gamespc.csv"
selected_game = ""
current_user = ""
user_id = ""
list_of_all_ratings = []

def get_current_rated(user_id_current, user_current):
    gameId_list_of_current_user = []
    ratings_csv = open('ratinggames.csv')
    data_ratinggames = csv.reader(ratings_csv)
    for item in data_ratinggames:
        if item[0] == user_id_current:
            gameId_list_of_current_user.append(item[1])
        list_of_all_ratings.append(item)
    ratings_csv.close()

    gameTitle_list_of_current_user = []
    game_titles = []
    game_ids = []
    game_csv = open('gamespc.csv')
    data_games = csv.reader(game_csv)
    for item in data_games:
        game_ids.append(item[0])
        game_titles.append(item[1])
    for item in gameId_list_of_current_user:
        for item2 in game_ids:
            if item2 == item:
                title_index = game_ids.index(item2)
                gameTitle_list_of_current_user.append(game_titles[title_index])
    game_csv.close()

    mygames_users = []
    mygames_titles = []
    my_games_list = []
    to_be_appended = ""
    fr = open('mygames.txt', 'r')
    my_games_list = fr.readlines()
    fr.close()
    if my_games_list == []:
        to_be_appended = to_be_appended + current_user + "::"
        for item in gameTitle_list_of_current_user:
            if item == gameTitle_list_of_current_user[len(gameTitle_list_of_current_user) - 1]:
                to_be_appended = to_be_appended + item + "\n"
            else:
                to_be_appended = to_be_appended + item + "||"
        fw = open('mygames.txt', 'w')
        fw.write(to_be_appended)
        fw.close()
    else:
        for item in my_games_list:
            item_split = item.split("::")
            mygames_users.append(item_split[0])
            mygames_titles.append(item_split[1])
        if user_current in mygames_users:
            pass
        else:
            to_be_appended = to_be_appended + current_user + "::"
            for item in gameTitle_list_of_current_user:
                if item == gameTitle_list_of_current_user[len(gameTitle_list_of_current_user) - 1]:
                    to_be_appended = to_be_appended + item + "\n"
                else:
                    to_be_appended = to_be_appended + item + "||"
            fw = open('mygames.txt', 'a')
            fw.write(to_be_appended)
            fw.close()

# Register
def register():
    global register_screen
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

    global username
    global password
    global username_entry
    global password_entry
    username = StringVar()
    password = StringVar()

    Label(register_screen, text="REGISTRATION", bg="black", fg="white", width="300", height="2",
          font=("Calibri", 13)).pack()
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
    def showpass():
        if password_entry.cget('show') == '*':
            password_entry.config(show='')
        else:
            password_entry.config(show='*')

    check_button = Checkbutton(register_screen, text="show password", command=showpass)
    check_button.place(x=40, y=150)
    Label(register_screen, text="").pack()

    # register
    Label(register_screen, text="").pack()
    Button(register_screen, text="Register", width=30, height=1, bg="light gray", command=register_user).pack()

def register_user():
    username_info = username.get()
    password_info = password.get()
    user_exists = False
    users = []

    fr = open('users.txt', "r")
    user_list = fr.readlines()
    fr.close()
    for user_list_line in user_list:
        user_list_line_list = user_list_line.split("||")
        users.append(user_list_line_list[1])

    if username_info in users:
        Label(register_screen, text="User Already Exists", fg="red", font=("calibri", 10)).pack()
    else:
        fa = open('users.txt', "a")
        if users == []:
            fa.write(str(0) + "||" + username_info + "||" + password_info + "\n")
        else:
            fa.write(str(len(users) + 1) + "||" + username_info + "||" + password_info + "\n")
        fa.close()
        Label(register_screen, text="Registration Success", fg="green", font=("calibri", 10)).pack()

    username_entry.delete(0, END)
    password_entry.delete(0, END)

#Login verify
def login_verify():
    global username1
    global current_user
    global user_id
    username1 = username_verify.get()
    password1 = password_verify.get()
    username_login_entry.delete(0, END)
    password_login_entry.delete(0, END)

    if username1:
        if password1:
            f = open('users.txt', "r")
            user_list = f.readlines()
            users = []
            passwords = []
            ids = []
            for user_list_line in user_list:
                user_list_line_split = user_list_line.split("||")
                ids.append(user_list_line_split[0])
                users.append(user_list_line_split[1])
                passwords.append(user_list_line_split[2])
            if username1 in users:
                user_index = users.index(username1)
                password_of_user = passwords[user_index]
                user_id = ids[user_index]
                if password1 + "\n" == password_of_user:
                    current_user = username1
                    get_current_rated(user_id, current_user)
                    recommend()
                else:
                    password_not_recognised()
            else:
                user_not_found()
            f.close()
        else:
            inputpassword()
    else:
        inputusername()

def close():
        verification_screen.destroy()

def buy():
    user_list_bought = []
    bought_list = []
    new_boughtlist = []
    new_cartlist=[]
    user_list_cart= []
    cart_list=[]
    f = open('mygames.txt', "r")
    user = current_user
    gametitle = value + "\n"
    gametitle2 = value
    user_list = f.readlines()
    f.close()
    no_titles_yet = False
    for username in user_list:
        username = username.split("::")
        user_list_bought.append(username[0])
        bought_list.append(username[1])
        if username[1] == "":
            no_titles_yet = True
    if user in user_list_bought:
        index_user = user_list_bought.index(user)
        bought_list[index_user] = bought_list[index_user][:-1]
        if no_titles_yet == False:
            bought_list[index_user] = '||'.join([bought_list[index_user],gametitle])
        else:
            bought_list[index_user] = gametitle
        for i in range(0,len(user_list_bought)):
            all_list = '::'.join([user_list_bought[i],bought_list[i]])
            new_boughtlist.append(all_list)
        f = open('mygames.txt', "w")
        for i in range(0,len(new_boughtlist)):
            f.write(new_boughtlist[i])
        f.close()
        #remove the item in the cart
        f=open('cart.txt',"r")
        user_list = f.readlines()
        for username in user_list:
            username = username.split("::")
            user_list_cart.append(username[0])
            cart_list.append(username[1])
        if user in user_list_cart:
            index_user = user_list_cart.index(user)
            my_cart = cart_list[index_user].split("||")
            #print(my_cart)
            my_cart[len(my_cart)-1]= my_cart[len(my_cart)-1][:-1]
            #print(my_cart)
            if gametitle2 in my_cart:
                game_title2_index = my_cart.index(gametitle2)
                my_cart.pop(game_title2_index)
                #print(my_cart)
                all_list = my_cart[0]
                my_cart[-1] = my_cart[-1] + "\n" #new dagdag
                #print(my_cart[-1])
                for x in range(1, len(my_cart)):
                    all_list = '||'.join([all_list,my_cart[x]])
                cart_list[index_user] = all_list
                for i in range(0, len(user_list_cart)):
                    new_cart_list = '::'.join([user_list_cart[i],cart_list[i]])
                    new_cartlist.append(new_cart_list)
                #print(new_cartlist)
                f = open('cart.txt', "w")
                for i in range(0, len(new_cartlist)):
                    f.write(new_cartlist[i])
                f.close()
    else:
        f = open('mygames.txt', "a")
        f.write(user+"::"+gametitle)
        f.close()
    success()

def thanks_msg():

    global verification_screen
    verification_screen = Toplevel(recommend_screen)
    verification_screen.title("Verification")
    # Screen Options
    verification_screen.iconbitmap('./rslogo.ico')
    screen_width = verification_screen.winfo_screenwidth()
    screen_height = verification_screen.winfo_screenheight()
    window_width = 300
    window_height = 190
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    verification_screen.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    # verification_screen.resizable(True, True)
    verification_screen.resizable(False, False)

    verify_label = Label(verification_screen, text="BUY A GAME", bg="black", fg="white", width="42", height="2", font=("Calibri", 10))
    verify_label.grid(row=0, column=0)

    verify_label = Label(verification_screen, text="You are buying: \n " + value,  width="42", height="8", font=("Calibri", 10))
    verify_label.grid(row=2, column=0)

    #cancel button
    cancelbutton = Button(verification_screen, text="CANCEL", bg="light gray", fg="black", width=20, height=1, command =close)
    cancelbutton.grid(row=3, column=0, sticky="w")

    #buy button
    buybutton = Button(verification_screen, text="BUY", bg="gray", fg="white", width=20, height=1, command = buy)
    buybutton.grid(row=3, column=0, sticky="e")

def success():
    messagebox.showinfo("Success", "You've successfully bought this game!")

def addcart():
    user_list_cart=[]
    cart_list = []
    new_cartlist=[]
    f = open('cart.txt', "r")
    user = current_user
    gametitle = value+"\n"
    user_list = f.readlines()
    f.close()
    for username in user_list:
        username = username.split("::")
        user_list_cart.append(username[0])
        cart_list.append(username[1])
    if user in user_list_cart:
        index_user = user_list_cart.index(user)
        cart_list[index_user]= cart_list[index_user][:-1]
        cart_list[index_user]= '||'.join([cart_list[index_user],gametitle])
        for i in range(0,len(user_list_cart)):
            all_list = '::'.join([user_list_cart[i],cart_list[i]])
            new_cartlist.append(all_list)
        f = open('cart.txt', "w")
        for i in range(0,len(new_cartlist)):
            f.write(new_cartlist[i])
        f.close()
    else:
        f = open('cart.txt', "a")
        f.write(user+"::"+gametitle)
        f.close()
    addtocart()

def addtocart():
    messagebox.showinfo("Success", "Added to cart.")

def inputusername():
    messagebox.showerror("Error", "Input username")

def inputpassword():
    messagebox.showerror("Error", "Input password")

#invalid password
def password_not_recognised():
    messagebox.askretrycancel("Incorrect password!", "Try again?")

#user not found
def user_not_found():
    messagebox.showerror("Error", "No matches found!")

#Login success
def login_sucess():
    messagebox.showinfo("Login", "Success")
   # recommend()


#all games
def all_games():
    global allgames
    allgames_screen = Toplevel(recommend_screen)
    allgames_screen.title("ALL GAMES")
    # Screen Options
    allgames_screen.iconbitmap('./rslogo.ico')
    screen_width = allgames_screen.winfo_screenwidth()
    screen_height = allgames_screen.winfo_screenheight()
    window_width = 510
    window_height = 460
    center_x = int(screen_width / 2 - window_width / 2) +50
    center_y = int(screen_height / 2 - window_height / 2) +30
    allgames_screen.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    #allgames_screen.resizable(True, True)
    allgames_screen.resizable(False, False)

    File = open(filepath)
    Reader = csv.reader(File)
    global Data
    Data = list(Reader)
    del (Data[0])


    list_of_entries = []
    for x in list(range(0, len(Data))):
        list_of_entries.append(Data[x][1])
    #print(list_of_entries)
    var = StringVar(value=list_of_entries)

    allgames_label = Label(allgames_screen, text="ALL GAMES", bg="#000066",
                                     fg="white", width="72",height="1",font=("Calibri", 10))
    allgames_label.grid(row=0, column=0)

    #all games listbox
    allgames_list = Listbox(allgames_screen, listvariable=var, width=83, height=17)
    allgames_list.grid(row=2, column=0)

    # search  games
    allgames_entry = Entry(allgames_screen, font=("Calibri", 10), width=30)
    allgames_entry.insert(0, "Search game ...")
    allgames_entry.grid(row=1, column=0, sticky="e")

    def callback(event):
        global value
        selection = event.widget.curselection()
        index = selection[0]
        value = event.widget.get(index)
        for i in list(range(0,len(Data))):
            if value == Data[i][1]:
                title2.config(text=Data[i][1])
                genre2.config(text=Data[i][2])
                price2.config(text=Data[i][3])
                releaseddate2.config(text=Data[i][4])
    allgames_list.bind('<<ListboxSelect>>', callback)

    def update(data):
        # clear the listbox
        allgames_list.delete(0, END)

    # Add games to listbox
        for item in data:
            allgames_list.insert(END, item)

    '''
    # update entry box with listbox clicked
    def fillout(e):
        recommended_entry.delete(0, END)
        recommended_entry.insert(0, recommended_list.get(ACTIVE))
    '''

    #check
    def check(e):
        typed = allgames_entry.get()

        if typed == '':
            data = list_of_entries
        else:
            data = []
            for item in list_of_entries:
                if typed.lower() in item.lower():
                    data.append(item)
        update(data)

    update(list_of_entries)

    #create binding
    #recommended_list.bind("<<ListboxSelect>>", fillout)

    #create binding on entry box
    allgames_entry.bind("<KeyRelease>", check)

    #Game details
    details_label = Label(allgames_screen, text="GAME DETAILS", bg="#000066", fg="white", width="72",height="1", font=("Calibri", 10))
    details_label.grid(row=3, column=0)

    # labels
    title = Label(allgames_screen, text=" TITLE: ").grid(row=4, column=0, sticky="w")
    releaseddate = Label(allgames_screen, text=" RELEASED DATE: ").grid(row=5, column=0, sticky="w")
    genre = Label(allgames_screen, text=" GENRE: ").grid(row=6, column=0, sticky="w")
    price = Label(allgames_screen, text=" PRICE: ").grid(row=7, column=0, sticky="w")

    # displays all games
    title2 = Label(allgames_screen, text=" ")
    title2.grid(row=4, column=0, sticky="e")
    releaseddate2 = Label(allgames_screen, text=" ")
    releaseddate2.grid(row=5, column=0, sticky="e")
    genre2 = Label(allgames_screen, text=" ")
    genre2.grid(row=6, column=0, sticky="e")
    price2 = Label(allgames_screen, text=" ")
    price2.grid(row=7, column=0, sticky="e")

    #addtocart button
    addcartbutton = Button(allgames_screen, text="ADD TO CART", bg="light gray", fg="black", width=35, height=2, command=addcart)
    addcartbutton.grid(row=9, column=0, sticky="w")

    #buy button
    buybutton = Button(allgames_screen, text="BUY", bg="gray", fg="white", width=35, height=2, command=thanks_msg)
    buybutton.grid(row=9, column=0, sticky="e")

def top_games(list_of_recommended, user_is_existing):
    File = open(filepath)
    Reader = csv.reader(File)
    global Data
    Data = list(Reader)
    del (Data[0])
    title_list = []
    list_of_entries = []

    if user_is_existing:
        for item in list_of_recommended:
            temp_item = item.split(' -- ')
            title_list.append(str(temp_item[0]))
        var = StringVar(value=title_list)
    else:
        for x in list(range(0, len(Data))):
            list_of_entries.append(str(Data[x][1]))
        var = StringVar(value=list_of_entries)

    recommended_label = Label(recommend_screen, text="RECOMMENDED GAMES FOR YOU", bg="#003300",
                              fg="white", width="72", height="1", font=("Calibri", 10))
    recommended_label.grid(row=0, column=0)

    # all games listbox
    recommended_list = Listbox(recommend_screen, listvariable=var, width=83, height=17)
    recommended_list.grid(row=2, column=0)

    # search  games
    recommended_entry = Entry(recommend_screen, font=("Calibri", 10), width=30)
    recommended_entry.insert(0, "Search game ...")
    recommended_entry.grid(row=1, column=0, sticky="e")

    def callback(event):
        global value
        global selected_game
        selection = event.widget.curselection()
        index = selection[0]
        value = event.widget.get(index)
        selected_game = value
        for i in list(range(0, len(Data))):
            if value == Data[i][1]:
                title2.config(text=Data[i][1])
                genre2.config(text=Data[i][2])
                price2.config(text=Data[i][3])
                releaseddate2.config(text=Data[i][4])
                #price2.config(text=Data[i][4])

    recommended_list.bind('<<ListboxSelect>>', callback)
    def update(data):
        # clear the listbox
        recommended_list.delete(0, END)

        # Add games to listbox

        for item in data:
            recommended_list.insert(END, item)

    '''
    # update entry box with listbox clicked
    def fillout(e):
        recommended_entry.delete(0, END)
        recommended_entry.insert(0, recommended_list.get(ACTIVE))
    '''

    # check
    def check(e):
        typed = recommended_entry.get()

        if typed == '':
            data = list_of_entries
        else:
            data = []
            for item in list_of_entries:
                if typed.lower() in item.lower():
                    data.append(item)
        update(data)

    if user_is_existing:
        update(title_list)
    else:
        update(list_of_entries)

    # create binding
    # recommended_list.bind("<<ListboxSelect>>", fillout)

    # create binding on entry box
    recommended_entry.bind("<KeyRelease>", check)

    # Game details
    details_label = Label(recommend_screen, text="GAME DETAILS", bg="#003300", fg="white", width="72", height="1",
                          font=("Calibri", 10))
    details_label.grid(row=3, column=0)

    # labels
    title = Label(recommend_screen, text=" TITLE: ").grid(row=4, column=0, sticky="w")
    releaseddate = Label(recommend_screen, text=" RELEASED DATE: ").grid(row=5, column=0, sticky="w")
    genre = Label(recommend_screen, text=" GENRE: ").grid(row=6, column=0, sticky="w")
    price = Label(recommend_screen, text=" PRICE: ").grid(row=7, column=0, sticky="w")

    # displays all games
    title2 = Label(recommend_screen, text=" ")
    title2.grid(row=4, column=0, sticky="e")
    releaseddate2 = Label(recommend_screen, text=" ")
    releaseddate2.grid(row=5, column=0, sticky="e")
    genre2 = Label(recommend_screen, text=" ")
    genre2.grid(row=6, column=0, sticky="e")
    price2 = Label(recommend_screen, text=" ")
    price2.grid(row=7, column=0, sticky="e")

    # addtocart button
    #addcartbutton = Button(recommend_screen, text="ADD TO CART", bg="light gray", fg="black", width=35, height=2,
                           #command=addcart)
    addcartbutton = Button(recommend_screen, text="ADD TO CART", bg="light gray", fg="black", width=35, height=2,command = game_in_cart_checker)
    addcartbutton.grid(row=8, column=0, sticky="w")

    # buy button
    buybutton = Button(recommend_screen, text="BUY", bg="gray", fg="white", width=35, height=2, command=thanks_msg)
    buybutton.grid(row=8, column=0, sticky="e")


def game_in_cart_checker():
    fr = open('cart.txt', 'r')
    cart_items = fr.readlines()
    fr.close()
    cart_items_list = []
    for items in cart_items:
        cart_items_list.append(items)

    users = []
    games = []
    for items in cart_items_list:
        items_split = items.split('::')
        users.append(items_split[0])
        games.append(items_split[1])

    if current_user in users:
        user_index = users.index(current_user)

    user_cart_list = games[user_index]
    user_cart_list_split = user_cart_list.split('||')
    user_cart_list_split[len(user_cart_list_split) - 1] = user_cart_list_split[len(user_cart_list_split) - 1][:-1]
    if selected_game in user_cart_list_split:
        game_in_cart_exists()
    else:
        #print("WENT HERE")
        addcart()


def game_in_cart_exists():
    messagebox.showinfo("GAME ALREADY IN CART", "SELECTED GAME IS ALREADY IN YOUR CART")

#my cart window
def add_cart():
    global addtocart_screen
    addtocart_screen = Toplevel(recommend_screen)
    addtocart_screen.title("MY CART")
    # Screen Options
    addtocart_screen.iconbitmap('./rslogo.ico')
    screen_width = addtocart_screen.winfo_screenwidth()
    screen_height = addtocart_screen.winfo_screenheight()
    window_width = 380
    window_height = 365
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    addtocart_screen.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    # recommend_screen.resizable(True, True)
    addtocart_screen.resizable(False, False)
    '''
    list_of_entries = []
    for x in list(range(0, len(Data))):
        list_of_entries.append(Data[x][1])
    # print(list_of_entries)
    var = StringVar(value=list_of_entries)

    '''
    user_list_cart = []
    cart_list = []
    new_cartlist = []
    mycartlist = []

    f = open('cart.txt', "r")
    user = current_user
    user_list = f.readlines()
    f.close()
    for username in user_list:
        username = username.split("::")
        #print(username)
        user_list_cart.append(username[0])
        cart_list.append(username[1])
    if user in user_list_cart:
        index_user = user_list_cart.index(user)
        cart_split_list = cart_list[index_user].split("||")
        cart_split_list[len(cart_split_list) - 1] = cart_split_list[len(cart_split_list) - 1][:-1]
        var = StringVar(value=cart_split_list)

    def callback_addtocart(event):
        selection = event.widget.curselection()
        index = selection[0]
        global value
        value = event.widget.get(index)

    # displays items in cart
    addtocart_list = Listbox(addtocart_screen, listvariable=var, width=63, height=20)
    addtocart_list.grid(row=0, column=0)

    addtocart_screen.bind('<<ListboxSelect>>', callback_addtocart)

    # buy button
    buybutton = Button(addtocart_screen, text="BUY", bg="gray", fg="white", width=53, height=2, command=thanks_msg)
    buybutton.grid(row=1, column=0)

def rategame():
    global rategame_screen
    rategame_screen = Toplevel(recommend_screen)
    rategame_screen.title("RATING")
    #Screen Options
    rategame_screen.iconbitmap('./rslogo.ico')
    screen_width = rategame_screen.winfo_screenwidth()
    screen_height = rategame_screen.winfo_screenheight()
    window_width = 241
    window_height = 150
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    rategame_screen.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    # recommend_screen.resizable(True, True)

    # slider current value
    current_value = tk.IntVar()

    def get_current_value():
        return '{: }'.format(current_value.get())

    def slider_changed(event):
        value_label.configure(text=get_current_value())

    def exportdata():
        user = current_user
        title = value
        user_list_id = []
        user_list_name = []

        for i in list(range(0, len(Data))):
            if value == Data[i][1]:
                gameId = Data[i][0]
        #print(user, title, gameId)

        f = open('users.txt', "r")
        userlist = f.readlines()
        f.close()
        for username in userlist:
            username = username.split("||")
            user_list_id.append(username[0])
            user_list_name.append(username[1])
        #print(user_list_name)
        #print(user_list_id)
        if user in user_list_name:
            index_user = user_list_name.index(user)
            print(index_user)

        #print(userid, gameId, title, get_current_value())

    rating_label = Label(rategame_screen, text=" 5 - highest; 1 - lowest", bg="black", fg="white", width="34", height="2",
                          font=("Calibri", 10))
    rating_label.grid(row=1, column=0)

    space = Label(rategame_screen, text="")
    space.grid(row=2, column=0)

    # slider
    slider = ttk.Scale(rategame_screen, from_=1, to=5, orient='horizontal',command=slider_changed,variable=current_value)
    slider.grid(row=4, column=0)

    #value label
    value_label = ttk.Label(rategame_screen,text=get_current_value())
    value_label.grid(row=5, column=0)

    space = Label(rategame_screen, text="")
    space.grid(row=6, column=0)

    #rate button
    ratebutton = Button(rategame_screen, text="RATE THIS GAME", bg="gray", fg="white", width=34, height=1, command= exportdata)
    ratebutton.grid(row=7, column=0)

#my games window
def my_games():
    global mygames_screen
    mygames_screen = Toplevel(recommend_screen)
    mygames_screen.title("MY GAMES")
    #Screen Options
    mygames_screen.iconbitmap('./rslogo.ico')
    screen_width = mygames_screen.winfo_screenwidth()
    screen_height = mygames_screen.winfo_screenheight()
    window_width = 428
    window_height = 470
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    mygames_screen.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    # recommend_screen.resizable(True, True)
    mygames_screen.resizable(False, False)

    user_bought_cart = []
    bought_list = []
    new_boughtlist = []
    myboughtlist = []

    f = open('mygames.txt', "r")
    user = current_user
    user_list = f.readlines()
    f.close()
    for username in user_list:
        username = username.split("::")
        print(username)
        user_bought_cart.append(username[0])
        bought_list.append(username[1])
    if user in user_bought_cart:
        index_user = user_bought_cart.index(user)
        bought_split_list = bought_list[index_user].split("||")
        bought_split_list[len(bought_split_list) - 1] = bought_split_list[len(bought_split_list) - 1][:-1]
        var = StringVar(value=bought_split_list)

    def callback_mygames(event):
        selection = event.widget.curselection()
        index = selection[0]
        global value
        value = event.widget.get(index)
        for i in list(range(0, len(Data))):
            if value == Data[i][1]:
                title2.config(text=Data[i][1])
                genre2.config(text=Data[i][2])
                price2.config(text=Data[i][3])
                releaseddate2.config(text=Data[i][4])

    #displays own games
    mygames_screen_list = Listbox(mygames_screen,listvariable=var, width=70, height=20)
    mygames_screen_list.grid(row=0, column=0)

    mygames_screen.bind('<<ListboxSelect>>', callback_mygames)

    # Game details
    details_label = Label(mygames_screen, text="GAME DETAILS", bg="black", fg="white", width="60", height="1",
                          font=("Calibri", 10))
    details_label.grid(row=1, column=0)

    # labels
    title = Label(mygames_screen, text=" TITLE: ").grid(row=2, column=0, sticky="w")
    releaseddate = Label(mygames_screen, text=" RELEASED DATE: ").grid(row=3, column=0, sticky="w")
    genre = Label(mygames_screen, text=" GENRE: ").grid(row=4, column=0, sticky="w")
    price = Label(mygames_screen, text=" PRICE: ").grid(row=5, column=0, sticky="w")

    # values
    title2 = Label(mygames_screen, text=" ")
    title2.grid(row=2, column=0, sticky="e")
    releaseddate2 = Label(mygames_screen, text=" ")
    releaseddate2.grid(row=3, column=0, sticky="e")
    genre2 = Label(mygames_screen, text=" ")
    genre2.grid(row=4, column=0, sticky="e")
    price2 = Label(mygames_screen, text=" ")
    price2.grid(row=5, column=0, sticky="e")

    # rate button
    ratebutton = Button(mygames_screen, text="RATE THIS GAME", bg="gray", fg="white", width=60, height=2,
                        command=rategame)
    ratebutton.grid(row=7, column=0)

#recommend window
def recommend():
    global recommend_screen
    list_of_users = get_user_list()
    final_new_menu = []
    if int(user_id) in list_of_users:
        user_is_existing = True
        final_new_menu = movie_recommender(int(user_id), 0, 15, 3)
        #print("THIS IS FROM THE SYSTEM")
        #print(final_new_menu)
    else:
        user_is_existing = False
        pass
    #main_screen.destroy()
    #recommend_screen = Tk()
    recommend_screen = Toplevel(main_screen)
    recommend_screen.title("RECOMMENDED GAMES")

    #Screen Options
    recommend_screen.iconbitmap('./rslogo.ico')
    screen_width = recommend_screen.winfo_screenwidth()
    screen_height = recommend_screen.winfo_screenheight()
    window_width = 510
    window_height = 480
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    recommend_screen.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    # recommend_screen.resizable(True, True)
    recommend_screen.resizable(False, False)

    #menubar
    menubar = Menu(recommend_screen)
    recommend_screen.config(menu=menubar)

    #library menu
    library_menu = Menu(menubar, tearoff=False, bg='light gray', fg='black')
    library_menu.add_command(label='All Games', command=all_games)
    #library_menu.add_command(label='Top Recommended Games', command= top_games)
    menubar.add_cascade(label="Library", menu=library_menu)

    #account menu
    account_menu = Menu(menubar, tearoff=False, bg='light gray', fg='black')
    #account_menu.add_command(label='My Games', command=my_games)
    account_menu.add_command(label='My Games', command=existing_games_checker)
    account_menu.add_command(label='My Cart', command=add_cart)
    #account_menu.add_command(label='Logout', command=recommend_screen.destroy)
    account_menu.add_command(label='Logout', command=logout)
    menubar.add_cascade(label="Account", menu=account_menu)

    top_games(final_new_menu, user_is_existing)

#No Existing Games
def no_existing_games():
    messagebox.showinfo("YOU HAVE NO GAMES", "PLEASE BUY A GAME FIRST TO SEE YOUR LIST")

def existing_games_checker():

    fr = open('mygames.txt', 'r')
    my_games_data = fr.read()
    fr.close()
    games_exist = False
    if my_games_data == "":
        no_existing_games()
    else:
        games_exist = True

    if games_exist:
        user_games_list = []
        fr = open('mygames.txt', 'r')
        my_games_list = fr.readlines()
        fr.close()
        for user_games in my_games_list:
            user_games_list.append(user_games)

        user_list = []
        games_list = []
        for user_games in user_games_list:
            user_games_split = user_games.split('::')
            user_list.append(user_games_split[0])
            games_list.append(user_games_split[1])
        if current_user in user_list:
            my_games()
        else:
            no_existing_games()
    else:
        no_existing_games()

def logout():
    recommend_screen.destroy()
    main_screen.deiconify()

#main window
def main_account_screen():
    global main_screen

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

    global username_verify
    global password_verify

    username_verify = StringVar()
    password_verify = StringVar()

    global username_login_entry
    global password_login_entry

    #please enter details below
    Label(text="RECOMMENDER SYSTEM", bg="black", fg="white", width="300", height="2", font=("Calibri", 13)).pack()
    Label(text="").pack()

    #username
    Label(main_screen, text="Username").pack(padx=40, side=TOP, anchor="w")
    username_login_entry = Entry(main_screen, textvariable=username_verify, width=35)
    username_login_entry.pack()

    #password
    Label(main_screen, text="Password").pack(padx=40, side=TOP, anchor="w")
    password_login_entry = Entry(main_screen, textvariable=password_verify, show='*', width=35)
    password_login_entry.pack()
    Label(main_screen, text="").pack()

    def show_password():
        if password_login_entry.cget('show') == '*':
            password_login_entry.config(show='')
        else:
            password_login_entry.config(show='*')

    #showpassword
    check_button = Checkbutton(main_screen, text="show password", command=show_password)
    check_button.place(x=40, y=150)
    Label(main_screen, text="").pack()

    #login
    Button(main_screen, text="Login", bg="light gray", width=30, height=1, command=login_verify).pack()
    main_screen.bind('<Return>', lambda event: login_verify())
    Label(text="").pack()

    #register
    Button(text="Not registered yet? Click here.", bg="white", height="1", width="25", command=register).pack()

    main_screen.mainloop()


main_account_screen()