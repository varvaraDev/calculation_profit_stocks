class RequestError(Exception):
    """Raise when trying to process incorrect data

    Args:
        message(string) text about error"""
    def __init__(self, error):
        self.message = error.args[0]
        if isinstance(error, IndexError):
            self.message = 'Invalid input data'

    def get_data(self):
        if self.message.endswith('\u0027'):
            self.message = self.message.replace('\u0027', ' ')
        return self.message


RemoteDataError_mess = '''RemoteDataError: Please check the id stocks and
                          Internet connection. Then try again.'''
