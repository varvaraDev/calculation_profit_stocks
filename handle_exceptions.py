class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


data_form = 'AAPL=2016-12-24=1200\r\nGOOG=2001-01-01=50\r\nAMZN=2012-01-01=150'.split('\r\n')


class RequestError(Exception):
    def __init__(self, error):
        self.message = error.args[0]

    def get_data(self):
        return self.message

# from flask import abort, redirect, url_for
#
# @app.route('/')
# def index():
#     return redirect(url_for('login'))
#
# @app.route('/login')
# def login():
#     abort(401)
#     this_is_never_executed()
#
#
# from flask import render_template
#
# @app.errorhandler(404)
# def page_not_found(error):
#     return render_template('page_not_found.html'), 404


# def get_err():
#         try:
#             raise TypeError
#         except (TypeError, TypeError, IndexError) as e:
#             return e
