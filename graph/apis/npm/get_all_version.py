from requests import get


def get_all_versions(pkg_name: str) -> list[str]:
    url = f'https://registry.npmjs.org/{pkg_name}'
    releases = get(url).json()['time']

    versions = list()

    for release in releases:

        aux = release.replace('.', '')

        if aux.isdigit():
            versions.append({
                'release': release,
                'release_date': releases[release]
            })

    return versions