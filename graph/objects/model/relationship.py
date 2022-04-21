from graph.objects.model.constraint import Constraint


class Relationship:

    def __init__(
        self,
        parent,
        child = None ,
        constraints: 'Constraint' = list()
    ) -> None:

        self.parent = parent
        self.child = child
        self.constraints = constraints