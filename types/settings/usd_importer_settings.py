from ..preset.usd_importer_preset import UsdImpotertPreset

from .settings import Settings

class UsdImporterSettings(UsdImpotertPreset):

    def __init__(self, asset_name: str, textures_path: str, save_path: str, settings: Settings = Settings()):

        super().__init__(save_path, settings)

        self.asset_name = asset_name
        self.textures_path = textures_path
        self.settings = settings