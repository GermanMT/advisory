from models.graph.objects.vulnerability.cve import CVE


class Version:

    def __init__(
        self,
        ver_name: str,
        release_date: str
    ) -> None:

        self.ver_name = ver_name
        self.release_date = release_date
        self.cves: 'CVE' = list()

    def __repr__(self) -> str:
        return self.ver_name