import os
from dotenv import load_dotenv
from nvdlib import searchCVE


load_dotenv()

NVD_API_KEY = os.getenv('NVD_API_KEY')

def get_cves(pkg_name: str):
    response = searchCVE(
        cpeMatchString = 'cpe:2.3:a:*:' + pkg_name + ':*:*:*:*:*:*:*:*', 
        cpe_dict = True, 
        key = NVD_API_KEY
    )

    return response