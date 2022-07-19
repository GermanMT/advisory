from advisory.objects.vulnerability.cve import CVE


class Version:

    def __init__(
        self,
        ver_name: str,
        release_date: str
    ) -> None:

        self.__ver_name: str = ver_name
        self.__release_date: str = release_date
        self.__cves: list['CVE'] = list()

    def get_ver_name(self) -> int:
        return self.__ver_name

    def get_release_date(self) -> int:
        return self.__release_date

    def get_cves(self) -> int:
        return self.__cves

    def add_cve(self, cve: 'CVE') -> None:
        self.__cves.append(cve)

    def __repr__(self) -> str:
        return self.__ver_name