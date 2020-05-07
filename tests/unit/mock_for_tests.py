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

BREACH_EMAIL_RESPONSE_MOCK = {
    "cursor": "",
    "hits": 2,
    "results": [
        {
            "city": "()",
            "domain": "example.org",
            "infected_path": "C:/Users/Usama/AppData/Local/Temp/6210230526.exe",
            "infected_time": "2020-03-26 16:56:49",
            "country": "()",
            "isp": "()",
            "email_username": "admin",
            "email": "admin@example.org",
            "spycloud_publish_date": "2020-04-16T00:00:00Z",
            "password": "test123",
            "target_url": "http://localhost:3000/en/session",
            "sighting": 1,
            "email_domain": "example.org",
            "source_id": 17551,
            "infected_machine_id": "0bb046a5-2ef2-4ec3-abbe-ba76f5b78e6c",
            "password_plaintext": "test123",
            "password_type": "plaintext",
            "document_id": "90f9c47d-c86d-400f-9a57-38fed22b5fad",
            "severity": 25
        },
        {
            "domain": "example.org",
            "target_url": "13.127.174.82",
            "infected_machine_id": "2fc6eba4-738d-11ea-807f-0a7889d429db",
            "user_browser": "Google Chrome New",
            "country": "India",
            "ip_addresses": [
                "210.56.127.202"
            ],
            "email_username": "admin",
            "email": "admin@example.org",
            "spycloud_publish_date": "2020-04-02T00:00:00Z",
            "password": "Admin@1234",
            "sighting": 6,
            "email_domain": "example.org",
            "source_id": 17494,
            "password_plaintext": "Admin@1234",
            "password_type": "plaintext",
            "document_id": "d27e8c1e-dd07-4237-bf51-40bcb5744fcc",
            "severity": 25
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


EXPECTED_SUCCESS_RESPONSE = {
    'data': {
        'sightings': {
            'count': 2,
            'docs': [
                {
                    'confidence': 'Medium',
                    'count': 1,
                    'external_ids': [
                        '90f9c47d-c86d-400f-9a57-38fed22b5fad',
                        '17551',
                        '0bb046a5-2ef2-4ec3-abbe-ba76f5b78e6c'
                    ],
                    'internal': False,
                    'observables': [
                        {
                            'type': 'email',
                            'value': 'admin@example.org'
                        }
                    ],
                    'observed_time': {
                        'start_time': '2020-04-16T00:00:00.000000Z'
                    },
                    'relations': [
                        {
                            'origin': 'Spycloud Breach Module',
                            'related': {
                                'type': 'email',
                                'value': 'admin@example.org'
                            },
                            'relation': 'Leaked_From',
                            'source': {
                                'type': 'domain',
                                'value': 'example.org'
                            }
                        }
                    ],
                    'schema_version': '1.0.16',
                    'severity': 'High',
                    'source': 'Spycloud',
                    'targets': [
                        {
                            'observables': [
                                {
                                    'type': 'url',
                                    'value': 'http://localhost:3000/en/session'
                                }
                            ],
                            'observed_time': {
                                'start_time': '2020-04-16T00:00:00.000000Z'
                            },
                            'type': 'email'
                        }
                    ],
                    'title': 'Reported to Spycloud',
                    'type': 'sighting'
                },
                {
                    'confidence': 'Medium',
                    'count': 6,
                    'external_ids': [
                        'd27e8c1e-dd07-4237-bf51-40bcb5744fcc',
                        '17494',
                        '2fc6eba4-738d-11ea-807f-0a7889d429db'
                    ],
                    'internal': False,
                    'observables': [
                        {
                            'type': 'email',
                            'value': 'admin@example.org'
                        }
                    ],
                    'observed_time': {
                        'start_time': '2020-04-02T00:00:00.000000Z'
                    },
                    'relations': [
                        {
                            'origin': 'Spycloud Breach Module',
                            'related': {
                                'type': 'email',
                                'value': 'admin@example.org'
                            },
                            'relation': 'Leaked_From',
                            'source': {
                                'type': 'domain',
                                'value': 'example.org'
                            }
                        },
                        {
                            'origin': 'Spycloud Breach Module',
                            'related': {
                                'type': 'email',
                                'value': 'admin@example.org'
                            },
                            'relation': 'Leaked_From',
                            'source': {
                                'type': 'ip',
                                'value': '210.56.127.202'
                            }
                        }
                    ],
                    'schema_version': '1.0.16',
                    'severity': 'High',
                    'source': 'Spycloud',
                    'targets': [
                        {
                            'observables': [
                                {
                                    'type': 'ip',
                                    'value': '13.127.174.82'
                                }
                            ],
                            'observed_time': {
                                'start_time': '2020-04-02T00:00:00.000000Z'
                            },
                            'type': 'email'
                        }
                    ],
                    'title': 'Reported to Spycloud',
                    'type': 'sighting'
                }
            ]
        }
    }
}
