from requests import get


def get_all_versions(pkg_name: str) -> list[str]:
    try:
        url = f'https://repo.packagist.org/packages/{pkg_name}.json'
        releases = get(url).json()['package']['versions']

        versions = list()

        for release in releases:

            aux = release.replace('.', '').replace('v', '')

            if aux.isdigit():
                versions.append({
                    'release': releases[release]['version_normalized'],
                    'release_date': releases[release]['time']
                })

        return versions

    except:

        return dict()