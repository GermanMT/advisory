from requests import get


def get_all_versions(pkg_name: str) -> list[str]:
    url = f'https://pypi.python.org/pypi/{pkg_name}/json'
    releases = get(url).json()['releases']
    versions = list()

    for release in releases:
        release_date = None
        for item in releases[release]:
            release_date = item['upload_time']

        aux = release.replace('.', '')

        if aux.isdigit():
            versions.append({
                'release': release,
                'release_date': release_date
            })

    return versions