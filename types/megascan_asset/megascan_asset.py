class MegascanAsset():

    NORMAL_TYP = '3d'
    COMBINED_TYP = 'combined'
    PLANTS_TYP = '3dplant'

    def __init__(self, name = '', type = NORMAL_TYP, id = '', asset_path = '', thumbnail = '', texture_path = ''):
        self.name = name
        self.type = type
        self.id = id
        self.asset_path = asset_path
        self.thumbnail = thumbnail
        self.texture_path = texture_path
        self.names_group = []
        self.variants = {}