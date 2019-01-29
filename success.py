from flask import jsonify


def success_200(dict):
    return jsonify(dict), 200
