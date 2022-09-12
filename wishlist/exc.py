class NotFound(Exception):
    def __init__(self, id_: int) -> None:
        super().__init__(f"Entity(id={id_}) not found!")

    @property
    def message(self) -> str:
        return str(self)
