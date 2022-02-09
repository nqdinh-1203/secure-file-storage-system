from tkinter import *
from PIL import ImageTk
from DB import *
from tkinter import messagebox
from utils import *
import requests
import json
import rsa


def registrationHandle():
    # Check if form is valid
    def isValid():
        username = usernameText.get()
        password = passwordText.get()
        rePassword = rePasswordText.get()

        # Check if any field is empty
        if username == '' or password == '' or rePassword == '':
            messagebox.showerror(
                'Lỗi', 'Vui lòng điền đầy đủ thông tin!', parent=root)
            return False

        # Check if 2 password are equal
        if password != rePassword:
            messagebox.showerror('Lỗi', 'Mật khẩu không khớp!', parent=root)
            return False

        # Submit to server
        submitClient(username, password)

        # Success
        #messagebox.showinfo('Thành công', 'Đăng ký thành công!', parent=root)
        return True

    # Need to fix
    def submitClient(username, password):
        pub, priv = rsa.key_gen(7)

        r = requests.get(
            f'http://127.0.0.1:5000/register/{username}/{password}/{pub[0]}/{priv[0]}/{pub[1]}')

        result = r.content.decode('utf-8').rstrip('\n')
        result_json = json.loads(result)
        res = result_json['Result:']

        if res == "Thanh cong":
            # Pha xác thực
            while True:
                verify = requests.get(
                    f'http://127.0.0.1:5000/verify/{username}/{pub[0]}')

                result1 = verify.content.decode('utf-8').rstrip('\n')
                print(result1)

                result1_json = json.loads(result1)
                # print(result1_json)

                res1 = result1_json['Result']

                # Nếu xác thực đúng thì thoát while
                if res1 == 'Thanh cong':
                    messagebox.showinfo(
                        'Thành công', 'Xác thực thành công')
                    break
                else:
                    messagebox.showerror('Thất bại', 'Xác thực thất bại')

                # Nếu sai thì tạo lại khóa mới và update và tiếp tục vòng lặp
                pub, priv = rsa.key_gen(7)
                requests.get(
                    f'http://127.0.0.1:5000/update/{username}/{pub[0]}/{priv[0]}/{pub[1]}')

            # Khi thoát ra khỏi vòng lặp là đằng ký thành công
            messagebox.showinfo('Thành công', 'Đăng ký thành công!')
        else:
            messagebox.showerror('Lỗi', 'Đã tồn tại tài khoản!')

    def onClosing():
        if messagebox.askokcancel("Thoát", "Bạn có muốn thoát?"):
            root.quit()
            root.destroy()

    def onEnter(event=None):
        isValid()

    def back():
        root.quit()
        root.destroy()

    root = Toplevel()
    root.title('Đăng ký tài khoản')
    center_window(root, 450, 450)
    root.resizable(FALSE, FALSE)

    # Add background
    bg = ImageTk.PhotoImage(
        file="./assets/Client/sign_up/form.png", master=root)
    background = Label(root,  image=bg)
    background.place(x=0, y=0)

    # Add username field
    usernameText = Entry(root, width=23, font=("Calibri 12"), bg="#81BFD3")
    usernameText.place(x=210, y=232)
    usernameText.bind('<Return>', onEnter)

    # Add password field
    passwordText = Entry(root, width=23, show="*",
                         font=("Calibri 12"), bg="#81BFD3")
    passwordText.place(x=210, y=282)
    passwordText.bind('<Return>', onEnter)

    # Add confirm password field
    rePasswordText = Entry(root, width=23, show="*",
                           font=("Calibri 12"), bg="#81BFD3")
    rePasswordText.bind('<Return>', onEnter)

    rePasswordText.place(x=210, y=335)

    # Add sign-up button
    signUpButton_image = ImageTk.PhotoImage(
        file="assets/Client/sign_up/button.png", master=root)
    signUpButton = Button(
        root,
        image=signUpButton_image,
        borderwidth=0,
        highlightthickness=0,
        command=isValid
    )
    signUpButton.place(x=200, y=370)

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
    backButton.place(x=305, y=370)

    root.protocol("WM_DELETE_WINDOW", onClosing)
    root.mainloop()
