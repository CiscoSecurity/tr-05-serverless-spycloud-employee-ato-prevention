from ctrlibrary.core.utils import get_observables
from ctrlibrary.threatresponse.enrich import enrich_observe_observables
from tests.functional.tests.constants import (
    MODULE_NAME,
    CTR_ENTITIES_LIMIT,
    CONFIDENCE,
    SOURCE
)


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
    observable = [{'type': 'email', 'value': 'admin@example.org'}]
    response_from_all_modules = enrich_observe_observables(
        payload=observable,
        **{'headers': module_headers}
    )['data']
    response_from_spycloud_module = get_observables(
        response_from_all_modules, MODULE_NAME)

    assert response_from_spycloud_module['module'] == MODULE_NAME
    assert response_from_spycloud_module['module_instance_id']
    assert response_from_spycloud_module['module_type_id']

    indicators = response_from_spycloud_module['data']['indicators']
    assert len(indicators['docs']) > 0
    for indicator in indicators['docs']:
        assert indicator['type'] == 'indicator'
        assert indicator['id'].startswith('transient:indicator-')
        assert indicator['tags']
        assert indicator['schema_version']
        assert indicator['producer'] == SOURCE
        assert indicator['valid_time']['start_time']
        assert indicator['confidence'] in CONFIDENCE
        assert indicator['title']
        assert indicator['description']
        assert indicator['short_description']
        assert indicator['external_ids']
        if indicator['external_references']:
            assert indicator[
                'external_references'][0]['source_name'] == SOURCE
            assert indicator['external_references'][0]['description']
            assert indicator['external_references'][0]['url']

    assert indicators['count'] == len(indicators['docs']) <= CTR_ENTITIES_LIMIT
