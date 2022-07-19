from advisory.models.graph.utils.versions import get_versions
from advisory.objects.model.relationship import Relationship
from advisory.objects.model.version import Version
from advisory.objects.vulnerability.cve import CVE


class Package:

    def __init__(
        self,
        level: int,
        pkg_name: str,
        pkg_manager: str,
        file: str,
        has_dependencies: bool,
        name_with_owner: str,
        parent_relationship: 'Relationship' = None,
        req_files: list[str] = list(),
        child_relationhips: list['Relationship'] = list()
    ) -> None:

        self.__level: int = level
        self.__pkg_name: str = pkg_name
        self.__pkg_manager: str = pkg_manager
        self.__file: str = file
        self.__has_dependencies: bool = has_dependencies
        self.__name_with_owner: str = name_with_owner
        self.__parent_relationship: 'Relationship' = parent_relationship
        self.__req_files: list[str] = req_files
        self.__child_relationhips: list['Relationship'] = child_relationhips
        self.__cves: list['CVE'] = list()
        self.__versions: dict[str, 'Version'] = dict()
        if self.__parent_relationship: self.generate_versions()

    def generate_versions(self) -> None:
        versions_ = get_versions(self.__pkg_name, self.__parent_relationship, self.__pkg_manager)
        parent_name = self.__parent_relationship.get_parent().get_pkg_name()
        self.__versions = {
            parent_name: 
            [Version(version['release'], version['release_date']) for version in versions_]
        }

    def get_level(self) -> int:
        return self.__level

    def get_pkg_name(self) -> str:
        return self.__pkg_name

    def get_pkg_manager(self) -> str:
        return self.__pkg_manager

    def get_file(self) -> str:
        return self.__file

    def get_has_dependencies(self) -> bool:
        return self.__has_dependencies

    def get_name_with_owner(self) -> str:
        return self.__name_with_owner

    def get_parent_relationship(self) -> 'Relationship':
        return self.__parent_relationship

    def get_req_files(self) -> list[str]:
        return self.__req_files

    def get_child_relationhips(self) -> list['Relationship']:
        return self.__child_relationhips

    def get_versions(self) -> dict[str, 'Version']:
        return self.__versions

    def get_cves(self) -> list['CVE']:
        return self.__cves

    def add_req_file(self, req_file: str) -> None:
        self.__req_files.append(req_file)

    def add_child_relationship(self, child_relationship: 'Relationship') -> None:
        self.__child_relationhips.append(child_relationship)

    def add_cve(self, cve: 'CVE') -> None:
        self.__cves.append(cve)


    def get_cve(
        self,
        id: str
    ) -> 'CVE':
        for cve in self.__cves:
            if cve.id == id:
                return cve