import time
import requests
import runpod
from runpod.serverless.utils.rp_validator import validate
from runpod.serverless.modules.rp_logger import RunPodLogger
from requests.adapters import HTTPAdapter, Retry
from schemas.api import API_SCHEMA
from schemas.img2img import IMG2IMG_SCHEMA
from schemas.txt2img import TXT2IMG_SCHEMA
from schemas.options import OPTIONS_SCHEMA
from schemas.controlnetseg import CONTROL_NET_SEG_REQUEST_SCHEMA
from schemas.autosamconfig import AUTOSAM_CONFIG_SCHEMA
from schemas.categorymask import CATEGORY_MASK_REQUEST_SCHEMA

BASE_URL = 'http://127.0.0.1:3000'
TIMEOUT = 600

session = requests.Session()
retries = Retry(total=10, backoff_factor=0.1, status_forcelist=[502, 503, 504])
session.mount('http://', HTTPAdapter(max_retries=retries))
logger = RunPodLogger()


# ---------------------------------------------------------------------------- #
#                              Automatic Functions                             #
# ---------------------------------------------------------------------------- #

def wait_for_service(url):
    retries = 0

    while True:
        try:
            requests.get(url)
            return
        except requests.exceptions.RequestException:
            retries += 1

            # Only log every 15 retries so the logs don't get spammed
            if retries % 15 == 0:
                logger.info('Service not ready yet. Retrying...')
        except Exception as err:
            logger.error(f'Error: {err}')

        time.sleep(0.2)


def send_get_request(endpoint):
    return session.get(
        url=f'{BASE_URL}/{endpoint}',
        timeout=TIMEOUT
    )


def send_post_request(endpoint, payload):
    return session.post(
        url=f'{BASE_URL}/{endpoint}',
        json=payload,
        timeout=TIMEOUT
    )


def validate_api(event):
    if 'api' not in event['input']:
        return {
            'errors': '"api" is a required field in the "input" payload'
        }

    api = event['input']['api']

    if type(api) is not dict:
        return {
            'errors': '"api" must be a dictionary containing "method" and "endpoint"'
        }

    api['endpoint'] = api['endpoint'].lstrip('/')

    endpoint = api['endpoint']
    if endpoint in ['sam/controlnet-seg', 'sam/category-mask']:
        if 'autosam_conf' not in event['input']:
            return {'errors': 'autosam_conf is required for this endpoint'}
        # Optionally, add any additional validation for autosam_conf here

    return validate(api, API_SCHEMA)


def validate_payload(event):
    method = event['input']['api']['method']
    endpoint = event['input']['api']['endpoint']
    payload = event['input']['payload']
    autosam_conf = event['input']['api'].get('autosam_conf')

    # List of endpoints that require autosam_conf
    endpoints_requiring_autosam_conf = [
        'sam/controlnet-seg',
        'sam/category-mask'
    ]

    # Validate autosam_conf if the endpoint requires it
    if endpoint in endpoints_requiring_autosam_conf:
        if not autosam_conf:
            return {
                'error': 'autosam_conf is required for this endpoint'
            }
    elif autosam_conf:
        return {
            'error': 'autosam_conf is not required for this endpoint'
        }

    schemas = {
        'txt2img': TXT2IMG_SCHEMA,
        'img2img': IMG2IMG_SCHEMA,
        'options': OPTIONS_SCHEMA,
        'sam/controlnet-seg': CONTROL_NET_SEG_REQUEST_SCHEMA,
        'sam/category-mask': CATEGORY_MASK_REQUEST_SCHEMA,
    }

    validated_input = validate(payload, schemas.get(endpoint))
    if 'error' in validated_input:
        return validated_input

    if endpoint in endpoints_requiring_autosam_conf:
        validated_autosam_conf = validate(autosam_conf, AUTOSAM_CONFIG_SCHEMA)
        if 'error' in validated_autosam_conf:
            return {'error': validated_autosam_conf['error']}
        validated_input['autosam_conf'] = validated_autosam_conf['validated_input']

    return endpoint, method, validated_input



# ---------------------------------------------------------------------------- #
#                                RunPod Handler                                #
# ---------------------------------------------------------------------------- #
def handler(event):
    validated_api = validate_api(event)

    if 'errors' in validated_api:
        return {
            'error': validated_api['errors']
        }

    validated_payload = validate_payload(event)

    if 'error' in validated_payload:
        return {
            'error': validated_payload['error']
        }

    endpoint, method, validated_input = validated_payload

    payload = validated_input.get('validated_input', validated_input)
    autosam_conf = validated_input.get('autosam_conf')
    if autosam_conf:
        payload['autosam_conf'] = autosam_conf

    try:
        logger.log(f'Sending {method} request to: /{endpoint}')

        if method == 'GET':
            response = send_get_request(endpoint)
        elif method == 'POST':
            response = send_post_request(endpoint, payload)
    except Exception as e:
        return {
            'error': str(e)
        }

    if response.status_code != 200:
        return {
            'error': f'Request failed with status code {response.status_code}: {response.text}'
        }

    try:
        return response.json()
    except ValueError:
        return {
            'error': 'Response is not in JSON format'
        }



if __name__ == "__main__":
    wait_for_service(url='http://127.0.0.1:3000/sdapi/v1/sd-models')
    logger.log('Automatic1111 API is ready', 'INFO')
    logger.log('Starting RunPod Serverless...', 'INFO')
    runpod.serverless.start(
        {
            'handler': handler
        }
    )
