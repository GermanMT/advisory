import json
import requests


class dependencies():

    def __init__(self, file_type: str) -> None:
        self.file_type = file_type
        self.headers = {
            'Accept': 'application/vnd.github.hawkgirl-preview+json',
            'Authorization': 'Bearer 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',
            }
        self.url = 'https://api.github.com/graphql'

    def get_dependencies(self, nameWithOwner: str) -> dict[str, str]:
        atts = nameWithOwner.split(' ')[0].split('/')
        query = '{\"query\":\"query {\\n repository(owner:\\\"' + atts[0] + '\\\", name:\\\"' + atts[1] + '\\\") {\\n dependencyGraphManifests { \\n totalCount \\n nodes { \\n filename \\n } \\n edges { \\n node { \\n blobPath \\n dependencies { \\n totalCount \\n nodes { \\n repository { \\n nameWithOwner \\n } \\n packageName \\n requirements \\n hasDependencies \\n packageManager \\n } \\n } \\n } \\n } \\n } \\n }\\n}\"}'

        response = requests.request('POST', self.url, data = query, headers = self.headers)
        return self.json_reader(response.json())

    def json_reader(self, data: json) -> dict[str, str]: 
        result = {}

        for edge in data['data']['repository']['dependencyGraphManifests']['edges']:
            for node in edge['node']['dependencies']['nodes']:
                if edge['node']['blobPath'].__contains__(self.file_type):
                    if node['repository'] != None:
                        req = node['requirements'] if node['requirements'] else 'Any'
                        result[node['packageName']] = req

        return result
