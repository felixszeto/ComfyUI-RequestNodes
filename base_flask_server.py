from flask import Flask, request, jsonify, Response, send_file
import json
from flask_cors import CORS
from flask_socketio import SocketIO
import io
import traceback
from werkzeug.exceptions import HTTPException
import random
import os

app = Flask(__name__)
CORS(app)

socketio = SocketIO(app, cors_allowed_origins='*')

@app.before_request
def log_request_info():
    print(f"\n--- Received Request ---")
    print(f"Method: {request.method}")
    print(f"Path: {request.path}")
    print(f"Headers: {request.headers}")
    if request.method == 'GET':
        print(f"Query Parameters: {request.args}")
    elif request.method in ['POST', 'PUT', 'PATCH']:
        try:
            print(f"Request Body (JSON): {request.get_json(silent=True)}")
        except:
            print(f"Request Body (Form): {request.form}")
    else:
        print(f"Request Data: {request.data}")
    print(f"------------------------\n")

@app.errorhandler(Exception)
def handle_exception(e):
    # 打印详细的错误堆栈信息
    print("发生错误:", str(e))
    print(traceback.format_exc())

    if isinstance(e, HTTPException):
        response = jsonify({
            "error": str(e),
            "status_code": e.code,
            "description": e.description
        })
        response.status_code = e.code
        return response

    response = jsonify({
        "error": "服务器内部错误",
        "details": str(e)
    })
    response.status_code = 500
    return response

@app.route('/api/echo', methods=['POST', 'PUT', 'PATCH'])
def echo_request_body():
    print(f"Received {request.method} request on /api/echo")
    try:
        data = request.get_json(silent=True)
        if data is None:
            data = request.form.to_dict()
        
        headers_info = {
            'Content-Type': request.headers.get('Content-Type'),
            'User-Agent': request.headers.get('User-Agent'),
            'Accept': request.headers.get('Accept')
        }

        response_data = {
            "received_method": request.method,
            "received_data": data,
            "received_headers": headers_info
        }
        print(f"Echoing data: {response_data}")
        return jsonify(response_data)
    except Exception as e:
        print(f"处理 /api/echo 请求时出错: {str(e)}")
        return jsonify({"error": "处理请求时发生错误", "details": str(e)}), 500

@app.route('/api/status/<int:code>', methods=['GET'])
def return_status_code(code):
    print(f"Received GET request on /api/status/{code}")
    try:
        if code < 100 or code > 599:
             print(f"错误: 无效的状态码: {code}")
             return jsonify({"error": f"Invalid status code: {code}"}), 400

        print(f"Returning response with status code: {code}")
        return jsonify({"message": f"Returning with status code {code}"}), code
    except Exception as e:
        print(f"处理 /api/status/{code} 请求时出错: {str(e)}")
        return jsonify({"error": "处理请求时发生错误", "details": str(e)}), 500


@app.route('/api/headers', methods=['GET'])
def return_custom_headers():
    print("Received GET request on /api/headers")
    response = jsonify({"message": "This response has custom headers"})
    response.headers['X-Custom-Header'] = 'Custom Value'
    response.headers['X-Another-Header'] = 'Another Value'
    response.headers['X-Request-Method'] = request.method # Example using request context
    print("Returning response with custom headers")
    return response

@app.route('/api/file', methods=['GET'])
def return_test_file():
    print("Received GET request on /api/file")
    try:
        # Create a simple text file in memory and return it
        file_content = b"This is the content of the test file from /api/file."
        file_data = io.BytesIO(file_content)
        file_data.seek(0)
        print("Sending file: test_file.txt")
        return send_file(
            file_data,
            mimetype="text/plain",
            as_attachment=True,
            download_name="test_file.txt",
            headers={'X-File-Source': '/api/file'}
        )
    except Exception as e:
        print(f"发送文件时出错: {str(e)}")
        return jsonify({"error": "发送文件时发生错误", "details": str(e)}), 500

@app.route('/api/random_failure', methods=['GET'])
def random_failure_endpoint():
    print("Received GET request on /api/random_failure")
    if random.random() < 0.2:
        print("Simulating random 500 error")
        return jsonify({"error": "Simulated internal server error from /api/random_failure"}), 500
    else:
        print("Returning successful response from /api/random_failure")
        return jsonify({"message": "Success from /api/random_failure", "status": "ok"})

@app.route('/api/request_info', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS'])
def return_request_info():
    print(f"Received {request.method} request on /api/request_info")
    try:
        request_info = {
            "method": request.method,
            "path": request.path,
            "headers": dict(request.headers), # Convert headers to dict for JSON serialization
            "query_parameters": request.args.to_dict(),
            "form_data": request.form.to_dict(),
            "json_data": request.get_json(silent=True), # silent=True prevents error if body is not JSON
            "raw_data": request.data.decode('utf-8', errors='ignore') # Attempt to decode raw data
        }
        print("Returning request info as JSON")
        return jsonify(request_info)
    except Exception as e:
        print(f"处理 /api/request_info 请求时出错: {str(e)}")
        return jsonify({"error": "处理请求时发生错误", "details": str(e)}), 500

@app.route('/api/form_test', methods=['POST'])
def handle_form_post():
    print(f"Received POST request on /api/form_test")
    try:
        form_data = request.form.to_dict()
        files_info = {}
        if request.files:
            upload_folder = 'uploads'
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
            
            for field_name in request.files:
                files_info[field_name] = []
                for file_storage in request.files.getlist(field_name):
                    filename = file_storage.filename
                    file_path = os.path.join(upload_folder, filename)
                    file_storage.save(file_path)
                    
                    files_info[field_name].append({
                        "filename": filename,
                        "content_type": file_storage.content_type,
                        "saved_path": file_path
                    })

        response_data = {
            "received_form_data": form_data,
            "received_files_info": files_info
        }
        print(f"Form test data: {response_data}")
        return jsonify(response_data)
    except Exception as e:
        print(f"处理 /api/form_test 请求时出错: {str(e)}")
        return jsonify({"error": "处理请求时发生错误", "details": str(e)}), 500


if __name__ == "__main__":
    print("Starting RestApiNode test server...")
    print("API available at http://127.0.0.1:7788/api/*")
    print("Root endpoint available at http://127.0.0.1:7788/")
    socketio.run(app, debug=True, host='0.0.0.0', port=7788, use_reloader=True)