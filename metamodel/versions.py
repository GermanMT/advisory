import requests

from pkg_resources import parse_version


def get_versions(pkg_name: str) -> list[str]:
    url = f'https://pypi.python.org/pypi/{pkg_name}/json'
    releases = requests.get(url).json()['releases']
    return sorted(releases, key=parse_version)
