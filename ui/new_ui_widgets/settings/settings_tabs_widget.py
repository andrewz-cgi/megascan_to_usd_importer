from PySide2.QtWidgets import QTabWidget
from PySide2.QtCore import Signal

from .main_settings_tab_widget import MainSettingsTabWidget
from .geometry_settings_tab_widget import GeometrySettingsTabWidget
from .material_settings_widget import MaterialSettingsTabWidget
from .export_settings_widget import ExportSettingsWidget
from .extra_settings_widget import ExtraSettingsTabWidget

from ....types.megascan_asset import MegascanAsset
from ....types.preset import PresetSettings
from ....types.settings import Settings

class SettingsTabsWidget(QTabWidget):

    def __init__(self, parent=None):

        super(SettingsTabsWidget, self).__init__(parent)

        self.main_tab_widget = MainSettingsTabWidget()
        self.addTab(self.main_tab_widget, MainSettingsTabWidget.title)

        self.geomerty_tab_widget = GeometrySettingsTabWidget()
        self.addTab(self.geomerty_tab_widget, GeometrySettingsTabWidget.title)

        self.material_tab_widget = MaterialSettingsTabWidget()
        self.addTab(self.material_tab_widget, MaterialSettingsTabWidget.title)

        self.export_tab_widget = ExportSettingsWidget()
        self.addTab(self.export_tab_widget, ExportSettingsWidget.title)

        self.extra_tab_widget = ExtraSettingsTabWidget()
        self.addTab(self.extra_tab_widget, ExtraSettingsTabWidget.title)

    @property
    def settings(self) -> Settings:
        return Settings(
            self.export_tab_widget.settings,
            self.extra_tab_widget.settings,
            self.geomerty_tab_widget.settings,
            self.main_tab_widget.settings,
            self.material_tab_widget.settings
        )

    @property
    def preset(self) -> PresetSettings:
        return PresetSettings(
            self.export_tab_widget.preset,
            self.extra_tab_widget.preset,
            self.geomerty_tab_widget.preset,
            self.main_tab_widget.preset,
            self.material_tab_widget.preset
        ) 
    
    def load_preset(self, preset: PresetSettings):
        self.export_tab_widget.load_preset(preset.export)
        self.extra_tab_widget.load_preset(preset.extra)
        self.geomerty_tab_widget.load_preset(preset.geometry)
        self.main_tab_widget.load_preset(preset.main)
        self.material_tab_widget.load_preset(preset.material)

    def update_info(self, asset_info: MegascanAsset):
        self.main_tab_widget.update_variants(asset_info)
        self.geomerty_tab_widget.update_settings(asset_info)