from Crypto.Cipher import AES
import random
import rsa


# Sinh key ngẫu nhiên 32 bytes
def random_key(bytes):
    key = ''
    for i in range(bytes):
        key += chr(random.randint(0, 127))

    return key


# AES dùng mode CBC
mode = AES.MODE_CBC
IV = 'This is an IV123'.encode("utf-8")
padding = '0'.encode('utf-8')


def pad_message(msg):
    while len(msg) % 16 != 0:
        msg += padding
    return msg


def encrypt(plaintext, key):
    cipher = AES.new(key.encode('utf-8'), mode, IV)
    padded_text = pad_message(plaintext)
    ciphertext = cipher.encrypt(padded_text)

    return ciphertext


def decrypt(ciphertext, key):
    cipher = AES.new(key.encode('utf-8'), mode, IV)
    plaintext = cipher.decrypt(ciphertext)

    return plaintext.rstrip(padding)


# Chuyen day chu thanh day so
def string_2_num(string):
    num = []
    for s in string:
        num.append(str(ord(s)))

    return num


# Input: key dạng string và publickey dạng tuple => dùng publickey để mã hóa rsa key
# Output: key được mã hóa dạng string
# Quá trình: Duyệt qua từng ký tự trong key rồi rsa ký tự đó lưu vào encrypted key
def encrypt_key(key: str, publickey: tuple):
    new_key = string_2_num(key)

    rsa_encrypted_key = []
    for k in new_key:
        temp = rsa.encrypt(publickey, k)
        rsa_encrypted_key.append(str(chr(int(temp))))

    return str(''.join(rsa_encrypted_key))


# Input: encrypted key dạng string và privatekey dạng tuple => dùng privatekey để giải mã rsa key
# Output: key được giải mã
# Quá trình: Duyệt qua từng ký tự trong encrypted key rồi rsa ký tự đó lưu vào decrypted key
def decrypt_key(encypted_key, privatekey):
    new_key = string_2_num(encypted_key)

    rsa_decrypted_key = []
    for k in new_key:
        temp = rsa.decrypt(privatekey, k)
        rsa_decrypted_key.append(str(chr(int(temp))))

    return str(''.join(rsa_decrypted_key))


# Main test==========================================================
# key = random_key(32)

# msg = 'my name is 0 dinh'.encode('utf-8')

# print(f'Key = {key}')
# ciphertext = encrypt(msg, key)
# print(f'Cipher text = {ciphertext}')
# plaintext = decrypt(ciphertext, key)
# print(f'Plaintext text = {plaintext}')

# (publickey, privatekey) = rsa.key_gen(7)

# encrypted_key = encrypt_key(key, publickey)
# print(f'Encrypted key = {encrypted_key}')

# decrypted_key = decrypt_key(encrypted_key, privatekey)
# print(f'Decrypted key = {decrypted_key}')

# new_key = list_2_string(decrypted_key)
# new_plaintext = decrypt(ciphertext, new_key)
# print(f'New Plaintext text = {new_plaintext}')
