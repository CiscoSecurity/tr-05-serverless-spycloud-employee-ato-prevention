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
            "infected_path": "C:/Users/Usama/AppData/Local"
                             "/Temp/6210230526.exe",
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


CATALOG_17551_RESPONSE_MOCK = {
    "cursor": "",
    "hits": 1,
    "results": [
        {
            "confidence": 3,
            "description": "test description for 17551",
            "title": "Vidar Stealer",
            "type": "PRIVATE",
            "acquisition_date": "2020-04-15T00:00:00Z",
            "site": "n/a",
            "spycloud_publish_date": "2020-04-16T00:00:00Z",
            "site_description": "test site description for 17551",
            "uuid": "3a7fc3d4-2f57-4076-951c-287332a4d1f8",
            "num_records": 1107872,
            "id": 17551,
            "assets": {
                "username": 540183,
                "city": 1107503,
                "target_url": 1107872,
                "infected_time": 1107503,
                "user_browser": 93,
                "country": 1107503,
                "ip_addresses": 1097638,
                "isp": 1107503,
                "infected_path": 1107503,
                "postal_code": 791450,
                "password": 1107872,
                "email": 567689,
                "infected_machine_id": 1107503
            }
        }
    ]
}


CATALOG_17494_RESPONSE_MOCK = {
    "cursor": "",
    "hits": 1,
    "results": [
        {
            "confidence": 3,
            "description": "test description for 17494",
            "title": "Russian Password Stealer",
            "type": "PRIVATE",
            "acquisition_date": "2020-04-01T00:00:00Z",
            "site": "n/a",
            "spycloud_publish_date": "2020-04-02T00:00:00Z",
            "site_description": "test site description for 17494",
            "uuid": "1293a093-5b3b-42c5-aa90-d5784ea8374f",
            "num_records": 3142306,
            "id": 17494,
            "assets": {
                "username": 1563727,
                "city": 330,
                "target_url": 3142306,
                "infected_machine_id": 3142306,
                "user_browser": 3142279,
                "country": 3142289,
                "ip_addresses": 3049094,
                "infected_path": 3856,
                "password": 3142306,
                "email": 1578579
            }
        }
    ]
}


CATALOG_PASS_RESPONSE_MOCK = {
    "cursor": "",
    "hits": 0,
    "results": []
}


SPYCLOUD_401_RESPONSE = {
    "message": "Unauthorized"
}


SPYCLOUD_403_RESPONSE = {
    "message": "Forbidden"
}


EXPECTED_RESPONSE_401_ERROR = {
    'errors': [
        {
            'code': 'authorization error',
            'message': 'Authorization failed: Unauthorized',
            'type': 'fatal'
        }
    ]
}

EXPECTED_RESPONSE_403_ERROR = {
    'errors': [
        {
            'code': 'authorization error',
            'message': 'Authorization failed: Forbidden',
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
        'indicators': {
            'count': 2,
            'docs': [
                {
                    'confidence': 'Low',
                    'description': 'test description for 17551',
                    'external_ids': [
                        '17551', '3a7fc3d4-2f57-4076-951c-287332a4d1f8'
                    ],
                    'external_references': [
                        {
                            'description': 'test site description for 17551',
                            'source_name': 'Spycloud',
                            'url': 'n/a'
                        },
                        {
                            'description': 'test description for 17551',
                            'external_id':
                                '3a7fc3d4-2f57-4076-951c-287332a4d1f8',
                            'source_name': 'Spycloud',
                            'url': 'https://portal.spycloud.com/breach/catalog'
                                   '/3a7fc3d4-2f57-4076-951c-287332a4d1f8'
                        }
                    ],
                    'producer': 'Spycloud',
                    'schema_version': '1.0.17',
                    'short_description': 'Vidar Stealer',
                    'tags': [
                        'username', 'city', 'target_url', 'infected_time',
                        'user_browser', 'country', 'ip_addresses', 'isp',
                        'infected_path', 'postal_code', 'password', 'email',
                        'infected_machine_id'
                    ],
                    'title': 'Vidar Stealer',
                    'type': 'indicator',
                    'valid_time': {
                        'start_time': '2020-04-16T00:00:00.000000Z'
                    }
                },
                {
                    'confidence': 'Low',
                    'description': 'test description for 17494',
                    'external_ids': [
                        '17494', '1293a093-5b3b-42c5-aa90-d5784ea8374f'
                    ],
                    'external_references': [
                        {
                            'description': 'test site description for 17494',
                            'source_name': 'Spycloud',
                            'url': 'n/a'
                        },
                        {
                            'description': 'test description for 17494',
                            'external_id':
                                '1293a093-5b3b-42c5-aa90-d5784ea8374f',
                            'source_name': 'Spycloud',
                            'url': 'https://portal.spycloud.com/breach/catalog'
                                   '/1293a093-5b3b-42c5-aa90-d5784ea8374f'
                        }
                    ],
                    'producer': 'Spycloud',
                    'schema_version': '1.0.17',
                    'short_description': 'Russian Password Stealer',
                    'tags': [
                        'username', 'city', 'target_url',
                        'infected_machine_id', 'user_browser', 'country',
                        'ip_addresses', 'infected_path', 'password', 'email'
                    ],
                    'title': 'Russian Password Stealer',
                    'type': 'indicator',
                    'valid_time': {
                        'start_time': '2020-04-02T00:00:00.000000Z'
                    }
                }
            ]
        },
        'sightings': {
            'count': 2,
            'docs': [
                {
                    'confidence': 'High',
                    'count': 1,
                    'data': {
                        'columns': [
                            {
                                'name': 'city',
                                'type': 'string'
                            },
                            {
                                'name': 'infected_path',
                                'type': 'string'
                            },
                            {
                                'name': 'infected_time',
                                'type': 'string'
                            },
                            {
                                'name': 'country',
                                'type': 'string'
                            },
                            {
                                'name': 'isp',
                                'type': 'string'
                            },
                            {
                                'name': 'email',
                                'type': 'string'
                            },
                            {
                                'name': 'password',
                                'type': 'string'
                            },
                            {
                                'name': 'target_url',
                                'type': 'string'
                            },
                            {
                                'name': 'password_plaintext',
                                'type': 'string'
                            },
                            {
                                'name': 'password_type',
                                'type': 'string'
                            }
                        ],
                        'rows': [
                            [
                                '()',
                                'C:/Users/Usama/AppData/Local/Temp'
                                '/6210230526.exe',
                                '2020-03-26 16:56:49',
                                '()',
                                '()',
                                'admin@example.org',
                                'test123',
                                'http://localhost:3000/en/session',
                                'test123',
                                'plaintext'
                            ]
                        ]
                    },
                    'description': 'Present in Vidar Stealer',
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
                        'start_time': '2020-04-16T00:00:00.000000Z',
                        'end_time': '2020-04-16T00:00:00.000000Z'
                    },
                    'relations': [],
                    'schema_version': '1.0.17',
                    'severity': 'High',
                    'source': 'Spycloud',
                    'source_uri': 'https://portal.spycloud.com/breach/catalog/'
                                  '3a7fc3d4-2f57-4076-951c-287332a4d1f8',
                    'targets': [
                        {
                            'observables': [
                                {
                                    'type': 'email',
                                    'value': 'admin@example.org'
                                }
                            ],
                            'observed_time': {
                                'start_time': '2020-04-16T00:00:00.000000Z',
                                'end_time': '2020-04-16T00:00:00.000000Z'
                            },
                            'type': 'email'
                        }
                    ],
                    'title': 'Reported to Spycloud',
                    'type': 'sighting'
                },
                {
                    'confidence': 'High',
                    'count': 6,
                    'data': {
                        'columns': [
                            {
                                'name': 'target_url',
                                'type': 'string'
                            },
                            {
                                'name': 'user_browser',
                                'type': 'string'
                            },
                            {
                                'name': 'country',
                                'type': 'string'
                            },
                            {
                                'name': 'ip_addresses',
                                'type': 'string'
                            },
                            {
                                'name': 'email',
                                'type': 'string'
                            },
                            {
                                'name': 'password',
                                'type': 'string'
                            },
                            {
                                'name': 'password_plaintext',
                                'type': 'string'
                            },
                            {
                                'name': 'password_type',
                                'type': 'string'
                            }
                        ],
                        'rows': [
                            [
                                '13.127.174.82',
                                'Google Chrome New',
                                'India',
                                ['210.56.127.202'],
                                'admin@example.org',
                                'Admin@1234',
                                'Admin@1234',
                                'plaintext'
                            ]
                        ]
                    },
                    'description': 'Present in Russian Password Stealer',
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
                        'start_time': '2020-04-02T00:00:00.000000Z',
                        'end_time': '2020-04-02T00:00:00.000000Z'
                    },
                    'relations': [],
                    'schema_version': '1.0.17',
                    'severity': 'High',
                    'source': 'Spycloud',
                    'source_uri': 'https://portal.spycloud.com/breach/catalog/'
                                  '1293a093-5b3b-42c5-aa90-d5784ea8374f',
                    'targets': [
                        {
                            'observables': [
                                {
                                    'type': 'email',
                                    'value': 'admin@example.org'
                                }
                            ],
                            'observed_time': {
                                'start_time': '2020-04-02T00:00:00.000000Z',
                                'end_time': '2020-04-02T00:00:00.000000Z'
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


EXPECTED_SUCCESS_RESPONSE_WITHOUT_1_CATALOG = {
    'data': {
        'indicators': {
            'count': 1,
            'docs': [
                {
                    'confidence': 'Low',
                    'description': 'test description for 17551',
                    'external_ids': [
                        '17551',
                        '3a7fc3d4-2f57-4076-951c-287332a4d1f8'
                    ],
                    'external_references': [
                        {
                            'description': 'test site description for 17551',
                            'source_name': 'Spycloud',
                            'url': 'n/a'
                        },
                        {
                            'description': 'test description for 17551',
                            'external_id':
                                '3a7fc3d4-2f57-4076-951c-287332a4d1f8',
                            'source_name': 'Spycloud',
                            'url':
                                'https://portal.spycloud.com/breach/catalog/'
                                '3a7fc3d4-2f57-4076-951c-287332a4d1f8'
                        }
                    ],
                    'producer': 'Spycloud',
                    'schema_version': '1.0.17',
                    'short_description': 'Vidar Stealer',
                    'tags': [
                        'username',
                        'city',
                        'target_url',
                        'infected_time',
                        'user_browser',
                        'country',
                        'ip_addresses',
                        'isp',
                        'infected_path',
                        'postal_code',
                        'password',
                        'email',
                        'infected_machine_id'
                    ],
                    'title': 'Vidar Stealer',
                    'type': 'indicator',
                    'valid_time': {
                        'start_time': '2020-04-16T00:00:00.000000Z'
                    }
                }
            ]
        },
        'sightings': {
            'count': 2,
            'docs': [
                {
                    'confidence': 'High',
                    'count': 1,
                    'data': {
                        'columns': [
                            {
                                'name': 'city',
                                'type': 'string'
                            },
                            {
                                'name': 'infected_path',
                                'type': 'string'
                            },
                            {
                                'name': 'infected_time',
                                'type': 'string'
                            },
                            {
                                'name': 'country',
                                'type': 'string'
                            },
                            {
                                'name': 'isp',
                                'type': 'string'
                            },
                            {
                                'name': 'email',
                                'type': 'string'
                            },
                            {
                                'name': 'password',
                                'type': 'string'
                            },
                            {
                                'name': 'target_url',
                                'type': 'string'
                            },
                            {
                                'name': 'password_plaintext',
                                'type': 'string'
                            },
                            {
                                'name': 'password_type',
                                'type': 'string'
                            }
                        ],
                        'rows': [
                            [
                                '()',
                                'C:/Users/Usama/AppData/Local/'
                                'Temp/6210230526.exe',
                                '2020-03-26 16:56:49',
                                '()',
                                '()',
                                'admin@example.org',
                                'test123',
                                'http://localhost:3000/en/session',
                                'test123',
                                'plaintext'
                            ]
                        ]
                    },
                    'description': 'Present in Vidar Stealer',
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
                        'start_time': '2020-04-16T00:00:00.000000Z',
                        'end_time': '2020-04-16T00:00:00.000000Z'
                    },
                    'relations': [],
                    'schema_version': '1.0.17',
                    'severity': 'High',
                    'source': 'Spycloud',
                    'source_uri': 'https://portal.spycloud.com/breach/catalog/'
                                  '3a7fc3d4-2f57-4076-951c-287332a4d1f8',
                    'targets': [
                        {
                            'observables': [
                                {
                                    'type': 'email',
                                    'value': 'admin@example.org'
                                }
                            ],
                            'observed_time': {
                                'start_time': '2020-04-16T00:00:00.000000Z',
                                'end_time': '2020-04-16T00:00:00.000000Z'
                            },
                            'type': 'email'
                        }
                    ],
                    'title': 'Reported to Spycloud',
                    'type': 'sighting'
                },
                {
                    'confidence': 'High',
                    'count': 6,
                    'data': {
                        'columns': [
                            {
                                'name': 'target_url',
                                'type': 'string'
                            },
                            {
                                'name': 'user_browser',
                                'type': 'string'
                            },
                            {
                                'name': 'country',
                                'type': 'string'
                            },
                            {
                                'name': 'ip_addresses',
                                'type': 'string'
                            },
                            {
                                'name': 'email',
                                'type': 'string'
                            },
                            {
                                'name': 'password',
                                'type': 'string'
                            },
                            {
                                'name': 'password_plaintext',
                                'type': 'string'
                            },
                            {
                                'name': 'password_type',
                                'type': 'string'
                            }
                        ],
                        'rows': [
                            [
                                '13.127.174.82',
                                'Google Chrome New',
                                'India',
                                ['210.56.127.202'],
                                'admin@example.org',
                                'Admin@1234',
                                'Admin@1234',
                                'plaintext'
                            ]
                        ]
                    },
                    'description': 'Present in breach',
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
                        'start_time': '2020-04-02T00:00:00.000000Z',
                        'end_time': '2020-04-02T00:00:00.000000Z'
                    },
                    'relations': [],
                    'schema_version': '1.0.17',
                    'severity': 'High',
                    'source': 'Spycloud',
                    'targets': [
                        {
                            'observables': [
                                {
                                    'type': 'email',
                                    'value': 'admin@example.org'
                                }
                            ],
                            'observed_time': {
                                'start_time': '2020-04-02T00:00:00.000000Z',
                                'end_time': '2020-04-02T00:00:00.000000Z'
                            },
                            'type': 'email'
                        }
                    ],
                    'title': 'Reported to Spycloud',
                    'type': 'sighting'
                }
            ]
        }
    },
    'errors': [
        {
            'code': 'not found',
            'message': 'SpyCloud did not return results for 17494',
            'type': 'warning'
        }
    ]
}


EXPECTED_RESPONSE_SSL_ERROR = {
    'errors': [
        {
            'code': 'unknown',
            'message': 'Unable to verify SSL certificate: self signed '
                       'certificate',
            'type': 'fatal'
        }
    ]
}

EXPECTED_AUTHORIZATION_HEADER_ERROR = {
    'errors': [
        {
            'code': 'authorization error',
            'message': 'Authorization failed: Authorization header is missing',
            'type': 'fatal'
        }
    ]
}

EXPECTED_AUTHORIZATION_TYPE_ERROR = {
    'errors': [
        {
            'code': 'authorization error',
            'message': 'Authorization failed: Wrong authorization type',
            'type': 'fatal'
        }
    ]
}

EXPECTED_JWT_STRUCTURE_ERROR = {
    'errors': [
        {
            'code': 'authorization error',
            'message': 'Authorization failed: Wrong JWT structure',
            'type': 'fatal'
        }
    ]
}

EXPECTED_JWT_PAYLOAD_STRUCTURE_ERROR = {
    'errors': [
        {
            'code': 'authorization error',
            'message': 'Authorization failed: Wrong JWT payload structure',
            'type': 'fatal'
        }
    ]
}

EXPECTED_WRONG_SECRET_KEY_ERROR = {
    'errors': [
        {
            'code': 'authorization error',
            'message': 'Authorization failed: Failed to decode JWT with '
                       'provided key',
            'type': 'fatal'
        }
    ]
}

EXPECTED_MISSED_SECRET_KEY_ERROR = {
    'errors': [
        {
            'code': 'authorization error',
            'message': 'Authorization failed: <SECRET_KEY> is missing',
            'type': 'fatal'
        }
    ]
}
