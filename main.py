from graph_builder import graph_builder

git_token = "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"
graph_factory = graph_builder.graph_factory(3, git_token)
graph_factory.create_graph("GermanMT/AMADEUS") 