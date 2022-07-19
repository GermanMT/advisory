from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from advisory.objects.model.package import Package
from advisory.objects.model.constraint import Constraint


class Relationship:

    def __init__(
        self,
        parent: 'Package',
        child: 'Package' = None ,
        constraints: list['Constraint'] = list()
    ) -> None:

        self.__parent: 'Package' = parent
        self.__child: 'Package' = child
        self.__constraints: list['Constraint'] = constraints

    def get_parent(self) -> int:
        return self.__parent

    def get_child(self) -> int:
        return self.__child

    def get_constraints(self) -> int:
        return self.__constraints

    def add_child(self, child) -> None:
        self.__child = child