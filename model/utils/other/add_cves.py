from cve.utils.nvd.cves import get_cves

from cve.CVE import CVE
from cve.CVSS import CVSS
from model.model import Package


def add_cves(package: 'Package') -> None:
    cves = list()

    cves = get_cves(package.pkg_name)
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
            cvss = CVSS('', 0, 0, 0, 0, 0, 0, 0)

        new_cve = CVE(id, 'nvd', description, cpes, cvss)
        if package.get_cve(id) == None:
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
