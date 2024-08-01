class MegascanGeometry():

    def __init__(self) -> None:
        self._uri = self._name = None

    def __str__(self) -> str:
        out_str = "Name -> {}\n\t\t\tUri -> {}".format(self._name, self._uri)
        return out_str

    # Name property
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = value

    # Uri property
    @property
    def uri(self):
        return self._uri
    @uri.setter
    def uri(self, value):
        self._uri = value