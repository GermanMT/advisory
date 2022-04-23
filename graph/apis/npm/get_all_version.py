import subprocess
import json


def get_all_versions(pkg_name: str) -> list[str]:
    _releases = subprocess.getstatusoutput(f'npm view {pkg_name} time --json')

    releases = json.loads(_releases[1])

    versions = list()

    for release in releases:

        aux = release.replace('.', '')

        if aux.isdigit():
            versions.append({
                'release': release,
                'release_date': releases[release]
            })

    return versions