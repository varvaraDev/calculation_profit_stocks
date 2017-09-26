

class RatesError(Exception):
    """This exception raised when try get not created shipments rates"""
    pass


class LabelNotCreated(Exception):
    """This exception raise when try return from base not created
    shipment label"""
    pass
