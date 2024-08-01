from .export_preset import ExportPreset
from .extra_preset import ExtraPreset
from .geometry_preset import GeometryPreset
from .main_preset import MainPreset
from .material_preset import MaterialPreset

class PresetSettings():

    def __init__(self, export = ExportPreset(), extra = ExtraPreset(), geometry = GeometryPreset(), main = MainPreset(), material = MaterialPreset()):
        
        self.export = export
        self.extra = extra
        self.geometry = geometry
        self.main = main
        self.material = material