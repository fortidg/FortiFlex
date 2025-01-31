import requests, json, logging
import os


FORTIFLEX_API_BASE_URI = "https://support.fortinet.com/ES/api/fortiflex/v2/"
FORTICARE_AUTH_URI = "https://customerapiauth.fortinet.com/api/v1/oauth/token/"

COMMON_HEADERS = {"Content-type": "application/json", "Accept": "application/json"}

username = os.environ.get('FORTICARE_USERNAME')
password = os.environ.get('FORTICARE_PASSWORD')
config_id = os.environ.get('FORTIFLEX_CONFIG_ID')

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


    ##This opens the api request and prints the entire thing
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


### This section will use the token to create an entitlement
def get_active(access_token, config_id):
    """Retrieve FortiFlex entitlements which are active and unassigned."""
    logging.info("--> Retrieve FortiFlex Entitlements...")

    uri = FORTIFLEX_API_BASE_URI + "entitlements/list"
    headers = COMMON_HEADERS.copy()
    headers["Authorization"] = f"Bearer {access_token}"

    body = {"configId": config_id}

    results = requests_post(uri, body, headers)


    if results:
        entitlements_list = results["entitlements"]
        serial_numbers = []
        for entitlement in entitlements_list:
            if entitlement['status'] == 'ACTIVE' and entitlement['description'] == '':
                serial_numbers.append(entitlement['serialNumber'])
        print(serial_numbers)
        return serial_numbers

    else:
        print("No results found.")

def stop_entitlements(access_token):
    """Stop FortiFlex entitlements which are active and unassigned."""
    logging.info("--> Stop entitlements...")
    serials = get_active(access_token, config_id)



    uri = FORTIFLEX_API_BASE_URI + "entitlements/stop"
    headers = COMMON_HEADERS.copy()
    headers["Authorization"] = f"Bearer {access_token}"

    if serials == []:
        print("No active entitlements found.")
        return
    else:
        for serial in serials:
            body = {"serialNumber": serial}
            print (serial)
            results = requests_post(uri, body, headers)
            print(results)
        return results




stop_entitlements(fauth())
