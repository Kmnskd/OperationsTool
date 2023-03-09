from flask import jsonify, make_response


class LdapManagerError(Exception):
    # def __init__(self, message=None):
    #     super().__init__(message)
    pass


class ErrorStatus(object):
    def status_code(self, status_code=200, status="success", message=""):
        data = {"status": status, "message": message}
        return make_response(jsonify(data), status_code)
