from flask import jsonify, make_response

def handler(error, status_code, status=None, msg=None):
    res = jsonify(
        result=status
    )

    return make_response(res, status_code)


def handle_key_error(error):
    status = "Error... Campos incompletos" if isinstance(
        error, KeyError) else "Error..."
    return handler(error, 422, status=status)