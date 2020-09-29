INVALID_ARGUMENT = 'invalid argument'
UNKNOWN = 'unknown'
NOT_FOUND = 'not found'
INTERNAL = 'internal error'
TOO_MANY_REQUESTS = 'too many requests'
AUTH_ERROR = 'authorization error'


class TRError(Exception):
    def __init__(self, code, message, type_='fatal'):
        super().__init__()
        self.code = code or UNKNOWN
        self.message = message or 'Something went wrong.'
        self.type_ = type_

    @property
    def json(self):
        return {'type': self.type_,
                'code': self.code,
                'message': self.message}


class SpycloudInternalServerError(TRError):
    def __init__(self):
        super().__init__(
            INTERNAL,
            'The Spycloud internal error.'
        )


class SpycloudNotFoundError(TRError):
    def __init__(self):
        super().__init__(
            NOT_FOUND,
            'The Spycloud not found.'
        )


class SpycloudUnexpectedResponseError(TRError):
    def __init__(self, payload):
        error_payload = payload.json()

        super().__init__(
            UNKNOWN,
            str(error_payload)
        )


class SpycloudTooManyRequestsError(TRError):
    def __init__(self):
        super().__init__(
            TOO_MANY_REQUESTS,
            'Too many requests have been made to '
            'Spycloud. Please, try again later.'
        )


class SpycloudCatalogError(TRError):
    def __init__(self, message):
        super().__init__(
            NOT_FOUND,
            message,
            'warning'
        )


class SpycloudSSLError(TRError):
    def __init__(self, error):
        message = getattr(
            error.args[0].reason.args[0], 'verify_message', ''
        ) or error.args[0].reason.args[0].args[0]

        super().__init__(
            UNKNOWN,
            f'Unable to verify SSL certificate: {message}'
        )


class AuthorizationError(TRError):
    def __init__(self, message):

        super().__init__(
            AUTH_ERROR,
            f"Authorization failed: {message}"
        )


class BadRequestError(TRError):
    def __init__(self, error_message):
        super().__init__(
            INVALID_ARGUMENT,
            error_message
        )
