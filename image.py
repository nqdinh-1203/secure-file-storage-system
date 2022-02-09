from functools import partial
import aes
from tkinter import *
from tkinter import filedialog


def encrypt_img(key: str, data):
    # if file is None:
    #     return

    # file_name = file.name

    # # Đọc data của img
    # with open(file_name, 'rb') as fin:
    #     img = fin.read()

    encrypted_img = aes.encrypt(data, key)

    return encrypted_img


def decrypt_img(key: str, data):
    # if file is None:
    #     return

    # file_name = file.name

    # # Đọc data của img
    # with open(file_name, 'rb') as fin:
    #     img = fin.read()

    decrypted_img = aes.decrypt(data, key)

    return decrypted_img
