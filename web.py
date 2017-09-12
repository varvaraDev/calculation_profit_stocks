import hug
from marshmallow import fields
# fields.DateTime()


@hug.object.post('/stocks')
def products_created(self, body=None):
    pass


@hug.exception(Exception)
def handle_exception(exception):
    print('ERROR')
    return {'error': "Python broke again! Don't blame us! {}".format(
                                                            exception)
            }
