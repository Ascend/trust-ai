# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os

from flask import Flask, render_template, make_response, jsonify, request, send_from_directory

app = Flask(__name__)


@app.route('/AIVAULT/v1/createMK', methods=('POST',))
def ai_vault():
    downloads = os.path.join(app.root_path, "/")
    with open(os.path.join(downloads, "test.json"), "w") as f:
        f.write("test file")
    return send_from_directory(directory=downloads, path="test.json"), 200


@app.route('/AIVAULT/v1/queryMK', methods=('GET',))
def query_mk():
    data = {
        "currentPage": 1,
        "pageSize": 5,
        "pageCount": 1,
        "totalCount": 1,
        "data": [
            {"MkID": 1,
             "MKName": "test",
             "MKUsage": "test",
             "MKRemarks": "test",
             "CreatedAt": "2022-06-15T11:02:28.464218241+08:00"
             }
        ]

    }
    return jsonify(data=data, msg="ok", status="00000000"), 200


@app.route('/AIVAULT/v1/deleteMK/<name>', methods=('DELETE',))
def delete_mk(name):
    return jsonify(data={}, msg="ok", status="00000000"), 200


@app.route('/AIVAULT/v1/createPSK', methods=('POST',))
def create_psk():
    data = {"PSK": "ABDSBDASD"}
    return jsonify(data=data, msg="ok", status="00000000"), 200


@app.route('/AIVAULT/v1/deletePSK/<name>', methods=('DELETE',))
def delete_psk(name):
    return jsonify(data={}, msg="ok", status="00000000"), 200


@app.route('/AIVAULT/v1/queryPSK', methods=('GET',))
def query_psk():
    data = {
        "currentPage": 1,
        "pageSize": 5,
        "pageCount": 1,
        "totalCount": 1,
        "data": [
            {
                "PSKName": "test",
                "PSKBindMKName": "test",
                "PSKRemarks": "test",
                "PSKCreateTime": "2022-06-15T11:02:28.464218241+08:00"
            }
        ]

    }
    return jsonify(data=data, msg="ok", status="00000000"), 200


@app.route('/AIVAULT/v1/version', methods=('GET',))
def get_version():
    data = {
        "version": "linux X86 V3.0.0",
    }
    return jsonify(data=data, msg="ok", status="00000000"), 200


@app.route('/AIVAULT/v1/certStatus', methods=('GET',))
def cert_status():
    data = {
        [{"CertType": "MGMT",
          "CertValidDate": "2022/6/8-2023",
          "CertAlarm": "No certificate",
          "CrlStatus": "No CRL certificate has been imported", },
         {"CertType": "SVC",
          "CertValidDate": "2022/6/8-2023",
          "CertAlarm": "No certificate",
          "CrlStatus": "No CRL certificate has been imported", }]
    }
    return jsonify(data=data, msg="ok", status="00000000"), 200


@app.route('/AIVAULT/v1/health', methods=('GET',))
def get_health():
    return jsonify(data="probe successfully", msg="ok", status="00000000"), 200


if __name__ == "__main__":
    app.run(ssl_context=("/home/luxiang/nginx/conf/server.pem", "/home/luxiang/nginx/conf/server.key"))
