class RequestError(Exception):
    """Raise when trying to process incorrect data

    Args:
        message(string) text about error"""
    def __init__(self, error):
        self.message = error.args[0]

    def get_data(self):
        if self.message.endswith('\u0027'):
            self.message = self.message.replace('\u0027', ' ')
        return self.message
