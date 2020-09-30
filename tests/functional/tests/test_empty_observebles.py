from ctrlibrary.core.utils import get_observables
from ctrlibrary.threatresponse.enrich import enrich_observe_observables
from tests.functional.tests.constants import MODULE_NAME


def test_positive_smoke_empty_observables(module_headers):
    """Perform testing for enrich observe observables endpoint to
    check that observable, on which Spycloud doesn't have information,
    will return empty data

    ID: CCTRI-1695-2b2f141b-d2ac-4a26-a254-2f9524e5ad75

    Steps:
        1. Send request to enrich observe observables endpoint

    Expectedresults:
        1. Response body contains empty data dict from Spycloud module

    Importance: Critical
    """
    observable = [{'type': 'email', 'value': 'marita67@example.org'}]
    response_from_all_modules = enrich_observe_observables(
        payload=observable,
        **{'headers': module_headers}
    )

    spycloud_data = response_from_all_modules['data']

    response_from_spycloud_module = get_observables(spycloud_data, MODULE_NAME)

    assert response_from_spycloud_module['module'] == MODULE_NAME
    assert response_from_spycloud_module['module_instance_id']
    assert response_from_spycloud_module['module_type_id']

    assert response_from_spycloud_module['data'] == {}
