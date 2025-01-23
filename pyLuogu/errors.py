class LuoguAPIError(Exception):
    """Base class for all exceptions raised by the Luogu API."""
    pass

class RequestError(LuoguAPIError):
    """Exception raised for errors in the request."""
    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.status_code = status_code

class AuthenticationError(LuoguAPIError):
    """Exception raised for authentication errors."""
    pass

class NotFoundError(LuoguAPIError):
    """Exception raised when a resource is not found."""
    pass

class RateLimitError(LuoguAPIError):
    """Exception raised when the rate limit is exceeded."""
    pass

class ServerError(LuoguAPIError):
    """Exception raised for server errors."""
    pass

class ForbiddenError(LuoguAPIError):
    """Exception raised when the user is forbidden to access the resource."""
    pass