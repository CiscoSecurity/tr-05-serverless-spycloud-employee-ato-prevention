INVALID_ARGUMENT = 'invalid argument'
PERMISSION_DENIED = 'permission denied'
UNKNOWN = 'unknown'
NOT_FOUND = 'not found'
INTERNAL = 'internal error'
TOO_MANY_REQUESTS = 'too many requests'


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


class SpycloudInvalidCredentialsError(TRError):
    def __init__(self):
        super().__init__(
            PERMISSION_DENIED,
            'The request is missing a valid API key.'
        )


class SpycloudForbidenError(TRError):
    def __init__(self):
        super().__init__(
            PERMISSION_DENIED,
            'The request has API key without necessary permissions.'
        )


class SpycloudUnexpectedResponseError(TRError):
    def __init__(self, payload):
        error_payload = payload.json().get('message', [])

        super().__init__(
            UNKNOWN,
            str(error_payload)
        )


class BadRequestError(TRError):
    def __init__(self, error_message):
        super().__init__(
            INVALID_ARGUMENT,
            error_message
        )
