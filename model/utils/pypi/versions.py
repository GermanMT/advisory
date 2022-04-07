from requests import get

from pkg_resources import parse_version

from operator import eq, gt, lt, ge, le, ne


ops = {
    '=': eq,
    '>': gt,
    '<': lt,
    '>=': ge,
    '<=': le,
    '!=': ne
}

def get_all_versions(pkg_name: str) -> list[str]:
    url = f'https://pypi.python.org/pypi/{pkg_name}/json'
    releases = get(url).json()['releases']
    versions = dict()

    for release in releases:
        release_date = None
        for item in releases[release]:
            release_date = item['upload_time']

        aux = release.replace('.', '')

        if aux.isdigit():
            versions[release] = release_date

    return versions

def approx_gt(version: str, version_: str) -> bool:
    dots = version.count('.')
    if dots == 2:
        version += '.0'
    elif dots == 1:
        version += '.0.0'
    elif dots == 0:
        version += '.0.0.0'

    parts = version.split('.')
    parts_ = version_.split('.')
    tam_ = len(parts_) - 1

    return parse_version(version) >= parse_version(version_) and parts[tam_] >= parts_[tam_]

def approx_gt_patch(version: str, version_: str) -> bool:
    parts = version.split('.')
    parts_ = version_.split('.')

    return parse_version(version) >= parse_version(version_) and parts[2] >= parts_[2]

def approx_gt_minor(version: str, version_: str) -> bool:
    parts = version.split('.')
    parts_ = version_.split('.')

    return parse_version(version) >= parse_version(version_) and parts[1] >= parts_[1]

def get_versions(pkg_name: str, relationhip) -> list[str]:
    distributions = dict()

    all_versions = get_all_versions(pkg_name)

    if relationhip:
        for version in all_versions:
            checkers = list()
            for constraint in relationhip.constraints:
                if constraint.signature.__contains__('Any'):
                    continue

                parts = constraint.signature.split(' ')
                if parts[0] == '~>':
                    checkers.append(approx_gt(version, parts[1]))
                elif parts[0] == '^':
                    checkers.append(approx_gt_minor(version, parts[1]))
                elif parts[0] == '~':
                    checkers.append(approx_gt_patch(version, parts[1]))
                else:
                    checkers.append(ops[parts[0]](parse_version(version), parse_version(parts[1])))

            if all(checkers):
                distributions[version] = all_versions[version]
    else:
        distributions = all_versions

    return distributions
