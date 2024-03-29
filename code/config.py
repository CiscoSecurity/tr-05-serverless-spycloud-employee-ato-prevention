import json

from uuid import NAMESPACE_X500


class Config:
    settings = json.load(open('container_settings.json', 'r'))
    VERSION = settings["VERSION"]

    NAMESPACE_BASE = NAMESPACE_X500

    SPYCLOUD_REQUEST_DURATION = 0.25  # in seconds

    SPYCLOUD_SOURCE_NAME = 'Spycloud'

    SPYCLOUD_API_URL = 'https://api.spycloud.io/enterprise-v2/{endpoint}'
    SPYCLOUD_UI_URL = 'https://portal.spycloud.com/breach/catalog/{uuid}'

    SPYCLOUD_BASE_HEADERS = {
        'Accept': 'application/json',
        'User-Agent': ('SecureX Threat Response Integrations '
                       '<tr-integrations-support@cisco.com>')
    }

    SPYCLOUD_OBSERVABLE_TYPES = {
        'email': 'Email'
    }

    SPYCLOUD_SEVERITY_RELATIONS = {
        'Low': (0, 2),
        'Medium': (3, 5),
        'High': (6, 25),
    }

    SPYCLOUD_CONFIDENCE_RELATIONS = {
        1: 'High',
        2: 'Medium',
        3: 'Low'
    }

    SPYCLOUD_IGNORING_FIELDS = [
        'sighting', 'infected_machine_id', 'email_domain', 'domain',
        'email_username', 'document_id', 'source_id', 'spycloud_publish_date',
        'severity'
    ]

    CTR_DEFAULT_ENTITIES_LIMIT = 100

    CTIM_SCHEMA_VERSION = '1.0.17'

    CTIM_SIGHTING_DEFAULT = {
        'type': 'sighting',
        'schema_version': CTIM_SCHEMA_VERSION,
        'source': SPYCLOUD_SOURCE_NAME,
        'confidence': 'High',
        'title': 'Reported to Spycloud',
        'internal': False
    }

    CTIM_SIGHTING_TITLE_TEMPLATE = 'Present in {title}'
    CATALOG_ERROR_TEMPLATE = 'SpyCloud did not return results for {catalog_id}'

    CTIM_INDICATOR_DEFAULT = {
        'type': 'indicator',
        'schema_version': CTIM_SCHEMA_VERSION,
        'producer': SPYCLOUD_SOURCE_NAME,
    }
