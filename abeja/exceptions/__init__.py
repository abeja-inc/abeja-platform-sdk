

class Error(Exception):
    pass


class HttpError(Error):

    def __init__(
            self,
            error,
            error_description,
            error_detail=None,
            status_code=None,
            url=None):
        self.error = error
        self.error_description = error_description
        self.error_detail = error_detail
        self.status_code = status_code
        self.url = url

    def __repr__(self):
        s = '<%s "%s": %s' % (self.__class__.__name__,
                              self.error, self.error_description)
        if self.status_code and self.url:
            s += ' (%s from %s)' % (self.status_code, self.url)
        if self.error_detail:
            s += ', ' + str(self.error_detail)
        return s + '>'

    __str__ = __repr__

    def _asdict(self):
        data = {
            'error': self.error,
            'error_description': self.error_description
        }
        if self.error_detail:
            data['error_detail'] = self.error_detail
        if self.status_code:
            data['status_code'] = self.status_code
        if self.url:
            data['url'] = self.url
        return data


class BadRequest(HttpError):
    pass


class Unauthorized(HttpError):
    pass


class Forbidden(HttpError):
    pass


class NotFound(HttpError):
    pass


class MethodNotAllowed(HttpError):
    pass


class Conflict(HttpError):
    pass


class InternalServerError(HttpError):
    pass


class UnsupportedURI(Error):
    pass


class InvalidDataFormat(Error):
    pass


class ResourceNotFound(Error):
    pass


class InvalidPathException(Error):

    def __init__(self, path):
        self.path = path


class EtagHashNotMatch(Error):
    pass
