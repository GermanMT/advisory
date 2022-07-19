class Constraint:
    
    def __init__(
        self,
        signature: str
        ) -> None:

        self.__signature: str = signature

    def get_signature(self) -> int:
        return self.__signature