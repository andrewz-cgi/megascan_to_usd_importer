from PySide2.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QSpinBox, QSpacerItem, QSizePolicy, QLineEdit, QCheckBox, QFrame

from ....types.megascan_asset import MegascanAsset
from ....types.preset import MainPreset
from ....types.settings import MainSettings

class MainSettingsTabWidget(QWidget):

    title = 'Main Settings'

    default_settings = {
        'export_variants': 0
    }

    def __init__(self, parent=None):

        super(MainSettingsTabWidget, self).__init__(parent)

        tab_layout = QVBoxLayout(self)

        #
        def_variant_layout = QHBoxLayout(self)
        def_variant_layout.addWidget(QLabel('Set Default Variant'))
        self.def_variant_combo_box = QComboBox()
        self.def_variant_combo_box.addItem('Load an asset ...')
        self.def_variant_combo_box.setEnabled(False)
        def_variant_layout.addWidget(self.def_variant_combo_box)
        tab_layout.addLayout(def_variant_layout)

        #
        variant_num_layout = QHBoxLayout(self)
        variant_num_layout.addWidget(QLabel('Variants Number'))
        self.variant_num_spin_box = QSpinBox()
        self.variant_num_spin_box.setRange(0, 10)
        self.variant_num_spin_box.setEnabled(False)
        variant_num_layout.addWidget(self.variant_num_spin_box)
        tab_layout.addLayout(variant_num_layout)

        #
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        tab_layout.addWidget(separator)

        #
        self.enable_variant_layers_checkbox = QCheckBox('Enable Variant Layers')
        self.enable_variant_layers_checkbox.stateChanged.connect(self.on_enable_variant_layers_checkbox_changed) 
        tab_layout.addWidget(self.enable_variant_layers_checkbox)
    
        #
        variant_set_layout = QHBoxLayout(self)
        variant_set_layout.addWidget(QLabel('Variant Set'))
        self.variant_set_line = QLineEdit()
        self.variant_set_line.setText(MainSettings.def_variant_set)
        self.variant_set_line.setEnabled(False)
        self.variant_set_line.setPlaceholderText(MainSettings.def_variant_set)
        variant_set_layout.addWidget(self.variant_set_line)
        tab_layout.addLayout(variant_set_layout)

        #
        variant_directory_layout = QHBoxLayout(self)
        variant_directory_layout.addWidget(QLabel('Variant Drirectory'))
        self.variant_directory_line = QLineEdit()
        self.variant_directory_line.setText(MainSettings.def_variant_directory)
        self.variant_directory_line.setEnabled(False)
        self.variant_directory_line.setPlaceholderText(MainSettings.def_variant_directory)
        variant_directory_layout.addWidget(self.variant_directory_line)
        tab_layout.addLayout(variant_directory_layout)

        tab_layout.addItem(QSpacerItem(100, 100, QSizePolicy.Expanding, QSizePolicy.Minimum))
    

    @property
    def settings(self) -> MainSettings:
        return MainSettings(
            self.enable_variant_layers_checkbox.isChecked(),
            self.variant_set_line.text() if self.variant_set_line.text() else MainSettings.def_variant_set,
            self.variant_directory_line.text() if self.variant_directory_line.text() else MainSettings.def_variant_directory,
            self.def_variant_combo_box.currentText(),
            self.variant_num_spin_box.value()
        )

    @property
    def preset(self) -> MainPreset:
        return MainPreset(
            self.enable_variant_layers_checkbox.isChecked(),
            self.variant_set_line.text() if self.variant_set_line.text() else MainSettings.def_variant_set,
            self.variant_directory_line.text() if self.variant_directory_line.text() else MainSettings.def_variant_directory
        )

    def load_preset(self, preset: MainPreset):
        self.enable_variant_layers_checkbox.setChecked(preset.enable_variant_layers)
        self.variant_set_line.setText(preset.variant_set)
        self.variant_directory_line.setText(preset.variant_directory)
        self.on_enable_variant_layers_checkbox_changed(preset.enable_variant_layers)

    
    def on_enable_variant_layers_checkbox_changed(self, state):
        self.variant_set_line.setEnabled(state)
        self.variant_directory_line.setEnabled(state) 


    def update_variants(self, asset_info: MegascanAsset):

        self.def_variant_combo_box.clear()

        variants_keys = sorted(asset_info.variants)

        if len(variants_keys) == 1:
            self.def_variant_combo_box.setEnabled(False)
            self.variant_num_spin_box.setEnabled(False)
            self.variant_num_spin_box.setValue(0)
            self.def_variant_combo_box.addItem('No variants found in the asset')
        else:
            self.def_variant_combo_box.setEnabled(True)
            self.variant_num_spin_box.setEnabled(True)
            self.variant_num_spin_box.setRange(0, len(variants_keys))
            for variant in variants_keys:
                self.def_variant_combo_box.addItem(variant)