import requests, json, graphviz

class graph_factory():

    def __init__(self, total_level, git_token):
        self.total_level = total_level
        self.headers = {
            'Accept': 'application/vnd.github.hawkgirl-preview+json',
            'Authorization': f'Bearer {git_token}',
            }
        self.url = 'https://api.github.com/graphql'
        self.graph = graphviz.Digraph()
        self.repositories = dict()
        self.current_level = 1

    def create_graph(self, nameWithOwner):
        self.repositories[nameWithOwner] = self.current_level
        self.get_dependencies(nameWithOwner)
        self.graph.render(directory='dependency-graph-circo', engine = 'circo')
        self.graph.render(directory='dependency-graph-dot', engine = 'dot')

    def get_dependencies(self, nameWithOwner, parent = None):
        self.graph.node(nameWithOwner)

        if parent in self.repositories:
            self.graph.edge(parent, nameWithOwner)
            self.current_level = self.repositories[parent] + 1
            self.repositories[nameWithOwner] = self.current_level

        if self.current_level >= self.total_level:
            return ''

        atts = nameWithOwner.split(' ')[0].split('/')
        query = '{\"query\":\"query {\\n repository(owner:\\\"' + atts[0] + '\\\", name:\\\"' + atts[1] + '\\\") {\\n dependencyGraphManifests { \\n totalCount \\n nodes { \\n filename \\n } \\n edges { \\n node { \\n blobPath \\n dependencies { \\n totalCount \\n nodes { \\n repository { \\n nameWithOwner \\n } \\n packageName \\n requirements \\n hasDependencies \\n packageManager \\n } \\n } \\n } \\n } \\n } \\n }\\n}\"}'

        response = requests.request('POST', self.url, data = query, headers = self.headers)
        result = self.json_reader(response.text, nameWithOwner)

        for nameWithOwner in result:
            self.get_dependencies(nameWithOwner, result[nameWithOwner])

    def json_reader(self, json_data, parent): 
        data = json.loads(json_data) 
        result = dict()

        for edge in data['data']['repository']['dependencyGraphManifests']['edges']:
            for node in edge['node']['dependencies']['nodes']:
                # node['hasDependencies']
                if node['repository'] != None:
                    # print(node['repository']['nameWithOwner'])
                    # print(node['hasDependencies'])
                    req = node['requirements'] if node['requirements'] else 'Any'
                    nameWithOwner = node['repository']['nameWithOwner'] + ' ' + req
                    result[nameWithOwner] = parent

        return result
