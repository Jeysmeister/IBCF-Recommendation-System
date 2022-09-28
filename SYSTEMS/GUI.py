from tkinter import *

root = Tk()

def close_root():
    root.destroy()

LabelUsername = Label(text="Username : ")
LabelPassword = Label(text="Password : ")
TextUsername = Entry(root, width=15)
TextPassword = Entry(root, show="*", width=15)

LabelUsername.pack()
TextUsername.pack()
LabelPassword.pack()
TextPassword.pack()
root.attributes('-fullscreen', True)
Button(root, text="Close", command=close_root).pack(side=BOTTOM, anchor="e", padx=8, pady=8)

root.mainloop()
