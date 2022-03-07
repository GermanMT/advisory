from cve.utils.nvd.cpes import get_cpes
from cve.utils.nvd.cve import get_cve

from cve.CVE import CVE
from cve.CVSS import CVSS
from model.model import Package

import time


def add_cves(package: 'Package') -> None:
    cves = list()

    for pkg_name in package.versions:
        for version in package.versions[pkg_name]:
            time.sleep(1)
            cpes_ = get_cpes(package.pkg_name + ' ' + version.ver_name)

            cve_names = list()

            for cpe in cpes_['result']['cpes']:
                for related_cve in cpe['vulnerabilities']:
                    if related_cve != '':
                        cve_names.append(related_cve)

            for cve_name in cve_names:
                if cve_name in cves:
                    continue
                else:
                    cve = get_cve(cve_name)
                    for item in cve['result']['CVE_Items']:
                        id = item['cve']['CVE_data_meta']['ID']
                        for data in item['cve']['description']['description_data']:
                            description = data['value']

                        cpes = list()

                        for node in item['configurations']['nodes']:
                            for cpe_match in node['cpe_match']:
                                for cpe_name in cpe_match['cpe_name']:
                                    cpes.append(cpe_name['cpe23Uri'])

                        cvss = get_cvss(item['impact']['baseMetricV3'])

                    cve = CVE(id, 'nvd', description, cpes, cvss)
                package.cves.append(cve)
                version.cves.append(cve)
                cves.append(cve_name)

def get_cvss(baseMetricV3: dict) -> 'CVSS':
    cvss3 = CVSS(
        baseMetricV3['cvssV3']['vectorString'],
        baseMetricV3['cvssV3']['attackVector'],
        baseMetricV3['cvssV3']['attackComplexity'],
        baseMetricV3['cvssV3']['integrityImpact'],
        baseMetricV3['cvssV3']['baseScore'],
        baseMetricV3['cvssV3']['baseSeverity'],
        baseMetricV3['exploitabilityScore'],
        baseMetricV3['impactScore']
    )

    return cvss3
