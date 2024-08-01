from .megascan_variant import MegascanVariant
import hou

class MegascanAsset():
    
    NORMAL_TYP = '3d'
    COMBINED_TYP = 'combined'
    PLANTS_TYP = '3dplant'

    VALID_ASSET_TYPES = (NORMAL_TYP, COMBINED_TYP, PLANTS_TYP)

    def __init__(self) -> None:
        self._name = self._type = self._id = self._thumbnail = self._folder_path = self.texture_path = None
        self._groups = []
        self._variants: dict[str, MegascanVariant] = {}
        #self._maps: dict[str, MegascanMapInfo] = {}

    def __str__(self) -> str:
        out_str = "Name -> {}\nType -> {}\nFolder path -> {}\nGroups -> {}\n".format(self._name, self._type, self._folder_path, self._groups)
        out_str += "--- Variants ---\n" 
        for key, var in self._variants.items():
            out_str += "\t{}\n{}".format(key, var.__str__())
        return out_str

    # Name property
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = value

    # Type property
    @property
    def type(self):
        return self._type
    @type.setter
    def type(self, value):
        if value not in self.VALID_ASSET_TYPES:
            hou.ui.displayMessage("Type {} not supported\nValid asset types are {}".format(value, self.VALID_TYPES), severity=hou.severityType.Error, title="Asset type unrecognized")
            return
        self._type = value

    # Id property
    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, value):
        self._id = value
    
    # Thumbnail property
    @property
    def thumbnail(self):
        return self._thumbnail
    @thumbnail.setter
    def thumbnail(self, value):
        self._thumbnail = value

    # Folder_folder property
    @property
    def folder_path(self):
        return self._folder_path
    @folder_path.setter
    def folder_path(self, value):
        self._folder_path = value

    # Groups property
    @property
    def groups(self):
        return self._groups
    @groups.setter
    def groups(self, value):
        self._groups = value

    # Geometries property
    @property
    def variants(self):
        return self._variants
    @variants.setter
    def variants(self, value):
        self._variants = value

    """
    # Maps property
    @property
    def maps(self):
        return self._maps
    @maps.setter
    def maps(self, value):
        self._maps = value
    """