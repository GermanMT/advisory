from models.graph.apis.nvd.cves import get_cves

from models.graph.objects.vulnerability.cve import CVE
from models.graph.objects.vulnerability.cvss import CVSS
from models.graph.graph import Package


def add_cves(package: 'Package') -> None:
    cves = list()

    if package.pkg_manager == 'COMPOSER':
        pkg_name = package.pkg_name.split('/')[1]
    else:
        pkg_name = package.pkg_name

    cves = get_cves(pkg_name)
    for cve in cves:
        id = cve.cve.CVE_data_meta.ID
        for data in cve.cve.description.description_data:
            description = data.value

        cpes = list()

        for node in cve.configurations.nodes:
            for cpe_match in node.cpe_match:
                for cpe_name in cpe_match.cpe_name:
                    cpes.append(cpe_name.cpe23Uri)

        try:
            cvss = get_cvss(cve.impact.baseMetricV3)
        except:
            cvss = CVSS('None', None, None, None, None, None, None, None)

        new_cve = CVE(id, 'nvd', description, cpes, cvss)

        if package.get_cve(id) == None:
            for parent in package.versions:
                for version in package.versions[parent]:
                    have_version = False
                    for cpe in cpes:
                        if cpe.__contains__(version.ver_name):
                            have_version = True
                    if have_version:
                        version.cves.append(new_cve)
            package.cves.append(new_cve)

def get_cvss(baseMetricV3: dict) -> 'CVSS':
    cvss3 = CVSS(
        baseMetricV3.cvssV3.vectorString,
        baseMetricV3.cvssV3.attackVector,
        baseMetricV3.cvssV3.attackComplexity,
        baseMetricV3.cvssV3.integrityImpact,
        baseMetricV3.cvssV3.baseScore,
        baseMetricV3.cvssV3.baseSeverity,
        baseMetricV3.exploitabilityScore,
        baseMetricV3.impactScore
    )

    return cvss3
