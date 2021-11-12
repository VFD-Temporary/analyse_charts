# a file to declare all the custom exception classes

class DatabaseLookupError(Exception):
    """To be raised when an error occurs while fetching values from the database"""
    pass

class NotInDatabaseException(Exception):
    """To be raised when a value or field is not present in the database"""
    pass

class NoDataException(Exception):
    """To be raised when the selected field in the database has no data"""

class DataStructuringError(Exception):
    """To be raised when an error occurs while structuring the response data"""
    pass

class DataFieldNotPresent(Exception):
    """To be raised when a data field is not present in the database"""
    pass

class UnExpexpectedDurationError(Exception):
    """To be raised if the date duration type is unrecognised"""
    pass

class InvalidDatesException(Exception):
    """To be raised when invalid dates are unexpectedly encountered"""
    pass


class IncorrectSlicingError(Exception):
    """To be raised when a slicing operation is performed and it returns an error"""
    pass


class DurationIndexFetchError(Exception):
    """To be raised if the incoming request does not have the login session details"""
    pass

class ResponseStructuringError(Exception):
    """To be raised if the incoming request does not have the login session details"""
    pass

class DateTypeCastingError(Exception):
    pass