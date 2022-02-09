from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from utils import center_window
import json
import requests

# Biến user để lưu thông tin user
user = None


def verifyLogin():
    # Send message to server that we will verify Login
    # LOGIN_REQUEST => MESSAGE
    global user
    global success

    username = usernameEntry.get()
    password = passwordEntry.get()

    if username == '' or password == '':
        messagebox.showerror(
            'Lỗi', 'Vui lòng điền đầy đủ thông tin!', parent=root)
        return

    r = requests.post(f'http://127.0.0.1:5000/login/{username}/{password}')
    result = r.content.decode('utf-8').rstrip('\n')

    result_json = json.loads(result)

    res = result_json['Result:']
    print('call')
    if res == "Thanh cong":
        messagebox.showinfo('Thành công', 'Đăng nhập thành công!')
        success = True

        r1 = requests.get(f'http://127.0.0.1:5000/{username}')
        user_string = r1.content.decode('utf-8').rstrip('\n')

        user_json = json.loads(user_string)
        user = user_json['data']

        root.quit()
        root.destroy()
    else:
        messagebox.showerror('Lỗi', 'Không tồn tại tài khoản!')


def onEnter(event=None):
    verifyLogin()


def back():
    root.quit()
    root.destroy()


def loginForm():
    global usernameEntry_image_label, usernameEntry, passwordEntry_image_label, passwordEntry, loginButton
    global usernameEntry, passwordEntry, loginButton, backButton
    print('login form')
    # Load ảnh cho Entry username
    username = StringVar()
    usernameEntry = Entry(root, bd=0, bg="#81BFD3", font=("Calibri 12"),
                          highlightthickness=0, textvariable=username)
    usernameEntry.bind('<Return>', onEnter)
    usernameEntry.place(x=235, y=193,
                        width=170, height=25)

    password = StringVar()
    passwordEntry = Entry(root, bd=0, bg="#81BFD3", font=("Calibri 12"),
                          highlightthickness=0, textvariable=password, show='*')
    passwordEntry.bind('<Return>', onEnter)
    passwordEntry.place(x=235, y=260, width=170, height=25)

    # load ảnh cho Button đăng nhập
    loginButton_image = ImageTk.PhotoImage(
        file="assets/Client/sign_in/sign_in.png", master=root)
    loginButton = Button(root, image=loginButton_image, borderwidth=0, highlightthickness=0,
                         command=verifyLogin)
    loginButton.image = loginButton_image
    loginButton.place(x=270, y=300)

    # Add back button
    backButton_image = ImageTk.PhotoImage(
        file="assets/Client/sign_up/back.png", master=root)
    backButton = Button(
        root,
        image=backButton_image,
        borderwidth=0,
        highlightthickness=0,
        command=back
    )
    backButton.image = backButton_image
    backButton.place(x=270, y=360)

# MAIN starts here


def signInHandle():
    global root, success, user
    success = False
    root = Tk()
    center_window(root, 450, 450)
    root.resizable(False, False)
    root.title("Đăng nhập")

    # Add background
    bg = ImageTk.PhotoImage(
        file="./assets/Client/sign_in/form.png", master=root)
    background = Label(root,  image=bg)
    background.place(x=0, y=0)
    loginForm()
    root.mainloop()
    return success, user
