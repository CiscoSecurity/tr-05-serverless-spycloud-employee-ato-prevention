from ctrlibrary.core.utils import get_observables
from ctrlibrary.threatresponse.enrich import enrich_observe_observables


def test_positive_indicators_email_observable(module_headers):
    """Perform testing for enrich observe observables endpoint to get
    indicators for observable from Spycloud module

    ID: CCTRI-1055-9d358875-e59f-4e06-a3ff-9a7ea7f67a31

    Steps:
        1. Send request to enrich observe observable endpoint

    Expectedresults:
        1. Check that data in response body contains expected indicators for
        observable from Spycloud module

    Importance: Critical
    """
    payload = {'type': 'email', 'value': 'admin@example.org'}
    example_tags = ['password', 'email', 'username', 'target_url']
    response = enrich_observe_observables(
        payload=[payload],
        **{'headers': module_headers}
    )['data']
    indicators = get_observables(response, 'Spycloud')['data']['indicators']
    assert len(indicators['docs']) > 0
    for indicator in indicators['docs']:
        assert indicator['type'] == 'indicator'
        assert indicator['id']
        assert any(i in indicator['tags'] for i in example_tags)
        assert indicator['schema_version']
        assert indicator['producer'] == 'Spycloud'
        assert 'start_time' in indicator['valid_time']
        assert indicator['confidence'] in ['Low', 'Medium', 'High']
        assert indicator['title']
        assert indicator['description']
        assert indicator['short_description']
        assert indicator['external_ids']
        if indicator['external_references']:
            assert indicator[
                'external_references'][0]['source_name'] == 'Spycloud'
            assert indicator['external_references'][0]['description']
            assert indicator['external_references'][0]['url']

    assert indicators['count'] == len(indicators['docs'])
