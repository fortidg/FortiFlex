import requests, json, logging
import os


FORTIFLEX_API_BASE_URI = "https://support.fortinet.com/ES/api/fortiflex/v2/"
FORTICARE_AUTH_URI = "https://customerapiauth.fortinet.com/api/v1/oauth/token/"

COMMON_HEADERS = {"Content-type": "application/json", "Accept": "application/json"}

username = os.environ.get('FORTICARE_USERNAME')
password = os.environ.get('FORTICARE_PASSWORD')
source_config_id = os.environ.get('FORTIFLEX_SOURCE_CONFIG_ID')
source_account_id = os.environ.get('FORTIFLEX_SOURCE_ACCOUNT_ID')
target_account_id = os.environ.get('FORTIFLEX_TARGET_ACCOUNT_ID')
target_config_id = os.environ.get('FORTIFLEX_TARGET_CONFIG_ID')
# Serial numbers can be provided as comma-separated string via environment variable
serial_numbers_env = os.environ.get('FORTIFLEX_SERIAL_NUMBERS', '')
serial_numbers = [sn.strip() for sn in serial_numbers_env.split(',') if sn.strip()] if serial_numbers_env else []


def requests_post(resource_url, json_body, headers, verify=True):
    """Requests Post"""
    logging.info("--> Post request...")
    logging.info(resource_url)
    logging.info(json_body)
    logging.info(headers)

    result = requests.post(resource_url, json=json_body, headers=headers, timeout=20, verify=verify)

    if result.ok:
        logging.info(result.content)
        return_value = json.loads(result.content)
    else:
        logging.info(result)
        return_value = None

    logging.info(result.content)
    return return_value

def fauth():
    """This first section pulls the OAUTH token from fortinet"""
    logging.info("--> Get FortiFlex OAUTH token...")
    fauth_url = "https://customerapiauth.fortinet.com/api/v1/oauth/token/"
    headers = {'Content-Type' : 'application/json; charset=utf-8'}
    body = {
        "username": username,
        "password": password,
        "client_id": "flexvm",
        "grant_type": "password"
    } 

    try: 
        response = requests.post(
        url=fauth_url,
        headers=headers,
        json=body,
        timeout=20,
        )
        jsonresponse = response.json()


    except Exception as err:
        print(f'Other error occurred: {err}')

    ##This code assigns a variable to the access_token dictionary
    token = jsonresponse['access_token']

    return token



def transfer_entitlement(access_token, serial_numbers_list=None):
    """Transfer FortiFlex entitlements"""
    logging.info("--> Transfer FortiFlex Entitlements...")
    
    # Use provided serial numbers or fall back to global/environment variable
    if serial_numbers_list is None:
        serial_numbers_list = serial_numbers
    
    uri = FORTIFLEX_API_BASE_URI + "entitlements/transfer"
    headers = COMMON_HEADERS.copy()
    headers["Authorization"] = f"Bearer {access_token}"

    body = {"sourceConfigId": source_config_id, 
            "sourceAccountId": source_account_id, 
            "targetAccountId": target_account_id, 
            "targetConfigId": target_config_id
            }
    
    # Include serial numbers in the request if provided
    if serial_numbers_list:
        body["serialNumbers"] = serial_numbers_list
        logging.info(f"Transferring serial numbers: {serial_numbers_list}")
    else:
        logging.info("No serial numbers specified - will transfer all available entitlements")
    
    logging.info(f"Request body: {body}")

    results = requests_post(uri, body, headers)


    if results:
        entitlements_list = results["entitlements"]
        print("Transfer successful:")
        print(entitlements_list)
        return entitlements_list
    else:
        print("Transfer failed - no results found.")
    return None


if __name__ == "__main__":
    # Enable logging to see debug information
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    print(f"Source Config ID: {source_config_id}")
    print(f"Source Account ID: {source_account_id}")
    print(f"Target Config ID: {target_config_id}")
    print(f"Target Account ID: {target_account_id}")
    print(f"Serial Numbers: {serial_numbers}")
    
    # Transfer entitlements using serial numbers from environment variable
    transfer_entitlement(fauth(), serial_numbers)
