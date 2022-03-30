from requests import get
from time import sleep

def get_cve(name: str):
    link = 'https://services.nvd.nist.gov/rest/json/cves/1.0?'
    nvd_token = 'f6b65d1a-52af-4c4f-80f0-c887a72502c8'

    headers = {
        'Authorization': f'Bearer {nvd_token}',
    }

    searchCriteria = f'&keyword={name}&addOns=dictionaryCpes'

    # sleep(1)
    request = get(link + searchCriteria, headers = headers)

    response = request.json()

    return response
