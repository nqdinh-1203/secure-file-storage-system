from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from PIL import ImageTk
from utils import center_window
import json
import requests
import sys
from urllib.parse import unquote


# Các list lưu thông tin img để xử lý trong code
id_img = []
img_name = []
size = []
date_up = []
id_user = []
# ==================================================================================

user = None

# Biến check đã xuất hiện bảng Info Img
isTreeAppear = False


# ==================================================================================
# Đọc các thông tin file ảnh đã lưu trong database và xuất ra màn hình (Search function)
def appearInfoImg(result):
    global isTreeAppear, myTree
    myTree = ttk.Treeview(root)
    countResult = 1
    myTree['columns'] = ("id", "name", "size", "date")
    myTree.column("#0", width=50, minwidth=30)
    myTree.column("id", width=80, minwidth=30)
    myTree.column("name", anchor=CENTER, width=150)
    myTree.column("size", anchor=CENTER, width=100)
    myTree.column("date", anchor=CENTER, width=130)
    #myTree.column("id_user", anchor=CENTER, width=50)

    # Create Headings
    myTree.heading("#0", text="Index", anchor=CENTER)
    myTree.heading("id", text="ID Image", anchor=CENTER)
    myTree.heading("name", text="Image", anchor=CENTER)
    myTree.heading("size", text="Size (KB)", anchor=CENTER)
    myTree.heading("date", text="Date Upload", anchor=CENTER)
    #myTree.heading("id_user", text="ID User", anchor=CENTER)

    isTreeAppear = True
    for i in result:
        myTree.insert(parent='', index='end', iid=None, text=str(countResult),
                      values=(i['id'], i['name'], i['size'], i['date']))
        id_img.append(i['id'])
        img_name.append(i['name'])
        size.append(i['size'])
        date_up.append(i['date'])
        # id_user.append(i['id_user'])
        countResult += 1

    myTree.place(x=42, y=170)


def updateInfoImg(myTree, result):
    myTree.place_forget()
    myTree.destroy()
    appearInfoImg(result)


def Search():
    print('search')

    try:
        global isTreeAppear, myTree
        # Phần dưới này để khi request đến server lấy db
        r = requests.get(f"http://127.0.0.1:5000/{user['name']}/search")

        result = r.content.decode('utf-8').rstrip('\n')

        result_json = json.loads(result)

        res = result_json['data:']

        # Tkinter Treeview
        if isTreeAppear == False:
            appearInfoImg(res)
        else:
            updateInfoImg(myTree, res)
    except:
        messagebox.showerror(
            'Lỗi', 'Server không tồn tại dữ liệu !')
# Lấy thông tin của user


def Information():
    # Đọc db để tìm thông tin user
    try:
        # Tạo 1 window mới để xuất thông tin user
        newWindow = Toplevel()
        print('info')
        newWindow.title("Information")
        newWindow.geometry("250x100")
        info = f"User ID: {user['id']}\n Username: {user['name']}\n RSA Public Key: {user['publickey']}"
        Label(newWindow, text=info).pack()
    except:
        messagebox.showerror(
            'Lỗi', 'Server không còn tồn tại để có thể gửi dữ liệu !')
# ==================================================================================


# ==================================================================================
# Thoát chương trình Client
def Exit():
    root.quit()
    root.destroy()
    sys.exit()
# ==================================================================================


# ==================================================================================
def Upload():
    print('upload')
    file = filedialog.askopenfile(
        mode='r', filetypes=(("JPEG files", "*.jpg*"),
                             ("PNG files", "*.png"),
                             ("All files", " *.*")))

    file_name = (file.name).replace('/', '\\')

    requests.get(
        f"http://127.0.0.1:5000/{user['id']}/{file_name}/{user['publickey']}/{user['n']}/upload")

    # Ma hoa hinh anh===================================
    # key = aes.random_key(32)
    # encrypted_img = image.encrypt_img(key, file)
    # ====================================================

# ============================================================================


# ============================================================================
def Download():
    print('download')
    window = Toplevel()
    window.title("Download Image")

    window.geometry('350x200')

    lbl = Label(window, text="Image name:")
    lbl.grid(column=0, row=0)

    txt1 = Entry(window, width=30)
    txt1.grid(column=1, row=0)

    def downloadimg():
        filename_list = (txt1.get()).split(',')

        for filename in filename_list:
            try:
                r = requests.get(
                    f'http://127.0.0.1:5000/{user["id"]}/{filename}/download')

                result = r.content.decode('utf-8').rstrip('\n')

                result_json = json.loads(result)

                res = result_json['Result']

                if res == 'Thanh cong':
                    messagebox.showinfo('Thành công', 'Tải thành công')
                else:
                    messagebox.showerror('Thất bại', 'Tải thất bại')
            except:
                messagebox.showerror('Thất bại', 'Tải thất bại')

    btn = Button(window, text="Download", command=downloadimg)
    btn.grid(column=0, row=2)

    txt = Label(
        window, text="Nhập nhiều tên cách nhau bằng dấu ','\nVí dụ: hinh1.png,hinh2.png,...")
    txt.place(x=60, y=70)

    window.mainloop()
# ============================================================================

# ============================================================================


def Share():
    print('share')

    window = Toplevel()
    window.title("share Image")

    window.geometry('350x200')

    lbl = Label(window, text="Image name:")
    lbc = Label(window, text="id_user:")

    lbl.grid(column=0, row=0)
    lbc.grid(column=0, row=1)

    txt1 = Entry(window, width=10)
    txt2 = Entry(window, width=10)

    txt1.grid(column=1, row=0)
    txt2.grid(column=1, row=1)

    def shareimg():

        try:
            res = txt1.get() + " " + txt2.get()
            li = res.split(' ')

            img_name_str = li[0]
            id_receivers = li[1]

            l = id_receivers.split(',')
            rcv_list = []

            for i in l:
                rcv_list.append(int(i))

            for id in rcv_list:
                r = requests.get(
                    f'http://127.0.0.1:5000/{user["id"]}/share/{img_name_str}/{id}')

                temp = r.content.decode('utf-8').rstrip('\n')

                temp_json = json.loads(temp)

                tmp = temp_json['Result']

                if tmp == 'Thanh cong':
                    messagebox.showinfo('Thành công', 'Chia sẻ thành công')
                else:
                    messagebox.showerror('Thất bại', 'Chia sẻ thất bại')
        except:
            messagebox.showerror('Thất bại', 'Chia sẻ thất bại')

    btn = Button(window, text="Share", command=shareimg)
    btn.grid(column=0, row=2)

    txt = Label(
        window, text="Nhập nhiều id cách nhau bằng dấu ','\nVí dụ: id1,id2,...")
    txt.place(x=60, y=90)

    window.mainloop()

# =======================================


def userGUI(user_info):
    global root
    global user
    user = user_info

    root = Toplevel()
    root.title("MENU")
    center_window(root, 800, 650)
    root.resizable(FALSE, FALSE)

    # Add background
    bg = ImageTk.PhotoImage(file="./assets/Client/user/menu.png", master=root)
    background = Label(root, image=bg)
    background.image = bg
    background.place(x=20, y=20)

    image = ImageTk.PhotoImage(file="assets/Client/user/user.png", master=root)
    buttonGetInfo = Button(
        root, image=image, highlightthickness=0, borderwidth=0, command=Information)
    buttonGetInfo.image = image
    buttonGetInfo.place(x=615, y=30)

    # Search Button
    searchButtonImage = ImageTk.PhotoImage(
        file="assets/Client/user/search.png", master=root)
    buttonSearch = Button(root, image=searchButtonImage, borderwidth=0,
                          highlightthickness=0, relief="flat", command=Search)
    buttonSearch.image = searchButtonImage
    buttonSearch.place(x=625, y=250)

    # Button Upload
    uploadButtonImage = ImageTk.PhotoImage(
        file="assets/Client/user/upload.png", master=root)
    buttonUpload = Button(root, borderwidth=0, image=uploadButtonImage,
                          highlightthickness=0, relief="flat", command=Upload)
    buttonUpload.image = uploadButtonImage
    buttonUpload.place(x=625, y=320)

    # Download Button
    downloadButtonImage = ImageTk.PhotoImage(
        file="assets/Client/user/download.png", master=root)
    downloadUpload = Button(root, borderwidth=0, image=downloadButtonImage,
                            highlightthickness=0, relief="flat", command=Download)
    downloadUpload.image = downloadButtonImage
    downloadUpload.place(x=625, y=390)

    # Share button
    shareButtonImage = ImageTk.PhotoImage(
        file="assets/Client/user/share.png", master=root)
    shareUpload = Button(root, borderwidth=0, image=shareButtonImage,
                         highlightthickness=0, relief="flat", command=Share)
    shareUpload.image = shareButtonImage
    shareUpload.place(x=625, y=460)

    # Exit button
    exitButtonImage = ImageTk.PhotoImage(
        file="assets/Client/user/exit.png", master=root)
    exitUpload = Button(root, borderwidth=0, image=exitButtonImage,
                        highlightthickness=0, relief="flat", command=Exit)
    exitUpload.image = exitButtonImage
    exitUpload.place(x=625, y=550)
