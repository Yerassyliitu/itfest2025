class EmailServiceUnavailableException(Exception):
    pass

class UserAlreadyExistsException(Exception):
    pass

class CacheServiceException(Exception):
    pass

class CodeExpiredException(Exception):
    pass

class InvalidCodeException(Exception):
    pass

class ServerErrorException(Exception):
    pass

class InvalidAccessTokenException(Exception):
    pass