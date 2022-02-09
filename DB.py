import sqlite3
from datetime import datetime
import sys
import os
import aes
import image
import rsa


def Get_listusername():
    conn = sqlite3.connect("data/database.db")
    sql = '''
    SELECT user_name, password, id, public_key 
    FROM User
    '''
    data = conn.execute(sql).fetchall()
    conn.close()
    return data


def get_rsakey(id):
    conn = sqlite3.connect("data/database.db")
    sql = '''
    SELECT public_key, private_key, n_key
    FROM User
    Where id = ?
    '''
    data = conn.execute(sql, (id, )).fetchone()
    conn.close()

    return (data[0], data[2]), (data[1], data[2])


def InfUser(username):
    conn = sqlite3.connect("data/database.db")
    sql = '''
    SELECT *
    FROM User
    where user_name = ?
    '''
    data = conn.execute(sql, (username, )).fetchone()
    conn.close()
    return data


def Register(username, password, e, d, n):
    conn = sqlite3.connect("data/database.db")
    user_list = Get_listusername()

    for user in user_list:
        if user[0] == username:
            conn.close()
            return False

    for user in user_list:
        if user[3] == e:
            return False

    sql = '''
        INSERT INTO User(user_name, password, public_key, private_key, n_key) 
        VALUES (?, ?, ?, ?, ?)
        '''
    conn.execute(sql, (username, password, e, d, n))
    conn.commit()
    conn.close()
    return True


def verify_user(username, e):
    user = InfUser(username)
    publickey = user[3]

    return e == int(publickey)


def update_user(username, e, d, n):
    conn = sqlite3.connect("data/database.db")
    sql = '''
        UPDATE User
        SET public_key = ?, private_key = ?, n_key = ? 
        WHERE user_name = ?
    '''
    conn.execute(sql, (e, d, n, username)).fetchone()
    conn.close()
    return


def getImgofUser(username):
    conn = sqlite3.connect("data/database.db")
    sql = '''
        SELECT I.id, I.name, I.size, I.date
        FROM User U, Image I
        WHERE U.id = I.id_user and U.user_name = ?
    '''
    data = conn.execute(sql, (username, )).fetchall()
    conn.close()
    return data


# def UploadImg(username, name_img, img):
#     li = Get_listusername()

#     for i in li:
#         if i[0] == username:
#             id = i[2]
#             break

#     conn = sqlite3.connect("data/database.db")
#     cursor = conn.cursor()
#     size = sys.getsizeof(img)
#     date = datetime.date(datetime.now())
#     sql = '''
#     INSERT INTO Image(name, img, size, date, id_user)
#     VALUES (?, ?, ?, ?, ?)
#     '''
#     cursor.execute(sql, (name_img, img, size, date, id))

#     conn.commit()
#     cursor.close()
#     conn.close()


# ==========================>> UPLOAD IMAGE <<===============================
def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData


def UploadImg(file_name, id_user, e, n):
    sqliteConnection = sqlite3.connect("data/database.db")
    cursor = sqliteConnection.cursor()
    sqlite_insert_blob_query = """ INSERT INTO Image
                                  (name, data, size, date, id_user, hash_key) 
                                  VALUES (?, ?, ?, ?, ?, ?)
                                """

    size = os.path.getsize(file_name)
    data = convertToBinaryData(file_name)
    date = datetime.date(datetime.now())

    # Mã hóa hình ảnh bằng aes
    key = aes.random_key(32)
    encrypted_data = image.encrypt_img(key, data)

    # Mã hóa key bằng RSA
    print(e)
    print(n)
    hash_key = aes.encrypt_key(key, (e, n))

    li = file_name.split('\\')
    file_name = li[len(li) - 1]

    name = file_name

    # Convert data into tuple format
    data_tuple = (name, encrypted_data, size, date, id_user, hash_key)
    cursor.execute(sqlite_insert_blob_query, data_tuple)
    sqliteConnection.commit()
    cursor.close()
    sqliteConnection.close()
# ===================================================================================


# ==========================>> LOGIN <<===============================
def Login(username, password):
    conn = sqlite3.connect("data/database.db")
    user_list = Get_listusername()

    for user in user_list:
        if user[0] == username and user[1] == password:
            conn.close()
            return True
    conn.close()
    return False
# =====================================================================


# ==========================>> SHARE IMAGE <<===============================
def get_filename_list(id_user):
    conn = sqlite3.connect("data/database.db")
    sql = '''
    SELECT I.name
    FROM User U, Image I
    WHERE U.id = ? and U.id = I.id_user
    '''
    data = conn.execute(sql, (id_user, )).fetchall()
    conn.close()
    return data


# Download
# Input: tên image và id user để truy vấn trong database
# Output: data giải mã của file có tên trên input
# Quá trình:
# - Lấy data đã mã hóa bằng aes và key mã hóa bằng rsa từ db về
# - Truy vấn trong db để tìm private key của user qua id => có private key
# - Giải mã hash key bằng private key => key
# - Từ key ở trên giải mã dữ liệu của hình được mã hóa => có plaintext
def get_data_img(name, id_user):
    conn = sqlite3.connect("data/database.db")
    sql = '''
    SELECT data, hash_key
    FROM Image i, User u
    Where i.name = ? and u.id = ? and u.id = i.id_user
    '''
    data = conn.execute(sql, (name, id_user)).fetchone()
    conn.close()

    if data is None:
        return False

    original_data = data[0]
    hash_key = data[1]
    publickey, privatekey = get_rsakey(id_user)

    key = aes.decrypt_key(hash_key, privatekey)

    decrypted_data = image.decrypt_img(key, original_data)

    return decrypted_data


def is_exist(id):
    data = Get_listusername()

    for user in data:
        if id == user[2]:
            return True
    return False


def ShareImg(id_sender, id_receiver, filename):
    if not is_exist(id_receiver):
        return False

    # Lấy hết tất cả các tên file mà id_sender sở hữu
    filename_list = get_filename_list(id_sender)
    for file in filename_list:
        if file[0] == filename:
            conn = sqlite3.connect("data/database.db")
            cursor = conn.cursor()

            # Lấy ảnh của sender và giải mã
            decrypted_data = get_data_img(filename, id_sender)

            # Tạo key aes mới và mã hóa ảnh vừa giải mã
            new_key = aes.random_key(32)
            encrypted_data = image.encrypt_img(new_key, decrypted_data)

            # Lấy publickey của receiver để mã hóa aes key
            publickey, privatekey = get_rsakey(id_receiver)

            # Mã hóa key aes bằng rsa
            hash_key = aes.encrypt_key(new_key, publickey)

            # Lưu data mã hóa mới và hash key mới vào db của receiver
            size = sys.getsizeof(encrypted_data)
            date = datetime.date(datetime.now())
            sql = '''
            INSERT INTO Image(name, data, size, date, id_user, hash_key) 
            VALUES (?, ?, ?, ?, ?, ?)
            '''
            cursor.execute(
                sql, (filename, encrypted_data, size, date, id_receiver, hash_key))
            #conn.execute(sql, (nameimg, img, size, date, id_user))
            conn.commit()
            cursor.close()
            conn.close()
            return True
    return False
# =====================================================================


if __name__ == "__main__":
    print(InfUser('a'))
