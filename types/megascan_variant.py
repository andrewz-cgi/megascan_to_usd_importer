from .megascan_geometry import MegascanGeometry

class MegascanVariant():

    def __init__(self) -> None:
        self._original: MegascanGeometry = None
        self._lods: list[MegascanGeometry] = []

    def __str__(self) -> str:
        otu_str = "\t\t--- Original ---\n"
        otu_str += "\t\t\t{}\n".format(self._original.__str__())
        otu_str += "\t\t--- Lods ---\n"
        for lod in self._lods:
            otu_str += "\t\t\t{}\n".format(lod.__str__())
        return otu_str
    
    # Original property
    @property
    def original(self):
        return self._original
    @original.setter
    def original(self, value):
        self._original = value

    # Lods property
    @property
    def lods(self):
        return self._lods
    @lods.setter
    def lods(self, value):
        self._lods = value 