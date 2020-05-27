from uuid import uuid4
from functools import partial
from datetime import datetime

import requests
from flask import Blueprint, current_app, g

from api.schemas import ObservableSchema
from api.utils import (
    get_json,
    get_jwt,
    jsonify_data,
    url_for,
    get_response_data,
    format_docs
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


def validate_spycloud_outputs(observable, key):

    breaches = []
    catalogs = {}

    headers = {
        **current_app.config['SPYCLOUD_BASE_HEADERS'],
        'X-API-Key': key
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
            'source': observable,
            'related': {
                'type': 'domain',
                'value': domain
            },
            'relation': 'Leaked_From',
        }
        relations.append(relation)

    return relations


def get_severity(breach, catalog):
    if not catalog.get('combo_list_flag'):
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


def get_data(breach):
    data = {
        'columns': [],
        'rows': [[]]
    }
    for item in breach.items():
        if item[0] not in current_app.config['SPYCLOUD_IGNORING_FIELDS']:
            column = {
                'name': item[0],
                'type': 'string'
            }
            data['columns'].append(column)
            data['rows'][0].append(item[1])

    return data


def get_external_references(result):
    external_references = []
    if result.get('site_description') and result.get('site'):
        external_references.append({
            'source_name': current_app.config['SPYCLOUD_SOURCE_NAME'],
            'description': result['site_description'],
            'url': result['site']
        })
    if result.get('uuid') and result.get('description'):
        external_references.append({
            "source_name": current_app.config['SPYCLOUD_SOURCE_NAME'],
            "description": result['description'],
            "url": current_app.config['SPYCLOUD_UI_URL'].format(
                uuid=result['uuid']),
            "external_id": result['uuid']
        })
    return external_references


def get_confidence(result):
    score = result['confidence']
    if score:
        return current_app.config['SPYCLOUD_CONFIDENCE_RELATIONS'][score]
    else:
        return 'Low'


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
        'data': get_data(breach),
        **current_app.config['CTIM_SIGHTING_DEFAULT']
    }

    return doc


def extract_indicators(catalog):
    start_time = datetime.strptime(
        catalog['spycloud_publish_date'], '%Y-%m-%dT%H:%M:%SZ'
    )

    valid_time = {
        'start_time': start_time.isoformat(
            timespec='microseconds') + 'Z',
    }

    indicator_id = f'transient:{uuid4()}'

    doc = {
        'id': indicator_id,
        'valid_time': valid_time,
        'confidence': get_confidence(catalog),
        'title': catalog['title'],
        'description': catalog['description'],
        'short_description': catalog['title'],
        'external_ids': [str(catalog['id']), catalog['uuid']],
        'external_references': get_external_references(catalog),
        'tags': list(catalog['assets'].keys()) or [],
        **current_app.config['CTIM_INDICATOR_DEFAULT']
    }

    return doc


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

    token = get_jwt().get('key', '')

    g.sightings = []
    g.indicators = []

    for observable in observables:
        spycloud_breach_outputs, spycloud_catalogs = validate_spycloud_outputs(
            observable, token)

        for output in spycloud_breach_outputs:

            breaches = output['results']
            breaches.sort(
                key=lambda x: x['spycloud_publish_date'], reverse=True)

            unique_catalog_id_set = set()

            if len(breaches) >= current_app.config['CTR_ENTITIES_LIMIT']:
                breaches = breaches[:current_app.config['CTR_ENTITIES_LIMIT']]

            for breach in breaches:
                g.sightings.append(
                    extract_sightings(breach, output, spycloud_catalogs))

                catalog_id = breach['source_id']
                if catalog_id not in unique_catalog_id_set:
                    g.indicators.append(
                        extract_indicators(spycloud_catalogs[catalog_id]))
                    unique_catalog_id_set.add(catalog_id)

    relay_output = {}

    if g.sightings:
        relay_output['sightings'] = format_docs(g.sightings)
    if g.indicators:
        relay_output['indicators'] = format_docs(g.indicators)

    return jsonify_data(relay_output)


@enrich_api.route('/refer/observables', methods=['POST'])
def refer_observables():
    # Not implemented
    return jsonify_data([])
