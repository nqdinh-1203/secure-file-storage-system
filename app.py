from flask import Flask, jsonify
import DB
app = Flask(__name__)


@app.route('/', methods=['GET'])
def DangNhap():
    return "Hello bro!!"


@app.route('/<string:username>', methods=['GET'])
def InfUser(username):
    user = DB.InfUser(username)
    data = {
        "id": user[0],
        "name": user[1],
        "password": user[2],
        "publickey": user[3],
        "privatekey": user[4],
        "n": user[5]
    }
    return jsonify({"data": data})


@app.route('/<string:username>/search', methods=['GET'])
def ImageofUser(username):
    rows = DB.getImgofUser(username)
    data = []
    for i in rows:
        data.append({
            "id": i[0],
            "name": i[1],
            "size": i[2],
            "date": i[3]
        })
    return jsonify({"data:": data})


@app.route('/<int:id_user>/<path:file_name>/<int:e>/<int:n>/upload', methods=['GET', 'POST'])
def UploadImg(id_user, file_name, e, n):
    DB.UploadImg(file_name, id_user, e, n)
    return jsonify({"Result:": "Thanh cong"})


@app.route('/register/<string:username>/<string:password>/<int:e>/<int:d>/<int:n>', methods=['GET', 'POST'])
def Register(username, password, e, d, n):
    check = DB.Register(username, password, e, d, n)
    if check:
        return jsonify({"Result:": "Thanh cong"})
    return jsonify({"Result:": "That bai"})


@app.route('/verify/<string:username>/<int:e>', methods=['GET', 'POST'])
def Verify(username, e):
    check = DB.verify_user(username, e)
    if check:
        return jsonify({"Result": "Thanh cong"})
    return jsonify({"Result": "That bai"})


@app.route('/update/<string:username>/<int:e>/<int:d>/<int:n>', methods=['GET', 'POST'])
def Update(username, e, d, n):
    DB.update_user(username, e, d, n)
    return 'Updated'


@app.route('/login/<string:username>/<string:password>', methods=['GET', 'POST'])
def Login(username, password):
    check = DB.Login(username, password)
    if check:
        return jsonify({"Result:": "Thanh cong"})
    return jsonify({"Result:": "That bai"})


@app.route('/<int:id_sender>/share/<string:filename>/<int:id_receiver>', methods=['GET', 'POST'])
def Share(id_sender, filename, id_receiver):
    check = DB.ShareImg(id_sender, id_receiver, filename)
    if check:
        return jsonify({"Result": "Thanh cong"})
    return jsonify({"Result": "That bai"})


@app.route('/<int:id_user>/<string:filename>/download', methods=['GET'])
def Download(id_user, filename):
    data = DB.get_data_img(filename, id_user)
    if data == False:
        return jsonify({"Result": "That bai"})

    new = filename.split('.')
    new_name = './Download_image/' + new[0] + '_dowload.' + new[1]
    with open(new_name, 'wb') as fout:
        fout.write(data)
    return jsonify({"Result": "Thanh cong"})


if __name__ == "__main__":
    app.run()
    
