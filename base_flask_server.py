
from flask import Flask, request, jsonify
import json
from flask_cors import CORS
from flask_socketio import SocketIO


app = Flask(__name__)
CORS(app)

socketio = SocketIO(app, cors_allowed_origins='*')

@app.route('/', methods=['GET', 'POST'])
def main():
    return "OK"


@app.route('/node', methods=['GET', 'POST'])
def testNode():
    if request.method == 'POST':
        # 打印POST请求的所有参数
        data = request.get_json()
        if not data:
            data = json.loads(request.data.decode())
        print("\n=== POST请求参数 ===")
        print("Headers:", dict(request.headers))
        print("JSON数据:", data)
        print("Form数据:", request.form)
        print("Files:", request.files)
        return jsonify({'message': 'success'})
    elif request.method == 'GET':
        # 打印GET请求的所有参数
        print("\n=== GET请求参数 ===")
        print("Headers:", dict(request.headers))
        print("查询参数:", request.args)
        print("Cookies:", request.cookies)
        return jsonify({'message': 'success'})

if __name__ == "__main__":
    socketio.run(app, debug=True, host='0.0.0.0', port=7788)
