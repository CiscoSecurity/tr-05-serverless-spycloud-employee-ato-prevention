import re
from uuid import uuid4
from functools import partial
from datetime import datetime

import requests
from flask import Blueprint, current_app

from api.schemas import ObservableSchema
from api.utils import (
    get_json,
    get_jwt,
    jsonify_data,
    url_for,
    get_response_data
)

enrich_api = Blueprint('enrich', __name__)


get_observables = partial(get_json, schema=ObservableSchema(many=True))


def group_observables(relay_input):
    # Leave only unique pairs.

    result = []
    for obj in relay_input:

        obj['type'] = obj['type'].lower()

        # Get only supported types.
        if obj['type'] in current_app.config['SPYCLOUD_OBSERVABLE_TYPES']:
            if obj in result:
                continue
            result.append(obj)

    return result


def validate_spycloud_outputs(observables):

    breaches = []
    catalogs = {}
    for observable in observables:

        headers = {
            **current_app.config['SPYCLOUD_BASE_HEADERS'],
            'X-API-Key': get_jwt().get('key', '')
        }

        url = url_for(f'breach/data/emails/{observable["value"]}')

        spycloud_breach_output = get_spycloud_breach_outputs(url, headers)

        if spycloud_breach_output:
            spycloud_breach_output['observable'] = observable
            breaches.append(spycloud_breach_output)

            for result in spycloud_breach_output['results']:

                url = url_for(f'breach/catalog/{result["source_id"]}')

                spycloud_breach_catalog = get_spycloud_breach_outputs(
                    url, headers)
                catalog = spycloud_breach_catalog['results'][0]
                catalogs.update({catalog['id']: catalog})

    return breaches, catalogs


def get_spycloud_breach_outputs(url, headers):
    response = requests.get(url, headers=headers)
    return get_response_data(response)


def get_relations(observable, catalog):
    relations = []
    if catalog.get('site') and catalog.get('site') != 'n/a':
        domain = catalog['site']
        relation = {
            'origin': 'Spycloud Breach Module',
            'source': {
                'type': 'domain',
                'value': domain
            },
            'related': observable['value'],
            'relation': 'Leaked_From',
        }
        relations.append(relation)

    return relations


def get_severity(breach, catalog):
    if not catalog['combo_list_flag']:
        severity_score = breach['severity']
        for s_name, borders in \
                current_app.config['SPYCLOUD_SEVERITY_RELATIONS'].items():
            if borders[0] <= severity_score <= borders[1]:
                return s_name
    else:
        return 'Medium'


def get_external_ids(breach):
    external_ids = []
    if breach.get('document_id'):
        external_ids.append(breach['document_id'])
    if breach.get('source_id'):
        external_ids.append(str(breach['source_id']))
    if breach.get('infected_machine_id'):
        external_ids.append(breach['infected_machine_id'])

    return external_ids


def extract_sightings(breach, output, catalogs):

    catalog = catalogs[breach['source_id']]

    start_time = datetime.strptime(
        breach['spycloud_publish_date'], '%Y-%m-%dT%H:%M:%SZ'
    )

    observed_time = {
        'start_time': start_time.isoformat(
            timespec='microseconds') + 'Z',
    }

    observable = {
        'value': output['observable']['value'],
        'type': output['observable']['type']
    }

    target = {
            'type': 'email',
            'observables': [observable],
            'observed_time': {
                'start_time': observed_time['start_time']
            }
    }

    doc = {
        'id': f'transient:{uuid4()}',
        'count': breach.get('sighting', 1),
        'observables': [observable],
        'observed_time': observed_time,
        'relations': get_relations(observable, catalog),
        'external_ids': get_external_ids(breach),
        'severity': get_severity(breach, catalog),
        'targets': [target],
        'title': current_app.config['CTIM_DEFAULT_SIGHTING_TITLE'].format(
            title=catalog['title']
        ),
        'source_uri': current_app.config['SPYCLOUD_UI_URL'].format(
            uuid=catalog['uuid']
        ),
        **current_app.config['CTIM_SIGHTING_DEFAULT']
    }

    return doc


def format_docs(docs):
    return {'count': len(docs), 'docs': docs}


@enrich_api.route('/deliberate/observables', methods=['POST'])
def deliberate_observables():
    # Not implemented
    return jsonify_data({})


@enrich_api.route('/observe/observables', methods=['POST'])
def observe_observables():
    relay_input = get_json(ObservableSchema(many=True))

    observables = group_observables(relay_input)

    if not observables:
        return jsonify_data({})

    spycloud_breach_outputs, spycloud_catalogs = validate_spycloud_outputs(
        observables)

    if not spycloud_breach_outputs and spycloud_catalogs:
        return jsonify_data({})

    sightings = []

    for output in spycloud_breach_outputs:

        breaches = output['results']
        breaches.sort(key=lambda x: x['spycloud_publish_date'], reverse=True)

        if len(breaches) >= current_app.config['CTR_ENTITIES_LIMIT']:
            breaches = breaches[:current_app.config['CTR_ENTITIES_LIMIT']]

        for breach in breaches:
            sightings.append(
                extract_sightings(breach, output, spycloud_catalogs))

    relay_output = {}

    if sightings:
        relay_output['sightings'] = format_docs(sightings)

    return jsonify_data(relay_output)


@enrich_api.route('/refer/observables', methods=['POST'])
def refer_observables():
    # Not implemented
    return jsonify_data([])
