import argparse
import json
import logging
import random
import sys
from urllib.parse import quote, urljoin

import requests
from jsonschema import validate, ValidationError
from faker import Faker

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Faker for data generation
fake = Faker()

def setup_argparse():
    """
    Sets up the argument parser for the CLI.
    Returns:
        argparse.ArgumentParser: The argument parser object.
    """
    parser = argparse.ArgumentParser(description="apivuln-API-Fuzzer-Lite: A lightweight API fuzzer based on OpenAPI/Swagger specifications.")
    parser.add_argument("openapi_spec", help="Path to the OpenAPI/Swagger specification file (JSON/YAML).  Must be valid JSON for this lite implementation.")
    parser.add_argument("base_url", help="Base URL of the API to fuzz.")
    parser.add_argument("--requests", type=int, default=10, help="Number of requests to send per endpoint. Defaults to 10.")
    parser.add_argument("--dry-run", action="store_true", help="Perform a dry run without sending actual requests.")

    return parser

def load_openapi_spec(spec_path):
    """
    Loads the OpenAPI/Swagger specification from a JSON file.

    Args:
        spec_path (str): Path to the OpenAPI specification file.

    Returns:
        dict: The loaded OpenAPI specification.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        json.JSONDecodeError: If the file is not a valid JSON.
    """
    try:
        with open(spec_path, 'r') as f:
            spec = json.load(f)
        return spec
    except FileNotFoundError:
        logging.error(f"Error: OpenAPI specification file not found at '{spec_path}'.")
        raise
    except json.JSONDecodeError as e:
        logging.error(f"Error: Invalid JSON format in the OpenAPI specification file: {e}")
        raise


# Nothing seeds Faker or random, so a run cannot be replayed. If the
# server falls over on request seven, the exact body that did it exists
# only in the debug log of the prepared request, if debug was on. For
# a lite fuzzer I accept that, but it caps how far a finding can be
# chased after the fact.
def generate_fuzzed_data(schema):
    """
    Generates fuzzed data based on the provided schema.  This is a simplified
    implementation and can be extended to support more complex fuzzing strategies.

    Args:
        schema (dict): The schema to generate data from.

    Returns:
        dict: The generated fuzzed data.
    """
    data = {}
    if schema and 'properties' in schema:
        for property_name, property_schema in schema['properties'].items():
            if 'type' in property_schema:
                property_type = property_schema['type']
                if property_type == 'string':
                    if 'enum' in property_schema:
                        data[property_name] = random.choice(property_schema['enum'])
                    else:
                        data[property_name] = fake.pystr(max_chars=20)  # Generate random strings
                elif property_type == 'integer':
                    data[property_name] = fake.pyint()  # Generate random integers
                elif property_type == 'number':
                    data[property_name] = fake.pyfloat() # Generate random floats
                elif property_type == 'boolean':
                    data[property_name] = fake.pybool()  # Generate random boolean
                # Add more data type handling as needed (array, object, etc.)
                else:
                    logging.warning(f"Unsupported data type: {property_type} for property {property_name}")
            else:
                 logging.warning(f"No data type specified for property {property_name}")
    return data


def fuzz_api(spec, base_url, num_requests, dry_run):
    """
    Fuzzes the API based on the OpenAPI specification.

    Args:
        spec (dict): The OpenAPI specification.
        base_url (str): The base URL of the API.
        num_requests (int): The number of requests to send per endpoint.
        dry_run (bool): If True, performs a dry run without sending actual requests.
    """
    stats = {'attempted': 0, 'succeeded': 0, 'failed': 0, 'validated': 0, 'validation_failed': 0}
    for path, path_item in spec['paths'].items():
        for method, operation in path_item.items():
            if method.upper() in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']:
                logging.info(f"Fuzzing endpoint: {method.upper()} {path}")
                for _ in range(num_requests):
                    if not dry_run:
                        stats['attempted'] += 1
                    try:
                        # Prepare request parameters (query, header, and path
                        # parameters) and the request body. Parameters can be
                        # declared on the operation or on the path item.
                        params = {}
                        request_body = None
                        headers = {}
                        resolved_path = path

                        all_parameters = []
                        if isinstance(path_item.get('parameters'), list):
                            all_parameters.extend(path_item['parameters'])
                        if 'parameters' in operation:
                            all_parameters.extend(operation['parameters'])
                        for param in all_parameters:
                            value = generate_fuzzed_data({'properties':{param['name']: param.get('schema', {})}}).get(param['name'])
                            if value is None:
                                value = 'fuzz'
                            if param['in'] == 'query':
                                params[param['name']] = value
                            elif param['in'] == 'header':
                                headers[param['name']] = value
                            elif param['in'] == 'path':
                                # Substitute the generated value into the
                                # templated path. Sending the literal braces
                                # would request a path the API does not have.
                                resolved_path = resolved_path.replace('{' + param['name'] + '}', quote(str(value), safe=''))

                        # urljoin treats a base without a trailing
                        # slash as a file and drops its last segment,
                        # so a base of http://host/api sends requests
                        # to http://host/ instead of http://host/api/.
                        # The base URL needs its trailing slash, and
                        # nothing here adds or checks for one.
                        url = urljoin(base_url, resolved_path.lstrip('/'))

                        # Handle request body
                        if 'requestBody' in operation and 'content' in operation['requestBody']:
                            for content_type, content_schema in operation['requestBody']['content'].items():
                                if 'schema' in content_schema:
                                    request_body = generate_fuzzed_data(content_schema['schema'])
                                    headers['Content-Type'] = content_type # Set content type header
                                    break # only consider the first content type

                        # Prepare the request based on the method
                        try:
                            if method.upper() == 'GET':
                                prepared_request = requests.Request('GET', url, params=params, headers=headers).prepare()
                            elif method.upper() == 'POST':
                                prepared_request = requests.Request('POST', url, json=request_body, params=params, headers=headers).prepare()
                            elif method.upper() == 'PUT':
                                prepared_request = requests.Request('PUT', url, json=request_body, params=params, headers=headers).prepare()
                            elif method.upper() == 'PATCH':
                                prepared_request = requests.Request('PATCH', url, json=request_body, params=params, headers=headers).prepare()
                            elif method.upper() == 'DELETE':
                                prepared_request = requests.Request('DELETE', url, params=params, headers=headers, data=request_body).prepare()
                            else:
                                logging.error(f"Unsupported HTTP method: {method.upper()}")
                                stats['failed'] += 1
                                continue

                        except Exception as e:
                            logging.error(f"Error preparing request: {e}")
                            stats['failed'] += 1
                            continue
                        
                        # Log the request details
                        logging.debug(f"Request URL: {prepared_request.url}")
                        logging.debug(f"Request Headers: {prepared_request.headers}")
                        logging.debug(f"Request Body: {prepared_request.body}")

                        if dry_run:
                            logging.info(f"Dry run: Skipping request to {prepared_request.url}")
                            continue  # Skip sending the actual request in dry run mode

                        # Send the request
                        try:
                            with requests.Session() as session:
                                # verify=False is deliberate for fuzzing local
                                # and self signed test targets, whose certs
                                # would fail validation before any fuzzing
                                # happened. It also means responses are not
                                # authenticated, so do not point this at an
                                # endpoint where identity matters. The
                                # timeout keeps one hung endpoint from
                                # holding the whole run.
                                response = session.send(prepared_request, verify=False, timeout=10)
                            # Counting every 4xx and 5xx as a failed
                            # request is a choice worth questioning: for
                            # a fuzzer those responses are the material,
                            # and a server that rejects every fuzzed
                            # input with a clean 400 has behaved well,
                            # not failed. The stats keep the word failed
                            # anyway, and main below exits 1 when nothing
                            # succeeded, so an API that shrugs off every
                            # request reads as untested.
                            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

                            # Validate the response against the schema (if available)
                            if 'responses' in operation and '200' in operation['responses'] and 'content' in operation['responses']['200']:
                                for content_type, content_schema in operation['responses']['200']['content'].items():
                                    if 'schema' in content_schema:
                                        try:
                                            validate(instance=response.json(), schema=content_schema['schema'])
                                            stats['validated'] += 1
                                            logging.info(f"Response validated successfully for {content_type}")
                                        except ValidationError as e:
                                            stats['validation_failed'] += 1
                                            logging.warning(f"Response validation error: {e}")
                                            logging.debug(f"Response body: {response.text}")
                                        except json.JSONDecodeError:
                                             logging.warning("Response is not valid JSON, skipping validation")
                                        break # only consider the first content type

                            stats['succeeded'] += 1
                            logging.info(f"Request successful. Status code: {response.status_code}")

                        except requests.exceptions.RequestException as e:
                            stats['failed'] += 1
                            logging.error(f"Request failed: {e}")
                        except Exception as e:
                            stats['failed'] += 1
                            logging.error(f"An unexpected error occurred: {e}")
                    except Exception as e:
                        if not dry_run:
                            stats['failed'] += 1
                        logging.error(f"An error occurred while processing endpoint {path}: {e}")
    logging.info(
        "Fuzzing completed. Requests attempted: %d, succeeded: %d, failed: %d, validated: %d, validation failures: %d."
        % (stats['attempted'], stats['succeeded'], stats['failed'], stats['validated'], stats['validation_failed'])
    )
    return stats



def main():
    """
    Main function to parse arguments, load the OpenAPI specification, and start fuzzing.
    """
    parser = setup_argparse()
    args = parser.parse_args()

    if args.requests < 1:
        logging.error("Error: --requests must be at least 1.")
        sys.exit(1)
    try:
        spec = load_openapi_spec(args.openapi_spec)
        if not isinstance(spec, dict) or "paths" not in spec:
            logging.error("Error: OpenAPI specification has no 'paths' object.")
            sys.exit(1)
        stats = fuzz_api(spec, args.base_url, args.requests, args.dry_run)
        if not args.dry_run and stats['succeeded'] == 0:
            logging.error("Error: No request succeeded, so the fuzzing run did not test the API.")
            sys.exit(1)
    except FileNotFoundError:
        sys.exit(1)
    except json.JSONDecodeError:
        sys.exit(1)
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Example Usage:
    # python main.py petstore.json http://petstore.swagger.io/v2 --requests 5
    main()
