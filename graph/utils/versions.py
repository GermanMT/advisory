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

def get_versions(pkg_name: str, relationhip, pkg_manager: str) -> list[str]:

    if pkg_manager == 'PIP':

        from graph.apis.pypi.get_all_version import get_all_versions
        all_versions = get_all_versions(pkg_name)

    elif pkg_manager == 'NPM':

        from graph.apis.npm.get_all_version import get_all_versions
        all_versions = get_all_versions(pkg_name)

    elif pkg_manager == 'COMPOSER':

        from graph.apis.composer.get_all_version import get_all_versions

        all_versions = get_all_versions(pkg_name)


    distributions = list()

    if relationhip:
        for version in all_versions:
            release = version['release']
            checkers = list()
            for constraint in relationhip.constraints:
                if constraint.signature.__contains__('Any'):
                    continue

                parts = constraint.signature.split(' ')
                if parts[0] == '~>':
                    checkers.append(approx_gt(release, parts[1]))
                elif parts[0] == '^':
                    checkers.append(approx_gt_minor(release, parts[1]))
                elif parts[0] == '~':
                    checkers.append(approx_gt_patch(release, parts[1]))
                else:
                    checkers.append(ops[parts[0]](parse_version(release), parse_version(parts[1])))

            if all(checkers):
                distributions.append(version)
    else:
        distributions = all_versions

    return distributions
