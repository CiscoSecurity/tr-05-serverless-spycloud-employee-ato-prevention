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


def validate_spycloud_breach_outputs(observables):
    # Return list of responses from Spycloud for all observables

    outputs = []
    for observable in observables:
        abuse_ipdb_output = get_spycloud_breach_outputs(
            observable['value'])

        if abuse_ipdb_output:
            abuse_ipdb_output['observable'] = observable
            outputs.append(abuse_ipdb_output)

    return outputs


def get_spycloud_breach_outputs(spycloud_input):

    url = url_for(f'breach/data/emails/{spycloud_input}')

    headers = {
        **current_app.config['SPYCLOUD_BASE_HEADERS'],
        'X-API-Key': get_jwt().get('key', '')
    }

    response = requests.get(url, headers=headers)

    return get_response_data(response)


def get_relations(breach, observable):
    relations = []
    domain = breach.get('domain')
    ips = breach.get('ip_addresses')
    if domain:
        relations.append(get_relation(domain, observable, 'domain'))
    if ips:
        for ip in ips:
            relations.append(get_relation(ip, observable, 'ip'))
    return relations


def get_relation(source, related, source_type):
    return {
        'origin': 'Spycloud Breach Module',
        'source': {
            'type': source_type,
            'value': source
        },
        'related': related,
        'relation': 'Leaked_From',
    }


def get_severity(breach):
    severity_score = breach['severity']
    for s_name, borders in \
            current_app.config['SPYCLOUD_SEVERITY_SCORE_RELATIONS'].items():
        if borders[0] <= severity_score <= borders[1]:
            return s_name


def get_targets(breach, observed_time):
    target = breach.get('target_url')

    if target:
        ip = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", target)
        if ip:
            target_type = 'ip'
        else:
            target_type = 'url'
        return {
            'type': 'email',
            'observables': [
                {
                    'value': target,
                    'type': target_type
                }
            ],
            'observed_time': {
                'start_time': observed_time['start_time']
            }
        }
    else:
        return []


def get_external_ids(breach):
    external_ids = []
    if breach.get('document_id'):
        external_ids.append(breach['document_id'])
    if breach.get('source_id'):
        external_ids.append(str(breach['source_id']))
    if breach.get('infected_machine_id'):
        external_ids.append(breach['infected_machine_id'])

    return external_ids


def extract_sightings(breach, output):
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

    sighting_id = f'transient:{uuid4()}'

    relations = get_relations(breach, observable)

    doc = {
        'id': sighting_id,
        'count': breach.get('sighting', 1),
        'observables': [observable],
        'observed_time': observed_time,
        'relations': relations,
        'external_ids': get_external_ids(breach),
        'severity': get_severity(breach),
        **current_app.config['CTIM_SIGHTING_DEFAULT']
    }

    targets = get_targets(breach, observed_time)
    if targets:
        doc['targets'] = [targets]

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

    spycloud_breach_outputs = validate_spycloud_breach_outputs(observables)

    if not spycloud_breach_outputs:
        return jsonify_data({})

    sightings = []

    for output in spycloud_breach_outputs:

        breaches = output['results']
        breaches.sort(key=lambda x: x['spycloud_publish_date'], reverse=True)

        if len(breaches) >= current_app.config['CTR_ENTITIES_LIMIT']:
            breaches = breaches[:current_app.config['CTR_ENTITIES_LIMIT']]

        for breach in breaches:
            sightings.append(extract_sightings(breach, output))

    relay_output = {}

    if sightings:
        relay_output['sightings'] = format_docs(sightings)

    return jsonify_data(relay_output)


@enrich_api.route('/refer/observables', methods=['POST'])
def refer_observables():
    # Not implemented
    return jsonify_data([])
