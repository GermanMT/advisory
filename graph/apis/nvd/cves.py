from nvdlib import searchCVE


def get_cves(pkg_name: str):
    response = searchCVE(
        cpeMatchString = 'cpe:2.3:a:*:' + pkg_name + ':*:*:*:*:*:*:*:*', 
        cpe_dict = True, 
        key = 'f6b65d1a-52af-4c4f-80f0-c887a72502c8'
    )

    return response