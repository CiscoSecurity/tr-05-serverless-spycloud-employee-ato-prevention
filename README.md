[![Travis CI Build Status](https://travis-ci.com/CiscoSecurity/tr-05-serverless-spycloud-employee-ato-prevention.svg?branch=develop)](https://travis-ci.com/CiscoSecurity/tr-05-serverless-spycloud-employee-ato-prevention)

# Spycloud Relay API

A sample Relay API implementation using the
[Spycloud API](https://portal.spycloud.com/docs/enterpriseapiv2)
as an example of a third-party Threat Intelligence service provider.

The API itself is just a simple Flask (WSGI) application which can be easily
packaged and deployed as an AWS Lambda Function working behind an AWS API
Gateway proxy using [Zappa](https://github.com/Miserlou/Zappa).

An already deployed Relay API (e.g., packaged as an AWS Lambda Function) can
be pushed to Threat Response as a Relay Module using the
[Threat Response Relay CLI](https://github.com/threatgrid/tr-lambda-relay).

## Installation

```bash
pip install -U -r requirements.txt
```

## Testing

```bash
pip install -U -r test-requirements.txt
```

- Check for *PEP 8* compliance: `flake8 .`.
- Run the suite of unit tests: `pytest -v tests/unit/`.

## Deployment

```bash
pip install -U -r deploy-requirements.txt
```

As an AWS Lambda Function:
- Deploy: `zappa deploy dev`.
- Check: `zappa status dev`.
- Update: `zappa update dev`.
- Monitor: `zappa tail dev --http`.

As a TR Relay Module:
- Create: `relay add`.
- Update: `relay edit`.
- Delete: `relay remove`.

**Note.** For convenience, each TR Relay CLI command may be prefixed with
`env $(cat .env | xargs)` to automatically read the required environment
variables from a `.env` file (i.e.`TR_API_CLIENT_ID`, `TR_API_CLIENT_PASSWORD`,
`URL`, `JWT`) and pass them to the corresponding command.

## Details
The Spycloud Relay API implements the following list of endpoints:
* `/observe/observables`,
* `/health`.

Other endpoints (`/deliberate/observables`, `/refer/observables`, `/respond/observables`, `/respond/trigger`) 
returns empty responses.

Supported types of observables:
* `email`,

Other types of observables will be ignored.

Spycloud API has a month limit of requests, which depends on the type of account.
If the limit is exceeded then an error message will be returned.

## JWT Generating

Payload for encryption must have structure:
```
{
    "key": "your_api_key_for_3rd_party"
}
```
Header:
```
{
    "alg": "HS256"
}
```

After encryption set your `SECRET_KEY` environment 
variable in AWS lambda for successful decryption in Relay API.

## Environment Variables

- `SECRET_KEY` - string key used while `JWT` encoding. Mandatory variable.
- `CTR_ENTITIES_LIMIT` - the maximum number of entities in a response.
 Applicable to: `Sighting`, `Indicator`.
 Must be a positive integer.
 Default value - `100`, used if the variable is not set or set variable is incorrect.

## Usage

```bash
pip install -U -r use-requirements.txt
```

```bash
export URL=<...>
export JWT=<...>

http POST "${URL}"/health Authorization:"Bearer ${JWT}"
http POST "${URL}"/observe/observables Authorization:"Bearer ${JWT}" < observables.json
```