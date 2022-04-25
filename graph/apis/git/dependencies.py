import requests

from graph.objects.model.package import Package

headers = {
    'Accept': 'application/vnd.github.hawkgirl-preview+json',
    'Authorization': 'Bearer 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',
}

endpoint = 'https://api.github.com/graphql'

def get_dependencies(parent: Package) -> dict[str, str]:
    owner, name = parent.name_with_owner.split('/')
    query = '''{
            repository(owner: \"%s\", name: \"%s\")
            {
                dependencyGraphManifests
                {
                    nodes
                    {
                        filename
                        dependencies
                        {
                            nodes
                            {
                                packageName
                                requirements
                                hasDependencies
                                repository
                                {
                                    nameWithOwner
                                }
                                packageManager
                            }
                        }
                    }
                }
            }
        }''' % (owner, name)

    response = requests.post(endpoint, json={"query": query}, headers = headers)

    return json_reader(response.json(), parent)

def json_reader(data, parent: Package) -> dict[str, str]: 
    dependencies = dict()

    for node in data['data']['repository']['dependencyGraphManifests']['nodes']:
        file = node['filename']
        parent.req_files.append(file)
        for node in node['dependencies']['nodes']:
            if node['repository'] != None and node['packageManager'] == parent.pkg_manager:
                package_manager = node['packageManager']
                has_dependencies = node['hasDependencies']
                name_with_owner = node['repository']['nameWithOwner']
                req = node['requirements'] if node['requirements'] else 'Any'
                dependencies[node['packageName']] = [package_manager, file, has_dependencies, name_with_owner, req]

    return dependencies
