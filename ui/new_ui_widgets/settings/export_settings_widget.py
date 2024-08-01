from PySide2.QtWidgets import QWidget, QLabel, QLineEdit, QGridLayout, QCheckBox, QComboBox, QSpacerItem, QSizePolicy

from ....types.preset import ExportPreset
from ....types.settings import ExportSettings

class ExportSettingsWidget(QWidget):

    title = 'Export Settings'

    def __init__(self, parent=None):

        super(ExportSettingsWidget, self).__init__(parent)

        self.tab_layout = QGridLayout(self)

        #
        self.tab_layout.addWidget(QLabel('Payload Layer'), 0, 0)
        self.payload_layer_name = QLineEdit()
        self.payload_layer_name.setText(ExportPreset.def_payload_layer_name)
        self.tab_layout.addWidget(self.payload_layer_name, 0, 1)

        #
        self.tab_layout.addWidget(QLabel('Geometry Layer'), 1, 0)
        self.geometry_layer_name = QLineEdit()
        self.geometry_layer_name.setText(ExportPreset.def_geometry_layer_name)
        self.tab_layout.addWidget(self.geometry_layer_name, 1, 1)

        #
        self.tab_layout.addWidget(QLabel('Material Layer'), 2, 0)
        self.material_layer_name = QLineEdit()
        self.material_layer_name.setText(ExportPreset.def_material_layer_name)
        self.tab_layout.addWidget(self.material_layer_name, 2, 1)

        #
        self.tab_layout.addWidget(QLabel('Extra Layer'), 3, 0)
        self.extra_layer_name = QLineEdit()
        self.extra_layer_name.setText(ExportPreset.def_extra_layer_name)
        self.tab_layout.addWidget(self.extra_layer_name, 3, 1)

        #
        self.localize_external_checkbox = QCheckBox('Localize External Non-USD file')
        self.tab_layout.addWidget(self.localize_external_checkbox, 4, 1)

        #
        self.tab_layout.addWidget(QLabel('Export Variants as'), 5, 0)
        self.export_variants_combo_box = QComboBox()
        self.export_variants_combo_box.addItem('Flatten Implicit Layers')
        self.export_variants_combo_box.addItem('Flatten All Layers')
        self.export_variants_combo_box.addItem('Separate Layers')
        self.export_variants_combo_box.addItem('Flatten Stage')
        self.tab_layout.addWidget(self.export_variants_combo_box, 5, 1)

        #self.tab_layout.addLayout(QSpacerItem(100, 100, QSizePolicy.Expanding, QSizePolicy.Minimum))
    
    @property
    def settings(self) -> ExportSettings:
        return ExportSettings(
            self.payload_layer_name.text() if self.payload_layer_name.text() else ExportPreset.def_payload_layer_name,
            self.geometry_layer_name.text() if self.geometry_layer_name.text() else ExportPreset.def_geometry_layer_name,
            self.material_layer_name.text() if self.material_layer_name.text() else ExportPreset.def_material_layer_name,
            self.extra_layer_name.text() if self.extra_layer_name.text() else ExportPreset.def_extra_layer_name,
            self.localize_external_checkbox.isChecked(),
            self.export_variants_combo_box.currentIndex()
        )

    @property
    def preset(self) -> ExportPreset:
        return ExportPreset(
            self.payload_layer_name.text() if self.payload_layer_name.text() else ExportPreset.def_payload_layer_name,
            self.geometry_layer_name.text() if self.geometry_layer_name.text() else ExportPreset.def_geometry_layer_name,
            self.material_layer_name.text() if self.material_layer_name.text() else ExportPreset.def_material_layer_name,
            self.extra_layer_name.text() if self.extra_layer_name.text() else ExportPreset.def_extra_layer_name,
            self.localize_external_checkbox.isChecked(),
            self.export_variants_combo_box.currentIndex()
        )
    
    def load_preset(self, preset: ExportPreset):
        self.payload_layer_name.setText(preset.payload_layer_name)
        self.geometry_layer_name.setText(preset.geometry_layer_name)
        self.material_layer_name.setText(preset.material_layer_name)
        self.extra_layer_name.setText(preset.extra_layer_name)
        self.localize_external_checkbox.setChecked(preset.localize_external),
        self.export_variants_combo_box.setCurrentIndex(preset.export_variants)