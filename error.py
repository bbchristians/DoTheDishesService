from flask import jsonify


class Error:
    def __init__(self, message):
        self.message = message

    def json(self):
        return {
            'error': self.message
        }


def error_400(message):
    return jsonify(Error(message).json()), 400
