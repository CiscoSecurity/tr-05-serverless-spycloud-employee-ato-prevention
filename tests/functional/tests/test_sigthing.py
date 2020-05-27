from ctrlibrary.core.utils import get_observables
from ctrlibrary.threatresponse.enrich import enrich_observe_observables


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
    payload = {'type': 'email', 'value': 'admin@example.org'}
    response = enrich_observe_observables(
        payload=[payload],
        **{'headers': module_headers}
    )['data']
    sightings = get_observables(response, 'Spycloud')['data']['sightings']
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
        {'name': 'username', 'type': 'string'}
    ]
    assert len(sightings['docs']) > 0

    for sighting in sightings['docs']:
        assert sighting['type'] == 'sighting'
        assert sighting['id']
        assert sighting['schema_version']
        assert sighting['source'] == 'Spycloud'
        assert 'https://portal.spycloud.com/breach/catalog/' in sighting[
            'source_uri']
        assert sighting['severity'] in ['Low', 'Medium', 'High']
        assert sighting['confidence'] in ['Low', 'Medium', 'High']
        assert sighting['title'] == 'Reported to Spycloud'
        assert sighting['count'] > 0
        assert len(sighting['external_ids']) > 0
        assert sighting['internal'] is False
        assert sighting['observables'][0] == payload

        if sighting['relations']:
            relation = sighting['relations'][0]
            assert relation['origin'] == 'Spycloud Breach Module'
            assert relation['relation'] == 'Leaked_From'
            assert relation['source'] == {
                'value': 'admin@example.org', 'type': 'email'}
            assert relation['related']['type']
            assert relation['related']['value']

        for target in sighting['targets']:
            assert target['type'] == 'email'
            assert target['observables'][0] == payload
            assert 'start_time' in target['observed_time']

        assert [
            i for i in sighting['data']['columns']
            if i not in columns_structure
        ] == []
        assert 'rows' in sighting['data']

    assert sightings['count'] == len(sightings['docs'])
