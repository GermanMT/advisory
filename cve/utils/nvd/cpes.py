import requests

def get_cpes(name: str):
    link = 'https://services.nvd.nist.gov/rest/json/cpes/1.0?'
    nvd_token = 'f6b65d1a-52af-4c4f-80f0-c887a72502c8'

    headers = {
        'Authorization': f'Bearer {nvd_token}',
    }

    searchCriteria = f'&keyword={name}&addOns=cves'

    request = requests.get(link + searchCriteria, headers = headers)

    response = request.json()

    return response
