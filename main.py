from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
import subprocess
import threading
import registration
import menu
import sign_in
from utils import center_window

root = Tk()

log_in_frame = Frame(root)


def onClosing():
    if messagebox.askokcancel("Thoát", "Bạn có muốn thoát?"):
        root.quit()
        root.destroy()


def clientStart():
    root.withdraw()
    check, user = sign_in.signInHandle()
    if check:
        menu.userGUI(user)
    # else:
    print('false')
    root.deiconify()


def registrationWindow():
    root.withdraw()
    registration.registrationHandle()
    root.deiconify()
    return


root.title('HỆ THỐNG LƯU TRỮ TẬP TIN AN TOÀN')
center_window(root, 800, 650)
root.resizable(FALSE, FALSE)

# Create widgets
# Add background
backgroundImage = ImageTk.PhotoImage(
    file="./assets/Client/background.png", master=root)
Client_text_label = Label(root, image=backgroundImage)
Client_text_label.place(x=0, y=0)

signinButtonImage = ImageTk.PhotoImage(
    file="./assets/Client/sign_in.png",
    master=root
)
signinButton = Button(
    root,
    image=signinButtonImage,
    padx=20,
    pady=20,
    highlightthickness=0, borderwidth=0,
    command=clientStart)
signinButton.place(x=510, y=470, width=200, height=50)

signUpButtonImage = ImageTk.PhotoImage(
    file="assets/Client/sign_up.png", master=root)
registerButton = Button(
    root,
    image=signUpButtonImage,
    padx=20,
    pady=20,
    highlightthickness=0, borderwidth=0,
    command=registrationWindow
)
registerButton.place(x=120, y=470, width=200, height=50)

root.protocol("WM_DELETE_WINDOW", onClosing)
root.mainloop()
