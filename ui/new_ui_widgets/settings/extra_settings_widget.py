from PySide2.QtWidgets import QWidget, QGridLayout, QCheckBox, QSpacerItem, QSizePolicy

from ....types.preset import ExtraPreset
from ....types.settings import ExtraSettings

class ExtraSettingsTabWidget(QWidget):

    title = 'Extra Settings'

    def __init__(self, parent=None):

        super(ExtraSettingsTabWidget, self).__init__(parent)

        self.tab_layout = QGridLayout(self)

        self.class_inherit_checkbox = QCheckBox('Class Inherit')
        self.tab_layout.addWidget(self.class_inherit_checkbox, 0, 0)

        self.double_sided_checkbox = QCheckBox('Double Sided')
        self.tab_layout.addWidget(self.double_sided_checkbox, 1, 0)

        self.import_thumbnail_checkbox = QCheckBox('Import Thumbnail')
        self.tab_layout.addWidget(self.import_thumbnail_checkbox, 2, 0)

        self.tab_layout.addItem(QSpacerItem(100, 200, QSizePolicy.Expanding, QSizePolicy.Minimum))
    
    @property
    def settings(self) -> ExtraSettings:
        return ExtraSettings(
            self.double_sided_checkbox.isChecked(),
            self.class_inherit_checkbox.isChecked(),
            self.import_thumbnail_checkbox.isChecked()
        )

    @property
    def preset(self) -> ExtraPreset:
        return ExtraPreset(
            self.double_sided_checkbox.isChecked(),
            self.class_inherit_checkbox.isChecked(),
            self.import_thumbnail_checkbox.isChecked()
        )
    
    def load_preset(self, preset: ExtraPreset):
        self.double_sided_checkbox.setChecked(preset.double_sided)
        self.class_inherit_checkbox.setChecked(preset.class_inherit)
        self.import_thumbnail_checkbox.setChecked(preset.import_thumbnail)