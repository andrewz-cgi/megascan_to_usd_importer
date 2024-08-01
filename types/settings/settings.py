from .export_settings import ExportSettings
from .extra_settings import ExtraSettings
from .geometry_settings import GeometrySettings
from .main_settings import MainSettings
from .material_settings import MaterialSettings

from ..preset.preset_settings import PresetSettings

class Settings(PresetSettings):

    def __init__(self, export = ExportSettings(), extra = ExtraSettings(), geometry = GeometrySettings(), main = MainSettings(), material = MaterialSettings()):

        super().__init__(export, extra, geometry, main, material)

        self.export = export
        self.extra = extra
        self.geometry = geometry
        self.main = main
        self.material = material