from ctrlibrary.core.utils import get_observables
from ctrlibrary.threatresponse.enrich import enrich_observe_observables
from tests.functional.tests.constants import (
    CONFIDENCE,
    SEVERITY,
    MODULE_NAME,
    CTR_ENTITIES_LIMIT,
    SPYCLOUD_URL,
    SOURCE
)


def test_positive_sighting_email_observable(module_headers):
    """Perform testing for enrich observe observables endpoint to get
    sighting for observable from Spycloud module

    ID: CCTRI-1051-036075ed-9fb2-4ea6-a5ad-e705b727b2d6

    Steps:
        1. Send request to enrich observe observable endpoint

    Expectedresults:
        1. Check that data in response body contains expected sighting for
        observable from Spycloud module

    Importance: Critical
    """
    observable = [{'type': 'email', 'value': 'admin@example.org'}]
    response_from_all_modules = enrich_observe_observables(
        payload=observable,
        **{'headers': module_headers}
    )['data']

    response_from_spycloud_module = get_observables(response_from_all_modules,
                                                    MODULE_NAME)

    assert response_from_spycloud_module['module'] == MODULE_NAME
    assert response_from_spycloud_module['module_instance_id']
    assert response_from_spycloud_module['module_type_id']

    sightings = response_from_spycloud_module['data']['sightings']
    columns_structure = [
        {'name': 'city', 'type': 'string'},
        {'name': 'infected_path', 'type': 'string'},
        {'name': 'infected_time', 'type': 'string'},
        {'name': 'country', 'type': 'string'},
        {'name': 'isp', 'type': 'string'},
        {'name': 'email', 'type': 'string'},
        {'name': 'password', 'type': 'string'},
        {'name': 'password_plaintext', 'type': 'string'},
        {'name': 'password_type', 'type': 'string'},
        {'name': 'gender', 'type': 'string'},
        {'name': 'target_url', 'type': 'string'},
        {'name': 'source_file', 'type': 'string'},
        {'name': 'record_modification_date', 'type': 'string'},
        {'name': 'salt', 'type': 'string'},
        {'name': 'user_browser', 'type': 'string'},
        {'name': 'target_domain', 'type': 'string'},
        {'name': 'account_signup_time', 'type': 'string'},
        {'name': 'account_login_time', 'type': 'string'},
        {'name': 'ip_addresses', 'type': 'string'},
        {'name': 'username', 'type': 'string'},
        {'name': 'postal_code', 'type': 'string'},
        {'name': 'country_code', 'type': 'string'}
    ]
    assert len(sightings['docs']) > 0

    for sighting in sightings['docs']:
        assert sighting['type'] == 'sighting'
        assert sighting['description']
        assert sighting['id'].startswith('transient:sighting-')
        assert sighting['schema_version']
        assert sighting['source'] == SOURCE
        assert sighting['source_uri'].startswith(SPYCLOUD_URL)
        assert sighting['severity'] in SEVERITY
        assert sighting['confidence'] in CONFIDENCE
        assert sighting['title'] == f'Reported to {SOURCE}'
        assert sighting['count'] > 0
        assert len(sighting['external_ids']) > 0
        assert sighting['internal'] is False
        assert sighting['observables'] == observable
        assert sighting['observed_time']['start_time'] == (
            sighting['observed_time']['end_time']
        )

        if sighting['relations']:
            relation = sighting['relations'][0]
            assert relation['origin'] == f'{SOURCE} Breach Module'
            assert relation['relation'] == 'Leaked_From'
            assert relation['source'] == observable[0]
            assert relation['related']['type']
            assert relation['related']['value']

        for target in sighting['targets']:
            assert target['type'] == observable[0]['type']
            assert target['observables'] == observable
            assert target['observed_time']['start_time'] == (
                target['observed_time']['end_time']
            )

        assert [
            i for i in sighting['data']['columns']
            if i not in columns_structure
        ] == []
        assert 'rows' in sighting['data']

    assert sightings['count'] == len(sightings['docs']) <= CTR_ENTITIES_LIMIT
