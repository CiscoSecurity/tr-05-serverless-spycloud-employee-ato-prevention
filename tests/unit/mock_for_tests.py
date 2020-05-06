WATCHLIST_RESPONSE_MOCK = {
    "cursor": "",
    "hits": 1,
    "results": [
        {
            "status": "ACTIVE",
            "infected_user_record_count": 115,
            "last_discovered": "2020-04-30T00:09:27Z",
            "verification_secret": "",
            "verified": "YES",
            "infected_employee_record_count": 60,
            "identifier_type": "domain",
            "infected_consumer_record_count": 55,
            "corporate_record_count": 11000,
            "identifier_name": "example.org"
        }
    ]
}


EXPECTED_RESPONSE_401_ERROR = {
    'errors': [
        {
            'code': 'permission denied',
            'message': 'The request is missing a valid API key.',
            'type': 'fatal'
        }
    ]
}

EXPECTED_RESPONSE_403_ERROR = {
    'errors': [
        {
            'code': 'permission denied',
            'message': 'The request has API key without necessary '
                       'permissions.',
            'type': 'fatal'
        }
    ]
}

EXPECTED_RESPONSE_404_ERROR = {
    'errors': [
        {
            'code': 'not found',
            'message': 'The Spycloud not found.',
            'type': 'fatal'
        }
    ]
}

EXPECTED_RESPONSE_500_ERROR = {
    'errors': [
        {
            'code': 'internal error',
            'message': 'The Spycloud internal error.',
            'type': 'fatal'
        }
    ]
}
