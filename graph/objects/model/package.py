from graph.utils.versions import get_versions
from graph.objects.model.relationship import Relationship
from graph.objects.model.version import Version
from graph.objects.vulnerability.cve import CVE


class Package:

    def __init__(
        self,
        level: int,
        pkg_name: str,
        pkg_manager: str,
        file: str,
        has_dependencies: bool,
        name_with_owner: str,
        req_files: list[str],
        parent_relationship: 'Relationship' = None,
        child_relationhips: list['Relationship'] = list()
    ) -> None:

        self.level = level
        self.pkg_name = pkg_name
        self.pkg_manager = pkg_manager
        self.file = file
        self.has_dependencies = has_dependencies
        self.name_with_owner = name_with_owner
        self.req_files = req_files
        self.parent_relationship = parent_relationship
        self.child_relationhips = child_relationhips
        self.versions = dict()
        self.cves: list['CVE'] = list()
        if parent_relationship: self.generate_versions()

    def generate_versions(self) -> None:
        versions_ = get_versions(self.pkg_name, self.parent_relationship, self.pkg_manager)
        parent_name = self.parent_relationship.parent.pkg_name
        self.versions = {
            parent_name: 
            [Version(version['release'], version['release_date']) for version in versions_]
        }

    def get_cve(
        self,
        id: str
    ) -> 'CVE':
        for cve in self.cves:
            if cve.id == id:
                return cve