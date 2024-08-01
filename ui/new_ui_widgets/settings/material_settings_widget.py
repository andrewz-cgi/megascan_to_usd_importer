from PySide2.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QLineEdit, QSpacerItem, QSizePolicy
from PySide2.QtCore import Qt

from ....types.preset import MaterialPreset
from ....types.settings import MaterialSettings

class MaterialSettingsTabWidget(QWidget):

    title = 'Material Settings'

    def __init__(self, parent=None):

        super(MaterialSettingsTabWidget, self).__init__(parent)

        tab_layout = QVBoxLayout(self)

        self.metalness_checkbox = QCheckBox('Metalness')
        tab_layout.addWidget(self.metalness_checkbox)

        self.opacity_checkbox = QCheckBox('Opacity')
        tab_layout.addWidget(self.opacity_checkbox)

        self.displacement_checkbox = QCheckBox('Displacement')
        tab_layout.addWidget(self.displacement_checkbox)

        self.translucency_checkbox = QCheckBox('Translucency')
        tab_layout.addWidget(self.translucency_checkbox)

        self.ao_checkbox = QCheckBox('AO')
        tab_layout.addWidget(self.ao_checkbox)

        self.color_variation_checkbox = QCheckBox('Color Variation')
        self.color_variation_checkbox.stateChanged.connect(self.on_color_variation_checkbox_changed)
        tab_layout.addWidget(self.color_variation_checkbox)

        self.color_variation_attribute = QLineEdit()
        self.color_variation_attribute.setText(MaterialPreset.def_color_variation_name)
        self.color_variation_attribute.setPlaceholderText(MaterialPreset.def_color_variation_name)
        self.color_variation_attribute.setEnabled(False)
        tab_layout.addWidget(self.color_variation_attribute)

        self.invert_roughness_checkbox = QCheckBox('Invert Roughness')
        tab_layout.addWidget(self.invert_roughness_checkbox)

        self.usd_preview_surface = QCheckBox('Create USD Preview Surface')
        tab_layout.addWidget(self.usd_preview_surface)

        tab_layout.addItem(QSpacerItem(0, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

    @property
    def settings(self) -> MaterialSettings:
        return MaterialSettings(
            self.metalness_checkbox.isChecked(),
            self.opacity_checkbox.isChecked(),
            self.displacement_checkbox.isChecked(),
            self.translucency_checkbox.isChecked(),
            self.ao_checkbox.isChecked(),
            self.color_variation_checkbox.isChecked(),
            self.color_variation_attribute.text() if self.color_variation_attribute.text() else MaterialPreset.def_color_variation_name,
            self.invert_roughness_checkbox.isChecked(),
            self.usd_preview_surface.isChecked()
        )

    @property
    def preset(self):
        return MaterialPreset(
            self.metalness_checkbox.isChecked(),
            self.opacity_checkbox.isChecked(),
            self.displacement_checkbox.isChecked(),
            self.translucency_checkbox.isChecked(),
            self.ao_checkbox.isChecked(),
            self.color_variation_checkbox.isChecked(),
            self.color_variation_attribute.text() if self.color_variation_attribute.text() else MaterialPreset.def_color_variation_name,
            self.invert_roughness_checkbox.isChecked(),
            self.usd_preview_surface.isChecked()
        )

    def load_preset(self, preset: MaterialPreset):
        self.metalness_checkbox.setChecked(preset.metalness)
        self.opacity_checkbox.setChecked(preset.opacity)
        self.displacement_checkbox.setChecked(preset.displacement)
        self.translucency_checkbox.setChecked(preset.translucency)
        self.ao_checkbox.setChecked(preset.ao)
        self.color_variation_checkbox.setChecked(preset.color_variation)
        self.color_variation_attribute.setText(preset.color_variation_name)
        self.color_variation_attribute.setEnabled(preset.color_variation)
        self.invert_roughness_checkbox.setChecked(preset.invert_roughness)
        self.usd_preview_surface.setChecked(preset.create_usd_preview_surface)


    def on_color_variation_checkbox_changed(self, state):
        if state ==  Qt.Checked:
            self.color_variation_attribute.setEnabled(True)
        else:
            self.color_variation_attribute.setEnabled(False)