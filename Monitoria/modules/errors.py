class Error(Exception):
    '''Base class for other exceptions'''
    pass

class MultipleFilesError(Error):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, files, message):
        self.files = expression
        self.message = message

class AmbiguousFileError(Error):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, message, files = []):
        self.message = message
        self.files = files

    def __str__(self):
        line = f"{self.message}"
        for file in self.files:
            line = line + '\n' + str(file)
        return line

class InvalidInputError(Error):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message

class StudentNotInClassError(Error):
    '''Exception raised if a external student is found during parsing '''
    def __init__(self, message):
        self.message = message
